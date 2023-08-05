import tarfile, tempfile, io, time, os
import pandas as pd
import sqlalchemy
import sqlalchemy.orm

import sunpeek.components as cmp
from sunpeek.components.helpers import ResultStatus
import sunpeek.serializable_models as smodels
from sunpeek.db_utils import db_data_operations, crud


def create_export_config(plant):

    collectors = [array.collector_type for array in plant.arrays]
    sensor_types = [sensor.sensor_type for sensor in plant.raw_sensors if sensor.sensor_type is not None]
    fluid_definitions = [plant.fluid_solar.fluid]

    return {"collectors": collectors, "sensor_types": sensor_types, "fluid_definitions": fluid_definitions, "plant": plant}


def _bundle(conf, sensors, plant, session):
    years = plant.time_index.year.unique()
    conf_file = io.BytesIO(bytes(conf.json(), 'UTF-8'))
    temp_handle, temp_path = tempfile.mkstemp(suffix='.tar.gz')
    index = pd.Series(plant.time_index, index=plant.time_index)

    with tarfile.open(temp_path, 'w:gz') as tf:
        info = tarfile.TarInfo(name=f"configuration_{plant.name}.json")
        info.size = len(conf_file.getbuffer())
        info.mtime = time.time()
        conf_file.seek(0)
        tf.addfile(tarinfo=info, fileobj=conf_file)

        for year in years:
            start = index[str(year)][0]
            end = index[str(year)][-1]
            df = db_data_operations.get_sensor_data(session.bind.raw_connection(), sensors, plant.raw_table_name,
                                                   start_timestamp=start, end_timestamp=end)
            f = io.BytesIO()
            df.to_csv(f, sep=';')
            info = tarfile.TarInfo(name=f"rawdata_{plant.name}_{year}.csv")
            info.size = len(f.getbuffer())
            info.mtime = time.time()
            f.seek(0)
            tf.addfile(tarinfo=info, fileobj=f)

        os.close(temp_handle)
        return temp_path


def _update_job(job, attr, value):
    if job:
        setattr(job, attr, value)
    return job


def create_export_package(plant: cmp.Plant, include_virtuals: bool, job: cmp.Job=None):
    if include_virtuals:
        sensors = [sensor.raw_name.lower() for sensor in plant.raw_sensors if not sensor.is_virtual]
    else:
        sensors = [sensor.raw_name.lower() for sensor in plant.raw_sensors]

    session = sqlalchemy.orm.object_session(plant)

    job = _update_job(job, 'status', ResultStatus.running)
    crud.update_component(session, job)

    try:
        conf = smodels.ConfigExport(**create_export_config(plant))
        temp_path = _bundle(conf, sensors, plant, session)

        job = _update_job(job, 'status', ResultStatus.done)
        job = _update_job(job, 'result_path', temp_path)
        crud.update_component(session, job)
        return temp_path
    except:
        _update_job(job, 'status', ResultStatus.failed)
        raise
