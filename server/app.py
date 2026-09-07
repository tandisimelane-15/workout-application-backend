from flask import Flask, request, make_response
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from models import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)


# =========================
# WORKOUT ROUTES
# =========================

@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()

    return make_response(
        WorkoutSchema(many=True).dump(workouts),
        200
    )


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout_by_id(id):
    workout = db.session.get(Workout, id)

    if not workout:
        return make_response(
            {'error': 'Workout not found'},
            404
        )

    return make_response(
        WorkoutSchema().dump(workout),
        200
    )


@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json()

    try:
        validated_data = WorkoutSchema().load(data)

        workout = Workout(
            date=validated_data['date'],
            duration_minutes=validated_data['duration_minutes'],
            notes=validated_data.get('notes')
        )

        db.session.add(workout)
        db.session.commit()

        return make_response(
            WorkoutSchema().dump(workout),
            201
        )

    except ValidationError as error:
        return make_response(
            {'errors': error.messages},
            422
        )

    except ValueError as error:
        return make_response(
            {'error': str(error)},
            422
        )


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = db.session.get(Workout, id)

    if not workout:
        return make_response(
            {'error': 'Workout not found'},
            404
        )

    db.session.delete(workout)
    db.session.commit()

    return make_response('', 204)


# =========================
# EXERCISE ROUTES
# =========================

@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()

    return make_response(
        ExerciseSchema(many=True).dump(exercises),
        200
    )


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise_by_id(id):
    exercise = db.session.get(Exercise, id)

    if not exercise:
        return make_response(
            {'error': 'Exercise not found'},
            404
        )

    return make_response(
        ExerciseSchema().dump(exercise),
        200
    )


@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json()

    try:
        validated_data = ExerciseSchema().load(data)

        exercise = Exercise(
            name=validated_data['name'],
            category=validated_data['category'],
            equipment_needed=validated_data['equipment_needed']
        )

        db.session.add(exercise)
        db.session.commit()

        return make_response(
            ExerciseSchema().dump(exercise),
            201
        )

    except ValidationError as error:
        return make_response(
            {'errors': error.messages},
            422
        )

    except (ValueError, IntegrityError) as error:
        db.session.rollback()

        return make_response(
            {'error': 'Exercise could not be created'},
            422
        )


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)

    if not exercise:
        return make_response(
            {'error': 'Exercise not found'},
            404
        )

    db.session.delete(exercise)
    db.session.commit()

    return make_response('', 204)


# =========================
# WORKOUT EXERCISE ROUTE
# =========================

@app.route(
    '/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises',
    methods=['POST']
)
def add_exercise_to_workout(workout_id, exercise_id):

    workout = db.session.get(Workout, workout_id)
    exercise = db.session.get(Exercise, exercise_id)

    if not workout:
        return make_response(
            {'error': 'Workout not found'},
            404
        )

    if not exercise:
        return make_response(
            {'error': 'Exercise not found'},
            404
        )

    data = request.get_json()

    try:
        validated_data = WorkoutExerciseSchema().load(data)

        workout_exercise = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            reps=validated_data['reps'],
            sets=validated_data['sets'],
            duration_seconds=validated_data['duration_seconds']
        )

        db.session.add(workout_exercise)
        db.session.commit()

        return make_response(
            WorkoutExerciseSchema().dump(workout_exercise),
            201
        )

    except ValidationError as error:
        return make_response(
            {'errors': error.messages},
            422
        )

    except (ValueError, IntegrityError):
        db.session.rollback()

        return make_response(
            {'error': 'Workout exercise could not be created'},
            422
        )


if __name__ == '__main__':
    app.run(port=5555, debug=True)