# Workout Application Backend

## Project Description

The Workout Application Backend is a RESTful API built with Flask and SQLAlchemy. It allows users to manage workouts, exercises, and the relationship between them.

The application supports creating, viewing, and deleting workouts and exercises, as well as assigning reusable exercises to different workouts. Each workout-exercise assignment stores its own training details, including sets, repetitions, and duration.

The project uses Flask-Migrate for database migrations and Marshmallow for request validation and serialization.

## Features

- Create, view, and delete workouts.
- Create, view, and delete exercises.
- Assign exercises to workouts.
- Reuse exercises across multiple workouts.
- Store sets, repetitions, and duration for each workout-exercise assignment.
- Validate incoming data using Marshmallow.
- Enforce database constraints to maintain data integrity.
- Seed the database with sample workout and exercise records.
- Run automated API tests using pytest.

## Technologies Used

- Python 3.14
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- Flask-Migrate
- Marshmallow
- SQLite
- Pytest

## Project Structure

```text
workout-api/
│
├── app.py
├── config.py
├── seed.py
├── README.md
├── Pipfile
├── Pipfile.lock
├── requirements.txt
├── .gitignore
│
├── models/
│   ├── __init__.py
│   ├── workout.py
│   ├── exercise.py
│   └── workout_exercise.py
│
├── routes/
│   ├── __init__.py
│   ├── workout_routes.py
│   ├── exercise_routes.py
│   └── workout_exercise_routes.py
│
├── schemas/
│   ├── __init__.py
│   ├── workout_schema.py
│   ├── exercise_schema.py
│   └── workout_exercise_schema.py
│
├── tests/
│   └── test_api.py
│
└── migrations/
```

## Database Models

The application uses three main models:

### 1. Workout

Stores workout information, including:
- ID
- Name
- Description
- Date

### 2. Exercise

Stores reusable exercise information, including:
- ID
- Name
- Description
- Muscle group

### 3. WorkoutExercise

An association model connecting workouts and exercises. It stores additional training information:
- Workout ID
- Exercise ID
- Sets
- Repetitions
- Duration in minutes

A workout can contain multiple exercises, and an exercise can be used in multiple workouts.

## Installation and Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd workout-api
```

### 2. Install Pipenv

```bash
pip install pipenv
```

### 3. Install project dependencies

```bash
pipenv install --dev
```

### 4. Activate the virtual environment

```bash
pipenv shell
```

## Database Setup

The application uses SQLite as its database.

Initialize Flask-Migrate:

```bash
flask --app app db init
```

Generate the initial migration:

```bash
flask --app app db migrate -m "Create workout database tables"
```

Apply the migration:

```bash
flask --app app db upgrade
```

**Note:** Run `db init` only once. If the `migrations/` directory already exists, skip that command.

## Seeding the Database

Populate the database with sample workouts, exercises, and workout-exercise assignments:

```bash
python seed.py
```

The seed script clears existing workout and exercise records before inserting the sample data. Run it only when you are comfortable resetting that data.

## Running the Application

Start the Flask development server:

```bash
python app.py
```

The API will be available at:

```text
http://127.0.0.1:5000
```

## API Endpoints

### Workouts

| Method | Endpoint | Description |
|---|---|---|
| POST | `/workouts/` | Create a workout |
| GET | `/workouts/` | Retrieve all workouts |
| GET | `/workouts/<id>` | Retrieve one workout |
| DELETE | `/workouts/<id>` | Delete a workout |

**Example: Create a workout**

```json
{
    "name": "Leg Day",
    "description": "Lower-body strength training",
    "date": "2026-10-30"
}
```

### Exercises

| Method | Endpoint | Description |
|---|---|---|
| POST | `/exercises/` | Create an exercise |
| GET | `/exercises/` | Retrieve all exercises |
| GET | `/exercises/<id>` | Retrieve one exercise |
| DELETE | `/exercises/<id>` | Delete an exercise |

**Example: Create an exercise**

```json
{
    "name": "Squats",
    "description": "Lower-body strength exercise",
    "muscle_group": "Legs"
}
```

### Workout Exercises

| Method | Endpoint | Description |
|---|---|---|
| POST | `/workout-exercises/` | Assign an exercise to a workout |
| GET | `/workout-exercises/` | Retrieve all workout-exercise assignments |

**Example: Assign an exercise to a workout**

```json
{
    "workout_id": 1,
    "exercise_id": 1,
    "sets": 3,
    "reps": 12
}
```

## Validation and Data Integrity

The application uses multiple validation levels:

- **Database constraints:** Enforce required values, positive training values, unique exercise names, and unique workout-exercise combinations.
- **Model validation:** Validate values when creating or assigning model objects.
- **Schema validation:** Validate incoming API request data using Marshmallow before database operations.

The API also handles errors such as missing records, invalid input, and duplicate records using appropriate HTTP status codes.

## Running Tests

Run the automated tests using:

```bash
pytest -v
```

The tests cover API functionality, including:
- Homepage response.
- Creating workouts and exercises.
- Retrieving records.
- Deleting workouts.
- Rejecting invalid input.
- Handling duplicate exercises.
- Assigning exercises to workouts.
- Handling missing workout records.

## Version Control

Git is used to track project changes.

Example commands:

```bash
git add .
git commit -m "Complete workout application backend"
git push origin main
```

## Author

Developed as part of the Moringa School Software Engineering program.v