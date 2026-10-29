from config import db


class Exercise(db.Model):
    # Define the database table name.
    __tablename__ = "exercises"

    # Give each exercise a unique ID.
    id = db.Column(db.Integer, primary_key=True)

    # Require a unique name for each exercise.
    name = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )

    # Store a description and the targeted muscle group.
    description = db.Column(db.String(255), nullable=False)
    muscle_group = db.Column(db.String(80), nullable=False)

    # Prevent empty names, descriptions, and muscle groups.
    __table_args__ = (
        db.CheckConstraint(
            "length(trim(name)) > 0",
            name="check_exercise_name"
        ),
        db.CheckConstraint(
            "length(trim(description)) > 0",
            name="check_exercise_description"
        ),
        db.CheckConstraint(
            "length(trim(muscle_group)) > 0",
            name="check_muscle_group"
        ),
    )

    # Connect an exercise to its workout assignments.
    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="exercise",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Exercise {self.name}>"