import datetime
import re

import jdatetime
import pytz


def jalali_end_of_month():
    return ((jdatetime.datetime.now().replace(day=29) + jdatetime.timedelta(days=5)).replace(day=1) -
            jdatetime.timedelta(days=1)).togregorian()


def jalali_start_of_month():
    return jdatetime.datetime.now().replace(day=1).togregorian()


def fix_date(date: str):
    pattern = r"[1-9][0-9]{3}\/[0-9]{2}\/[0-9]{2}"
    matched_date = re.match(pattern, date)
    if not matched_date:
        tmp = ''
        for i in date.split('/'):
            tmp += i
        return f'{tmp[:4]}/{tmp[4:6]}/{tmp[6:8]}'
    return matched_date.group()


def jalali_date(date):
    if not date:
        return '-'
    try:
        return str(jdatetime.datetime.fromgregorian(date=date).astimezone(
            pytz.timezone('Asia/Tehran')).strftime('%Y-%m-%d'))
    except:
        return jalali_datetime(date)


def jalali_datetime(date):
    return str(jdatetime.datetime.fromgregorian(datetime=date).astimezone(pytz.timezone('Asia/Tehran')).strftime(
        '%Y-%m-%d %H:%M:%S'))
