from flask import Flask

from config import Config
from database.db import db

from routes.job_routes import job_bp
from routes.candidate_routes import candidate_bp


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(job_bp)
    app.register_blueprint(candidate_bp)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
