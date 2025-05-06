from tabulate import tabulate
from termcolor import colored  # Importing termcolor for coloring output
import matplotlib.pyplot as plt
import os
from datetime import datetime
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset
# Main entry point showing a text menu and routing to module functions


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

# Determines which module to run based on user's choice


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
        proj_unit = input_validation(colored("Enter the time unit (year, quarter-year month, week, day, half-day, quarter-day, hour, minute, second): ", 'yellow'), type='time_unit')

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
        # Keep compounding growth until the target is reached
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
        proj_unit = input_validation(colored("Enter the time unit (year, quarter-year, month, week, day, half-day, quarter-day, hour, minute, second): ", 'yellow'), type='time_unit')

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
            proj_unit = input_validation(colored("Enter the projection time unit (year, quarter-year, month, week, day, half-day, quarter-day, hour, minute, second): ", 'yellow'), type='time_unit')
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
        # Keep compounding growth until the target is reached
            while population < target:
                added = population * rate_per_fission
                new_pop = population + added
            # Record population state for later tabulated display
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
            # Record population state for later tabulated display
                rows.append([round(population, 2), round(added, 2), round(new_pop, 2)])
                population = new_pop
                time_elapsed += fission_unit_seconds

        print(f"\n{colored('Projection time:', 'cyan')} {time_elapsed} seconds")
        print(f"\n{colored('Table of results', 'cyan')} {population}")
        
        print(tabulate(rows, headers=[colored("Opening", 'yellow'), colored("Added", 'yellow'), colored("Closing", 'yellow')], tablefmt="grid"))

    elif module_number == 5:
        # Part 5: Simulate increases in fission-event frequency with styled dark graph and correctly sized zoom

        print(colored("\nMODULE 5: Model increases in fission-event frequency", 'red'))

        init = 1000
        rate = 100
        unit = "day"
        duration = 1

        os.makedirs("graphs", exist_ok=True)

        fission_frequencies = {
            "quarter-day": time_conversion("quarter-day", 1),
            "2-hour": 2 * 3600,
            "hour": 3600,
            "minute": 60,
            "second": 1
        }

        background_color = "#0e1a24"
        main_line_color = "#fca311"
        grid_color = "#2c3e50"
        text_color = "#e0e0e0"

        # Loop through all preset fission frequencies
        for label, fission_seconds in fission_frequencies.items():
            total_seconds = time_conversion(unit, duration)
            fissions = int(total_seconds / fission_seconds)
            rate_per_fission = (rate / 100) / fissions

            print(colored(f"\n--- Fission every {label} ---", 'yellow'))
            population = init
            populations = [population]
            rows = []

            for i in range(fissions):
                added = population * rate_per_fission
                new_pop = population + added

                if label in ["minute", "second"]:
                    if i == 0 or i == fissions - 1:
            # Record population state for later tabulated display
                        rows.append([round(population, 2), round(added, 2), round(new_pop, 2)])
                else:
            # Record population state for later tabulated display
                    rows.append([round(population, 2), round(added, 2), round(new_pop, 2)])

                population = new_pop
                populations.append(population)

            if label in ["minute", "second"]:
                print("Start and end only (too many rows to display):")
            print(tabulate(
                rows,
                headers=[colored("Opening", 'yellow'), colored("Added", 'yellow'), colored("Closing", 'yellow')],
                tablefmt="grid"
            ))
            print(f"{colored('Final population after 1 day:', 'cyan')} {round(population, 4)}")

            timestamp = datetime.now().strftime("%A_%H-%M")
            filename = f"graphs/{timestamp}_{label}.png"

            fig, ax = plt.subplots(figsize=(8, 4))
            fig.patch.set_facecolor(background_color)
            ax.set_facecolor(background_color)

            ax.plot(
                range(len(populations)),
                populations,
                marker='o' if label not in ["minute", "second"] else '.',
                markersize=4 if label not in ["minute", "second"] else 1,
                linestyle='-',
                linewidth=1.5,
                color=main_line_color,
                label=label
            )

            ax.set_title(f'Fission every {label}', fontsize=14, fontweight='bold', color=text_color)
            ax.set_xlabel('Fission Event Number', fontsize=12, color=text_color)
            ax.set_ylabel('Population Size', fontsize=12, color=text_color)
            ax.tick_params(colors=text_color)
            ax.grid(True, linestyle='--', color=grid_color, alpha=0.3)
            ax.legend(loc='upper left', fontsize=10, facecolor=background_color, labelcolor=text_color)

            if label in ["minute", "second"]:
                axins = inset_axes(
                    ax,
                    width="35%",
                    height="35%",
                    loc='lower right',
                    bbox_to_anchor=(0.0, 0.08, 1, 1),  # slightly raised
                    bbox_transform=ax.transAxes
                )
                zoom_range = 50
                axins.plot(
                    range(zoom_range),
                    populations[:zoom_range],
                    marker='o',
                    markersize=2,
                    linestyle='-',
                    linewidth=1,
                    color=main_line_color
                )
                axins.set_xlim(0, zoom_range)
                axins.set_ylim(
                    min(populations[:zoom_range]) * 0.999,
                    max(populations[:zoom_range]) * 1.001
                )
                axins.tick_params(colors=text_color, labelsize=8)
                axins.set_facecolor(background_color)
                axins.grid(True, linestyle='--', color=grid_color, alpha=0.4)
                axins.set_xticklabels([])
                axins.set_yticklabels([])
                mark_inset(ax, axins, loc1=1, loc2=3, fc="none", ec="gray")

            plt.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.15)
            plt.savefig(filename, facecolor=fig.get_facecolor())
            plt.close()

            print(colored(f"\nGraph saved to: {filename}", 'green'))
            print(colored("Graph saved successfully!", 'green'))

# Core logic for calculating population growth for both model types


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

# Reusable function for safely getting validated input from the user


def input_validation(prompt, type):
    '''
    Validates user input based on the expected type.
    Retries up to 3 times before exiting the program.
    '''
    valid_menu = {'1', '2', '3', '4', '5', '6'}
    valid_units = {'year', 'quarter-year', 'week', 'month', 'day', 'half-day', 'quarter-day', 'hour', 'minute', 'custom', 'second'}

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

# Collects all inputs for the naive population growth model


def naive_model():
    '''
    Collects input values for the naive population model.
    Returns initial population, growth rate, time unit, and model type.
    '''
    print(colored("\nNaive model", 'green'))
    init = input_validation(colored("Enter the initial population: ", 'yellow'), type='int')
    rate = input_validation(colored("Enter the growth rate (as a percentage without the symbol): ", 'yellow'), type='float')
    unit = input_validation(colored("Enter the growth time unit (year, quarter-year, month, week, day, half-day, quarter-day, hour, minute, second): ", 'yellow'), type='time_unit')
    return init, rate, unit, "naive"

# Collects inputs for a sophisticated (compound) growth model


def sophisticated_model():
    '''
    Collects input values for the sophisticated population model.
    Returns initial population, growth rate, time unit, model type, and fission-event frequency.
    '''
    print(colored("\nSophisticated model", 'blue'))
    init = input_validation(colored("Enter the initial population: ", 'yellow'), type='int')
    rate = input_validation(colored("Enter the growth rate (as a percentage without the symbol): ", 'yellow'), type='float')
    unit = input_validation(colored("Enter the growth time unit (year, quarter-year, month, week, day, half-day, quarter-day, hour, minute, second): ", 'yellow'), type='time_unit')
    freq = input_validation(colored("Enter the fission-event frequency time unit (year, quarter-year, month, week, day, half-day, quarter-day, hour, minute, custom, second): ", 'yellow'), type='time_unit')

    if freq == "custom":
        freq = input_validation(colored("Enter the number of fission events per growth rate time unit: ", 'yellow'), type='float')

    return init, rate, unit, "sophisticated", freq

# Converts a given unit of time (like days or hours) into seconds


def time_conversion(unit, amount):
    '''
    Converts a time quantity from a unit to seconds.
    It takes the unit and the number of those units as arguments and returns the equivalent number of seconds.
    '''
    seconds_per_unit = {
        "year": 31536000,
        "quarter-year": 7884000,
        "month": 2592000,
        "week": 604800,
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
