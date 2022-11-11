# Firetail Python Lambda Middleware

[![PyPI package](https://img.shields.io/badge/pip%20install-firetail--lambda-brightgreen)](https://pypi.org/project/firetail-lambda/) [![version number](https://img.shields.io/pypi/v/firetail-lambda?color=green&label=version)](https://github.com/Firetail-io/firetail-py-lambda/releases) [![Actions Status](https://github.com/Firetail-io/firetail-py-lambda/workflows/Test/badge.svg)](https://github.com/Firetail-io/firetail-py-lambda/actions) [![License: LGPL v3](https://img.shields.io/badge/License-LGPL_v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0) [![codecov](https://codecov.io/gh/FireTail-io/firetail-py-lambda/branch/main/graph/badge.svg?token=HU206RRZZ4)](https://codecov.io/gh/FireTail-io/firetail-py-lambda)

###Overview

The purpose of this module is to correctly log out the AWS Lambda event and response payload to allow the firetail extension to then send it on to the firetail logging api

The firetail_handler is a decorator that wraps around an event handler function in a AWS Lambda to extract the event and response payloads into a base64 logging message. 

###Supported Lambda Runtimes
- [x] Python 3.7
- [x] Python 3.8
- [x] Python 3.9

###Installation
Install the module with using pip
```bash
pip install -U firetail-lambda
```



Implementing Middleware in lambda function
```python
from firetail_lambda import firetail_handler

@firetail_handler()
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
from firetail_lambda import firetail_handler

@firetail_handler()
def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Hello"
        })
    }

@firetail_handler()
def lambda_handler_2(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Hello 2"
        })
    }
```

