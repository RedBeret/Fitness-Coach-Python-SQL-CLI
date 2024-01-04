# lib/cli.py

import random
import sqlite3

from tabulate import tabulate

from lib.models.__init__ import CONN, CURSOR
from lib.models.user import User

CONN = sqlite3.connect("./lib/data/workout_plans.db")
CURSOR = CONN.cursor()
from .helpers import (
    delete_exercise,
    delete_user,
    display_workout_plan,
    exit_program,
    generate_random_workout,
    get_duration_minutes,
    get_workout_type,
    list_exercises,
    list_user_workouts,
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
            workout_management_menu()
        elif choice == "4":
            exercise_management_menu()
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
def workout_management_menu():
    while True:
        print("\nWorkout Management")
        print("1: Create New Workout")
        print("2: View All Workouts")
        print("3: Update Workout")
        print("4: Delete Workout")
        print("0: Return to Main Menu")
        choice = input("Please choose an option: ")
        if choice == "1":
            create_workout()
        elif choice == "2":
            list_workouts()
        elif choice == "3":
            update_workout()
        elif choice == "4":
            delete_workout()
        elif choice == "0":
            main_menu(current_user)
        else:
            print("Invalid choice. Please try again.")


# --- Exercise Management Functions ---
def exercise_management_menu():
    while True:
        print("\nExercise Management")
        print("1: Create New Exercise")
        print("2: View All Exercises")
        print("3: Update Exercise")
        print("4: Delete Exercise")
        print("0: Return to Main Menu")
        choice = input("Please choose an option: ")
        if choice == "1":
            exercise_management_menu()
            create_exercise()
        elif choice == "2":
            exercise_management_menu()
            list_exercises()
        elif choice == "3":
            exercise_management_menu()
            update_exercise()
        elif choice == "4":
            exercise_management_menu()
            delete_exercise()
        elif choice == "0":
            main_menu(current_user)
        else:
            print("Invalid choice. Please try again.")
            exercise_management_menu()


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
            else:
                print("Unable to generate a workout plan for the specified duration.")
        elif choice == "2":
            main_menu(current_user)
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    current_user = welcome_message()
    main_menu()
