""" TEST BOT """
# -*- coding: utf-8 -*-

import unittest
from .context import bot


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_traffic(self):
        """ testing """
        assert True


if __name__ == '__main__':
    unittest.main()
