
from datetime import date

from app import create_app
from config import db
from models import Workout, Exercise, WorkoutExercise


# Create the Flask application and its database context.
app = create_app()


def seed_database():
    with app.app_context():

        # Clear existing records before adding fresh sample data.
        db.session.query(WorkoutExercise).delete()
        db.session.query(Workout).delete()
        db.session.query(Exercise).delete()
        db.session.commit()

        # Create sample workouts.
        workouts = [
            Workout(
                name="Leg Day",
                description="Lower-body strength training",
                date=date(2026, 10, 30)
            ),
            Workout(
                name="Upper Body",
                description="Upper-body strength training",
                date=date(2026, 10, 31)
            ),
            Workout(
                name="Full Body",
                description="Complete body workout",
                date=date(2026, 11, 1)
            )
        ]

        # Create reusable exercises.
        exercises = [
            Exercise(
                name="Squats",
                description="Lower-body strength exercise",
                muscle_group="Legs"
            ),
            Exercise(
                name="Push-ups",
                description="Upper-body strength exercise",
                muscle_group="Chest"
            ),
            Exercise(
                name="Plank",
                description="Core stability exercise",
                muscle_group="Core"
            ),
            Exercise(
                name="Lunges",
                description="Leg strength and balance exercise",
                muscle_group="Legs"
            ),
            Exercise(
                name="Pull-ups",
                description="Upper-body pulling exercise",
                muscle_group="Back"
            )
        ]

        # Add workouts and exercises to the database.
        db.session.add_all(workouts)
        db.session.add_all(exercises)
        db.session.commit()

        # Assign exercises to workouts with sets and repetitions.
        assignments = [
            WorkoutExercise(
                workout_id=workouts[0].id,
                exercise_id=exercises[0].id,
                sets=3,
                reps=12
            ),
            WorkoutExercise(
                workout_id=workouts[0].id,
                exercise_id=exercises[3].id,
                sets=3,
                reps=10
            ),
            WorkoutExercise(
                workout_id=workouts[1].id,
                exercise_id=exercises[1].id,
                sets=3,
                reps=15
            ),
            WorkoutExercise(
                workout_id=workouts[1].id,
                exercise_id=exercises[4].id,
                sets=3,
                reps=8
            ),
            WorkoutExercise(
                workout_id=workouts[2].id,
                exercise_id=exercises[2].id,
                sets=3,
                reps=10,
                duration_minutes=1
            )
        ]

        # Save all workout-exercise assignments.
        db.session.add_all(assignments)
        db.session.commit()

        print("Database seeded successfully!")
        print(f"Created {len(workouts)} workouts.")
        print(f"Created {len(exercises)} exercises.")
        print(f"Created {len(assignments)} workout assignments.")


if __name__ == "__main__":
    seed_database()
