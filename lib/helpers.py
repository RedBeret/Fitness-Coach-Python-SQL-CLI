# lib/helpers.py
import random

from tabulate import tabulate

from lib.models.__init__ import CONN, CURSOR
from lib.models.exercise import Exercise
from lib.models.workout import Workout


def delete_user(current_user):
    if current_user:
        while True:
            confirm = input(
                f"Are you sure you want to delete your account {current_user.username}, all associated workouts, and logout? (yes/no): "
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


def get_valid_input(prompt, check_type, error_message):
    while True:
        user_input = input(prompt)
        if check_type == "alpha" and user_input.isalpha():
            return user_input
        elif (
            check_type == "positive_int"
            and user_input.isdigit()
            and int(user_input) > 0
        ):
            return int(user_input)
        else:
            print(error_message)


def list_all_exercises():
    exercises = Exercise.get_all()
    if not exercises:
        print("No exercises found.")
        return None

    headers = ["ID", "Name", "Sets", "Reps", "Duration (Min)", "Muscle Group"]
    exercise_data = []

    for exercise in exercises:
        exercise_id = exercise.id
        exercise_name = str(exercise.name)
        exercise_sets = exercise.sets
        exercise_reps = exercise.reps_per_set
        exercise_duration = exercise.duration_minutes
        exercise_category = exercise.muscle_group

        exercise_info = [
            exercise_id,
            exercise_name,
            exercise_sets,
            exercise_reps,
            exercise_duration,
            exercise_category,
        ]
        exercise_data.append(exercise_info)

    print(tabulate(exercise_data, headers, tablefmt="grid"))
    return exercises


def select_exercise_from_list():
    exercises = list_all_exercises()
    if exercises is None:
        return None
    while True:
        exercise_id = input("Enter the ID of the exercise: ")
        if exercise_id.isdigit() and any(
            exercise.id == int(exercise_id) for exercise in exercises
        ):
            return int(exercise_id)
        else:
            print("Invalid exercise ID. Please try again.")


def confirm_action(prompt):
    while True:
        confirm = input(prompt)
        if confirm.lower() in ["yes", "no"]:
            return confirm.lower() == "yes"
        else:
            print("Please enter 'yes' or 'no'.")


# Workout Management Functions


def create_workout():
    workout_type = get_workout_type()
    duration = int(input("Enter the workout duration in minutes: "))
    workout = Workout(workout_type, duration)


def list_workouts(username):
    # Get all workouts for the given user
    user_workouts = Workout.get_all(username)
    if not user_workouts:
        print("No workouts found.")
        return None

    # For each workout, get the associated exercises
    workout_data = []
    for user_workout in user_workouts:
        workout_id = user_workout.workout_id
        workout = Workout.get(id=workout_id)
        workout_date = workout.date
        workout_duration = workout.workout_duration
        workout_goal = workout.goal

        # Get all exercises for this workout
        workout_exercises = WorkoutExercise.get_all(where={"workout_id": workout_id})
        exercise_names = ", ".join(
            [
                str(WorkoutExercise.get(id=we.exercise_id).name)
                for we in workout_exercises
            ]
        )

        workout_info = [
            workout_id,
            workout_date,
            workout_duration,
            workout_goal,
            exercise_names,
        ]
        workout_data.append(workout_info)

    headers = ["ID", "Date", "Duration (Min)", "Goal", "Exercises"]
    print(tabulate(workout_data, headers, tablefmt="grid"))
    return user_workouts


def delete_workout():
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
