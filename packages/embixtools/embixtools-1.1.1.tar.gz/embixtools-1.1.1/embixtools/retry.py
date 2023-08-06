import logging
import time
from functools import partial
from functools import wraps

################################################################
# Decorator for retrying a function when it fails
# with the option of waiting bewteen tries.
# If the 'wait_between_tries' arg is not provided, 
# the function will be retried immediately.
# ex : 
#   @retry(nb_tries = 3, wait_between_tries = {'minutes': 5})
#   def myfunc(param):
#       do_sth()
#   >> will execute myfunc a maximum of 3 times
#   >> it will wait 5 minutes between tries
################################################################
def retry(nb_tries, wait_between_tries={}):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            try: 
                return function(*args, **kwargs)
            except KeyboardInterrupt: 
                raise
            except Exception as e:
                failed_func = function.__qualname__
                if nb_tries == 1: 
                    logging.error(f'<{failed_func}> failed too many times.')
                    logging.error(' '.join(f'{e.__class__.__qualname__}:\n{str(e)}'.split()))
                    raise
                time.sleep(
                    + wait_between_tries.get('seconds', 0)
                    + wait_between_tries.get('minutes', 0) * 60
                    + wait_between_tries.get('hours', 0) * 3600
                )
                return retry(nb_tries-1, wait_between_tries)(function)(*args, **kwargs)
        return wrapper
    return decorator