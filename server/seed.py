#!/usr/bin/env python3

from app import app
#the db import is importing the database connection
from models import db, Exercise, Workout, WorkoutExercise
from datetime import date

#this allows me to work inside the app and operate on the database with no errors caused
with app.app_context():

    # 1. Clearing existing data
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    # 2. Creating Exercise objects
    push_up = Exercise(
        name="Push-up",
        category="Chest",
        equipment_needed=False
    )

    squat = Exercise(
        name="Squat",
        category="Legs",
        equipment_needed=False
    )

    plank = Exercise(
        name="Plank",
        category="Core",
        equipment_needed=False
    )

    dumbbell_curl = Exercise(
        name="Dumbbell Curl",
        category="Arms",
        equipment_needed=True
    )

    # 3. Creating Workout objects
    workout1 = Workout(
        date=date(2026, 4, 10),
        duration_minutes=45,
        notes="Full body workout"
    )

    workout2 = Workout(
        date=date(2026, 4, 11),
        duration_minutes=30,
        notes="Quick core session"
    )

    #  4. Creating WorkoutExercise 
    we1 = WorkoutExercise(
        workout=workout1,
        exercise=push_up,
        sets=3,
        reps=15
    )

    we2 = WorkoutExercise(
        workout=workout1,
        exercise=squat,
        sets=4,
        reps=12
    )

    we3 = WorkoutExercise(
        workout=workout2,
        exercise=plank,
        duration_seconds=60
    )

    we4 = WorkoutExercise(
        workout=workout2,
        exercise=dumbbell_curl,
        sets=3,
        reps=10
    )

    # 5. Adding everything to the database
    db.session.add_all([
        push_up, squat, plank, dumbbell_curl,
        workout1, workout2,
        we1, we2, we3, we4
    ])

    #  6. Commit changes
    db.session.commit()

    print(" Database seeded successfully!")