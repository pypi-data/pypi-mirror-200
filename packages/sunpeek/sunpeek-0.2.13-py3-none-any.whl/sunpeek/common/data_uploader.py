"""
Implements the data ingestion process as roughly described in HarvestIT #187.
Data source backend can either be DataFrame or database (as implemented in Context class).
This module implements the same data ingestion process for both data sources.

Instantiate with DataUploader_df or DataUploader_db,
then do_upload() to trigger the upload.

Data ingestion is implemented in this module. Data stored (in database or dataframe) have gone through some
sanity checking. As a result, we can rely on having a timezone-aware, sorted datetime index with no duplicates,
data is either numeric or NaN, all component slots are populated with data.
The same import & sanity procedures are used for both database and dataframe backend.
Any further, dynamic data processing steps are done on-the-fly (see `Context` class): ignored intervals and min-max
replacement intervals.
In this way, for instance, an ignored range can be added or deleted in a plant, and sensor data will behave
accordingly. This is implemented in common.context.

Data ingestion triggers virtual sensor calculation.
do_upload() returns data quality check ("sensor validation"), available as per-day and per-sensor information.

Notes
-----
Main method is do_upload() which returns the upload response in a dict. What it does:
- checks timezone info in csv files
- handles strings in data
- sorts timestamps and drops duplicates
- calculates virtual sensors
- calls sensor validation and kernel method validation
- uploads data to store in raw_data table in db#
"""

import os
import warnings

import numpy as np
from typing import List, Union
import time
import pandas as pd
import pytz
from io import BytesIO
from typing import Dict
from pydantic import validator
from sunpeek.common import utils
from sunpeek.common.context import Context
import datetime
from starlette.datastructures import UploadFile

import sunpeek.db_utils.db_data_operations as hit_db
from sunpeek.base_model import BaseModel

from sunpeek.db_utils import DATETIME_COL_NAME


class DataUploadResponseFile(BaseModel):
    name: Union[str, None]
    exists: Union[bool, None]
    size_bytes: Union[int, None]
    missing_columns: Union[List[str], None]
    error_cause: Union[str, None]


class DataUploadResponse(BaseModel):
    sensor_validation: Union[Dict[str, str], None]
    response_per_file: Union[List[DataUploadResponseFile], None]
    db_response: Union[dict, None]

    @validator('sensor_validation', pre=True)
    def df_to_val(cls, dct):
        return {k: v.to_json(date_format='iso') for k, v in dct.items() if not isinstance(v, str)}


class DataUploader_df:
    """
    Data uploads of csv files to a plant using Context backend with datasource 'dataframe'.

    Parameters
    ----------
    files : List of csv files to import.
    plant : Plant, A configured plant.
    timezone : str Optional timezone information, if not given in the csv data.

    Notes
    -----
    This class does not need and not use the database. Use DataUploader_db for database backend.
    The csv files need not be in chronological order.
    Number of columns needs not be the same across files.
    Timezone information must either be given in csv timestamps or as timezone.
    """

    def __init__(self,
                 plant,
                 files: List[Union[UploadFile, str, os.PathLike]],
                 timezone: Union[str, pytz.timezone] = None,
                 csv_separator: str = ';',
                 csv_decimal: str = None,
                 csv_encoding: str = 'utf-8',
                 datetime_format: str = None,
                 eval_start: datetime.date = None,
                 eval_end: datetime.date = None,
                 ):
        """
        Parameters
        ----------
        plant : Plant
        files : files to upload
        timezone : optional, str or pytz.timezone. To be provided if csv data has no timezone information.
        csv_separator : str, used in pd.read_csv as 'sep' kwarg
        csv_decimal : str, used in pd.read_csv as 'decimal' kwarg
        csv_encoding : str, used in pd.read_csv as 'encoding' kwarg
        datetime_format : str, used to parse datetimes from csv file. Leave to None infers the format.
        eval_start : datetime, limit the data that is read and imported
        eval_end : datetime, limit the data that is read and imported
        """
        assert (files is not None), 'No files to upload supplied.'
        if not isinstance(files, list):
            files = [files]
        assert (len(files) > 0), 'No files to upload supplied.'
        self.files = files

        self.plant = plant
        self.eval_start = eval_start
        self.eval_end = eval_end
        self.output = DataUploadResponse()

        self.timezone = timezone
        self.datetime_format = datetime_format
        self.csv_decimal = csv_decimal

        self.read_csv = lambda x, **kwargs: pd.read_csv(x,
                                                        encoding=csv_encoding,
                                                        sep=csv_separator,
                                                        on_bad_lines='skip',
                                                        parse_dates=False,
                                                        dtype='str',
                                                        **kwargs)

    def do_upload(self, calculate_virtuals: bool = True):
        """Full measurement data ingestion process, also triggers virtual sensor calculation and sensor validation.

        Parameters
        ----------
        calculate_virtuals : bool, whether to trigger virtual sensor calculation.

        Raises
        ------
        FileNotFoundError
        ConnectionError

        Returns
        -------
        dict : Response from the data upload, various info fields including sensor validation etc.
        """
        start_time = time.time()
        self._pre_upload()

        # Full data ingestion process, common for all context datasources (database, dataframe).
        self.csv_to_plant(calculate_virtuals)

        self._post_upload()
        utils.hit_logger.info(f"[data_uploader] --- finished after {(time.time() - start_time)} seconds ---")

        return self.output

    def csv_to_plant(self, calculate_virtuals: bool):
        """Full data ingestion process, from csv to plant with dataframe context.
        Reads csv files to DataFrame, sets plant context datasource, does sensor validation.

        Returns
        -------
        sensor_validation : dict
        """
        df = self.all_csv_to_single_df(usecols=self.plant.get_raw_names(include_virtuals=False))

        sensor_validation = self.plant.use_dataframe(df, calculate_virtuals=calculate_virtuals)
        self.output.sensor_validation = sensor_validation

        return sensor_validation

    def all_csv_to_single_df(self, usecols: List[str] = None):
        """Concatenates the uploaded csv files into a single df.

        Parameters
        ----------
        usecols : List[str], passed to read_csv as usecols.

        Returns
        -------
        df_all_files : pd.DataFrame

        Raises
        ------
        AssertionError

        Notes
        -----
        - Columns which do not match with any of the plant's sensor raw_names are dropped.
        - Works for fastAPI's UploadFile as well as for normal csv files.
        """
        utils.hit_logger.info(f"[data_uploader] Reading csv files to DataFrame.")
        utils.hit_logger.info(f"[data_uploader] Concatenating {len(self.files)} files.")

        # Iterate trough files and gather DataFrames
        df_all_files = None
        self.output.response_per_file = []
        for file in self.files:
            file_response = DataUploadResponseFile()
            try:
                is_upload = hasattr(file, 'filename')
                if is_upload:
                    file_response.name = file.filename
                else:
                    try:
                        file_response.name = os.path.basename(file)
                    except TypeError:
                        file_response.name = None
                if is_upload:
                    file_response.exists = True

                else:
                    try:
                        file_response.exists = os.path.exists(file)
                    except TypeError:
                        file_response.exists = True

                assert file_response.exists, \
                    f'Cannot find file: "{file_response.name}".'

                # Create BytesIO object
                if is_upload:
                    bio = file.file
                elif isinstance(file, BytesIO):
                    bio = file
                    bio.seek(0)
                else:
                    with open(file, 'rb') as f:
                        bio = BytesIO(f.read())
                file_response.size_bytes = bio.__sizeof__()

                try:
                    df_file, missing_columns = self._one_csv_to_df(bio, usecols)
                except ValueError as ex:
                    utils.hit_logger.exception(ex)
                    file_response.error_cause = f'Error: {ex}'
                    continue
                file_response.missing_columns = missing_columns

                # Concatenate the dataframes
                df_all_files = pd.concat([df_all_files, df_file], ignore_index=False)
                assert isinstance(df_all_files.index, pd.DatetimeIndex), \
                    'Cannot concatenate DataFrames with mixed timezones since this results in the ' \
                    'DataFrame index not being a DatetimeIndex anymore.'

            finally:
                self.output.response_per_file.append(file_response)

        assert df_all_files is not None, \
            'Reading csv files resulted in a DataFrame with no rows.'
        df_all_files = df_all_files.sort_index()
        df_all_files = df_all_files[~df_all_files.index.duplicated(keep=False)]
        assert len(df_all_files) >= 2, \
            'Reading csv files resulted in a DataFrame with less than 2 rows.'

        return df_all_files

    def _one_csv_to_df(self, bio, usecols=None):
        """Read a BytesIO object to DataFrame.

        Parameters
        ----------
        bio : BytesIO object, from an UploadFile or from a normal csv file.
        usecols : List[str], columns to read in pd.read_csv()

        Returns
        -------
        df : DataFrame with tz-aware DatetimeIndex
        missing_columns : List[str], columns not found in the file

        Raises
        ------
        AssertionError

        Notes
        -----
        Returns a DataFrame with DatetimeIndex taken from the first column, index is named according to
         sunpeek.db_utils.DATETIME_COL_NAME.
        Missing columns are added as all-NaN columns.
        """
        try:
            # Parse timestamps from first column
            ds_cache = self._parse_timestamps(bio)
            skiprows = ds_cache.isna()

            # Limit the rows to read in the file, if bounds were provided
            if self.eval_start is not None:
                skiprows = skiprows | (ds_cache < self.eval_start)
            if self.eval_end is not None:
                skiprows = skiprows | (ds_cache > self.eval_end)
            ds_cache = ds_cache[~skiprows]
            # convert to numbers, for pd.read_csv()
            skiprows = [i for i, x in enumerate(np.insert(skiprows, 0, False)) if x]

            # Main read_csv call
            bio.seek(0)
            df = self.read_csv(bio,
                               usecols=lambda x: x in usecols,
                               skiprows=skiprows)
            # read_csv with decimal kwarg fails when reading string, hence the two calls to apply()
            if self.csv_decimal is not None:
                df = df.apply(lambda x: x.str.replace(self.csv_decimal, '.'))
            df = df.apply(pd.to_numeric, errors='coerce')
            df = pd.DataFrame(index=ds_cache) if df.empty else df.set_index(ds_cache)
            df = df.rename_axis(DATETIME_COL_NAME)

            # Add missing real sensor column names as NaN columns
            missing_columns = set(self.plant.get_raw_names(include_virtuals=False)) - set(df.columns)
            df[list(missing_columns)] = np.nan

            return df, list(missing_columns)

        except Exception as ex:
            utils.hit_logger.exception(ex)
            warnings.warn(f'Failed to read csv file using pandas read_csv. {ex}')
            raise ValueError(f'Failed to read csv file using pandas read_csv. {ex}') from ex

    def _parse_timestamps(self, bio):
        """Parse timestamps from first column in bio, validate timezone, return tz-aware DatetimeIndex
        """
        bio.seek(0)
        ds = self.read_csv(bio, usecols=[0]).iloc[:, 0]
        ds = pd.to_datetime(ds, errors='coerce', format=self.datetime_format)
        # Does not parse timezone-aware datetimes correctly, e.g. '2017-04-30 00:00:00+00:00' is parsed as NaT:
        # ds = pd.to_datetime(ds, errors='coerce', infer_datetime_format=True)

        try:
            ds = pd.DatetimeIndex(ds)
        except:
            # Mixed timezone timestamp columns lead to Index class df.index with dtype 'object'
            # see https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html
            raise ValueError(
                '[data_uploader] Could not convert timestamps of the csv file to a DatetimeIndex. '
                'One cause why this happens are mixed-timezone timestamps or only some rows having timezones.')

        ds = utils.validate_timezone(ds, self.timezone)

        return ds

    def _pre_upload(self):
        pass

    def _post_upload(self):
        pass


class DataUploader_db(DataUploader_df):
    """Data upload from csv files to database.
    """

    def __init__(self, session, **kwargs):
        super().__init__(**kwargs)
        self._sensor_raw_names = None
        self.output.db_response = {}
        # Try to establish database connection, raises ConnectionError
        self.db_connection = hit_db.get_db_connection()
        self.session = session

    @property
    def table_name(self):
        return self.plant.raw_table_name

    def _get_types_dict(self):
        types_dict = {DATETIME_COL_NAME: datetime.datetime}
        for sensor in self.plant.raw_sensors:
            if getattr(sensor.sensor_type, 'name', '') == 'bool':
                types_dict[sensor.raw_name] = bool
            elif getattr(sensor.sensor_type, 'compatible_unit_str', '') == 'str':
                types_dict[sensor.raw_name] = str
            else:
                types_dict[sensor.raw_name] = float

        return types_dict

    def _create_raw_data_table(self):
        """Creates raw data table if it does not exists in the database.
        """
        # Create database inferring runtime types
        try:
            types_dict = self._get_types_dict()
            hit_db.create_table_dynamic(self.session.get_bind(), self.table_name, types_dict)
            self.output.db_response['new_table_created'] = True
            self.output.db_response['new_table_name'] = self.table_name

        except Exception as ex:
            utils.hit_logger.exception(ex)
            hit_db.disconnect_db(self.db_connection)
            raise

    def _update_table(self):
        types_dict = self._get_types_dict()
        hit_db.create_new_data_cols(self.session.get_bind(), self.table_name, types_dict)

    def _pre_upload(self):
        table_exists = hit_db.db_table_exists(self.session.get_bind(), self.table_name)
        if table_exists:
            utils.hit_logger.info(f"[data_uploader] Table {self.table_name} exists in database. Adding columns for any "
                                  f"new sensors for plant {self.plant.name}.")
            self._update_table()
        else:
            utils.hit_logger.info(f"[data_uploader] Creating table {self.table_name} in database.")
            self._create_raw_data_table()

    def _post_upload(self):
        # Save dataframe to database
        df = self.plant.context.df

        # Before writing to database, any overlapping (not only duplicate) data in db is deleted.
        utils.hit_logger.info(f"[data_uploader] Deleting overlapping data from table {self.table_name}.")
        self.output.db_response['overlap_response'] = \
            hit_db.delete_overlapping_data(self.db_connection, self.table_name,
                                           overlapping_boundaries=(df.index[0], df.index[-1]))

        for name in [s.raw_name for s in self.plant.raw_sensors if getattr(s.sensor_type, 'name', '') == 'bool']:
            df[name] = df[name].astype(bool)

        # Write new data (including virtual sensors) to db.
        utils.hit_logger.info(f"[data_uploader] Writing dataframe to table {self.table_name}...")
        # Timestamps need to solved as DATETIME_COL_NAME col if saved in db
        df = df.rename_axis(DATETIME_COL_NAME).reset_index()  # TODO reset_index() not necessary, done twice, see execute_batch

        # Save dataframe (containing csv data + virtual sensor calculations) to database
        # self.output.db_response['measure_data_saved_db_ok'] = hit_db.execute_batch(self.db_connection, df, self.table_name)
        df.set_index(DATETIME_COL_NAME, inplace=True)
        self.output.db_response['measure_data_saved_db_ok'] = hit_db.df_to_db(self.db_connection, df, self.table_name)
        if self.output.db_response['measure_data_saved_db_ok']:
            # self.session.commit()
            self.db_connection.commit()
            utils.hit_logger.info(f"[data_uploader] Data succesfully saved in db table {self.table_name}.")
            hit_db.disconnect_db(self.db_connection)
        else:
            utils.hit_logger.info(f"[data_uploader] Error writing data to db table {self.table_name}.")
            self.db_connection.rollback()
            hit_db.disconnect_db(self.db_connection)
            raise ConnectionError('Failed to store data in database table.')

        # From now on, data is accessed by 'db' and uses the full datetime range available in the db
        self.plant.context = Context(plant=self.plant, datasource='db',
                                     eval_start=self.eval_start, eval_end=self.eval_end)
