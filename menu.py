class Menu:

    def __init__(self, options):
        self.options = options
        self.options_dict = {}
        self.setup_menu_dictionary()


    def setup_menu_dictionary(self):
        for index, option in enumerate(self.options, 1):
            self.options_dict[index] = option
         

    def display_options(self):
        for index, option in enumerate(self.options, 1):
            print(f'{index} : {option}')
        selection = input(">>: ")
        self.choose_option(selection)

    
    def choose_option(self, selection):
        print(self.options_dict)
        try:
            chosen_selection = self.options_dict[int(selection)]
            return chosen_selection
        except KeyError:
            print(f"Please select an option between 1 and {len(self.options)}")
            self.display_options()

    




