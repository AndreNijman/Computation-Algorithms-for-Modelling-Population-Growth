def menu(opt):
    '''
    This function displays a menu to the user and prompts for their choice.
    It returns the user's choice as a string.
    The menu includes options to compare models, time model projections, compare sophisticated models,
    generate detailed projections, and model increases in fission-event frequency.
    The user can also exit the program.
    '''
    if opt == 0:
        print("This program has five modules. Choose a module to run by typing its number")
        print("(1) Compare a naive and sophisticated model")
        print("(2) Time for a sophisticated model to reach the target population")
        print("(3) Compare two sophisticated population models")
        print("(4) Generate detailed projections formatted as columns")
        print("(5) Model increases in fission-event frequency")
        print("(6) Exit program")
        input_validation(prompt="Enter your choice: ", type='menu')
    elif opt == 1:
        print("Debug: Model 1 selected")
        naive_and_sophisticated_model()
    elif opt == 2:
        print("Debug: Model 2 selected")
        time_to_target_population()
    elif opt == 3:
        print("Debug: Model 3 selected")
        compare_sophisticated_models()
    elif opt == 4:
        print("Debug: Model 4 selected")
        generate_detailed_projections()
    elif opt == 5:
        print("Debug: Model 5 selected")
        fission_event_frequency()
    elif opt == 6:
        print("Debug: Exit selected")
        print("Exiting program. Goodbye!")
        exit()


def input_validation(prompt, type):
    '''
    This function prompts the user for input until they provide a valid choice.
    It returns the user's valid choice as a string.
    '''
    if type == 'menu':
        valid_choices = ['1', '2', '3', '4', '5', '6']
    while True:
        choice = input(prompt).strip()
        if choice in valid_choices:
            if type == 'menu':
                menu(int(choice))
        else:
            print(f"Invalid choice. Please enter one of the following: {', '.join(valid_choices)}")


def naive_and_sophisticated_model():
    print("This option is not implemented yet.")


def time_to_target_population():
    print("This option is not implemented yet.")


def compare_sophisticated_models():
    print("This option is not implemented yet.")


def generate_detailed_projections():
    print("This option is not implemented yet.")


def fission_event_frequency():
    print("This option is not implemented yet.")


# Call the menu function to display the menu and get the user's choice
menu(0)
