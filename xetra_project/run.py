"""
Run the Xetra ETL application
"""

import argparse
import logging
import logging.config
import yaml

from xetra.common.s3 import S3BucketConnector
from xetra.transformers.xetra_transformer import XetraETL, XetraSourceConfig, XetraTargetConfig

def main():
    """
    Entry point to run xetra ETL job.
    """

    # Parse YAML file as an argument object
    parser = argparse.ArgumentParser(description='Run the Xetra ETL Job.')
    parser.add_argument('config', help='A configuration file in YAML format.')
    args = parser.parse_args()

#   config_path = '/Users/macbook/Documents/Github/Data-Engineering/xetra_project/configs/xetra_report1_config.yml'
#   config = yaml.safe_load(open(config_path))
    config = yaml.safe_load(open(args.config, encoding="utf8"))

#    print(config)


    # Configure and create instance of logging.
    log_config = config['logging']
    logging.config.dictConfig(log_config)
    logger = logging.getLogger(__name__)

    # Read S3 configuration
    s3_config = config['S3']

    # Create S3Bucket connector classes for source and target
    s3_bucket_src = S3BucketConnector(access_key=s3_config['access_key'],
                                      secret_key=s3_config['secret_key'],
                                      endpoint_url=s3_config['src_endpoint_url'],
                                      bucket=s3_config['src_bucket'])
    s3_bucket_trg = S3BucketConnector(access_key=s3_config['access_key'],
                                      secret_key=s3_config['secret_key'],
                                      endpoint_url=s3_config['trg_endpoint_url'],
                                      bucket=s3_config['trg_bucket'])

    # Read source configuration
    source_config = XetraSourceConfig(**config['source'])

    # Read target configuration
    target_config = XetraTargetConfig(**config['target'])

    # Read meta file configuration
    meta_config = config['meta']

    # Create instance of XetraETL class
    logger.info('Xetra ETL job started.')
    xetra_etl = XetraETL(s3_bucket_src, s3_bucket_trg,
                         meta_config['meta_key'], source_config, target_config)

    # Run etl job for xetra report 1
    xetra_etl.etl_report1()
    logger.info('Xetra ETL job finished.')


if __name__ == '__main__':
    main()
