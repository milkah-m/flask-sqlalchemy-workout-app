from flask import Flask, request, make_response
from flask_migrate import Migrate

from models import db, Exercise, Workout, WorkoutExercise

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)



# GET /workouts → List all workouts
@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = []

    for w in Workout.query.all():
        workouts.append({
            "id": w.id,
            #using str here to change date object to string...
            "date": str(w.date),
            "duration_minutes": w.duration_minutes,
            "notes": w.notes
        })

    return make_response(workouts, 200)


# GET /workouts/<id>
# Stretch goal: include reps/sets/duration data from WorkoutExercises
# Show a single workout with its associated exercises
@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get(id)

    if not workout:
        return make_response({"error": "Workout not found"}, 404)

    exercises = []


    for we in workout.exercises:
        exercises.append({
            "exercise_id": we.exercise.id,
            "name": we.exercise.name,
            "sets": we.sets,
            "reps": we.reps,
            "duration_seconds": we.duration_seconds
        })

    body = {
        "id": workout.id,
        "date": str(workout.date),
        "duration_minutes": workout.duration_minutes,
        "notes": workout.notes,
        "exercises": exercises
    }

    return make_response(body, 200)


# POST /workouts → Create workout
@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json()

    workout = Workout(
        date=data.get("date"),
        duration_minutes=data.get("duration_minutes"),
        notes=data.get("notes")
    )

    db.session.add(workout)
    db.session.commit()

    return make_response({"message": "Workout created"}, 201)


# DELETE /workouts/<id> → Delete workout (+ stretch)
@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get(id)

    if not workout:
        return make_response({"error": "Workout not found"}, 404)

    # 🔥 stretch: delete associated WorkoutExercises
    for we in workout.exercises:
        db.session.delete(we)

    db.session.delete(workout)
    db.session.commit()

    return make_response({"message": "Workout deleted"}, 200)


# =========================
# 💪 EXERCISE ROUTES
# =========================

# GET /exercises → List all exercises
@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = []

    for e in Exercise.query.all():
        exercises.append({
            "id": e.id,
            "name": e.name,
            "category": e.category,
            "equipment_needed": e.equipment_needed
        })

    return make_response(exercises, 200)


# GET /exercises/<id> → Show exercise + workouts
@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.get(id)

    if not exercise:
        return make_response({"error": "Exercise not found"}, 404)

    workouts = []

    for we in exercise.workouts:
        workouts.append({
            "workout_id": we.workout.id,
            "date": str(we.workout.date),
            "sets": we.sets,
            "reps": we.reps,
            "duration_seconds": we.duration_seconds
        })

    body = {
        "id": exercise.id,
        "name": exercise.name,
        "category": exercise.category,
        "equipment_needed": exercise.equipment_needed,
        "workouts": workouts
    }

    return make_response(body, 200)


# POST /exercises → Create exercise
@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json()

    exercise = Exercise(
        name=data.get("name"),
        category=data.get("category"),
        equipment_needed=data.get("equipment_needed", False)
    )

    db.session.add(exercise)
    db.session.commit()

    return make_response({"message": "Exercise created"}, 201)


# DELETE /exercises/<id> → Delete exercise (+ stretch)
@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get(id)

    if not exercise:
        return make_response({"error": "Exercise not found"}, 404)

    # 🔥 stretch: delete associated WorkoutExercises
    for we in exercise.workouts:
        db.session.delete(we)

    db.session.delete(exercise)
    db.session.commit()

    return make_response({"message": "Exercise deleted"}, 200)


# =========================
# 🔗 JOIN TABLE ROUTE
# =========================

# POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises
@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise(workout_id, exercise_id):

    workout = Workout.query.get(workout_id)
    exercise = Exercise.query.get(exercise_id)

    if not workout or not exercise:
        return make_response({"error": "Workout or Exercise not found"}, 404)

    data = request.get_json()

    we = WorkoutExercise(
        workout=workout,
        exercise=exercise,
        sets=data.get("sets"),
        reps=data.get("reps"),
        duration_seconds=data.get("duration_seconds")
    )

    db.session.add(we)
    db.session.commit()

    return make_response({"message": "Exercise added to workout"}, 201)


# =========================
# 🚀 RUN
# =========================
if __name__ == '__main__':
    app.run(port=5555, debug=True)