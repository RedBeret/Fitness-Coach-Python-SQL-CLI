# lib/cli.py

import random
import sqlite3
import time
from datetime import date, datetime

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
from rich.table import Table

console = Console()

from lib.models.__init__ import CONN, CURSOR
from lib.models.user import User
from lib.models.workout import Workout

from .helpers import (
    confirm_action,
    delete_user,
    display_workout_details,
    display_workout_plan,
    exit_program,
    get_duration_minutes,
    get_valid_input,
    get_workout_type,
    list_all_exercises,
    list_workouts_for_selection,
    select_exercise_from_list,
    select_workout_id,
)
from .models.exercise import Exercise


def welcome_message():
    username = input("Please enter your username: ")
    current_user = User.get_or_create(username)
    print(f"Welcome, {current_user.username}!")
    main_menu(current_user)


def main_menu(current_user):
    gym_art = """
      GGGG   Y   Y  M   M
     G       Y   Y  MM MM
     G  GG    Y Y   M M M
     G   G     Y    M   M
      GGG      Y    M   M
    """
    console.print(gym_art, style="bold blue")

    while True:
        welcome_panel = Panel(
            f"Welcome, [bold green]{current_user.username}![/bold green] to the Fitness App",
            expand=False,
        )
        console.print(welcome_panel)
        menu_table = Table(box=box.ROUNDED, show_header=True, header_style="bold green")
        menu_table.add_column("Option", justify="center")
        menu_table.add_column("Action", justify="center")

        menu_table.add_row("1", "Quick Start Workout")
        menu_table.add_row("2", "User Management")
        menu_table.add_row("3", "Workout Management")
        menu_table.add_row("4", "Exercise Management")
        menu_table.add_row("0", "Exit")

        console.print(menu_table)
        choice = input("Please choose an option: ")
        if choice == "1":
            quick_start_workout(current_user)
        elif choice == "2":
            user_management_menu(current_user)
        elif choice == "3":
            workout_management_menu(current_user)
        elif choice == "4":
            exercise_management_menu(current_user)
        elif choice == "0":
            exit_program()
        else:
            print("Invalid choice. Please try again.")


# --- User Management Functions ---
def user_management_menu(current_user):
    while True:
        console.print(Panel("User Management", style="bold green"))

        menu_table = Table(box=box.ROUNDED, show_header=True, header_style="bold green")
        menu_table.add_column("Option", justify="center")
        menu_table.add_column("Action", justify="center")

        menu_table.add_row("1", "Delete My Account")
        menu_table.add_row("0", "Return to Main Menu")

        console.print(menu_table)
        choice = input("Please choose an option: ")
        if choice == "1":
            if delete_user(current_user):
                print("You have been logged out.")
                return
        elif choice == "0":
            return
        else:
            print("Invalid choice. Please try again.")


# --- Workout Management Functions ---
def workout_management_menu(current_user):
    while True:
        console.print(Panel("Workout Management", style="bold green"))

        menu_table = Table(box=box.ROUNDED, show_header=True, header_style="bold green")
        menu_table.add_column("Option", justify="center")
        menu_table.add_column("Action", justify="center")

        menu_table.add_row("1", "View All Workouts")
        menu_table.add_row("2", "Delete Workout")
        menu_table.add_row("0", "Return to Main Menu")

        console.print(menu_table)
        choice = input("Please choose an option: ")
        if choice == "1":
            list_workouts(current_user)
        elif choice == "2":
            delete_workout(current_user)
        elif choice == "0":
            main_menu(current_user)
        else:
            print("Invalid choice. Please try again.")


def create_workout(current_user):
    workout_type = get_workout_type()
    duration = int(input("Enter the workout duration in minutes: "))

    try:
        workout_instance = Workout.create(
            username=current_user.username,
            workout_duration=duration,
            goal=workout_type,
        )
        print("Workout saved successfully.")
    except Exception as e:
        print(f"Error saving workout: {e}")


def list_workouts(current_user):
    workouts = list_workouts_for_selection(current_user.username)
    if workouts is None:
        return

    workout_id = select_workout_id(
        "Enter the ID of a workout to view its details, or '0' to return: "
    )
    if workout_id > 0:
        print("Sorry, this feature is not yet implemented.")
        # Future implementation: display_workout_details(workout_id)
    else:
        return


def delete_workout(current_user):
    workouts = list_workouts_for_selection(current_user.username)
    if workouts is None:
        return

    workout_id = select_workout_id(
        "Enter the ID of the workout to delete, or '0' to cancel: "
    )
    if workout_id == 0:
        print("Deletion cancelled.")
        return

    confirm = input(
        f"Are you sure you want to delete workout ID {workout_id}? (yes/no): "
    )
    if confirm.lower() == "yes":
        try:
            Workout.delete_by_id(workout_id)
            print(f"Workout ID {workout_id} has been deleted.")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("Deletion cancelled.")


# --- Exercise Management Functions ---
def exercise_management_menu(current_user):
    while True:
        console.print(Panel("Exercise Menu", style="bold green"))

        menu_table = Table(box=box.ROUNDED, show_header=True, header_style="bold green")
        menu_table.add_column("Option", justify="center")
        menu_table.add_column("Action", justify="center")

        menu_table.add_row("1", "Create New Exercise")
        menu_table.add_row("2", "View All Exercises")
        menu_table.add_row("3", "Update Exercise")
        menu_table.add_row("4", "Delete Exercise")
        menu_table.add_row("0", "Return to Main Menu")

        console.print(menu_table)
        choice = input("Please choose an option: ")
        if choice == "1":
            create_exercise()
        elif choice == "2":
            list_exercises()
        elif choice == "3":
            update_exercise()
        elif choice == "4":
            delete_exercise()
        elif choice == "0":
            main_menu(current_user)
        else:
            print("Invalid choice. Please try again.")


def create_exercise():
    exercise_name = str(
        get_valid_input(
            "Enter the exercise name: ",
            "alpha",
            "Exercise name should only contain letters. Please try again.",
        )
    )
    description = input("Enter the exercise description: ")
    instructions = input(
        "Enter the exercise instructions on how to perform the exercise: "
    )

    sets = int(
        get_valid_input(
            "Enter the number of sets: ",
            "positive_int",
            "Number of sets should be a positive number. Please try again.",
        )
    )
    reps_per_set = int(
        get_valid_input(
            "Enter the number of reps per set: ",
            "positive_int",
            "Number of reps per set should be a positive number. Please try again.",
        )
    )
    duration_minutes = int(
        get_valid_input(
            "Enter the exercise duration (in minutes): ",
            "positive_int",
            "Exercise duration should be a positive number in minutes. Please try again.",
        )
    )
    muscle_group = get_workout_type()
    Exercise.create(
        name=exercise_name,
        sets=sets,
        description=description,
        instructions=instructions,
        reps_per_set=reps_per_set,
        duration_minutes=duration_minutes,
        muscle_group=muscle_group,
    )

    print(f"Exercise '{exercise_name}' has been created successfully.")


def list_exercises():
    list_all_exercises()


def update_exercise():
    exercise_id = select_exercise_from_list()
    if exercise_id is None:
        return

    exercise = Exercise.find_by_id(exercise_id)

    new_sets = get_valid_input(
        f"You chose {exercise.name}. Please enter the new number of sets (current: {exercise.sets} sets): ",
        "positive_int",
        "Invalid input. Please enter a positive number.",
    )
    new_reps_per_set = get_valid_input(
        f"Enter the new number of reps per set (current: {exercise.reps_per_set} reps per set): ",
        "positive_int",
        "Invalid input. Please enter a positive number.",
    )
    new_duration_minutes = get_valid_input(
        f"Enter the new exercise duration (in minutes) (current: {exercise.duration_minutes} minutes): ",
        "positive_int",
        "Invalid input. Please enter a positive number.",
    )

    exercise.sets = new_sets
    exercise.reps_per_set = new_reps_per_set
    exercise.duration_minutes = new_duration_minutes

    exercise.update()

    print(f"Exercise {exercise.name} has been updated successfully.")


def delete_exercise():
    exercise_id = select_exercise_from_list()
    if exercise_id:
        exercise = Exercise.find_by_id(exercise_id)
        if not exercise:
            print("Exercise not found.")
            return
        if confirm_action(
            f"Are you sure you want to delete {exercise.name}? (yes/no): "
        ):
            exercise.delete()
            print(f"Exercise '{exercise.name}' has been deleted successfully.")
        else:
            print("Exercise deletion cancelled.")


# --- Quick Start Workout ---


def quick_start_workout(current_user):
    workout_types = {"1": "Upper Body", "2": "Lower Body", "3": "Stretching"}

    print("\nQuick Start Workout")

    while True:
        console.print(Panel("Choose a workout type:", style="bold green"))

        menu_table = Table(box=box.ROUNDED, show_header=True, header_style="bold green")
        menu_table.add_column("Option", justify="center")
        menu_table.add_column("Workout Type", justify="center")

        for option, workout_type in workout_types.items():
            menu_table.add_row(option, workout_type)

        console.print(menu_table)

        choice = input("Please choose an option: ")
        if choice in workout_types:
            workout_type = workout_types[choice]
            duration_minutes = get_duration_minutes()

            selected_exercises = generate_random_workout(duration_minutes, workout_type)
            with Progress() as progress:
                task = progress.add_task(
                    "[cyan]Generating Personalized workout...", total=30
                )
                while not progress.finished:
                    progress.update(task, advance=0.5)
                    time.sleep(0.05)
            if selected_exercises:
                workout_instance = Workout.create(
                    username=current_user.username,
                    workout_duration=duration_minutes,
                    goal=workout_type,
                )

                for exercise_id in selected_exercises:
                    CURSOR.execute(
                        "INSERT INTO workout_exercises (workout_id, exercise_id) VALUES (?, ?)",
                        (workout_instance.id, exercise_id),
                    )
                CONN.commit()

                print("Workout saved successfully.")
                display_workout_plan(selected_exercises)
            else:
                print("Unable to generate a workout plan for the specified duration.")

            input("Press Enter to return to the main menu...")
            main_menu(current_user)


def generate_random_workout(duration_minutes, workout_type):
    CURSOR.execute(
        "SELECT id, duration_minutes FROM exercises WHERE muscle_group = ?",
        (workout_type,),
    )
    exercises = CURSOR.fetchall()

    if not exercises:
        print(f"No exercises found for {workout_type} workout.")
        return []

    selected_exercises = []
    current_duration = 0

    while current_duration < duration_minutes:
        available_exercises = [
            (exercise_id, duration)
            for exercise_id, duration in exercises
            if duration <= (duration_minutes - current_duration)
        ]

        if not available_exercises:
            break

        exercise_id, exercise_duration = random.choice(available_exercises)
        selected_exercises.append(exercise_id)
        current_duration += exercise_duration

        if current_duration >= duration_minutes:
            break

    return selected_exercises


if __name__ == "__main__":
    current_user = welcome_message()
    main_menu()
