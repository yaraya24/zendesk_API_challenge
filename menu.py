class Menu:

    def __init__(self, options):
        self.options = options
        self.options_dict = {}
        self.setup_menu_dictionary()


    def setup_menu_dictionary(self):
        for index, option in enumerate(self.options, 1):
            self.options_dict[index] = option
         

    def display_options(self):
        print('\n Options:')
        for index, option in enumerate(self.options, 1):
            print(f'{index} : {option}')
        selection = input(">>: ")
        return self.choose_option(selection)

    
    def choose_option(self, selection):
        try:
            chosen_selection = self.options_dict[int(selection)]
            return chosen_selection
        except (KeyError, ValueError):
            print(f"Please select a valid number as shown in the options")
            return self.display_options()
        

        






