
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Create the database extension.
# It will be connected to the Flask application in app.py.
db = SQLAlchemy()

# Create the migration extension.
# It manages changes to the database structure.
migrate = Migrate()
