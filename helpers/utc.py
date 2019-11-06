import datetime


def getUTCtime():
    return str(datetime.datetime.now().replace(microsecond=0).isoformat())