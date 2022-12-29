"""
Run the Xetra ETL application
"""

import logging
import logging.config
import yaml


def main():
    """
    Entry point to run xetra ETL job.
    """

    # Parsing YAML file.
    config_path = '/Users/macbook/Documents/Github/Data-Engineering/xetra_project/configs/xetra_report1_config.yml'
    config = yaml.safe_load(open(config_path))
    print(config)


    # Configure logging.
    log_config = config['logging']
    logging.config.dictConfig(log_config)
    logger = logging.getLogger(__name__)
    logger.info("This is a test logger message.")

if __name__ == '__main__':
    main()
