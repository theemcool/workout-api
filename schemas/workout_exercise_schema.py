
from marshmallow import Schema, fields, validate


class WorkoutExerciseSchema(Schema):
    # Validate the exercise assignment and training values.
    id = fields.Int(dump_only=True)

    workout_id = fields.Int(
        required=True,
        validate=validate.Range(min=1)
    )

    exercise_id = fields.Int(
        required=True,
        validate=validate.Range(min=1)
    )

    sets = fields.Int(
        load_default=3,
        validate=validate.Range(min=1)
    )

    reps = fields.Int(
        load_default=10,
        validate=validate.Range(min=1)
    )

    duration_minutes = fields.Int(
        allow_none=True,
        load_default=None,
        validate=validate.Range(min=1)
    )
