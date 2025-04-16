import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import unittest
from unittest.mock import patch, MagicMock
from decimal import Decimal
from hello_world import app

class TestLambdaFunction(unittest.TestCase):

    @patch('hello_world.app.boto3.resource')
    def test_lambda_handler_success(self, mock_boto3_resource):
        # Mock the table and its methods
        mock_table = MagicMock()
        mock_table.get_item.return_value = {
            "Item": {"count": Decimal("5")}
        }
        mock_table.put_item.return_value = {}

        # Mock boto3.resource('dynamodb') to return an object with .Table() method that returns mock_table
        mock_dynamodb = MagicMock()
        mock_dynamodb.Table.return_value = mock_table
        mock_boto3_resource.return_value = mock_dynamodb

        event = {}
        context = {}
        response = app.lambda_handler(event, context)

        self.assertEqual(response['statusCode'], 200)
        self.assertIn('visitor_count', str(response['body']))

    def test_decimal_to_int(self):
        result = app.decimal_to_int(Decimal('10'))
        self.assertEqual(result, 10)

        with self.assertRaises(TypeError):
            app.decimal_to_int("not a decimal")

if __name__ == '__main__':
    unittest.main(verbosity=2)
