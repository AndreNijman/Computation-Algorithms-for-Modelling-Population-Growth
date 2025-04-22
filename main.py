from tabulate import tabulate  # Used to format projections in columns (Part 4)

def menu():
    '''
    Displays the main menu to the user and prompts for their selection.
    Loops until the user chooses to exit (Part 6).
    '''
    while True:
        print("\nThis program has five modules. Choose a module to run by typing its number")
        print("(1) Compare a naive and sophisticated model")
        print("(2) Time for a sophisticated model to reach the target population")
        print("(3) Compare two sophisticated population models")
        print("(4) Generate detailed projections formatted as columns")
        print("(5) Model increases in fission-event frequency")
        print("(6) Exit program")

        # Validate menu selection
        choice = input_validation(prompt="Enter your choice: ", type='menu')

        if choice == 6:
            print("Exiting program. Goodbye!")
            break
        else:
            run_chosen_module(choice)

def run_chosen_module(module_number):
    '''
    Runs the module chosen by the user.
    Handles all five main module functions of the program.
    '''
    if module_number == 1:
        # Compare naive and sophisticated model over same timeframe
        n_init, n_rate, n_unit, n_type = naive_model()
        s_init, s_rate, s_unit, s_type, s_freq = sophisticated_model()

        print("\nFuture Projection timeframe for both models")
        proj_time = input_validation("Enter the amount of time to project into the future: ", type='int')
        proj_unit = input_validation("Enter the time unit (day, half-day, quarter-day, hour, minute): ", type='time_unit')

        print(f"\nNaive Model: I = {n_init}, g = {n_rate}% per {n_unit}")
        print(f"Sophisticated Model: I = {s_init}, g = {s_rate}% per {s_unit}, fission event frequency = {s_freq}")
        print(f"Projection time: {proj_time} {proj_unit}\n")

        naive_result = run_models(n_init, n_rate, n_unit, n_type,
                                  projection_time=proj_time, projection_time_unit=proj_unit)
        print(f'Naive model projected population size: {naive_result}')

        sophisticated_result = run_models(s_init, s_rate, s_unit, s_type,
                                          fission_event_frequency=s_freq,
                                          projection_time=proj_time, projection_time_unit=proj_unit)
        print(f'Sophisticated model projected population size: {sophisticated_result}')

    elif module_number == 2:
        # Time to reach a target population using the sophisticated model
        s_init, s_rate, s_unit, s_type, s_freq = sophisticated_model()
        target = input_validation("Enter the target population: ", type='int')

        print(f"\nSophisticated Model: I = {s_init}, g = {s_rate}% per {s_unit}, fission event frequency = {s_freq}")
        print(f"Target amount: {target}\n")

        growth_unit_seconds = time_conversion(s_unit, 1)
        if isinstance(s_freq, str):
            fission_unit_seconds = time_conversion(s_freq, 1)
            fissions_per_unit = growth_unit_seconds / fission_unit_seconds
            fission_unit_label = s_freq
        else:
            fissions_per_unit = s_freq
            fission_unit_seconds = growth_unit_seconds / fissions_per_unit
            fission_unit_label = "custom time unit"

        rate_per_fission = (s_rate / 100) / fissions_per_unit
        population = s_init
        time_elapsed = 0
        populations = [round(population, 2)]

        # Simulate population growth until the target is reached
        while population < target:
            added = population * rate_per_fission
            population += added
            populations.append(round(population, 2))
            time_elapsed += fission_unit_seconds

        print("Forward projection (per fission event):")
        print(populations)
        fission_count = len(populations) - 1
        print(f"Time taken: {fission_count} {fission_unit_label}(s) ({time_elapsed} seconds)")

    elif module_number == 3:
        # Compare two separate sophisticated models over the same timeframe
        print("\nMODULE 3: Compare two sophisticated population models")

        print("\nModel A:")
        a_init, a_rate, a_unit, a_type, a_freq = sophisticated_model()

        print("\nModel B:")
        b_init, b_rate, b_unit, b_type, b_freq = sophisticated_model()

        proj_time = input_validation("Enter the amount of time to project: ", type='int')
        proj_unit = input_validation("Enter the time unit (day, half-day, quarter-day, hour, minute): ", type='time_unit')

        a_result = run_models(a_init, a_rate, a_unit, a_type,
                              fission_event_frequency=a_freq,
                              projection_time=proj_time, projection_time_unit=proj_unit)

        b_result = run_models(b_init, b_rate, b_unit, b_type,
                              fission_event_frequency=b_freq,
                              projection_time=proj_time, projection_time_unit=proj_unit)

        print(f"\nModel A final population: {a_result}")
        print(f"Model B final population: {b_result}")

    elif module_number == 4:
        # Generate and print a column-formatted projection table using tabulate
        print("\nMODULE 4: Generate detailed projections formatted as columns")
        s_init, s_rate, s_unit, s_type, s_freq = sophisticated_model()

        target = input_validation("Enter the population size to project to (enter 0 to use time instead): ", type='int')

        if target == 0:
            proj_time = input_validation("Enter the amount of time to project for: ", type='int')
            proj_unit = input_validation("Enter the projection time unit (day, half-day, quarter-day, hour, minute): ", type='time_unit')
        else:
            proj_time = None
            proj_unit = "population"

        growth_unit_seconds = time_conversion(s_unit, 1)
        if isinstance(s_freq, str):
            fission_unit_seconds = time_conversion(s_freq, 1)
            fissions_per_unit = growth_unit_seconds / fission_unit_seconds
        else:
            fissions_per_unit = s_freq
            fission_unit_seconds = growth_unit_seconds / fissions_per_unit

        rate_per_fission = (s_rate / 100) / fissions_per_unit
        rows = []
        population = s_init
        time_elapsed = 0

        # Projection by population or time
        if proj_unit == "population":
            while population < target:
                added = population * rate_per_fission
                new_pop = population + added
                rows.append([round(population, 2), round(added, 2), round(new_pop, 2)])
                population = new_pop
                time_elapsed += fission_unit_seconds
        else:
            total_seconds = time_conversion(proj_unit, proj_time)
            while True:
                if time_elapsed + fission_unit_seconds > total_seconds:
                    break
                added = population * rate_per_fission
                new_pop = population + added
                rows.append([round(population, 2), round(added, 2), round(new_pop, 2)])
                population = new_pop
                time_elapsed += fission_unit_seconds

        print(tabulate(rows, headers=["Opening", "Added", "Closing"], tablefmt="grid"))

def run_chosen_module(module_number):
    '''
    Runs the module chosen by the user.
    Handles all five main module functions of the program.
    '''
    if module_number == 5:
        # Show how more frequent fission events affect growth (Part 5)
        print("\nMODULE 5: Model increases in fission-event frequency")
        init, rate, unit, model_type, _ = sophisticated_model()

        max_events = input_validation("Enter the maximum number of fission events per growth time unit: ", type='int')
        step = input_validation("Enter the step size to increase frequency: ", type='int')
        duration = input_validation("Enter how many of your chosen time units to project: ", type='int')

        results = []
        for freq in range(1, max_events + 1, step):
            # Calculate the rate per fission event for each frequency
            fission_rate = (rate / 100) / freq

            # Calculate the number of fissions over the projection time
            total_fissions = (time_conversion(unit, duration) / time_conversion(unit, 1)) * freq

            # Use compound growth with fission frequency
            final_pop = init * (1 + fission_rate) ** total_fissions

            results.append([freq, round(final_pop, 2)])

        print("\nEffect of increasing fission-event frequency:")
        print(tabulate(results, headers=["Fission Events/Unit", "Final Population"], tablefmt="grid"))



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
    Calculates and returns the projected population using the selected model type.
    For naive model: uses simple interest.
    For sophisticated model: uses compound interest adjusted by fission frequency.
    '''
    total_projection_time = time_conversion(projection_time_unit, projection_time)
    growth_unit_time = time_conversion(growth_time_unit, 1)

    if model_type == "naive":
        # A = P(1 + rt) for naive model
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
    Converts a time quantity from a unit to seconds.
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
