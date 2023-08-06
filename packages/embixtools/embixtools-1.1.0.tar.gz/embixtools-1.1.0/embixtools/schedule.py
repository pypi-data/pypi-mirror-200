import logging
import time
import pytz
from datetime import datetime, timedelta
from functools import wraps, partial
import threading

################################################################
# Decorator for executing a function periodically
# ex : 
#   @do_every(minutes=30)
#   def myfunc(param):
#       do_sth()
#   >> will execute myfunc every 30 minutes
################################################################
def do_every(hours=0, minutes=0, seconds=0, microseconds=0):
    paris = pytz.timezone('Europe/Paris')
    wait = microseconds*1e-6 + seconds + 60*minutes + 3600*hours
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            def f():
                now = datetime.now(paris)
                function(*args,**kwargs)
                logging.info("="*100)
                logging.info(f"Next action : {(now+timedelta(seconds=wait)).strftime('%Y-%m-%d %H:%M:%S')}")
            threading.Timer(wait, wrapper, *args, **kwargs).start()
            f()
        return wrapper
    return decorator

################################################################
# Decorator for executing a function at a specific time
# ex : 
#   @do_at('15:34:57')
#   def myfunc(param):
#       do_sth()
#   >> will execute myfunc at next 15:34:57 (Paris time)
################################################################
def do_at(start=None):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            utc = pytz.utc
            paris = pytz.timezone('Europe/Paris')
            now_time = datetime.now(paris)
            sch_time = now_time
            wait = 0
            if not start is None:
                # compute the delay to wait before executing the function
                sch_time = paris.localize(
                    datetime.combine(
                        date = now_time.date(), 
                        time = paris.localize(datetime.strptime(start,'%H:%M:%S')).time()
                    )
                )
                if sch_time < now_time:
                    sch_time += timedelta(hours=24)
                wait = (sch_time - now_time).total_seconds()
            # schedule 'function' to be executed after computed delay
            logging.info("="*100)
            logging.info(f"Next action : {sch_time.strftime('%Y-%m-%d %H:%M:%S')}")
            threading.Timer(wait, partial(function,*args,**kwargs)).start()
        return wrapper
    return decorator

################################################################
# Decorator for scheduling a periodic function
# It combines @do_at and @do_every
# ex : 
#   @schedule(start = '15:34:57', every={'hours': 2})
#   def myfunc(param):
#       do_sth()
#   >> will execute myfunc every 2 hours, 
#      starting at 15:34:57 for the first execution
################################################################
def schedule(start=None, every={}):
    def decorator(function):
        @do_at(start)
        @do_every(**every)
        @wraps(function)
        def wrapper(*args, **kwargs):
            function(*args, **kwargs)
        return wrapper
    return decorator