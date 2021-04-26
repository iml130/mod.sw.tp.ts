""" Contains a method to receive the utc time as string """

import datetime

def get_utc_time():
    return datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
