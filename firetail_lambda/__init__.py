import base64
import json
import time

from .version import __version__


class firetail_app:
    def __init__(self):
        self.sanitization_callback=default_sanitization_callback
        self.enable_sleeper=False
        self.sanitize_headers = ['authorization', 'x-api-key']

def default_sanitization_callback(event, response):
    return event, response

def firetail_handler(self):
    def decorator(func):
        def wrapper_func(*args, **kwargs):
            start_time = time.time()
            
            # make sure it is a valid handler function
            if len(args) < 2:
                return func(*args, **kwargs)

            # Unpack the args
            event, _ = args

            # Get the response returned down the chain
            handler_start_time = time.time()
            response = func(*args, **kwargs)
            handler_execution_time = (time.time() - handler_start_time) * 1000 # Milliseconds

            # Sanitise the event & response, create our log payload, and print it
            event, response = self.sanitization_callback(event, response)
            log_payload = base64.b64encode(json.dumps({
                "event": event,
                "response": response,
                "execution_time": handler_execution_time
            }).encode("utf-8")).decode("ascii")
            print("firetail:log-ext:%s" % (log_payload))

            ## Ensure the execution time is >25ms to give the logs API time to propagate our print() to the extension.
            if self.enable_sleeper:
                time.sleep(max(time.time() - start_time + 500/1000, 0))

            # Return the response from down the chain
            return response
        return wrapper_func
    return decorator

