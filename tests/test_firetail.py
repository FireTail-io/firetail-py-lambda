import unittest
import json
import contextlib
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


if __name__ == '__main__':
    unittest.main()
