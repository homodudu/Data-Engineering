"""
Connector and methods accessing S3
"""

import os
import logging
from io import StringIO, BytesIO
from memory_profiler import profile

import boto3
import pandas as pd

from xetra.common.constants import S3FileTypes
from xetra.common.custom_exceptions import WrongFormatException

class S3BucketConnector():
    """
    Class for interacting with S3 buckets
    """
    def __init__(self, access_key: str, secret_key: str, endpoint_url: str, bucket: str):
        """
        Constructor (initialise attributes) for S3BucketConnector

        :param access_key: accesskey for accessing S3
        :param secret_key: secretkey for accessing S3
        :param endpoint_url: endpoint url to S3
        :param bucket: S3 bucket name
        """

        self._logger = logging.getLogger(__name__)
        self.endpoint_url = endpoint_url
        self.session = boto3.Session(aws_access_key_id=os.environ[access_key],
                                     aws_secret_access_key=os.environ[secret_key])
        self._s3 = self.session.resource(service_name='s3', endpoint_url=endpoint_url)
        self._bucket = self._s3.Bucket(bucket)

    @profile
    def list_files_in_prefix(self, prefix: str):
        """
        List all files with a prefix on the the S3 bucket

        param prefix: prefix on the S3 bucket that should be filtered

        returns:
            files: list of all files containing prefix in the key
        """
        files = [obj.key for obj in self._bucket.objects.filter(Prefix=prefix)]
        return files

    @profile
    def read_csv_to_df(self, key: (str), encoding: str = 'utf-8', sep: str = ','):
        """
        Read csv file from S3 bucket and return a dataframe

        :param key: key of file to be read
        :encoding: encoding of the data inside csv file
        :sep: separator of csv file

        param prefix: prefix on the S3 bucket that should be filtered

        returns:
            data-frame: Pandas Dataframe containing CSV file data
        """
        self._logger.info('Reading file %s/%s/%s/', self.endpoint_url, self._bucket.name, key)
        csv_obj = self._bucket.Object(key=key).get().get('Body').read().decode(encoding)
        data = StringIO(csv_obj)
        data_frame = pd.read_csv(data, sep=sep)
        return data_frame

    @profile
    def write_df_to_s3(self, data_frame: pd.DataFrame, key: str, file_format: str):
        """
        Write pandas dataframe to S3 bucket
        supported formats: .csv, .parquet

        :data_frame: Pandas Dataframe that should be written
        :key: target key of the saved file
        :file_format: format of the saved file
        """
        if data_frame.empty:
            self._logger.info('Dataframe is empty. No file to be written!')
            return None

        if file_format == S3FileTypes.CSV.value:
            out_buffer = StringIO()
            data_frame.to_csv(out_buffer, index=False)
            return self.__put_object(out_buffer,key)

        if file_format == S3FileTypes.PARQUET.value:
            out_buffer = BytesIO()
            data_frame.to_parquet(out_buffer, index=False)
            return self.__put_object(out_buffer,key)

        self._logger.info('Cannot write %s to S3. File format not supported!', file_format)
        raise WrongFormatException

    @profile
    def __put_object(self, out_buffer: StringIO or BytesIO, key: str):
        """
        Helper function for self.write_df_to_s3()

        :out_buffer: StringIO | BytesIO that should be written
        :key: target key of the saved file
        """

        self._logger.info('Writing file to %s/%s/%s/', self.endpoint_url, self._bucket.name, key)
        self._bucket.put_object(Body=out_buffer.getvalue(), Key=key)
        return True
