from database.db import db


class Candidate(db.Model):
    __tablename__ = "candidates"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(100)
    )

    phone = db.Column(
        db.String(20)
    )

    skills = db.Column(
        db.Text
    )

    match_score = db.Column(
        db.Float
    )

    resume_text = db.Column(
        db.Text
    )

    def __repr__(self):
        return f"<Candidate {self.email}>"


class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.Text
    )

    skills = db.Column(
        db.Text
    )

    experience = db.Column(
        db.String(50)
    )

    education = db.Column(
        db.String(100)
    )

    def __repr__(self):
        return f"<Job {self.title}>"
