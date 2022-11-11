

import contextlib
import copy
import json
import time
import unittest
from io import StringIO

from firetail_lambda import firetail_app, firetail_handler

api_gateway_v1 = {
    "body": "eyJ0ZXN0IjoiYm9keSJ9",
    "resource": "/{proxy+}",
    "path": "/path/to/resource",
    "httpMethod": "POST",
    "isBase64Encoded": True,
    "queryStringParameters": {
        "foo": "bar"
    },
    "multiValueQueryStringParameters": {
        "foo": [
        "bar"
        ]
    },
    "pathParameters": {
        "proxy": "/path/to/resource"
    },
    "stageVariables": {
        "baz": "qux"
    },
    "headers": {
        "Authorization": "Bearer jwt123.123.123",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "en-US,en;q=0.8",
        "Cache-Control": "max-age=0",
        "CloudFront-Forwarded-Proto": "https",
        "CloudFront-Is-Desktop-Viewer": "true",
        "CloudFront-Is-Mobile-Viewer": "false",
        "CloudFront-Is-SmartTV-Viewer": "false",
        "CloudFront-Is-Tablet-Viewer": "false",
        "CloudFront-Viewer-Country": "US",
        "Host": "1234567890.execute-api.us-east-1.amazonaws.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Custom User Agent String",
        "Via": "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)",
        "X-Amz-Cf-Id": "cDehVQoZnx43VYQb9j2-nvCh-9z396Uhbp027Y2JvkCPNLmGJHqlaA==",
        "X-Forwarded-For": "127.0.0.1, 127.0.0.2",
        "X-Forwarded-Port": "443",
        "X-Forwarded-Proto": "https"
    },
    "multiValueHeaders": {
        "Authorization":[
            "Bearer jwt123.123.123"
        ],
        "Accept": [
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        ],
        "Accept-Encoding": [
        "gzip, deflate, sdch"
        ],
        "Accept-Language": [
        "en-US,en;q=0.8"
        ],
        "Cache-Control": [
        "max-age=0"
        ],
        "CloudFront-Forwarded-Proto": [
        "https"
        ],
        "CloudFront-Is-Desktop-Viewer": [
        "true"
        ],
        "CloudFront-Is-Mobile-Viewer": [
        "false"
        ],
        "CloudFront-Is-SmartTV-Viewer": [
        "false"
        ],
        "CloudFront-Is-Tablet-Viewer": [
        "false"
        ],
        "CloudFront-Viewer-Country": [
        "US"
        ],
        "Host": [
        "0123456789.execute-api.us-east-1.amazonaws.com"
        ],
        "Upgrade-Insecure-Requests": [
        "1"
        ],
        "User-Agent": [
        "Custom User Agent String"
        ],
        "Via": [
        "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)"
        ],
        "X-Amz-Cf-Id": [
        "cDehVQoZnx43VYQb9j2-nvCh-9z396Uhbp027Y2JvkCPNLmGJHqlaA=="
        ],
        "X-Forwarded-For": [
        "127.0.0.1, 127.0.0.2"
        ],
        "X-Forwarded-Port": [
        "443"
        ],
        "X-Forwarded-Proto": [
        "https"
        ]
    },
    "requestContext": {
        "accountId": "123456789012",
        "resourceId": "123456",
        "stage": "prod",
        "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
        "requestTime": "09/Apr/2015:12:34:56 +0000",
        "requestTimeEpoch": 1428582896000,
        "identity": {
        "cognitoIdentityPoolId": None,
        "accountId": None,
        "cognitoIdentityId": None,
        "caller": None,
        "accessKey": None,
        "sourceIp": "127.0.0.1",
        "cognitoAuthenticationType": None,
        "cognitoAuthenticationProvider": None,
        "userArn": None,
        "userAgent": "Custom User Agent String",
        "user": None
        },
        "path": "/prod/path/to/resource",
        "resourcePath": "/{proxy+}",
        "httpMethod": "POST",
        "apiId": "1234567890",
        "protocol": "HTTP/1.1"
    }
    }

class TestSimple(unittest.TestCase):

    def test_handler_api(self):
        event = {}
        app = firetail_app()
        @firetail_handler(app)
        def handler(event, context):
            return 201, json.dumps({"message": "success"})
        
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            handler(event, "")
        output = temp_stdout.getvalue().strip()
        self.assertEqual(output, 'firetail:loggingapi:eyJldmVudCI6IHt9LCAicmVzcG9uc2UiOiBbMjAxLCAie1wibWVzc2FnZVwiOiBcInN1Y2Nlc3NcIn0iXX0=')

    def test_incorrect_handler_api(self):
        event = {}
        app = firetail_app()
        @firetail_handler(app)
        def handler(argument):
            return 201, json.dumps({"message": "success"})
        
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            handler(event)
        output = temp_stdout.getvalue().strip()
        self.assertEqual(output, '')

    def test_handler_sleeper_api(self):
        event = {}
        app = firetail_app()
        app.enable_sleeper = True
        @firetail_handler(app)
        def handler(event, context):
            return 201, json.dumps({"message": "success"})
        
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            start = time.time()
            handler(event, "")
            end = time.time()
            
            difference = end - start
        output = temp_stdout.getvalue().strip()
        self.assertGreaterEqual(difference, .5)
        self.assertEqual(output, 'firetail:loggingapi:eyJldmVudCI6IHt9LCAicmVzcG9uc2UiOiBbMjAxLCAie1wibWVzc2FnZVwiOiBcInN1Y2Nlc3NcIn0iXX0=')

    def test_handler_sanitizer(self):
        event = api_gateway_v1
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
        def handler(event, context):
            return 201, json.dumps({"message": "success"})
        
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            handler(event, "")
            
        output = temp_stdout.getvalue().strip()
        self.assertEqual(output, 'firetail:loggingapi:eyJldmVudCI6IHsiYm9keSI6ICJleUowWlhOMElqb2lZbTlrZVNKOSIsICJyZXNvdXJjZSI6ICIve3Byb3h5K30iLCAicGF0aCI6ICIvcGF0aC90by9yZXNvdXJjZSIsICJodHRwTWV0aG9kIjogIlBPU1QiLCAiaXNCYXNlNjRFbmNvZGVkIjogdHJ1ZSwgInF1ZXJ5U3RyaW5nUGFyYW1ldGVycyI6IHsiZm9vIjogImJhciJ9LCAibXVsdGlWYWx1ZVF1ZXJ5U3RyaW5nUGFyYW1ldGVycyI6IHsiZm9vIjogWyJiYXIiXX0sICJwYXRoUGFyYW1ldGVycyI6IHsicHJveHkiOiAiL3BhdGgvdG8vcmVzb3VyY2UifSwgInN0YWdlVmFyaWFibGVzIjogeyJiYXoiOiAicXV4In0sICJoZWFkZXJzIjogeyJBY2NlcHQiOiAidGV4dC9odG1sLGFwcGxpY2F0aW9uL3hodG1sK3htbCxhcHBsaWNhdGlvbi94bWw7cT0wLjksaW1hZ2Uvd2VicCwqLyo7cT0wLjgiLCAiQWNjZXB0LUVuY29kaW5nIjogImd6aXAsIGRlZmxhdGUsIHNkY2giLCAiQWNjZXB0LUxhbmd1YWdlIjogImVuLVVTLGVuO3E9MC44IiwgIkNhY2hlLUNvbnRyb2wiOiAibWF4LWFnZT0wIiwgIkNsb3VkRnJvbnQtRm9yd2FyZGVkLVByb3RvIjogImh0dHBzIiwgIkNsb3VkRnJvbnQtSXMtRGVza3RvcC1WaWV3ZXIiOiAidHJ1ZSIsICJDbG91ZEZyb250LUlzLU1vYmlsZS1WaWV3ZXIiOiAiZmFsc2UiLCAiQ2xvdWRGcm9udC1Jcy1TbWFydFRWLVZpZXdlciI6ICJmYWxzZSIsICJDbG91ZEZyb250LUlzLVRhYmxldC1WaWV3ZXIiOiAiZmFsc2UiLCAiQ2xvdWRGcm9udC1WaWV3ZXItQ291bnRyeSI6ICJVUyIsICJIb3N0IjogIjEyMzQ1Njc4OTAuZXhlY3V0ZS1hcGkudXMtZWFzdC0xLmFtYXpvbmF3cy5jb20iLCAiVXBncmFkZS1JbnNlY3VyZS1SZXF1ZXN0cyI6ICIxIiwgIlVzZXItQWdlbnQiOiAiQ3VzdG9tIFVzZXIgQWdlbnQgU3RyaW5nIiwgIlZpYSI6ICIxLjEgMDhmMzIzZGVhZGJlZWZhN2FmMzRkNWZlYjQxNGNlMjcuY2xvdWRmcm9udC5uZXQgKENsb3VkRnJvbnQpIiwgIlgtQW16LUNmLUlkIjogImNEZWhWUW9abng0M1ZZUWI5ajItbnZDaC05ejM5NlVoYnAwMjdZMkp2a0NQTkxtR0pIcWxhQT09IiwgIlgtRm9yd2FyZGVkLUZvciI6ICIxMjcuMC4wLjEsIDEyNy4wLjAuMiIsICJYLUZvcndhcmRlZC1Qb3J0IjogIjQ0MyIsICJYLUZvcndhcmRlZC1Qcm90byI6ICJodHRwcyJ9LCAibXVsdGlWYWx1ZUhlYWRlcnMiOiB7IkFjY2VwdCI6IFsidGV4dC9odG1sLGFwcGxpY2F0aW9uL3hodG1sK3htbCxhcHBsaWNhdGlvbi94bWw7cT0wLjksaW1hZ2Uvd2VicCwqLyo7cT0wLjgiXSwgIkFjY2VwdC1FbmNvZGluZyI6IFsiZ3ppcCwgZGVmbGF0ZSwgc2RjaCJdLCAiQWNjZXB0LUxhbmd1YWdlIjogWyJlbi1VUyxlbjtxPTAuOCJdLCAiQ2FjaGUtQ29udHJvbCI6IFsibWF4LWFnZT0wIl0sICJDbG91ZEZyb250LUZvcndhcmRlZC1Qcm90byI6IFsiaHR0cHMiXSwgIkNsb3VkRnJvbnQtSXMtRGVza3RvcC1WaWV3ZXIiOiBbInRydWUiXSwgIkNsb3VkRnJvbnQtSXMtTW9iaWxlLVZpZXdlciI6IFsiZmFsc2UiXSwgIkNsb3VkRnJvbnQtSXMtU21hcnRUVi1WaWV3ZXIiOiBbImZhbHNlIl0sICJDbG91ZEZyb250LUlzLVRhYmxldC1WaWV3ZXIiOiBbImZhbHNlIl0sICJDbG91ZEZyb250LVZpZXdlci1Db3VudHJ5IjogWyJVUyJdLCAiSG9zdCI6IFsiMDEyMzQ1Njc4OS5leGVjdXRlLWFwaS51cy1lYXN0LTEuYW1hem9uYXdzLmNvbSJdLCAiVXBncmFkZS1JbnNlY3VyZS1SZXF1ZXN0cyI6IFsiMSJdLCAiVXNlci1BZ2VudCI6IFsiQ3VzdG9tIFVzZXIgQWdlbnQgU3RyaW5nIl0sICJWaWEiOiBbIjEuMSAwOGYzMjNkZWFkYmVlZmE3YWYzNGQ1ZmViNDE0Y2UyNy5jbG91ZGZyb250Lm5ldCAoQ2xvdWRGcm9udCkiXSwgIlgtQW16LUNmLUlkIjogWyJjRGVoVlFvWm54NDNWWVFiOWoyLW52Q2gtOXozOTZVaGJwMDI3WTJKdmtDUE5MbUdKSHFsYUE9PSJdLCAiWC1Gb3J3YXJkZWQtRm9yIjogWyIxMjcuMC4wLjEsIDEyNy4wLjAuMiJdLCAiWC1Gb3J3YXJkZWQtUG9ydCI6IFsiNDQzIl0sICJYLUZvcndhcmRlZC1Qcm90byI6IFsiaHR0cHMiXX0sICJyZXF1ZXN0Q29udGV4dCI6IHsiYWNjb3VudElkIjogIjEyMzQ1Njc4OTAxMiIsICJyZXNvdXJjZUlkIjogIjEyMzQ1NiIsICJzdGFnZSI6ICJwcm9kIiwgInJlcXVlc3RJZCI6ICJjNmFmOWFjNi03YjYxLTExZTYtOWE0MS05M2U4ZGVhZGJlZWYiLCAicmVxdWVzdFRpbWUiOiAiMDkvQXByLzIwMTU6MTI6MzQ6NTYgKzAwMDAiLCAicmVxdWVzdFRpbWVFcG9jaCI6IDE0Mjg1ODI4OTYwMDAsICJpZGVudGl0eSI6IHsiY29nbml0b0lkZW50aXR5UG9vbElkIjogbnVsbCwgImFjY291bnRJZCI6IG51bGwsICJjb2duaXRvSWRlbnRpdHlJZCI6IG51bGwsICJjYWxsZXIiOiBudWxsLCAiYWNjZXNzS2V5IjogbnVsbCwgInNvdXJjZUlwIjogIjEyNy4wLjAuMSIsICJjb2duaXRvQXV0aGVudGljYXRpb25UeXBlIjogbnVsbCwgImNvZ25pdG9BdXRoZW50aWNhdGlvblByb3ZpZGVyIjogbnVsbCwgInVzZXJBcm4iOiBudWxsLCAidXNlckFnZW50IjogIkN1c3RvbSBVc2VyIEFnZW50IFN0cmluZyIsICJ1c2VyIjogbnVsbH0sICJwYXRoIjogIi9wcm9kL3BhdGgvdG8vcmVzb3VyY2UiLCAicmVzb3VyY2VQYXRoIjogIi97cHJveHkrfSIsICJodHRwTWV0aG9kIjogIlBPU1QiLCAiYXBpSWQiOiAiMTIzNDU2Nzg5MCIsICJwcm90b2NvbCI6ICJIVFRQLzEuMSJ9fSwgInJlc3BvbnNlIjogWzIwMSwgIntcIm1lc3NhZ2VcIjogXCJzdWNjZXNzXCJ9Il19')


if __name__ == '__main__': # pragma: no cover
    unittest.main() # pragma: no cover
