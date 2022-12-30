"""
TestS3BucketConnectorMethods
"""
import os
import unittest
from io import StringIO, BytesIO

import boto3
import pandas as pd
from moto import mock_s3

from xetra.common.s3 import S3BucketConnector
from xetra.common.custom_exceptions import WrongFormatException

class TestS3BucketConnectorMethods(unittest.TestCase):
    """
    Testing the S3BucketConnector class
    """

    def setUp(self):
        """
        Set up the environment
        """
        # Mocking s3 connection start
        self.mock_s3 = mock_s3()
        self.mock_s3.start()

        # Defining the class arguments
        self.s3_access_key = 'AWS_ACCESS_KEY_ID'
        self.s3_secret_key = 'AWS_SECRET_KEY_ID'
        self.s3_endpoint_url = 'https://s3-eu-west-2.amazonaws.com'
        self.s3_bucket_name = 'test-bucket'

        # Create s3 access keys as environment variables
        os.environ[self.s3_access_key] = 'KEY1'
        os.environ[self.s3_secret_key] = 'KEY2'

        # Create bucket on the mocked s3
        self.s3 = boto3.resource(service_name='s3', endpoint_url=self.s3_endpoint_url)
        self.s3.create_bucket(Bucket=self.s3_bucket_name,
                                 CreateBucketConfiguration={
                                        'LocationConstraint': 'eu-west-2'
        })
        self.s3_bucket = self.s3.Bucket(self.s3_bucket_name)

        # Create test instance
        self.s3_bucket_connector = S3BucketConnector(self.s3_access_key,
                                                     self.s3_secret_key,
                                                     self.s3_endpoint_url,
                                                     self.s3_bucket_name
                                                     )

    def test_list_files_in_prefix_ok(self):
        """
        Test the test_list_files_in_prefix for getting 2 file keys
        as list from mocked s3 bucket
        """
        # Expected results from correct prefix and uploaded files.
        prefix_exp = 'prefix/'
        key1_exp = f'{prefix_exp}test1.csv'
        key2_exp = f'{prefix_exp}test2.csv'

        # Test init
        csv_content = """col1, col1, valA, valB """
        self.s3.meta.client.put_object(Bucket=self.s3_bucket_name, Body=csv_content, Key=key1_exp)
        self.s3.meta.client.put_object(Bucket=self.s3_bucket_name, Body=csv_content, Key=key2_exp)

        # Method execution
        list_result = self.s3_bucket_connector.list_files_in_prefix(prefix_exp)

        # Tests after method execution
        self.assertEqual(len(list_result), 2)
        self.assertIn(key1_exp, list_result)
        self.assertIn(key2_exp, list_result)

        # Clean up after tests
        self.s3_bucket.delete_objects(
            Delete={
                'Objects': [
                    {
                        'Key': key1_exp
                    },
                    {
                        'Key': key2_exp
                    },
                ]
            }
        )

    def test_list_files_in_prefix_wrong_prefix(self):
        """
        Test the test_list_files_in_prefix method in cases of wrong
        or non-existing prefix from mocked s3 bicket
        """

        # Expected results from wrong prefix
        prefix_exp = 'no-prefix/'

        # Method execution
        list_result = self.s3_bucket_connector.list_files_in_prefix(prefix_exp)

        # Tests after method execution
        self.assertTrue(not list_result)

    def test_read_csv_to_df_ok(self):
        """
        Test the read_csv_to_df method for reading
        csv file from the mocked s3 bucket
        """

        # Expected results
        key_exp = 'test.csv'
        col1_exp = 'col1'
        col2_exp = 'col2'
        val1_exp = 'val1'
        val2_exp = 'val2'
        log_exp = f'Reading file {self.s3_endpoint_url}/{self.s3_bucket_name}/{key_exp}'

        # Test init
        csv_content = f'{col1_exp},{col2_exp}\n{val1_exp},{val2_exp}'
        self.s3_bucket.put_object(Body=csv_content, Key=key_exp)

        # Method execution
        with self.assertLogs() as logm:
            df_result = self.s3_bucket_connector.read_csv_to_df(key_exp)
            # Log test after method execution
            self.assertIn(log_exp, logm.output[0])

        # Test after method execution
        self.assertEqual(df_result.shape[0],1)
        self.assertEqual(df_result.shape[1],2)
        self.assertEqual(val1_exp, df_result[col1_exp][0])
        self.assertEqual(val2_exp, df_result[col2_exp][0])

        # Clean up after tests
        self.s3_bucket.delete_objects(
            Delete={
                'Objects': [
                    {
                        'Key': key_exp
                    },
                ]
            }
        )

    def test_write_df_to_s3_empty(self):
        """
        Test write_df_to_s3 method with an empty DataFrame as input
        """
        # Expected results
        return_exp = None
        log_exp = 'Dataframe is empty. No file to be written!'

        # Test init
        df_empty = pd.DataFrame()
        key_exp = 'key.csv'
        file_format = 'csv'

        # Method execution
        with self.assertLogs() as logm:
            result = self.s3_bucket_connector.write_df_to_s3(df_empty, key_exp, file_format)
            # Log test after method execution
            self.assertIn(log_exp, logm.output[0])

        # Test after method execution
        self.assertEqual(return_exp, result)

    def test_write_df_to_s3_csv(self):
        """
        Test write_df_to_s3_csv method is successful
        """

        # Expected results
        return_exp = True
        df_exp = pd.DataFrame([['A','B'], ['C', 'D']], columns = ['col1', 'col2'])
        key_exp = 'test.csv'
        log_exp = f'Writing file to {self.s3_endpoint_url}/{self.s3_bucket_name}/{key_exp}'

        # Test init
        file_format = 'csv'

        # Method execution
        with self.assertLogs() as logm:
            result = self.s3_bucket_connector.write_df_to_s3(df_exp, key_exp, file_format)
            df_result = self.s3_bucket_connector.read_csv_to_df(key_exp)
            # Log test after method execution
            self.assertIn(log_exp, logm.output[0])

        # Test after method execution
        data = self.s3_bucket.Object(key=key_exp).get().get('Body').read().decode('utf-8')
        out_buffer = StringIO(data)
        df_result = pd.read_csv(out_buffer)
        self.assertEqual(return_exp, result)
        self.assertTrue(df_exp.equals(df_result))

        # Cleanup after test
        self.s3_bucket.delete_objects(
            Delete={
                'Objects': [
                    {
                        'Key': key_exp
                    }
                ]
            }
        )

    def test_write_df_to_s3_parquet(self):
        """
        Test write_df_to_s3_parquet method is successful
        """

        # Expected results
        return_exp = True
        df_exp = pd.DataFrame([['A','B'], ['C', 'D']], columns = ['col1', 'col2'])
        key_exp = 'test.parquet'
        log_exp = f'Writing file to {self.s3_endpoint_url}/{self.s3_bucket_name}/{key_exp}'

        # Test init
        file_format = 'parquet'

        # Method execution
        with self.assertLogs() as logm:
            result = self.s3_bucket_connector.write_df_to_s3(df_exp, key_exp, file_format)
            # Log test after method execution
            self.assertIn(log_exp, logm.output[0])

        # Test after method execution
        data = self.s3_bucket.Object(key=key_exp).get().get('Body').read()
        out_buffer = BytesIO(data)
        df_result = pd.read_parquet(out_buffer)
        self.assertEqual(return_exp, result)
        self.assertTrue(df_exp.equals(df_result))

        # Cleanup after test
        self.s3_bucket.delete_objects(
            Delete={
                'Objects': [
                    {
                        'Key': key_exp
                    }
                ]
            }
        )

    def test_write_df_to_s3_wrong_format(self):
        """
        Test write_df_to_s3_parquet method with a not supported format
        """

        # Expected results
        df_exp = pd.DataFrame([['A','B'], ['C', 'D']], columns = ['col1', 'col2'])
        key_exp = 'test.parquet'
        format_exp = 'wrong_format'
        log_exp = f'Cannot write {format_exp} to S3. File format not supported!'
        exception_exp = WrongFormatException

        # Method execution
        with self.assertLogs() as logm:
            with self.assertRaises(exception_exp):
                self.s3_bucket_connector.write_df_to_s3(df_exp, key_exp, format_exp)
            # Log test after method execution
            self.assertIn(log_exp, logm.output[0])

    def tearDown(self):
        """
        Execute after unit tests
        """
        # Mocking s3 connection stop
        self.mock_s3.stop()

if __name__ == "__main__":
    unittest.main()
