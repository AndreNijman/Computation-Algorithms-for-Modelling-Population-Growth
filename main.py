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
        n_initpopulation, n_growth_rate, n_growth_time_unit, n_model_type = naive_model()
        s_initpopulation, s_growth_rate, s_growth_time_unit, s_model_type, fission_event_frequency = sophisticated_model()

        projection_time = input_validation("Enter the amount of time to project into the future: ", type='int')
        projection_time_unit = input_validation("Enter the time unit (day, half-day, quarter-day, hour, minute): ", type='time_unit')

        print(run_models(n_initpopulation, n_growth_rate, n_growth_time_unit, n_model_type,
                         projection_time=projection_time, projection_time_unit=projection_time_unit))

        print(run_models(s_initpopulation, s_growth_rate, s_growth_time_unit, s_model_type,
                         fission_event_frequency=fission_event_frequency,
                         projection_time=projection_time, projection_time_unit=projection_time_unit))

def input_validation(prompt, type):
    '''
    Prompts the user for valid input based on type.
    Exits after 3 failed attempts.
    '''
    valid_menu = {'1', '2', '3', '4', '5', '6'}
    valid_units = {'day', 'half-day', 'quarter-day', 'hour', 'minute'}

    for _ in range(3):
        value = input(prompt).strip().lower()

        try:
            if type == 'menu' and value in valid_menu:
                run_chosen_module(int(value))
                return
            elif type == 'int':
                return int(value)
            elif type == 'float':
                return float(value)
            elif type == 'time_unit' and value in valid_units:
                return value
        except ValueError:
            pass

        print("Invalid input. Please try again.")

    print("Too many invalid attempts. Exiting. (AAHAAN, IK ITS YOU SPAMMING 😔)")
    exit()

def naive_model():
    '''
    This function runs the naive model.
    It prompts the user for input and returns parameters for a simple interest-based projection.
    '''
    print("\nNaive model")
    initial_population = input_validation("Enter the initial population: ", type='int')
    growth_rate = input_validation("Enter the growth rate (as a percentage without the symbol): ", type='float')
    growth_time_unit = input_validation("Enter the growth time unit (day, half-day, quarter-day, hour, minute): ", type='time_unit')
    return initial_population, growth_rate, growth_time_unit, "naive"

def sophisticated_model():
    '''
    This function runs the sophisticated model.
    It prompts the user for input and returns parameters for a compound interest-based projection with fission event timing.
    '''
    print("\nSophisticated model")
    initial_population = input_validation("Enter the initial population: ", type='int')
    growth_rate = input_validation("Enter the growth rate (as a percentage without the symbol): ", type='float')
    growth_time_unit = input_validation("Enter the growth time unit (day, half-day, quarter-day, hour, minute): ", type='time_unit')
    fission_event_frequency = input_validation("Enter the fission event frequency (day, half-day, quarter-day, hour, minute): ", type='time_unit')
    return initial_population, growth_rate, growth_time_unit, "sophisticated", fission_event_frequency

def run_models(initial_population, growth_rate, growth_time_unit, model_type, fission_event_frequency=None, projection_time=None, projection_time_unit=None):
    '''
    This function calculates and returns the projected population using the selected model type.
    For naive model: uses simple interest.
    For sophisticated model: uses compound interest adjusted by fission frequency.
    '''
    t = time_conversion(projection_time_unit, projection_time)  # Convert projection time to seconds

    if model_type == "naive":
        # A = P(1 + rt) for naive model
        return initial_population * (1 + (growth_rate / 100) * (t / time_conversion(growth_time_unit, 1)))

    elif model_type == "sophisticated":
        # A = P(1 + r/n)^(nt) for sophisticated model
        n = t / time_conversion(fission_event_frequency, 1)  # number of fission events
        r = (growth_rate / 100) / time_conversion(fission_event_frequency, 1)  # rate per second of fission interval
        return initial_population * (1 + r) ** n


def time_conversion(unit, amount):
    '''
    This function converts a time quantity from a unit to seconds.
    It takes the unit and the number of those units as arguments and returns the equivalent number of seconds.
    '''
    seconds_per_unit = {
        "day": 86400,
        "half-day": 43200,
        "quarter-day": 21600,
        "hour": 3600,
        "minute": 60,
        "second": 1
    }
    return seconds_per_unit[unit] * amount

# Call the menu function to display the menu and start the program
menu()
