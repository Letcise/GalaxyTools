import os
import time

def _time_config():
    os.environ['TZ'] = 'Asia/Shanghai'
    time.tzset()

def _auto_config():
    _time_config()

_auto_config()