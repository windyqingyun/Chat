import uuid
import time


def get_uuid():
    return str(uuid.uuid4())

def get_now():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

def get_dict(obj):
    dict = {}
    dict.update(obj.__dict__)
    return dict
