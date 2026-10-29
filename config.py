from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Set up the database and migration extensions.
# They will be connected to the Flask app in app.py.
db = SQLAlchemy()
migrate = Migrate()
