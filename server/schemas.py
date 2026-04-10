from marshmallow import Marshmallow
from marshmallow import fields, validates, ValidationError

from models import Exercise, Workout, WorkoutExercise

ma = Marshmallow()


#exercise schema
class ExerciseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Exercise
        load_instance = True

    @validates("name")
    def validate_name(self, value):
        if not value:
            raise ValidationError("Name is required")


#workout exercise schema
class WorkoutExerciseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WorkoutExercise
        load_instance = True

    
    exercise = fields.Nested(ExerciseSchema, only=("id", "name"))

    @validates("reps")
    def validate_reps(self, value):
        if value is not None and value <= 0:
            raise ValidationError("Reps must be greater than 0")

    @validates("sets")
    def validate_sets(self, value):
        if value is not None and value <= 0:
            raise ValidationError("Sets must be greater than 0")


#workout schema
class WorkoutSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Workout
        load_instance = True

    
    exercises = fields.Nested(WorkoutExerciseSchema, many=True)

    @validates("duration_minutes")
    def validate_duration(self, value):
        if value <= 0:
            raise ValidationError("Duration must be greater than 0")