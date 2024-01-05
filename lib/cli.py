# lib/cli.py

import sqlite3

from tabulate import tabulate

from lib.models.__init__ import CONN, CURSOR
from lib.models.user import User
from lib.models.workout import Workout


# CONN = sqlite3.connect("./lib/data/workout_plans.db")
# CURSOR = CONN.cursor()
from .helpers import (
    confirm_action,
    delete_user,
    display_workout_plan,
    exit_program,
    generate_random_workout,
    get_duration_minutes,
    get_valid_input,
    get_workout_type,
    list_all_exercises,
    list_workouts,
    select_exercise_from_list,
    create_workout,
    delete_workout,
)
from .models.exercise import Exercise


def welcome_message():
    username = input("Please enter your username: ")
    current_user = User.get_or_create(username)
    print(f"Welcome, {current_user.username}!")
    main_menu(current_user)


def main_menu(current_user):
    print(
        """  GGGG   Y   Y  M   M
 G       Y   Y  MM MM
 G  GG    Y Y   M M M
 G   G     Y    M   M
  GGG      Y    M   M
"""
    )

    while True:
        print("\nWelcome to the Fitness App CLI")
        print("1: Quick Start Workout")
        print("2: User Management")
        print("3: Workout Management")
        print("4: Exercise Management")
        print("0: Exit")
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
    print("\nUser Management")
    print("1: Delete My Account")
    print("0: Return to Main Menu")
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
        print("\nWorkout Management")
        print("1: Create New Workout")
        print("2: View All Workouts")
        print("3: Delete Workout")
        print("0: Return to Main Menu")
        choice = input("Please choose an option: ")
        if choice == "1":
            create_workout()
        elif choice == "2":
            list_workouts(current_user.username)
        elif choice == "3":
            delete_workout()
        elif choice == "0":
            main_menu(current_user)
        else:
            print("Invalid choice. Please try again.")


# --- Exercise Management Functions ---
def exercise_management_menu(current_user):
    while True:
        print("\nExercise Management")
        print("1: Create New Exercise")
        print("2: View All Exercises")
        print("3: Update Exercise")
        print("4: Delete Exercise")
        print("0: Return to Main Menu")
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

    # Update the exercise object with the new values
    exercise.sets = new_sets
    exercise.reps_per_set = new_reps_per_set
    exercise.duration_minutes = new_duration_minutes

    # Save the updated exercise to the database
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
    print("\nQuick Start Workout")
    # gets workout type from user
    workout_type = get_workout_type()
    # gets duration from user
    duration_minutes = get_duration_minutes()

    # Just a placeholder for now to not error out and cycle.
    # Total time (mins, rounded) = round(((sets * reps * time_per_rep_3sec) + ((sets - 1) * rest_between_sets_45sec) + setup_time_10sec) / 60)

    exercises = [
        {"Exercise Name": "Push-Ups", "Sets": 3, "Reps": 12, "Duration (Min)": 3},
        {"Exercise Name": "Squats", "Sets": 3, "Reps": 10, "Duration (Min)": 3},
    ]

    workout_plan = generate_random_workout(exercises, duration_minutes)
    if workout_plan:
        display_workout_plan(workout_plan)

        # Create and save the workout instance to the database.

        try:
            workout_instance = Workout.create(
                username=current_user,
                workout_duration=duration_minutes,
                goal=workout_type,
            )
            print("Workout saved successfully.")
        except Exception as e:
            print(f"Error saving workout: {e}")
    else:
        print("Unable to generate a workout plan for the specified duration.")

    while True:
        print("\nChoose an option:")
        print("1: Generate a Different Workout")
        print("2: Return to Main Menu")

        choice = input("Please choose an option: ")

        if choice == "1":
            workout_plan = generate_random_workout(exercises, duration_minutes)
            if workout_plan:
                display_workout_plan(workout_plan)

                # Create and save the workout instance to the database.
            try:
                workout_instance = Workout.create(
                    username=current_user,
                    workout_duration=duration_minutes,
                    goal=workout_type,
                )
                print("Workout saved successfully.")
            except Exception as e:
                print(f"Error saving workout: {e}")
            else:
                print("Unable to generate a workout plan for the specified duration.")
        elif choice == "2":
            main_menu(current_user)
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    current_user = welcome_message()
    main_menu()
