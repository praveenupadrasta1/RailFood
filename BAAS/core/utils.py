import pyotp, string, random, requests
from datetime import datetime

from django.conf import settings
from django.utils import timezone

import pytz
from BAAS.config import PASSWORD_MIN_LENGTH, DETAILS_KEY, STATUS_KEY, STATUS_CODE_KEY, DATA_KEY
from core.formats import DATE_INPUT_FORMAT, ACCEPTED_TIME_FORMAT

import logging
logger = logging.getLogger(__name__)


def get_otp():
    """
    This method generates otp based on base32secret
    :return:
    """
    base32secret = pyotp.random_base32()
    otp = pyotp.TOTP(base32secret)
    return otp.now()


def frame_response(details, status, status_code):
    return {
        DETAILS_KEY: details,
        STATUS_KEY: status,
        STATUS_CODE_KEY: status_code}


def frame_data_for_internal_use(data, status):
    return {
        DATA_KEY: data,
        STATUS_KEY: status}


def generate_random_password():
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(PASSWORD_MIN_LENGTH))


def get_data_from_external_api(url):
    response = requests.get(url)
    print response
    if response.status_code == 200:
        return response.json()
    logger.error(str(response.status_code) + ' from ' + url)
    response.raise_for_status()


def remove_keys(dict, keys):
    for k in keys:
        dict.pop(k, None)
    return dict


def convert_time_format(time, convert_from_format, convert_to_format):
    return datetime.strptime(str(time), convert_from_format).strftime(convert_to_format)


def convert_date_format(date, convert_from_format ,convert_to_format ):
    return datetime.strptime(str(date), convert_from_format).strftime(convert_to_format)


def get_mins_difference_between_two_dates(from_date, to_date):
    return divmod((from_date - to_date).total_seconds(), 60)[0]


def get_local_time_from_utc(date):
    tz = pytz.timezone(settings.TIME_ZONE)
    local_time = date.astimezone(tz)
    return local_time


def convert_str_to_date_obj(date):
    return datetime.strptime(date, DATE_INPUT_FORMAT)


def convert_str_time_to_time_obj(time):
    return datetime.strptime(time, ACCEPTED_TIME_FORMAT)


def convert_datetime_to_utc(date_time, datetime_format):
    local = pytz.timezone(datetime_format)
    local_dt = local.localize(date_time, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    return utc_dt