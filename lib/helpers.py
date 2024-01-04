# lib/helpers.py
import random

from tabulate import tabulate

from lib.models.__init__ import CONN, CURSOR

# User Management Functions


def delete_user(current_user):
    if current_user:
        while True:
            confirm = input(
                f"Are you sure you want to delete your account ({current_user.username}), all associated workouts, and logout? (yes/no): "
            )
            if confirm.lower() == "yes":
                delete_user_workouts(current_user.id)  # Delete the user's workouts
                current_user.delete()
                print(
                    f"Account {current_user.username} and all associated records deleted successfully."
                )
                exit_program()
                return True
            elif confirm.lower() == "no":
                print("Account deletion cancelled.")
                return False
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")


def delete_user_workouts(user_id):
    CURSOR = CONN.cursor()
    CURSOR.execute("DELETE FROM user_workouts WHERE user_id = ?", (user_id,))
    CURSOR.execute("DELETE FROM users WHERE id = ?", (user_id,))
    CONN.commit()


# Workout Management Functions
# def create_workout():
#     workout_type = get_workout_type()
#     duration = int(input("Enter the workout duration in minutes: "))
#     workout = Workout(workout_type, duration)
#     pass


def list_user_workouts():
    pass


def delete_workout():
    pass


# Exercise Management Functions


def list_exercises():
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
        duration = input("Enter the workout duration in minutes (whole numbers only): ")

        if duration.isdigit() and int(duration) > 0:
            return int(duration)
        else:
            print("Invalid input. Please enter a positive whole number.")


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
                break
        if not added_exercise:
            break
    return workout_plan


def exit_program():
    print("Goodbye!")
    exit()
