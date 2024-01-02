# lib/cli.py
import random

from tabulate import tabulate

from .helpers import (
    create_exercise,
    create_user,
    create_workout,
    delete_exercise,
    delete_user,
    delete_workout,
    display_workout_plan,
    exit_program,
    generate_random_workout,
    get_duration_minutes,
    get_workout_type,
    list_exercises,
    list_users,
    list_workouts,
    update_exercise,
    update_user,
    update_workout,
)


# Adding sections to seperate the functions
def main_menu():
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
            quick_start_workout()
        elif choice == "2":
            user_management_menu()
        elif choice == "3":
            workout_management_menu()
        elif choice == "4":
            exercise_management_menu()
        elif choice == "0":
            exit_program()
        else:
            print("Invalid choice. Please try again.")


# --- User Management Functions ---
def user_management_menu():
    while True:
        print("\nUser Management")
        print("1: Create New User")
        print("2: View All Users")
        print("3: Update User")
        print("4: Delete User")
        print("0: Return to Main Menu")
        choice = input("Please choose an option: ")
        if choice == "1":
            create_user()
        elif choice == "2":
            list_users()
        elif choice == "3":
            update_user()
        elif choice == "4":
            delete_user()
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
            workout_management_menu()
            create_workout()
        elif choice == "2":
            workout_management_menu()
            list_workouts()
        elif choice == "3":
            workout_management_menu()
            update_workout()
        elif choice == "4":
            workout_management_menu()
            delete_workout()
        elif choice == "0":
            main_menu()
        else:
            print("Invalid choice. Please try again.")
            workout_management_menu()


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
            main_menu()
        else:
            print("Invalid choice. Please try again.")
            exercise_management_menu()


# --- Quick Start Workout ---


def quick_start_workout():
    print("\nQuick Start Workout")
    # Get user input for name in alphabetical characters only
    while True:
        name = input("Enter your name: ")
        if any(not (char.isalpha() or char == " ") for char in name):
            print("Invalid name. Names should only contain letters and spaces.")
        else:
            break
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
            main_menu()
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()
