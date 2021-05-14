class Menu:
    """Classs that will display and provide selection options for menus in the terminal"""

    def __init__(self, options):
        self.options = options
        self.options_dict = {}
        self.setup_menu_dictionary()

    def setup_menu_dictionary(self):
        """Method that converts a list of options to a dictionary with the option number (selection) as the key and the option as the value"""
        for index, option in enumerate(self.options, 1):
            self.options_dict[index] = option

    def display_options(self):
        """ Prints the options with the selection keys"""
        print("\n Options:")
        for index, option in enumerate(self.options, 1):
            print(f"{index} : {option}")
        selection = input(">>: ")
        return self.choose_option(selection)

    def choose_option(self, selection):
        """ Method that will return the selected option or re-print the options if an invalid value is entered"""
        try:
            chosen_selection = self.options_dict[int(selection)]
            return chosen_selection
        except (KeyError, ValueError):
            print('\033[31m' + "Please select a valid number as shown in the options" '\033[0m')
            return self.display_options()
