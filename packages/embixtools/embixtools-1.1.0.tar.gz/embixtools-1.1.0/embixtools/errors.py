from functools import wraps

def raises(exc):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            try: 
                return function(*args, **kwargs)
            except Exception as e: 
                raise exc(args, kwargs)
        return wrapper
    return decorator