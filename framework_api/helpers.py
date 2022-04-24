from datetime import datetime

from framework_api.settings import logging


def info_logging(data, status_code=None):
    message = f"\n - timestamp = {datetime.timestamp(datetime.now())}\
        \n - data = {data} "
    if status_code:
        message += f"\n - status_code= {status_code}"
    logging.info(message)


def error_logging(data, status_code=None):
    message = f"\n - timestamp = {datetime.timestamp(datetime.now())}\
        \n - data = {data} "
    if status_code:
        message += f"\n - status_code= {status_code}"
    logging.error(message)
