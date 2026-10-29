
from marshmallow import Schema, fields, validate, validates, ValidationError


class WorkoutSchema(Schema):
    # Validate the workout's basic information.
    id = fields.Int(dump_only=True)

    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100)
    )

    description = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=255)
    )

    date = fields.Date(required=True)

    @validates("name")
    def validate_name(self, value, **kwargs):
        if not value.strip():
            raise ValidationError("Workout name cannot be empty.")

    @validates("description")
    def validate_description(self, value, **kwargs):
        if not value.strip():
            raise ValidationError("Workout description cannot be empty.")
