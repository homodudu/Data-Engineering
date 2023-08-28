"""
Run the intrastat read, analyse, transform and export application.
"""
import argparse
import logging
import logging.config
import yaml

from intra.intrastat import IntrastatRATE
from intra.commodity_codes import CommodityCodesRTE
from intra.fx_rates import FxRatesRTE

def main():
    """
    Entry point to run intrastat rate process.
    """
    # Parse YAML file as an argument object
    parser = argparse.ArgumentParser(description='Run the Intrastat RATE Job.')
    parser.add_argument('config', help='A configuration file in YAML format.')
    config_path = '/Users/macbook/Documents/Github/Data-Engineering/intrastat/intrastat_prod/configs/intrastat_config.yml'
    config = yaml.safe_load(open(config_path, encoding='utf8'))

    # Create and configure instance of logging.
    log_config = config['logging']
    logging.config.dictConfig(log_config)
    logger = logging.getLogger(__name__)

    # Read yaml configs
    cc_config = config['COMMODITY_CODES']
    fx_config = config['FX_RATES']
    intra_config = config['INTRASTAT']

    #Run sub rte processes to obtain url reference data.
    logger.info('Commodity code job started.')
    df_cn8_codes = CommodityCodesRTE().rte_process(cc_config['endpoint_url'])
    logger.info('Commodity code job finished.')
    logger.info('FX rate job started.')
    df_fx_rates = FxRatesRTE().rte_process(fx_config['endpoint_url'], fx_config['xml_child'], fx_config['xml_namespaces'])
    logger.info('FX rate job finished.')

    #Run main rate intrastat process.
    logger.info('Intrastat job started.')
    IntrastatRATE().rate_process(intra_config['endpoint_url'], df_cn8_codes, df_fx_rates, intra_config['output_filename'])
    logger.info('Intrastat job finished.')

if __name__ == '__main__':
    main()
