""" TEST GOV FUNCTIONS """
# -*- coding: utf-8 -*-

import unittest
from bot.gov import connnect_gov_api


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_connnect_gov_api(self):
        """ Testing Traffic Functions """
        test_api = connnect_gov_api('https://api.data.gov.sg/v1/transport/traffic-images')
        assert test_api.status_code is 200


if __name__ == '__main__':
    unittest.main()
