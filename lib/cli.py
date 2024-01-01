# lib/cli.py


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
            user_management_menu()
            # create_user()
        elif choice == "2":
            user_management_menu()
            # list_users()
        elif choice == "3":
            user_management_menu()
            # update_user()
        elif choice == "4":
            user_management_menu()
            # delete_user()
        elif choice == "0":
            main_menu()
        else:
            print("Invalid choice. Please try again.")
            user_management_menu()


def workout_management_menu():
    while True:
        print("\nworkout Management")
        print("1: Create New workout")
        print("2: View All workouts")
        print("3: Update workout")
        print("4: Delete workout")
        print("0: Return to Main Menu")
        choice = input("Please choose an option: ")
        if choice == "1":
            workout_management_menu()
            # create_workout()
        elif choice == "2":
            workout_management_menu()
            # list_workouts()
        elif choice == "3":
            workout_management_menu()
            # update_workout()
        elif choice == "4":
            workout_management_menu()
            # delete_workout()
        elif choice == "0":
            main_menu()
        else:
            print("Invalid choice. Please try again.")
            workout_management_menu()


def exercise_management_menu():
    while True:
        print("\nexercise Management")
        print("1: Create New exercise")
        print("2: View All exercises")
        print("3: Update exercise")
        print("4: Delete exercise")
        print("0: Return to Main Menu")
        choice = input("Please choose an option: ")
        if choice == "1":
            exercise_management_menu()
            # create_exercise()
        elif choice == "2":
            exercise_management_menu()
            # list_exercises()
        elif choice == "3":
            exercise_management_menu()
            # update_exercise()
        elif choice == "4":
            exercise_management_menu()
            # delete_exercise()
        elif choice == "0":
            main_menu()
        else:
            print("Invalid choice. Please try again.")
            exercise_management_menu()


def main_menu():
    while True:
        print("\nWelcome to the Fitness App CLI")
        print("1: User Management")
        print("2: Workout Management")
        print("3: Exercise Management")
        print("0: Exit")
        choice = input("Please choose an option: ")
        if choice == "1":
            user_management_menu()
        elif choice == "2":
            workout_management_menu()
        elif choice == "3":
            exercise_management_menu()
        elif choice == "0":
            exit_program()
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
