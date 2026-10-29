
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from config import db
from models.exercise import Exercise
from schemas.exercise_schema import ExerciseSchema

# Group exercise-related endpoints under /exercises.
exercise_bp = Blueprint(
    "exercises", __name__, url_prefix="/exercises"
)

# Create schema instances for one exercise and multiple exercises.
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)


# Create a new exercise.
@exercise_bp.route("/", methods=["POST"])
def create_exercise():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "A valid JSON object is required."}), 400

    try:
        # Validate the submitted exercise information.
        validated_data = exercise_schema.load(data)

        exercise = Exercise(**validated_data)

        # Save the new exercise.
        db.session.add(exercise)
        db.session.commit()

        return jsonify(exercise_schema.dump(exercise)), 201

    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400

    except ValueError as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400

    except IntegrityError:
        db.session.rollback()
        return jsonify({
            "error": "An exercise with this name already exists."
        }), 409


# Retrieve all available exercises.
@exercise_bp.route("/", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()

    return jsonify(exercises_schema.dump(exercises)), 200


# Retrieve one exercise using its ID.
@exercise_bp.route("/<int:exercise_id>", methods=["GET"])
def get_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if not exercise:
        return jsonify({"error": "Exercise not found."}), 404

    return jsonify(exercise_schema.dump(exercise)), 200


# Delete an exercise using its ID.
@exercise_bp.route("/<int:exercise_id>", methods=["DELETE"])
def delete_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if not exercise:
        return jsonify({"error": "Exercise not found."}), 404

    db.session.delete(exercise)

    try:
        db.session.commit()

        return jsonify({
            "message": "Exercise deleted successfully."
        }), 200

    except IntegrityError:
        db.session.rollback()

        return jsonify({
            "error": "This exercise is assigned to a workout and cannot be deleted."
        }), 409
