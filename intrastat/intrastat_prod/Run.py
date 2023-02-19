"""
Run the intrastat read, analyse, transform and export application.
"""
from intra.constants import Intrastat,CommodityCodes,FxRates
from intra.intrastat import IntrastatRATE
from intra.commodity_codes import CommodityCodesRTE
from intra.fx_rates import FxRatesRTE

def main():
    """
    Entry point to run intrastat rate process.
    """
    #Run sub rte processes to obtain url reference data.
    df_cn8_codes = CommodityCodesRTE().rte_process(CommodityCodes.URL)
    df_fx_rates = FxRatesRTE().rte_process(FxRates.URL, FxRates.XML_CHILD, FxRates.XML_NAMESPACES)
    #Run main rate intrastat process.
    IntrastatRATE().rate_process(Intrastat.URL, df_cn8_codes, df_fx_rates, Intrastat.OUTPUT_FILENAME)

if __name__ == '__main__':
    main()
