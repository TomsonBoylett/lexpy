import unittest
import os

from lexpy.dawg import DAWG
from lexpy.exceptions import InvalidWildCardExpressionError


HERE = os.path.dirname(__file__)

class TestDAWGWordCount(unittest.TestCase):

    def test_with_count(self):
        d = DAWG()
        d.add_all([[l for l in 'ash'], [l for l in 'ashes'], [l for l in 'ashes'], [l for l in 'ashley']])
        d.reduce()
        expected = [([l for l in 'ash'], 1), ([l for l in 'ashes'], 2), ([l for l in 'ashley'], 1)]
        self.assertListEqual(expected, d.search('a*', with_count=True))

    def test_without_count(self):
        d = DAWG()
        d.add_all([[l for l in 'ash'], [l for l in 'ashes'], [l for l in 'ashes'], [l for l in 'ashley']])
        d.reduce()
        expected = [[l for l in 'ash'], [l for l in 'ashes'], [l for l in 'ashley']]
        self.assertListEqual(expected, d.search('a*'))