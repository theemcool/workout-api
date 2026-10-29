
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from config import db
from models.workout import Workout
from schemas.workout_schema import WorkoutSchema

# Group workout-related endpoints under /workouts.
workout_bp = Blueprint(
    "workouts", __name__, url_prefix="/workouts"
)

# Create schema instances for one workout and multiple workouts.
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)


# Create a new workout.
@workout_bp.route("/", methods=["POST"])
def create_workout():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "A valid JSON object is required."}), 400

    try:
        # Validate the incoming data using the workout schema.
        validated_data = workout_schema.load(data)

        workout = Workout(**validated_data)

        # Save the workout in the database.
        db.session.add(workout)
        db.session.commit()

        return jsonify(workout_schema.dump(workout)), 201

    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400

    except ValueError as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400


# Retrieve all workouts.
@workout_bp.route("/", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()

    # Convert database records into JSON responses.
    return jsonify(workouts_schema.dump(workouts)), 200


# Retrieve a specific workout using its ID.
@workout_bp.route("/<int:workout_id>", methods=["GET"])
def get_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if not workout:
        return jsonify({"error": "Workout not found."}), 404

    return jsonify(workout_schema.dump(workout)), 200


# Delete a workout using its ID.
@workout_bp.route("/<int:workout_id>", methods=["DELETE"])
def delete_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if not workout:
        return jsonify({"error": "Workout not found."}), 404

    db.session.delete(workout)
    db.session.commit()

    return jsonify({
        "message": "Workout deleted successfully."
    }), 200
