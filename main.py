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
        print("\nFuture Projection timeframe for both models")
        projection_time = input_validation("Enter the amount of time to project into the future: ", type='int')
        projection_time_unit = input_validation("Enter the time unit (day, half-day, quarter-day, hour, minute): ", type='time_unit')

        print(f"\nNaive Model: I = {n_initpopulation}, g = {n_growth_rate}% per {n_growth_time_unit}")
        print(f"Sophisticated Model: I = {s_initpopulation}, g = {s_growth_rate}% per {s_growth_time_unit}, fission event frequency = {fission_event_frequency}")
        print(f"Projection time: {projection_time} {projection_time_unit}\n")

        naive_result = run_models(n_initpopulation, n_growth_rate, n_growth_time_unit, n_model_type,
                                  projection_time=projection_time, projection_time_unit=projection_time_unit)
        print(f'Naive model projected population size: {naive_result}')

        sophisticated_result = run_models(s_initpopulation, s_growth_rate, s_growth_time_unit, s_model_type,
                                          fission_event_frequency=fission_event_frequency,
                                          projection_time=projection_time, projection_time_unit=projection_time_unit)
        print(f'Sophisticated model projected population size: {sophisticated_result}')

    if module_number == 2:
        print("\nTime for a sophisticated model to reach the target population")
        initial_population, growth_rate, growth_time_unit, model_type = sophisticated_model()
        target_population = input_validation("Enter the target population: ", type='int')
        fission_event_frequency = input_validation("Enter the fission-event frequency time unit (day, half-day, quarter-day, hour, minute): ", type='time_unit')

        if fission_event_frequency == "custom":
            custom_frequency = input_validation("Enter the number of fission events per growth rate time unit: ", type='float')
            fission_event_frequency = custom_frequency

        time_to_target = run_models(initial_population, growth_rate, growth_time_unit, model_type,
                                     fission_event_frequency=fission_event_frequency,
                                     projection_time=target_population, projection_time_unit="population")
        print(f'Time to reach target population: {time_to_target} seconds')


def input_validation(prompt, type):
    '''
    Prompts the user for valid input based on type.
    Exits after 3 failed attempts.
    '''
    valid_menu = {'1', '2', '3', '4', '5', '6'}
    valid_units = {'day', 'half-day', 'quarter-day', 'hour', 'minute', 'custom'}

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

    print("Too many invalid attempts. Exiting. AAHAAN STOP SPAMMING, IK ITS YOU 😔😔😔")
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
    fission_event_frequency = input_validation("Enter the fission-event frequency time unit (day, half-day, quarter-day, hour, minute, custom): ", type='time_unit')

    if fission_event_frequency == "custom":
        custom_frequency = input_validation("Enter the number of fission events per growth rate time unit: ", type='float')
        return initial_population, growth_rate, growth_time_unit, "sophisticated", custom_frequency

    return initial_population, growth_rate, growth_time_unit, "sophisticated", fission_event_frequency


def run_models(initial_population, growth_rate, growth_time_unit, model_type, fission_event_frequency=None, projection_time=None, projection_time_unit=None):
    '''
    This function calculates and returns the projected population using the selected model type.
    For naive model: uses simple interest.
    For sophisticated model: uses compound interest adjusted by fission frequency.
    '''

    total_projection_time_in_seconds = time_conversion(projection_time_unit, projection_time)  # Convert projection time to seconds
    growth_time_unit_in_seconds = time_conversion(growth_time_unit, 1) # Convert growth time unit to seconds

    if model_type == "naive":
        # A = P(1 + rt) for naive model
        projected_population = initial_population * (1 + (growth_rate / 100) * (total_projection_time_in_seconds / growth_time_unit_in_seconds))
        return projected_population

    elif model_type == "sophisticated":
        if isinstance(fission_event_frequency, str):  # Standard time unit
            fission_event_frequency_in_seconds = time_conversion(fission_event_frequency, 1)
            fissions_per_growth_unit = growth_time_unit_in_seconds / fission_event_frequency_in_seconds
        else:  # Custom frequency
            fissions_per_growth_unit = fission_event_frequency

        rate_per_fission = (growth_rate / 100) / fissions_per_growth_unit
        total_fissions = total_projection_time_in_seconds / growth_time_unit_in_seconds * fissions_per_growth_unit
        projected_population = initial_population * (1 + rate_per_fission) ** total_fissions
        return projected_population


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
