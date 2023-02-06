"""
Intergration test the Intrastat component methods.
"""
import unittest
import pandas as pd
import intra.constants as cn

from intra.constants import Intrastat,CommodityCodes,FxRates
from intra.intrastat import IntrastatRATE
from intra.commodity_codes import CommodityCodesRTE
from intra.fx_rates import FxRatesRTE

class IntTestXetraETLMethods(unittest.TestCase):
    """
    Integration testing the Intrastat class.
    """
    def setUp(self):
        """
        Set up the environment
        """
        # Define the class arguments


    def test_int_intrastat(self):
        """
        Integration tests for rate method
        """
        # Expected results

        # Method execution

        # Test after method execution


    def tearDown(self):
        """
        Execute after unit tests
        """

if __name__ == '__main__':
    unittest.main()
