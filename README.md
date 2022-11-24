# Firetail Python Lambda Middleware

[![PyPI package](https://img.shields.io/badge/pip%20install-firetail--lambda-brightgreen)](https://pypi.org/project/firetail-lambda/) [![version number](https://img.shields.io/pypi/v/firetail-lambda?color=green&label=version)](https://github.com/Firetail-io/firetail-py-lambda/releases) [![Actions Status](https://github.com/Firetail-io/firetail-py-lambda/workflows/Test/badge.svg)](https://github.com/Firetail-io/firetail-py-lambda/actions) [![License: LGPL v3](https://img.shields.io/badge/License-LGPL_v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0) [![codecov](https://codecov.io/gh/FireTail-io/firetail-py-lambda/branch/main/graph/badge.svg?token=HU206RRZZ4)](https://codecov.io/gh/FireTail-io/firetail-py-lambda)

### Overview

The purpose of this module is to correctly log out the AWS Lambda event and response payload to allow the firetail extension to then send it on to the firetail logging api

The firetail_handler is a decorator that wraps around an event handler function in a AWS Lambda to extract the event and response payloads into a base64 logging message. 


### Supported Lambda Runtimes
 ✅ Python 3.7
 ✅ Python 3.8
 ✅ Python 3.9


### Installation
Install the module with using pip
```bash
pip install -U firetail-lambda
```



Implementing Middleware in lambda function
```python
import json
from firetail_lambda import firetail_handler, firetail_app

app = firetail_app()

@firetail_handler(app)
def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Hello"
        })
    }
```
Multiple Event handlers
```python
import json
from firetail_lambda import firetail_handler, firetail_app

app = firetail_app()

@firetail_handler(app)
def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Hello"
        })
    }

@firetail_handler(app)
def lambda_handler_2(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Hello 2"
        })
    }
```

Custom Sanitization callback
```python
import copy
import json
from firetail_lambda import firetail_handler, firetail_app

def sanitize_payloads(event, response):
    new_event = copy.copy(event)
    remove_headers = ['authorization','Authorization', 'x-api-key']
    if 'headers' in event:
        for header in remove_headers:
            if header in event['headers']:
                del new_event['headers'][header]
            if 'multiValueHeaders' in event and header in event['multiValueHeaders']:
                del new_event['multiValueHeaders'][header]
                        
    return new_event, response

app = firetail_app()
app.sanitization_callback = sanitize_payloads

@firetail_handler(app)
def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Hello"
        })
    }

```
