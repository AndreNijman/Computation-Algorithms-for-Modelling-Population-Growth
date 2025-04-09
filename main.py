def menu():
    '''
    This function displays a menu to the user and prompts for their choice.
    It returns the user's choice as a string.
    The menu includes options to compare models, time model projections, compare sophisticated models,
    generate detailed projections, and model increases in fission-event frequency.
    The user can also exit the program.
    '''
    print("This program has five modules. Choose a module to run by typing its number")
    print("(1) Compare a naive and sophisticated model")
    print("(2) Time for a sophisticated model to reach the target population")
    print("(3) Compare two sophisticated population models")
    print("(4) Generate detailed projections formatted as columns")
    print("(5) Model increases in fission-event frequency")
    print("(6) Exit program")
    input_validation(prompt="Enter your choice: ", type='menu')


def run_chosen_module(module_number):
    '''
    This function runs the chosen module based on the user's input.
    It takes the module number as an argument and calls the corresponding function.
    '''
    if module_number == 1:
        naive_model()
        sophisticated_model()
    elif module_number == 2:
        print("Debug: Module 2 selected")
    elif module_number == 3:
        print("Debug: Module 3 selected")
    elif module_number == 4:
        print("Debug: Module 4 selected")
    elif module_number == 5:
        print("Debug: Module 5 selected")


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
                run_chosen_module(int(choice))
                break
        else:
            print(f"Invalid choice. Please enter one of the following: {', '.join(valid_choices)}")


def naive_model():
    '''
    This function runs the naive model.
    It prompts the user for input and performs calculations based on the naive model.
    '''
    initial_population = int(input("Enter the initial population: "))
    growth_rate = float(input("Enter the growth rate (as a percentage without the symbol): "))
    growth_time_unit = input("Enter the growth time unit (day, half-day, quarter-day, hour, minute): ").strip().lower()
    
    return initial_population, growth_rate, growth_time_unit, "naive"

def sophisticated_model():
    '''
    This function runs the sophisticated model.
    It prompts the user for input and performs calculations based on the sophisticated model.
    '''
    initial_population = int(input("Enter the initial population: "))
    growth_rate = float(input("Enter the growth rate (as a percentage without the symbol): "))
    growth_time_unit = input("Enter the growth time unit (day, half-day, quarter-day, hour, minute): ").strip().lower()
    return initial_population, growth_rate, growth_time_unit, "sophisticated"

def run_models(initial_population, growth_rate, growth_time_unit, model_type):
    '''
    This function runs the chosen model (naive or sophisticated) based on the user's input.
    It performs calculations and displays the results.
    '''
    if model_type == "naive":
        # Perform naive model calculations
        print("Running naive model...")
        # Add your calculations here
    elif model_type == "sophisticated":
        # Perform sophisticated model calculations
        print("Running sophisticated model...")
        # Add your calculations here
        
        
def time_conversion():
    periods = {
        "day":86400,
        "half-day":43200,
        "quarter-day":60*60*6,
        "hour":3600,
        "minute":60,
        "second":1
    }
    c = periods[period]/periods[convert]
    print(str(c))
amount = time_conversion()
print(f"There are {amount} {period}s in {convert}.")


# Call the menu function to display the menu and get the user's choice
menu()
#A = P(1+rt)
#A = P(1+(r/n))^nt
