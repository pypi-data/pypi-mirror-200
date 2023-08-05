from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.datastructures import UploadFile
from sqlalchemy.orm import Session

from sunpeek.common.utils import hit_logger
from sunpeek.common.data_uploader import DataUploader_db
from sunpeek.serializable_models import DataUploadResponse
from sunpeek.api.dependencies import session, crud
from sunpeek.api.routers.plant import plant_router

# from api.models import DataUploadResponse


files_router = APIRouter(
    prefix="/data",
    tags=["data"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@files_router.post("/div-zero")
def zero_div():
    """This method server as a usage example only for the log class and the HTTP exception raising. It must be deleted for release"""

    try:
        x = 1 / 0
    except (Exception) as err:

        # how to use the logger to report an exception
        hit_logger.exception(err)
        # how to manually report using the INFO level
        hit_logger.info("This wont print in file because of loggers level")
        # str(err) gives the message related to the exception
        error_dict = {"message": "UPS something went wrong", "error": str(err)}
        # raise HTTPException so the API returns an error code instead of freezing
        raise HTTPException(status_code=500, detail=error_dict)


@plant_router.post("/data", tags=["data"], response_model=DataUploadResponse)
def upload_measure_data(
        plant_id: int,
        files: List[UploadFile],
        timezone: str = None,
        sess: Session = Depends(session),
        crd: crud = Depends(crud)) -> DataUploadResponse:
    """Ingests csv files to database. For details, see docstring of the `data_uploader` module.

    Parameters
    ----------
    plant_id : A pre-configured plant with this name must exist in the database.
    files : list, List of csv files that are batch ingested.
    timezone : str, a timezone string like 'Europe/Vienna'
    sess : sqlalchemy.orm.Session
    crd : api.dependencies.crud

    Returns
    -------
    upload_response : DataUploadResponse

    Raises
    ------
    ConnectionError
    HTTPException
    """
    try:
        up = DataUploader_db(plant=crd.get_plants(sess, plant_id),
                             files=files,
                             timezone=timezone,
                             session=sess)
        response = up.do_upload()
        return response  # DataUploadResponse

    except Exception as ex:
        hit_logger.exception(ex)
        raise HTTPException(status_code=500,
                            detail="Something went wrong while uploading the files, please check the system log for "
                                   "details and try again.")
