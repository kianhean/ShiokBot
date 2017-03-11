""" TEST LUCKY DRAW FUNCTIONS """
# -*- coding: utf-8 -*-

import unittest
from bot.draw import FourD


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_FourD(self):
        """ Testing 4D Results """
        test_api = FourD()
        assert len(test_api) > 50


if __name__ == '__main__':
    unittest.main()
