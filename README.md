# Workout Application Backend

## Description

Workout Application Backend is a Flask REST API that allows users to create and manage workouts and exercises.

A workout can contain multiple exercises, while an exercise can be used in multiple workouts. The `WorkoutExercise` model connects workouts and exercises and stores information such as sets, reps, and duration.

## Features

- Create and view workouts
- Create and view exercises
- Add exercises to workouts
- Delete workouts and exercises
- Track sets, reps, and exercise duration
- View exercises associated with a workout
- View workouts associated with an exercise
- Input validation using Marshmallow and SQLAlchemy
- Database management using Flask-Migrate
- Sample data provided through a seed file

## Installation

1. Clone the repository

```bash
git clone https://github.com/tandisimelane-15/workout-application-backend.git
```

2. Open the project folder

```bash
cd workout-application-backend
```

3. Install the dependencies

```bash
pipenv install
```

4. Activate the virtual environment

```bash
pipenv shell
```

5. Move into the server directory

```bash
cd server
```

6. Set the Flask application

```bash
export FLASK_APP=app.py
```

7. Run the database migrations

```bash
flask db upgrade head
```

8. Seed the database

```bash
python seed.py
```

## How to Run the Project

Start the Flask server from the `server` directory:

```bash
export FLASK_APP=app.py
export FLASK_RUN_PORT=5555
flask run
```

The application runs on port `5555`.

## API Endpoints

### Workouts

- `GET /workouts` - Returns all workouts
- `GET /workouts/<id>` - Returns a workout and its associated exercises
- `POST /workouts` - Creates a new workout
- `DELETE /workouts/<id>` - Deletes a workout

### Exercises

- `GET /exercises` - Returns all exercises
- `GET /exercises/<id>` - Returns an exercise and its associated workouts
- `POST /exercises` - Creates a new exercise
- `DELETE /exercises/<id>` - Deletes an exercise

### Workout Exercises

- `POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` - Adds an exercise to a workout with sets, reps, and duration

## Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Marshmallow
- SQLite
- Pipenv

## Future Implementations

- Add the ability to update workouts and exercises
- Add an endpoint to remove an individual exercise from a workout
- Add user authentication
- Add workout progress tracking

## How to Contribute

Pull requests are welcome. For major changes, please open an issue first.

## License

MIT License

Copyright (c) 2026 Abigail Tandiwe

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Contact

- LinkedIn: [Abigail Tandiwe](https://www.linkedin.com/in/abigailtandi)
- Email: tandisimelane24@gmail.com