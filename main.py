def menu():
    '''
    Displays the main menu to the user and prompts for their selection.
    Calls input validation to handle the choice.
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
    Runs the selected module based on user input.
    '''
    if module_number == 1:
        # Naive model input
        n_init, n_rate, n_unit, n_type = naive_model()

        # Sophisticated model input
        s_init, s_rate, s_unit, s_type, s_freq = sophisticated_model()

        # Timeframe input
        print("\nFuture Projection timeframe for both models")
        proj_time = input_validation("Enter the amount of time to project into the future: ", type='int')
        proj_unit = input_validation("Enter the time unit (day, half-day, quarter-day, hour, minute): ", type='time_unit')

        # Summarise inputs
        print(f"\nNaive Model: I = {n_init}, g = {n_rate}% per {n_unit}")
        print(f"Sophisticated Model: I = {s_init}, g = {s_rate}% per {s_unit}, fission event frequency = {s_freq}")
        print(f"Projection time: {proj_time} {proj_unit}\n")

        # Run projections
        naive_result = run_models(n_init, n_rate, n_unit, n_type,
                                  projection_time=proj_time, projection_time_unit=proj_unit)
        print(f'Naive model projected population size: {naive_result}')

        sophisticated_result = run_models(s_init, s_rate, s_unit, s_type,
                                          fission_event_frequency=s_freq,
                                          projection_time=proj_time, projection_time_unit=proj_unit)
        print(f'Sophisticated model projected population size: {sophisticated_result}')

    elif module_number == 2:
        # Sophisticated model input
        s_init, s_rate, s_unit, s_type, s_freq = sophisticated_model()

        # Target population input
        target = input_validation("Enter the target population: ", type='int')

        # Summarise inputs
        print(f"\nSophisticated Model: I = {s_init}, g = {s_rate}% per {s_unit}, fission event frequency = {s_freq}")
        print(f"Target amount: {target}\n")

        # Run projection to target
        result = run_models(s_init, s_rate, s_unit, s_type,
                            fission_event_frequency=s_freq,
                            projection_time=target, projection_time_unit="population")
        print(f'Time to reach target population: {result} seconds')


def input_validation(prompt, type):
    '''
    Validates user input based on the expected type.
    Retries up to 3 times before exiting the program.
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
    Collects input values for the naive population model.
    Returns initial population, growth rate, time unit, and model type.
    '''
    print("\nNaive model")
    init = input_validation("Enter the initial population: ", type='int')
    rate = input_validation("Enter the growth rate (as a percentage without the symbol): ", type='float')
    unit = input_validation("Enter the growth time unit (day, half-day, quarter-day, hour, minute): ", type='time_unit')
    return init, rate, unit, "naive"


def sophisticated_model():
    '''
    Collects input values for the sophisticated population model.
    Returns initial population, growth rate, time unit, model type, and fission-event frequency.
    '''
    print("\nSophisticated model")
    init = input_validation("Enter the initial population: ", type='int')
    rate = input_validation("Enter the growth rate (as a percentage without the symbol): ", type='float')
    unit = input_validation("Enter the growth time unit (day, half-day, quarter-day, hour, minute): ", type='time_unit')
    freq = input_validation("Enter the fission-event frequency time unit (day, half-day, quarter-day, hour, minute, custom): ", type='time_unit')

    if freq == "custom":
        freq = input_validation("Enter the number of fission events per growth rate time unit: ", type='float')

    return init, rate, unit, "sophisticated", freq


def run_models(initial_population, growth_rate, growth_time_unit, model_type,
               fission_event_frequency=None, projection_time=None, projection_time_unit=None):
    '''
    Calculates and returns the projected population or time based on model type.
    '''
    total_projection_time = time_conversion(projection_time_unit, projection_time)
    growth_unit_time = time_conversion(growth_time_unit, 1)

    if model_type == "naive":
        # Simple interest formula
        return initial_population * (1 + (growth_rate / 100) * (total_projection_time / growth_unit_time))

    elif model_type == "sophisticated":
        if isinstance(fission_event_frequency, str):
            fission_time = time_conversion(fission_event_frequency, 1)
            fissions_per_unit = growth_unit_time / fission_time
        else:
            fissions_per_unit = fission_event_frequency

        rate_per_fission = (growth_rate / 100) / fissions_per_unit

        if projection_time_unit == "population":
            # Compute how long until the population reaches the target
            current = initial_population
            time = 0
            fission_time = growth_unit_time / fissions_per_unit
            while current < projection_time:
                current *= (1 + rate_per_fission)
                time += fission_time
            return time

        total_fissions = (total_projection_time / growth_unit_time) * fissions_per_unit
        return initial_population * (1 + rate_per_fission) ** total_fissions


def time_conversion(unit, amount):
    '''
    Converts time from given unit to seconds.
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


# Start the program
menu()
