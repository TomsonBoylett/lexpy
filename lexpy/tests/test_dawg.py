import os
import unittest

from lexpy.dawg import DAWG
from lexpy.utils import build_dawg_from_file
from lexpy.exceptions import InvalidWildCardExpressionError

HERE = os.path.dirname(__file__)

large_dataset = os.path.join(HERE, 'data/ridyhew_master.txt')
small_dataset = os.path.join(HERE, 'data/TWL06.txt')


class TestWordCount(unittest.TestCase):

    def test_word_count_greater_than_zero(self):
        self.dawg = DAWG()
        self.dawg.add_all([['a', 's', 'h'], ['a', 's', 'h', 'e', 's'], ['a', 's', 'h', 'l', 'e', 'y']])
        self.dawg.reduce()
        self.assertGreater(self.dawg.get_word_count(), 0, "The number of words should be greater than 0")
        self.assertEqual(3, self.dawg.get_word_count(), "Word count not equal")

    def test_word_count_zero(self):
        self.dawg = DAWG()
        self.dawg.add_all([])
        self.dawg.reduce()
        self.assertEqual(0, self.dawg.get_word_count(), "Word count not equal")


class TestDAWGExactWordSearch(unittest.TestCase):

    def test_word_in_dawg(self):
        self.dawg = DAWG()
        self.dawg.add_all([['a', 's', 'h'], ['a', 's', 'h', 'l', 'e', 'y']])
        self.dawg.reduce()
        self.assertTrue(['a', 's', 'h'] in self.dawg, "Word should be in dawg")

    def test_word_not_int_dawg1(self):
        self.dawg = DAWG()
        self.dawg.add_all([['a', 's', 'h'], ['a', 's', 'h', 'l', 'e', 'y']])
        self.dawg.reduce()
        self.assertFalse(['s', 'a', 'l' , 'a', 'r', 'y'] in self.dawg, "Word should not be in dawg")
    
    def test_word_not_int_dawg2(self):
        self.dawg = DAWG()
        self.dawg.add_all([['a', 's', 'h'], ['a', 's', 'h', 'l', 'e', 'y']])
        self.dawg.reduce()
        self.assertFalse([l for l in 'mash lolley'] in self.dawg, "Word should not be in dawg")

class TesDAWGWordInsert(unittest.TestCase):

    def test_word_add(self):
        self.dawg = DAWG()
        self.dawg.add([l for l in 'axe'])
        self.assertIsInstance(self.dawg, DAWG, "Object should be of type `lexpy.dawg.DAWG`")
        self.assertTrue([l for l in 'axe'] in self.dawg, "Word should be in dawg")


    def test_word_add_all_list(self):
        self.dawg = DAWG()
        self.dawg.add_all([[l for l in 'axe'], [l for l in 'kick']]) #list
        self.dawg.reduce()
        self.assertIsInstance(self.dawg, DAWG, "Object should be of type `lexpy.dawg.DAWG`")
        self.assertTrue([l for l in 'axe'] in self.dawg, "Word should be in dawg")
        self.assertTrue([l for l in 'kick'] in self.dawg, "Word should be in dawg")
        self.assertEqual(2, self.dawg.get_word_count(), "Word count not equal")

    def test_word_add_all_tuple(self):
        self.dawg = DAWG()
        self.dawg.add_all(([l for l in 'axe'], [l for l in 'kick'])) #tuple
        self.dawg.reduce()
        self.assertIsInstance(self.dawg, DAWG, "Object should be of type `lexpy.dawg.DAWG`")
        self.assertTrue([l for l in 'axe'] in self.dawg, "Word should be in dawg")
        self.assertTrue([l for l in 'kick'] in self.dawg, "Word should be in dawg")
        self.assertEqual(2, self.dawg.get_word_count(), "Word count not equal")

    def test_word_add_all_with_number(self):
        self.dawg = DAWG()
        self.dawg.add_all(([l for l in 'axe'], [l for l in 'kick'])) #tuple with one integer.
        self.dawg.reduce()
        self.assertIsInstance(self.dawg, DAWG, "Object should be of type `lexpy.dawg.DAWG`")
        self.assertTrue([l for l in 'axe'] in self.dawg, "Word should be in dawg")
        self.assertTrue([l for l in 'kick'] in self.dawg, "Word should be in dawg")
        self.assertEqual(2, self.dawg.get_word_count(), "Word count not equal")

    def test_word_add_all_gen(self):
        def gen_words():
            a = [[l for l in 'ash'], [l for l in 'ashley'], [l for l in 'simpson']]
            for word in a:
                yield word
        self.dawg = DAWG()
        self.dawg.add_all(gen_words()) # generator
        self.dawg.reduce()
        self.assertIsInstance(self.dawg, DAWG, "Object should be of type `lexpy.dawg.DAWG`")
        self.assertTrue([l for l in 'ash'] in self.dawg, "Word should be in dawg")
        self.assertTrue([l for l in 'ashley'] in self.dawg, "Word should be in dawg")
        self.assertTrue([l for l in 'simpson'] in self.dawg, "Word should be in dawg")
        self.assertEqual(3, self.dawg.get_word_count(), "Word count not equal")

    def test_word_add_all_file_path(self):
        self.dawg = DAWG()
        self.dawg.add_all(small_dataset) # From a file
        self.dawg.reduce()
        self.assertIsInstance(self.dawg, DAWG, "Object should be of type `lexpy.dawg.DAWG`")
        self.assertTrue([l for l in 'AARGH'] in self.dawg, "Word should be in dawg")
        self.assertTrue([l for l in 'AARRGHH'] in self.dawg, "Word should be in dawg")
        self.assertTrue([l for l in 'AAS'] in self.dawg, "Word should be in dawg")
        self.assertEqual(178691, self.dawg.get_word_count(), "Word count not equal")


class TestDAWGNodeCount(unittest.TestCase):

    def test_dawg_node_count(self):
        self.dawg = DAWG()
        self.dawg.add_all([[l for l in 'ash'], [l for l in 'ashley']])
        self.dawg.reduce()
        self.assertIsInstance(self.dawg, DAWG, "Object should be of type `lexpy.dawg.DAWG`")
        self.assertTrue([l for l in 'ash'] in self.dawg, "Word should be in dawg")
        self.assertTrue([l for l in 'ashley'] in self.dawg, "Word should be in dawg")
        self.assertEqual(2, self.dawg.get_word_count(), "Word count not equal")
        self.assertEqual(6, len(self.dawg), "Number of nodes")

    def test_dawg_reduced_node_count(self):
        self.dawg = DAWG()
        self.dawg.add_all([[l for l in 'tap'], [l for l in 'taps'], [l for l in 'top'], [l for l in 'tops']])
        self.dawg.reduce()
        self.assertEqual(6, len(self.dawg), "Number of nodes")


class TestDAWGPrefixExists(unittest.TestCase):
    def test_dawg_node_prefix_exists(self):
        self.dawg = DAWG()
        self.dawg.add_all([[l for l in 'ash'], [l for l in 'ashley']])
        self.dawg.reduce()
        self.assertIsInstance(self.dawg, DAWG, "Object should be of type `lexpy.dawg.DAWG`")
        self.assertTrue([l for l in 'ash'] in self.dawg, "Word should be in dawg")
        self.assertTrue([l for l in 'ashley'] in self.dawg, "Word should be in dawg")
        self.assertEqual(2, self.dawg.get_word_count(), "Word count not equal")

        self.assertTrue(self.dawg.contains_prefix([l for l in 'ash']), "Prefix should be present in DAWG")
        self.assertTrue(self.dawg.contains_prefix([l for l in 'as']), "Prefix should be present in DAWG")
        self.assertTrue(self.dawg.contains_prefix([l for l in 'a']), "Prefix should be present in DAWG")

    def test_dawg_node_prefix_not_exists(self):
        self.dawg = DAWG()
        self.dawg.add_all([[l for l in 'ash'], [l for l in 'ashley']])
        self.dawg.reduce()
        self.assertIsInstance(self.dawg, DAWG, "Object should be of type `lexpy.dawg.DAWG`")
        self.assertTrue([l for l in 'ash'] in self.dawg, "Word should be in dawg")
        self.assertTrue([l for l in 'ashley'] in self.dawg, "Word should be in dawg")
        self.assertEqual(2, self.dawg.get_word_count(), "Word count not equal")
        self.assertFalse(self.dawg.contains_prefix([l for l in 'xmas']), "Prefix should be present in DAWG")
        self.assertFalse(self.dawg.contains_prefix([l for l in 'xor']), "Prefix should be present in DAWG")
        self.assertFalse(self.dawg.contains_prefix([l for l in 'sh']), "Prefix should be present in DAWG")


class TestDAWGPrefixSearch(unittest.TestCase):
    def test_dawg_prefix_search(self):
        self.dawg = DAWG()
        self.dawg.add_all([[l for l in 'ashlame'], [l for l in 'ashley'], [l for l in 'ashlo'], [l for l in 'askoiu']])
        self.dawg.reduce()
        self.assertIsInstance(self.dawg, DAWG, "Object should be of type `lexpy.dawg.DAWG`")
        self.assertFalse([l for l in 'ash'] in self.dawg, "Word should not be in dawg")
        self.assertTrue([l for l in 'ashley'] in self.dawg, "Word should be in dawg")
        self.assertEqual(4, self.dawg.get_word_count(), "Word count not equal")
        self.assertTrue(self.dawg.contains_prefix([l for l in 'ash']), "Prefix should be present in DAWG")
        self.assertEqual(sorted(self.dawg.search_with_prefix([l for l in 'ash'])), sorted([[l for l in 'ashlame'], [l for l in 'ashley'], [l for l in 'ashlo']]),
                              'The lists should be equal')


class TestWildCardSearch(unittest.TestCase):
    def test_dawg_asterisk_search(self):
        self.dawg = DAWG()
        self.dawg.add_all([[l for l in 'ash'], [l for l in 'ashley']])
        self.dawg.reduce()
        self.assertIsInstance(self.dawg, DAWG, "Object should be of type `lexpy.dawg.DAWG`")
        self.assertTrue([l for l in 'ash'] in self.dawg, "Word should be in dawg")
        self.assertTrue([l for l in 'ashley'] in self.dawg, "Word should be in dawg")
        self.assertEqual(sorted(self.dawg.search('a*')), sorted([[l for l in 'ash'], [l for l in 'ashley']]), 'The lists should be equal')

    def test_dawg_question_search(self):
        self.dawg = DAWG()
        self.dawg.add_all([[l for l in 'ab'], [l for l in 'as'], [l for l in 'ash'], [l for l in 'ashley']])
        self.dawg.reduce()
        self.assertIsInstance(self.dawg, DAWG, "Object should be of type `lexpy.dawg.DAWG`")
        self.assertTrue([l for l in 'ash'] in self.dawg, "Word should be in dawg")
        self.assertTrue([l for l in 'ashley'] in self.dawg, "Word should be in dawg")
        self.assertEqual(sorted(self.dawg.search('a?')), sorted([[l for l in 'ab'], [l for l in 'as']]), 'The lists should be equal')

    def test_dawg_wildcard_search(self):
        self.dawg = DAWG()
        self.dawg.add_all([[l for l in 'ab'], [l for l in 'as'], [l for l in 'ash'], [l for l in 'ashley']])
        self.dawg.reduce()
        self.assertIsInstance(self.dawg, DAWG, "Object should be of type `lexpy.dawg.DAWG`")
        self.assertTrue([l for l in 'ash'] in self.dawg, "Word should be in dawg")
        self.assertTrue([l for l in 'ashley'] in self.dawg, "Word should be in dawg")
        self.assertEqual(sorted(self.dawg.search('*a******?')), sorted([[l for l in 'ab'], [l for l in 'as'], [l for l in 'ash'], [l for l in 'ashley']]),
                              'The lists should be equal')

    def test_dawg_wildcard_exception(self):
        self.dawg = DAWG()
        self.dawg.add_all([[l for l in 'ab'], [l for l in 'as'], [l for l in 'ash'], [l for l in 'ashley']])
        self.dawg.reduce()
        self.assertIsInstance(self.dawg, DAWG, "Object should be of type `lexpy.dawg.DAWG`")
        self.assertTrue([l for l in 'ash'] in self.dawg, "Word should be in dawg")
        self.assertTrue([l for l in 'ashley'] in self.dawg, "Word should be in dawg")
        self.assertRaises(InvalidWildCardExpressionError, self.dawg.search, '#$%^a')


class TestBuildFromFile(unittest.TestCase):
    def test_dawg_build_from_file_path(self):
        self.dawg = build_dawg_from_file(small_dataset)
        self.dawg.reduce()
        self.assertIsInstance(self.dawg, DAWG, "Object should be of type `lexpy.dawg.DAWG`")
        self.assertTrue([l for l in 'ZYGOMORPHIES'] in self.dawg, "Word should be in dawg")
        self.assertTrue([l for l in 'ZYGOMATA'] in self.dawg, "Word should be in dawg")
        self.assertTrue([l for l in 'ZYGOMORPHY'] in self.dawg, "Word should be in dawg")
        self.assertEqual(178691, self.dawg.get_word_count(), "Word count not equal")

    def test_dawg_build_from_file_object(self):
        with open(small_dataset, 'r') as input_file:
            self.dawg = build_dawg_from_file(input_file)
            self.dawg.reduce()
        self.assertIsInstance(self.dawg, DAWG, "Object should be of type `lexpy.dawg.DAWG`")
        self.assertTrue([l for l in 'ZYGOMORPHIES'] in self.dawg, "Word should be in dawg")
        self.assertTrue([l for l in 'ZYGOMATA'] in self.dawg, "Word should be in dawg")
        self.assertTrue([l for l in 'ZYGOMORPHY'] in self.dawg, "Word should be in dawg")
        self.assertEqual(178691, self.dawg.get_word_count(), "Word count not equal")


class TestSearchWithinDistance(unittest.TestCase):

    def test_edit_distance_search(self):
        self.dawg = DAWG()
        input_words = [[l for l in 'abhor'], [l for l in 'abuzz'], [l for l in 'accept'], [l for l in 'acorn'], [l for l in 'agony'], [l for l in 'albay'], [l for l in 'albin'], [l for l in 'algin'], [l for l in 'alisa'], [l for l in 'almug'],
                       [l for l in 'altai'], [l for l in 'amato'], [l for l in 'ampyx'], [l for l in 'aneto'], [l for l in 'arbil'], [l for l in 'arrow'], [l for l in 'artha'], [l for l in 'aruba'], [l for l in 'athie'], [l for l in 'auric'],
                       [l for l in 'aurum'], [l for l in 'cap'], [l for l in 'common'], [l for l in 'dime'], [l for l in 'eyes'], [l for l in 'foot'], [l for l in 'likeablelanguage'], [l for l in 'lonely'], [l for l in 'look'],
                       [l for l in 'nasty'], [l for l in 'pet'], [l for l in 'psychotic'], [l for l in 'quilt'], [l for l in 'shock'], [l for l in 'smalldusty'], [l for l in 'sore'], [l for l in 'steel'], [l for l in 'suit'],
                       [l for l in 'tank'], [l for l in 'thrill']]
        self.dawg.add_all(input_words)
        self.dawg.reduce()
        self.assertListEqual(self.dawg.search_within_distance([l for l in 'arie'], dist=2), [[l for l in 'arbil'], [l for l in 'athie'], [l for l in 'auric']])



if __name__ == '__main__':
    unittest.main()