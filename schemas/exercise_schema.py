
from marshmallow import Schema, fields, validate, validates, ValidationError


class ExerciseSchema(Schema):
    # Validate an exercise's details.
    id = fields.Int(dump_only=True)

    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100)
    )

    description = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=255)
    )

    muscle_group = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=80)
    )

    @validates("name")
    def validate_name(self, value, **kwargs):
        if not value.strip():
            raise ValidationError("Exercise name cannot be empty.")

    @validates("description")
    def validate_description(self, value, **kwargs):
        if not value.strip():
            raise ValidationError("Description cannot be empty.")

    @validates("muscle_group")
    def validate_muscle_group(self, value, **kwargs):
        if not value.strip():
            raise ValidationError("Muscle group cannot be empty.")
