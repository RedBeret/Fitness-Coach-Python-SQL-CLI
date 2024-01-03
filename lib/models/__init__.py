import sqlite3

CONN = sqlite3.connect("./lib/data/workout_plans.db")
CURSOR = CONN.cursor()
