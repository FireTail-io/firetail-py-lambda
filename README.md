# Firetail Python Lambda Middleware

[![PyPI package](https://img.shields.io/badge/pip%20install-example--pypi--package-brightgreen)](https://pypi.org/project/firetail-lambda/) [![version number](https://img.shields.io/pypi/v/firetail-lambda?color=green&label=version)](https://github.com/Firetail-io/firetail-py-lambda/releases) [![Actions Status](https://github.com/Firetail-io/firetail-py-lambda/workflows/Test/badge.svg)](https://github.com/Firetail-io/firetail-py-lambda/actions) [![License](https://img.shields.io/github/license/Firetail-io/firetail-py-lambda)](https://github.com/Firetail-io/firetail-py-lambda/blob/main/LICENSE)

The purpose of this module is to correctly log out the event and response payload to allow the firetail extension to then send it on to the firetail logging api

```bash
pip install firetail-lambda
```

How to implement

Add Environment variables to code/lambda
```bash
export FIRETAIL_API_URL=https://api.logging.eu-west-1.sandbox.firetail.app/logs/bulk
export FIRETAIL_API_TOKEN=<your-api-token>
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

