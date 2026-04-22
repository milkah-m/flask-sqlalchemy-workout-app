from flask_marshmallow import Marshmallow
from marshmallow import fields, validates, ValidationError, post_dump

from models import Exercise, Workout, WorkoutExercise

ma = Marshmallow()


#exercise schema
class ExerciseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Exercise
        load_instance = True
        include_fk = True 


    @validates("name")
    def validate_name(self, value):
        if not value:
            raise ValidationError("Name is required")


#workout exercise schema
class WorkoutExerciseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WorkoutExercise
        load_instance = True
        include_fk = True

    workout_id = fields.Integer(load_only=True)
    exercise_id = fields.Integer(load_only=True)

    exercise = fields.Nested(ExerciseSchema, only=("id", "name"))

    @validates("reps")
    def validate_reps(self, value):
        if value is not None and value <= 0:
            raise ValidationError("Reps must be greater than 0")

    @validates("sets")
    def validate_sets(self, value):
        if value is not None and value <= 0:
            raise ValidationError("Sets must be greater than 0")

    @validates("duration_seconds")
    def validate_duration(self, value):
        if value is not None and value <= 0:
            raise ValidationError("Duration must be greater than 0")
        
    @post_dump
    def remove_nulls(self, data, **kwargs):
        return {k: v for k, v in data.items() if v is not None}


#workout schema
class WorkoutSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Workout
        load_instance = True

    
    exercises = fields.Nested(
        WorkoutExerciseSchema, 
        many=True,
        
    )
