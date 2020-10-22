import datetime


def get_utc_time():
    return datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')


if __name__ == "__main__":
    print(get_utc_time())
