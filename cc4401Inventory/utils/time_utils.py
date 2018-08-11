import pytz
from datetime import datetime, date
import json

def to_chile_time_normalization(naive_time):
    return pytz.timezone("Chile/Continental").localize(naive_time, is_dst=None)


def to_datetime(datestring):
    return datetime.strptime(datestring, '%Y-%m-%d %H:%M')


holiday_dict = None

def is_holiday(a_date):
    '''
    :param a_date: The date to check for
    :type a_date: datetime
    :return: Whether a_date is holiday or not
    :rtype: bool
    '''
    global holiday_dict
    if holiday_dict is None:
        holiday_dict = {}
        with open('external/holidays_chile.json') as f:
            data = json.load(f)['data']
            for hday in data:
                holiday_dict[datetime.strptime(hday['date'], '%Y-%m-%d').strftime('%m-%d')] = True

    return holiday_dict.get(a_date.strftime('%m-%d'), False)


def is_non_workday(a_date):
    '''
    :param a_date: The date to check for
    :type a_date: datetime
    :return: Whether a_date is a non work day or not
    :rtype: bool
    '''
    weekday = a_date.weekday()
    return weekday >= 5 or is_holiday(a_date)

#print(is_holiday('02-02'))
