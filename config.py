import os

class Config:
    # Grabs the folder where the script runs.
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Secret key for session management. You can generate random strings here:
    # https://randomkeygen.com/
    SECRET_KEY = 'aAY7f65rv9moADbbVxBuUE39Xc7DSbUG'
    SCHEMA_PATH = 'schema_versions/'
    UPLOAD_PATH = 'uploads/'
    REPORT_PATH = 'pages/'
    ALLOWED_EXTENSIONS = set(['xml', 'ocx'])
    FLASK_ENV = 'production'
    # Debug mode = True if FLASK_ENV = development.
    DEBUG = True

