import unittest
from menu import Menu

class test_menus(unittest.TestCase):
    def setUp(self):
        self.menus = Menu(['red', 'green', 'black', 'blue'])

    def test_menu_options(self):
        self.assertEqual(self.menus.options, ['red', 'green', 'black', 'blue'])
        self.assertEqual(self.menus.options_dict[1], 'red')
        self.assertEqual(self.menus.options_dict[2], 'green')
        self.assertEqual(self.menus.options_dict[3], 'black')
        self.assertEqual(self.menus.options_dict[4], 'blue')
        self.assertEqual(len(self.menus.options), 4)
        self.assertEqual(len(self.menus.options_dict), 4)

    def test_menu_selection(self):
        chosen_selection = self.menus.choose_option(1)
        self.assertTrue(chosen_selection == 'red')
        chosen_selection = self.menus.choose_option(4)
        self.assertTrue(chosen_selection == 'blue')
        
        