

import contextlib
import json
import time
import unittest
from io import StringIO

from firetail_lambda import firetail_handler


class TestSimple(unittest.TestCase):

    def test_handler_api(self):
        event = {}
        @firetail_handler()
        def handler(event, context):
            return 201, json.dumps({"message": "success"})
        
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            handler(event, "")
        output = temp_stdout.getvalue().strip()
        self.assertEqual(output, 'firetail:loggingapi:eyJldmVudCI6IHt9LCAicmVzcG9uc2UiOiBbMjAxLCAie1wibWVzc2FnZVwiOiBcInN1Y2Nlc3NcIn0iXX0=')

    def test_incorrect_handler_api(self):
        event = {}
        @firetail_handler()
        def handler(argument):
            return 201, json.dumps({"message": "success"})
        
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            handler(event)
        output = temp_stdout.getvalue().strip()
        self.assertEqual(output, '')

    def test_handler_sleeper_api(self):
        event = {}
        @firetail_handler(enable_sleeper=True)
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


if __name__ == '__main__': # pragma: no cover
    unittest.main() # pragma: no cover
