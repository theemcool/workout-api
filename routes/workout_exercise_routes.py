
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from config import db
from models.workout import Workout
from models.exercise import Exercise
from models.workout_exercise import WorkoutExercise
from schemas.workout_exercise_schema import WorkoutExerciseSchema

# Group workout-exercise endpoints under /workout-exercises.
workout_exercise_bp = Blueprint(
    "workout_exercises",
    __name__,
    url_prefix="/workout-exercises"
)

# Create schema instances for one assignment and multiple assignments.
assignment_schema = WorkoutExerciseSchema()
assignments_schema = WorkoutExerciseSchema(many=True)


# Assign an exercise to a workout.
@workout_exercise_bp.route("/", methods=["POST"])
def add_exercise_to_workout():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "A valid JSON object is required."}), 400

    try:
        # Validate workout ID, exercise ID, sets, reps and duration.
        validated_data = assignment_schema.load(data)

        workout_id = validated_data["workout_id"]
        exercise_id = validated_data["exercise_id"]

        # Confirm that the workout exists.
        workout = db.session.get(Workout, workout_id)

        if not workout:
            return jsonify({"error": "Workout not found."}), 404

        # Confirm that the exercise exists.
        exercise = db.session.get(Exercise, exercise_id)

        if not exercise:
            return jsonify({"error": "Exercise not found."}), 404

        # Create the relationship between the workout and exercise.
        assignment = WorkoutExercise(**validated_data)

        db.session.add(assignment)
        db.session.commit()

        return jsonify(assignment_schema.dump(assignment)), 201

    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400

    except ValueError as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400

    except IntegrityError:
        db.session.rollback()

        return jsonify({
            "error": "This exercise is already assigned to the workout."
        }), 409


# Retrieve all workout-exercise assignments.
@workout_exercise_bp.route("/", methods=["GET"])
def get_assignments():
    assignments = WorkoutExercise.query.all()

    return jsonify(assignments_schema.dump(assignments)), 200
