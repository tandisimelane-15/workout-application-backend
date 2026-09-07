#!/usr/bin/env python3

from datetime import date

from app import app
from models import db, Exercise, Workout, WorkoutExercise


with app.app_context():

    print("Clearing database...")

    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    db.session.commit()

    print("Creating exercises...")

    pushups = Exercise(
        name="Push-ups",
        category="Strength",
        equipment_needed=False
    )

    squats = Exercise(
        name="Squats",
        category="Strength",
        equipment_needed=False
    )

    treadmill = Exercise(
        name="Treadmill",
        category="Cardio",
        equipment_needed=True
    )

    plank = Exercise(
        name="Plank",
        category="Core",
        equipment_needed=False
    )

    exercises = [
        pushups,
        squats,
        treadmill,
        plank
    ]

    db.session.add_all(exercises)

    print("Creating workouts...")

    workout1 = Workout(
        date=date(2026, 9, 5),
        duration_minutes=45,
        notes="Morning strength workout"
    )

    workout2 = Workout(
        date=date(2026, 9, 6),
        duration_minutes=30,
        notes="Cardio and core workout"
    )

    db.session.add_all([
        workout1,
        workout2
    ])

    db.session.commit()

    print("Adding exercises to workouts...")

    workout_exercise1 = WorkoutExercise(
        workout_id=workout1.id,
        exercise_id=pushups.id,
        reps=15,
        sets=3,
        duration_seconds=0
    )

    workout_exercise2 = WorkoutExercise(
        workout_id=workout1.id,
        exercise_id=squats.id,
        reps=20,
        sets=3,
        duration_seconds=0
    )

    workout_exercise3 = WorkoutExercise(
        workout_id=workout2.id,
        exercise_id=treadmill.id,
        reps=0,
        sets=1,
        duration_seconds=1200
    )

    workout_exercise4 = WorkoutExercise(
        workout_id=workout2.id,
        exercise_id=plank.id,
        reps=0,
        sets=3,
        duration_seconds=60
    )

    db.session.add_all([
        workout_exercise1,
        workout_exercise2,
        workout_exercise3,
        workout_exercise4
    ])

    db.session.commit()

    print("Database seeded successfully!")