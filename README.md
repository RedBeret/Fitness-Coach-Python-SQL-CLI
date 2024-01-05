# Python CLI Bodyweight Fitness

## Introduction

The Python CLI Bodyweight Fitness is a command-line interface application designed to assist users in generating workout routines quickly and easily, based on their available time and muscle groups they want to exercise. It provides features such as generating workout plans, randomizing exercises for variety, storing workouts for later reference, and more.

## Core Requirements and Fitness Application Alignment

### Python CLI Application

- This application is a Command Line Interface (CLI) program, allowing users to interact via the command line. It provides clear instructions and prompts for user-friendly interactions across a variety of potential user activities.

### ORM with at Least Two Model Classes

- The application implements model classes, including User, Exercise, and Workout, to represent entities within the fitness application. These classes are mapped to a database table.

### One-to-Many Relationship

- A one-to-many relationship exists between User and Workout, where a user can have multiple workouts. This relationship is well-defined and implemented in the ORM.

### Property Methods for Constraints

- Property methods are included in the classes to enforce data integrity and constraints. For example, input validation for usernames, workout types, durations, etc., is handled.

### CRUD Operations

- Each model class provides methods for creating, reading, updating, and deleting records. These operations are directly linked to the database.

### Interactive CLI Menus

- The CLI offers interactive menus for users to perform actions such as creating workouts, viewing past workouts, and more. The application loops appropriately until the user decides to exit.

### User Input Validation and Error Handling

- The CLI gracefully handles invalid inputs and provides informative error messages to enhance usability and robustness.

### Best Practices in OOP and Code Organization

- The project follows Object-Oriented Programming (OOP) principles, including encapsulation, inheritance, and abstraction. The code is well-organized into modules and classes for readability and maintainability.

### Project Structure and Documentation

- The project maintains a clean and well-organized structure, including a README.md file with detailed instructions on how to set up and use the application.

## Getting Started

To get started with the Python CLI Bodyweight Fitness Coach, follow the installation and usage instructions below.

## User Stories

### Core Deliverables

- Opening the App and User Greeting
- Workout Type Selection
- Workout Duration Selection
- Generating a Workout Plan
- Randomization for Variety
- Displaying the Workout Plan
- Option to Re-generate Workout Plan

## Project Structure

The project is organized as follows:

```
python-cli-fitness-coach/
│ lib
│   data
│       exercise_database.py
│       seed.py
│       workout_plans.db
│   models
│       __init__
│       exercise.py
│       user.py
│       workout.py
│   cli.py
│   debug.py
│   helpers.py
│ .gitignore
│ main.py
│ Pipfile
│ Pipfile.lock
│ README.md
```

## Dependencies

The project relies on the following Python libraries, which are specified in the Pipfile:

- `ipdb`
- `pytest`
- `click`
- `tabulate`
- `rich`

You can install these dependencies using Pipenv (name) or Pipenv install.
