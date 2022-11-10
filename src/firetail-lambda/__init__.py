__version__ = "0.1.0"

import base64, json, time

def firetail_handler(enable_sleeper=False):
    def decorator(func):
        def wrapper_func(*args, **kwargs):
            compatible = True
            start_time = time.time()
            
            # make sure it is a valid handler function
            if len(args) < 2:
                compatible = False
            if compatible:
                # Unpack the args
                event, _ = args

            # Get the response returned down the chain
            response = func(*args, **kwargs)

            # Create our log payload, and print it
            if compatible:
                log_payload = base64.b64encode(json.dumps({"event": event,"response": response}).encode("utf-8")).decode("ascii")
                print("firetail:loggingapi:%s" % (log_payload))

            ## Ensure the execution time is >25ms to give the logs API time to propagate our print() to the extension.
            if enable_sleeper and compatible:
                time.sleep(max(time.time() - start_time + 500/1000, 0))

            # Return the response from down the chain
            return response
        return wrapper_func
    return decorator

