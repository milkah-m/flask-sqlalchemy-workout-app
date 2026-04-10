# 💪 Workout Tracker API

A RESTful backend API for logging and managing workouts and exercises, built with Flask, SQLAlchemy, and Marshmallow.

---

## Description

Workout Tracker lets you create workouts, build an exercise library, and link exercises to workouts with set/rep/duration data via a join table. The API supports full CRUD on workouts and exercises, with nested serialization and robust validation at both the model and schema layers.

---

## Models & Relationships

- **Exercise** — a reusable exercise (name, category, equipment needed)
- **Workout** — a dated session with duration and optional notes
- **WorkoutExercise** — join table linking workouts to exercises, storing sets, reps, and duration

A `Workout` has many `Exercises` through `WorkoutExercises`, and vice versa.

---

## Installation

**Prerequisites:** Python 3.8+, `pipenv` (or `pip`)

```bash
# 1. Clone the repo
git clone https://github.com/your-username/workout-tracker-api.git
cd workout-tracker-api

# 2. Install dependencies
pipenv install
pipenv shell

# 3. Set up the database
flask db init
flask db migrate -m "initial migration"
flask db upgrade

# 4. Seed the database
python seed.py
```

---

## Running the App

```bash
python app.py
```

The server runs on **http://localhost:5555**.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/workouts` | List all workouts |
| GET | `/workouts/<id>` | Get a single workout |
| POST | `/workouts` | Create a workout |
| DELETE | `/workouts/<id>` | Delete a workout |
| GET | `/exercises` | List all exercises |
| GET | `/exercises/<id>` | Get a single exercise |
| POST | `/exercises` | Create an exercise |
| DELETE | `/exercises/<id>` | Delete an exercise |
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout |

---

## Tech Stack

- [Flask](https://flask.palletsprojects.com/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-Migrate](https://flask-migrate.readthedocs.io/)
- [Marshmallow](https://marshmallow.readthedocs.io/) / [Flask-Marshmallow](https://flask-marshmallow.readthedocs.io/)
- SQLite