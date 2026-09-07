from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from marshmallow import Schema, fields, validate

db = SQLAlchemy()

class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)

    # Table constraints
    name = db.Column(db.String, nullable=False, unique=True)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    workout_exercises = db.relationship(
        'WorkoutExercise',
        back_populates='exercise',
        cascade='all, delete-orphan'
    )

    workouts = association_proxy(
        'workout_exercises',
        'workout'
    )

    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name.strip()) < 2:
            raise ValueError('Exercise name must contain at least 2 characters.')
        return name.strip()

    @validates('category')
    def validate_category(self, key, category):
        if not category or len(category.strip()) < 2:
            raise ValueError('Category must contain at least 2 characters.')
        return category.strip()

    def __repr__(self):
        return f'<Exercise {self.id}: {self.name}>'


class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)

    # Table constraints
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    __table_args__ = (
        db.CheckConstraint(
            'duration_minutes > 0',
            name='check_workout_duration_positive'
        ),
    )

    workout_exercises = db.relationship(
        'WorkoutExercise',
        back_populates='workout',
        cascade='all, delete-orphan'
    )

    exercises = association_proxy(
        'workout_exercises',
        'exercise'
    )

    @validates('duration_minutes')
    def validate_duration(self, key, duration):
        if duration is None or duration <= 0:
            raise ValueError('Workout duration must be greater than 0.')
        return duration

    def __repr__(self):
        return f'<Workout {self.id}: {self.date}>'


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)

    workout_id = db.Column(
        db.Integer,
        db.ForeignKey('workouts.id'),
        nullable=False
    )

    exercise_id = db.Column(
        db.Integer,
        db.ForeignKey('exercises.id'),
        nullable=False
    )

    reps = db.Column(db.Integer, nullable=False, default=0)
    sets = db.Column(db.Integer, nullable=False, default=0)
    duration_seconds = db.Column(db.Integer, nullable=False, default=0)

    __table_args__ = (
        db.CheckConstraint('reps >= 0', name='check_reps_nonnegative'),
        db.CheckConstraint('sets >= 0', name='check_sets_nonnegative'),
        db.CheckConstraint(
            'duration_seconds >= 0',
            name='check_duration_seconds_nonnegative'
        ),
        db.UniqueConstraint(
            'workout_id',
            'exercise_id',
            name='unique_workout_exercise'
        ),
    )

    workout = db.relationship(
        'Workout',
        back_populates='workout_exercises'
    )

    exercise = db.relationship(
        'Exercise',
        back_populates='workout_exercises'
    )

    @validates('reps', 'sets', 'duration_seconds')
    def validate_numbers(self, key, value):
        if value is None or value < 0:
            raise ValueError(f'{key} cannot be negative.')
        return value

    def __repr__(self):
        return (
            f'<WorkoutExercise {self.id}: '
            f'Workout {self.workout_id}, Exercise {self.exercise_id}>'
        )
class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)

    name = fields.String(
        required=True,
        validate=validate.Length(
            min=2,
            error='Exercise name must contain at least 2 characters.'
        )
    )

    category = fields.String(
        required=True,
        validate=validate.Length(
            min=2,
            error='Category must contain at least 2 characters.'
        )
    )

    equipment_needed = fields.Boolean(required=True)

    workout_exercises = fields.Nested(
        lambda: WorkoutExerciseSchema(exclude=('exercise',)),
        many=True,
        dump_only=True
    )


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)

    date = fields.Date(required=True)

    duration_minutes = fields.Int(
        required=True,
        validate=validate.Range(
            min=1,
            error='Workout duration must be at least 1 minute.'
        )
    )

    notes = fields.String(allow_none=True)

    workout_exercises = fields.Nested(
        lambda: WorkoutExerciseSchema(exclude=('workout',)),
        many=True,
        dump_only=True
    )


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)

    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)

    reps = fields.Int(
        required=True,
        validate=validate.Range(
            min=0,
            error='Reps cannot be negative.'
        )
    )

    sets = fields.Int(
        required=True,
        validate=validate.Range(
            min=0,
            error='Sets cannot be negative.'
        )
    )

    duration_seconds = fields.Int(
        required=True,
        validate=validate.Range(
            min=0,
            error='Duration seconds cannot be negative.'
        )
    )

    exercise = fields.Nested(
        lambda: ExerciseSchema(exclude=('workout_exercises',)),
        dump_only=True
    )

    workout = fields.Nested(
        lambda: WorkoutSchema(exclude=('workout_exercises',)),
        dump_only=True
    )