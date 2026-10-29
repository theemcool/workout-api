
from flask import Flask, jsonify
from config import db, migrate

# Import all models so SQLAlchemy registers their database tables.
from models import Workout, Exercise, WorkoutExercise

# Import the API blueprints.
from routes.workout_routes import workout_bp
from routes.exercise_routes import exercise_bp
from routes.workout_exercise_routes import workout_exercise_bp


def create_app(test_config=None):
    # Create the Flask application.
    app = Flask(__name__)

    # Set the default application configuration.
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///workout.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Allow tests to use a separate temporary database.
    if test_config:
        app.config.update(test_config)

    # Connect SQLAlchemy and Flask-Migrate to the application.
    db.init_app(app)
    migrate.init_app(app, db)

    # Register the workout, exercise, and assignment routes.
    app.register_blueprint(workout_bp)
    app.register_blueprint(exercise_bp)
    app.register_blueprint(workout_exercise_bp)

    # Provide a homepage to confirm that the API is running.
    @app.route("/")
    def home():
        return jsonify({
            "message": "Workout API is running"
        }), 200

    return app


# Create the application instance.
app = create_app()


# Run the development server when this file is executed directly.
if __name__ == "__main__":
    app.run(debug=True)
