"""
TestS3BucketConnectorMethods
"""

import os
import unittest

import boto3
from moto import mock_s3

from xetra.common.s3 import S3BucketConnector

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
        list_result = self.s3_bucket_connector.list_file_in_prefix(prefix_exp)

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
        list_result = self.s3_bucket_connector.list_file_in_prefix(prefix_exp)

        # Tests after method execution
        self.assertTrue(not list_result)

    def tearDown(self):
        """
        Execute after unit tests
        """
        # Mocking s3 connection stop
        self.mock_s3.stop()

if __name__ == "__main__":
    unittest.main()
