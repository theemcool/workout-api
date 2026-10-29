from config import db


class WorkoutExercise(db.Model):
    # This table connects workouts and exercises.
    __tablename__ = "workout_exercises"

    # Give each assignment a unique ID.
    id = db.Column(db.Integer, primary_key=True)

    # Reference the workout receiving the exercise.
    workout_id = db.Column(
        db.Integer,
        db.ForeignKey("workouts.id"),
        nullable=False
    )

    # Reference the exercise being assigned.
    exercise_id = db.Column(
        db.Integer,
        db.ForeignKey("exercises.id"),
        nullable=False
    )

    # Store the number of sets and repetitions.
    sets = db.Column(db.Integer, nullable=False, default=3)
    reps = db.Column(db.Integer, nullable=False, default=10)

    # Duration is optional for exercises measured by repetitions.
    duration_minutes = db.Column(db.Integer, nullable=True)

    # Enforce valid training values and prevent duplicate assignments.
    __table_args__ = (
        db.CheckConstraint(
            "sets > 0",
            name="check_positive_sets"
        ),
        db.CheckConstraint(
            "reps > 0",
            name="check_positive_reps"
        ),
        db.CheckConstraint(
            "duration_minutes IS NULL OR duration_minutes > 0",
            name="check_positive_duration"
        ),
        db.UniqueConstraint(
            "workout_id",
            "exercise_id",
            name="unique_workout_exercise"
        ),
    )

    # Allow access to the related workout and exercise objects.
    workout = db.relationship(
        "Workout",
        back_populates="workout_exercises"
    )
    exercise = db.relationship(
        "Exercise",
        back_populates="workout_exercises"
    )

    def __repr__(self):
        return (
            f"<WorkoutExercise workout={self.workout_id} "
            f"exercise={self.exercise_id}>"
        )