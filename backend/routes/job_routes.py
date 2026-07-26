from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for
)

from database.db import db
from database.models import Job

job_bp = Blueprint(
    "job",
    __name__
)


@job_bp.route("/jobs/new")
def new_job():

    return render_template(
        "create_job.html"
    )


@job_bp.route(
    "/jobs/create",
    methods=["POST"]
)
def create_job():

    job = Job(

        title=request.form["title"],

        skills=request.form["skills"],

        experience=request.form["experience"],

        education=request.form["education"],

        description=request.form["description"]

    )

    db.session.add(job)

    db.session.commit()

    return redirect(
        url_for("job.list_jobs")
    )


@job_bp.route("/jobs")
def list_jobs():

    jobs = Job.query.order_by(
        Job.id.desc()
    ).all()

    return render_template(
        "jobs.html",
        jobs=jobs
    )


@job_bp.route(
    "/jobs/delete/<int:id>",
    methods=["POST"]
)
def delete_job(id):

    job = Job.query.get_or_404(id)

    db.session.delete(job)

    db.session.commit()

    return redirect(
        url_for("job.list_jobs")
    )
