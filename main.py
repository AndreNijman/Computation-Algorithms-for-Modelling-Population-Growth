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
        print("This option is not implemented yet.")
    elif opt == 2:
        print("This option is not implemented yet.")
    elif opt == 3:
        print("This option is not implemented yet.")
    elif opt == 4:
        print("This option is not implemented yet.")
    elif opt == 5:
        print("This option is not implemented yet.")
    elif opt == 6:
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
            menu(choice)
        else:
            print(f"Invalid choice. Please enter one of the following: {', '.join(valid_choices)}")

# Call the menu function to display the menu and get the user's choice
menu(0)