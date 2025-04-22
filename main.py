from tabulate import tabulate
from termcolor import colored  # Importing termcolor for coloring output

def menu():
    '''
    Displays the main menu to the user and prompts for their selection.
    Loops until the user chooses to exit (Part 6).
    '''
    while True:
        print(colored("\nThis program has five modules. Choose a module to run by typing its number", 'yellow'))
        print(colored("(1) Compare a naive and sophisticated model", 'green'))
        print(colored("(2) Time for a sophisticated model to reach the target population", 'blue'))
        print(colored("(3) Compare two sophisticated population models", 'magenta'))
        print(colored("(4) Generate detailed projections formatted as columns", 'cyan'))
        print(colored("(5) Model increases in fission-event frequency", 'red'))
        print(colored("(6) Exit program", 'white'))

        # Validate menu selection
        choice = input_validation(prompt=colored("Enter your choice: ", 'yellow'), type='menu')

        if choice == 6:
            print(colored("Exiting program. Goodbye!", 'red'))
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

        print(colored("\nFuture Projection timeframe for both models", 'yellow'))
        proj_time = input_validation(colored("Enter the amount of time to project into the future: ", 'yellow'), type='int')
        proj_unit = input_validation(colored("Enter the time unit (day, half-day, quarter-day, hour, minute): ", 'yellow'), type='time_unit')

        print(f"\n{colored('Naive Model:', 'green')} I = {n_init}, g = {n_rate}% per {n_unit}")
        print(f"{colored('Sophisticated Model:', 'blue')} I = {s_init}, g = {s_rate}% per {s_unit}, fission event frequency = {s_freq}")
        print(f"{colored('Projection time:', 'cyan')} {proj_time} {proj_unit}\n")

        naive_result = run_models(n_init, n_rate, n_unit, n_type,
                                  projection_time=proj_time, projection_time_unit=proj_unit)
        print(f'{colored("Naive model projected population size:", "green")} {naive_result}')

        sophisticated_result = run_models(s_init, s_rate, s_unit, s_type,
                                          fission_event_frequency=s_freq,
                                          projection_time=proj_time, projection_time_unit=proj_unit)
        print(f'{colored("Sophisticated model projected population size:", "blue")} {sophisticated_result}')

    elif module_number == 2:
        # Time to reach a target population using the sophisticated model
        s_init, s_rate, s_unit, s_type, s_freq = sophisticated_model()
        target = input_validation(colored("Enter the target population: ", 'yellow'), type='int')

        print(f"\n{colored('Sophisticated Model:', 'blue')} I = {s_init}, g = {s_rate}% per {s_unit}, fission event frequency = {s_freq}")
        print(f"{colored('Target amount:', 'cyan')} {target}\n")

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

        print(colored("Forward projection (per fission event):", 'yellow'))
        print(populations)
        fission_count = len(populations) - 1
        print(f"{colored('Time taken:', 'cyan')} {fission_count} {fission_unit_label}(s) ({time_elapsed} seconds)")

    elif module_number == 3:
        # Compare two separate sophisticated models over the same timeframe
        print(colored("\nMODULE 3: Compare two sophisticated population models", 'magenta'))

        print(colored("\nModel A:", 'green'))
        a_init, a_rate, a_unit, a_type, a_freq = sophisticated_model()

        print(colored("\nModel B:", 'blue'))
        b_init, b_rate, b_unit, b_type, b_freq = sophisticated_model()

        proj_time = input_validation(colored("Enter the amount of time to project: ", 'yellow'), type='int')
        proj_unit = input_validation(colored("Enter the time unit (day, half-day, quarter-day, hour, minute): ", 'yellow'), type='time_unit')

        a_result = run_models(a_init, a_rate, a_unit, a_type,
                              fission_event_frequency=a_freq,
                              projection_time=proj_time, projection_time_unit=proj_unit)

        b_result = run_models(b_init, b_rate, b_unit, b_type,
                              fission_event_frequency=b_freq,
                              projection_time=proj_time, projection_time_unit=proj_unit)

        print(f"\n{colored('Model A final population:', 'green')} {a_result}")
        print(f"{colored('Model B final population:', 'blue')} {b_result}")

    elif module_number == 4:
        # Generate and print a column-formatted projection table using tabulate
        print(colored("\nMODULE 4: Generate detailed projections formatted as columns", 'cyan'))
        s_init, s_rate, s_unit, s_type, s_freq = sophisticated_model()

        target = input_validation(colored("Enter the population size to project to (enter 0 to use time instead): ", 'yellow'), type='int')

        if target == 0:
            proj_time = input_validation(colored("Enter the amount of time to project for: ", 'yellow'), type='int')
            proj_unit = input_validation(colored("Enter the projection time unit (day, half-day, quarter-day, hour, minute): ", 'yellow'), type='time_unit')
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

        print(tabulate(rows, headers=[colored("Opening", 'yellow'), colored("Added", 'yellow'), colored("Closing", 'yellow')], tablefmt="grid"))

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
        return initial_population * (1 + (growth_rate / 100) * (total_projection_time / growth_unit_time))

    elif model_type == "sophisticated":
        if isinstance(fission_event_frequency, str):
            fission_time = time_conversion(fission_event_frequency, 1)
            fissions_per_unit = growth_unit_time / fission_time
        else:
            fissions_per_unit = fission_event_frequency

        rate_per_fission = (growth_rate / 100) / fissions_per_unit

        if projection_time_unit == "population":
            current = initial_population
            time = 0
            fission_time = growth_unit_time / fissions_per_unit
            while current < projection_time:
                current *= (1 + rate_per_fission)
                time += fission_time
            return time

        total_fissions = (total_projection_time / growth_unit_time) * fissions_per_unit
        return initial_population * (1 + rate_per_fission) ** total_fissions


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
                return int(value)  # Return the valid choice directly, no need to call run_chosen_module here
            elif type == 'int':
                return int(value)
            elif type == 'float':
                return float(value)
            elif type == 'time_unit' and value in valid_units:
                return value
        except ValueError:
            pass

        print(colored("Invalid input. Please try again.", 'red'))

    print(colored("Too many invalid attempts. Exiting. AAHAAN STOP SPAMMING, IK ITS YOU 😔😔😔", 'red'))
    exit()

def naive_model():
    '''
    Collects input values for the naive population model.
    Returns initial population, growth rate, time unit, and model type.
    '''
    print(colored("\nNaive model", 'green'))
    init = input_validation(colored("Enter the initial population: ", 'yellow'), type='int')
    rate = input_validation(colored("Enter the growth rate (as a percentage without the symbol): ", 'yellow'), type='float')
    unit = input_validation(colored("Enter the growth time unit (day, half-day, quarter-day, hour, minute): ", 'yellow'), type='time_unit')
    return init, rate, unit, "naive"

def sophisticated_model():
    '''
    Collects input values for the sophisticated population model.
    Returns initial population, growth rate, time unit, model type, and fission-event frequency.
    '''
    print(colored("\nSophisticated model", 'blue'))
    init = input_validation(colored("Enter the initial population: ", 'yellow'), type='int')
    rate = input_validation(colored("Enter the growth rate (as a percentage without the symbol): ", 'yellow'), type='float')
    unit = input_validation(colored("Enter the growth time unit (day, half-day, quarter-day, hour, minute): ", 'yellow'), type='time_unit')
    freq = input_validation(colored("Enter the fission-event frequency time unit (day, half-day, quarter-day, hour, minute, custom): ", 'yellow'), type='time_unit')

    if freq == "custom":
        freq = input_validation(colored("Enter the number of fission events per growth rate time unit: ", 'yellow'), type='float')

    return init, rate, unit, "sophisticated", freq


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
