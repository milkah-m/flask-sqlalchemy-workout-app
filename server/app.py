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



#workout routes
# GET /workouts
@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return make_response(WorkoutSchema(many=True).dump(workouts), 200)


# GET /workouts/<id>
@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get(id)

    if not workout:
        return make_response({"error": "Workout not found"}, 404)

    return make_response(WorkoutSchema().dump(workout), 200)


# POST /workouts
@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json()

    try:
        workout = WorkoutSchema().load(data)
    except ValidationError as e:
        return make_response(e.messages, 400)

    db.session.add(workout)
    db.session.commit()

    return make_response(WorkoutSchema().dump(workout), 201)


# DELETE /workouts/<id>
@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get(id)

    if not workout:
        return make_response({"error": "Workout not found"}, 404)

    # delete associated join records
    for we in workout.exercises:
        db.session.delete(we)

    db.session.delete(workout)
    db.session.commit()

    return make_response({"message": "Workout deleted"}, 200)



#exercise routes
# GET /exercises
@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return make_response(ExerciseSchema(many=True).dump(exercises), 200)


# GET /exercises/<id>
@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.get(id)

    if not exercise:
        return make_response({"error": "Exercise not found"}, 404)

    return make_response(ExerciseSchema().dump(exercise), 200)


# POST /exercises
@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json()

    try:
        exercise = ExerciseSchema().load(data)
    except ValidationError as e:
        return make_response(e.messages, 400)

    db.session.add(exercise)
    db.session.commit()

    return make_response(ExerciseSchema().dump(exercise), 201)


# DELETE /exercises/<id>
@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get(id)

    if not exercise:
        return make_response({"error": "Exercise not found"}, 404)

    # delete associated join records
    for we in exercise.workouts:
        db.session.delete(we)

    db.session.delete(exercise)
    db.session.commit()

    return make_response({"message": "Exercise deleted"}, 200)


#workout exercise route
# POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises
@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise(workout_id, exercise_id):

    workout = Workout.query.get(workout_id)
    exercise = Exercise.query.get(exercise_id)

    if not workout or not exercise:
        return make_response({"error": "Workout or Exercise not found"}, 404)

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
    db.session.commit()

    return make_response(WorkoutExerciseSchema().dump(we), 201)


if __name__ == '__main__':
    app.run(port=5555, debug=True)