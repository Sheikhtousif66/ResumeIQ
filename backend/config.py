import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "uploads"
)

DATABASE_PATH = os.path.join(
    BASE_DIR,
    "resumeiq.db"
)


class Config:

    SECRET_KEY = "resumeiq-secret-key"

    UPLOAD_FOLDER = UPLOAD_FOLDER

    SQLALCHEMY_DATABASE_URI = \
        "sqlite:///" + DATABASE_PATH

    SQLALCHEMY_TRACK_MODIFICATIONS = False
