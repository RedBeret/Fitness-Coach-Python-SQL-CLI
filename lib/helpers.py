# lib/helpers.py
import random

from tabulate import tabulate


# User Management Functions
def create_user():
    pass


def list_users():
    pass


def update_user():
    pass


def delete_user():
    pass


# Workout Management Functions
def create_workout():
    pass


def list_workouts():
    pass


def update_workout():
    pass


def delete_workout():
    pass


# Exercise Management Functions
def create_exercise():
    pass


def list_exercises():
    pass


def update_exercise():
    pass


def delete_exercise():
    pass


# Misc Functions
def get_workout_type():
    while True:
        print("Choose a workout type:")
        print("1: Upper Body")
        print("2: Lower Body")
        print("3: Stretching")
        choice = input("Please choose an option: ")

        if choice == "1":
            return "Upper Body"
        elif choice == "2":
            return "Lower Body"
        elif choice == "3":
            return "Stretching"
        else:
            print("Invalid choice. Please try again.")


def get_duration_minutes():
    while True:
        try:
            return int(input("Enter the workout duration in minutes: "))
        except ValueError:
            print("Invalid input. Please enter a number.")


def display_workout_plan(workout_plan):
    headers = ["Exercise Name", "Sets", "Reps", "Duration (Min)"]
    table_data = []

    for exercise in workout_plan:
        table_data.append(
            [
                exercise["Exercise Name"],
                exercise["Sets"],
                exercise["Reps"],
                exercise["Duration (Min)"],
            ]
        )

    print(tabulate(table_data, headers, tablefmt="grid"))


def generate_random_workout(exercises, duration_minutes):
    workout_plan = []
    current_duration = 0

    while current_duration < duration_minutes:
        random.shuffle(exercises)
        added_exercise = False
        for exercise in exercises:
            exercise_duration = exercise["Duration (Min)"]
            if current_duration + exercise_duration <= duration_minutes:
                workout_plan.append(exercise)
                current_duration += exercise_duration
                added_exercise = True
        if not added_exercise:
            break
    return workout_plan


def exit_program():
    print("Goodbye!")
    exit()
