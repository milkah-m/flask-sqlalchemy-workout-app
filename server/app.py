from flask import Flask, request, make_response
from flask_migrate import Migrate
from marshmallow import ValidationError

from models import db, Exercise, Workout, WorkoutExercise
from schemas import ma, ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
ma.init_app(app)


# exercise

@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return make_response(ExerciseSchema(many=True).dump(exercises), 200)


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.get(id)

    if not exercise:
        return make_response({"error": "Exercise not found"}, 404)

    return make_response(ExerciseSchema().dump(exercise), 200)


@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json()

    try:
        exercise = ExerciseSchema().load(data)
    except ValidationError as e:
        return make_response(e.messages, 400)

    db.session.add(exercise)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return make_response({"error": str(e)}, 400)

    return make_response(ExerciseSchema().dump(exercise), 201)

@app.route('/exercises/<int:id>', methods=['PATCH'])
def update_exercise(id):
    exercise = Exercise.query.get(id)

    if not exercise:
        return make_response({"error": "Exercise not found"}, 404)

    data = request.get_json()

    try:
        updated = ExerciseSchema(partial=True).load(
            data,
            instance=exercise,
            session=db.session
        )
    except ValidationError as e:
        return make_response(e.messages, 400)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return make_response({"error": str(e)}, 400)

    return make_response(ExerciseSchema().dump(updated), 200)


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get(id)

    if not exercise:
        return make_response({"error": "Exercise not found"}, 404)

    db.session.delete(exercise)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return make_response({"error": str(e)}, 400)

    return make_response({"message": "Exercise deleted"}, 200)


# workout

@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return make_response(WorkoutSchema(many=True).dump(workouts), 200)


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get(id)

    if not workout:
        return make_response({"error": "Workout not found"}, 404)

    return make_response(WorkoutSchema().dump(workout), 200)


@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json()

    try:
        workout = WorkoutSchema().load(data)
    except ValidationError as e:
        return make_response(e.messages, 400)

    db.session.add(workout)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return make_response({"error": str(e)}, 400)

    return make_response(WorkoutSchema().dump(workout), 201)


@app.route('/workouts/<int:id>', methods=['PATCH'])
def update_workout(id):
    workout = Workout.query.get(id)

    if not workout:
        return make_response({"error": "Workout not found"}, 404)

    data = request.get_json()

    try:
        updated = WorkoutSchema(partial=True).load(
            data,
            instance=workout,
            session=db.session
        )
    except ValidationError as e:
        return make_response(e.messages, 400)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return make_response({"error": str(e)}, 400)

    return make_response(WorkoutSchema().dump(updated), 200)


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get(id)

    if not workout:
        return make_response({"error": "Workout not found"}, 404)

    db.session.delete(workout)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return make_response({"error": str(e)}, 400)

    return make_response({"message": "Workout deleted"}, 200)


# workout-exercise

@app.route('/workout_exercises', methods=['GET'])
def get_workout_exercises():
    we = WorkoutExercise.query.all()
    return make_response(WorkoutExerciseSchema(many=True).dump(we), 200)


@app.route('/workout_exercises/<int:id>', methods=['GET'])
def get_workout_exercise(id):
    we = WorkoutExercise.query.get(id)

    if not we:
        return make_response({"error": "WorkoutExercise not found"}, 404)

    return make_response(WorkoutExerciseSchema().dump(we), 200)


@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise(workout_id, exercise_id):

    workout = Workout.query.get(workout_id)
    exercise = Exercise.query.get(exercise_id)

    if not workout or not exercise:
        return make_response({"error": "Workout or Exercise not found"}, 404)

    existing = WorkoutExercise.query.filter_by(
        workout_id=workout_id,
        exercise_id=exercise_id
    ).first()

    if existing:
        return make_response({"error": "Exercise already added to this workout"}, 400)

    data = request.get_json()

    try:
        we = WorkoutExerciseSchema().load({
            **data,
            "workout_id": workout_id,
            "exercise_id": exercise_id
        })
    except ValidationError as e:
        return make_response(e.messages, 400)

    db.session.add(we)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return make_response({"error": str(e)}, 400)

    return make_response(WorkoutExerciseSchema().dump(we), 201)


@app.route('/workout_exercises/<int:id>', methods=['PATCH'])
def update_workout_exercise(id):
    we = WorkoutExercise.query.get(id)

    if not we:
        return make_response({"error": "WorkoutExercise not found"}, 404)

    data = request.get_json()

    try:
        updated = WorkoutExerciseSchema(partial=True).load(
            data,
            instance=we,
            session=db.session
        )
    except ValidationError as e:
        return make_response(e.messages, 400)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return make_response({"error": str(e)}, 400)

    return make_response(WorkoutExerciseSchema().dump(updated), 200)


@app.route('/workout_exercises/<int:id>', methods=['DELETE'])
def delete_workout_exercise(id):
    we = WorkoutExercise.query.get(id)

    if not we:
        return make_response({"error": "WorkoutExercise not found"}, 404)

    db.session.delete(we)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return make_response({"error": str(e)}, 400)

    return make_response({"message": "WorkoutExercise deleted"}, 200)


# run

if __name__ == '__main__':
    app.run(port=5555, debug=True)