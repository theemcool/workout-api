from config import db


class Workout(db.Model):
    # Define the database table name.
    __tablename__ = "workouts"

    # Give each workout a unique ID.
    id = db.Column(db.Integer, primary_key=True)

    # Store the workout name and description.
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    # Store the scheduled workout date.
    date = db.Column(db.Date, nullable=False)

    # Prevent empty workout names and descriptions.
    __table_args__ = (
        db.CheckConstraint(
            "length(trim(name)) > 0",
            name="check_workout_name"
        ),
        db.CheckConstraint(
            "length(trim(description)) > 0",
            name="check_workout_description"
        ),
    )

    # Connect a workout to its exercise assignments.
    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Workout {self.name}>"