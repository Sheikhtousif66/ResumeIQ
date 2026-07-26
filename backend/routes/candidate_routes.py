from flask import (
    Blueprint,
    request,
    render_template,
    current_app,
    redirect
)

from werkzeug.utils import secure_filename
import os

from database.db import db
from database.models import Candidate, Job

from parser.pdf_parser import extract_pdf_text

from utils.regex_extractor import (
    extract_email,
    extract_phone
)

from extractor.information_extractor import (
    extract_name,
    extract_skills
)

from extractor.matcher import (
    calculate_match_score,
    compare_skills
)

candidate_bp = Blueprint(
    "candidate",
    __name__
)


@candidate_bp.route("/")
def index():

    jobs = Job.query.all()

    return render_template(
        "index.html",
        jobs=jobs
    )


@candidate_bp.route("/candidates")
def candidates():

    search = request.args.get("search", "")

    if search:

        candidate_list = Candidate.query.filter(
            Candidate.name.ilike(f"%{search}%")
        ).order_by(
            Candidate.match_score.desc()
        ).all()

    else:

        candidate_list = Candidate.query.order_by(
            Candidate.match_score.desc()
        ).all()

    return render_template(
        "candidates.html",
        candidates=candidate_list,
        search=search
    )


@candidate_bp.route("/candidate/<int:id>")
def view_candidate(id):

    candidate = Candidate.query.get_or_404(id)

    return render_template(
        "candidate_details.html",
        candidate=candidate
    )


@candidate_bp.route("/candidate/delete/<int:id>")
def delete_candidate(id):

    candidate = Candidate.query.get_or_404(id)

    db.session.delete(candidate)

    db.session.commit()

    return redirect("/candidates")


@candidate_bp.route(
    "/upload",
    methods=["POST"]
)
def upload():

    if "resume" not in request.files:

        return {
            "error": "No file selected"
        }

    file = request.files["resume"]

    if file.filename == "":

        return {
            "error": "Empty filename"
        }

    job_id = request.form.get("job_id")

    job = Job.query.get(job_id)

    if job is None:

        return {
            "error": "Invalid Job Selected"
        }

    filename = secure_filename(
        file.filename
    )

    save_path = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(save_path)

    text = extract_pdf_text(
        save_path
    )

    email = extract_email(text)

    phone = extract_phone(text)

    name = extract_name(text)

    skills = extract_skills(text)

    job_description = f"""
    {job.title}

    {job.description}

    Skills:
    {job.skills}

    Experience:
    {job.experience}

    Education:
    {job.education}
    """

    match_score = calculate_match_score(
        text,
        job_description
    )

    matched_skills, missing_skills = compare_skills(
        skills,
        job.skills
    )

    candidate = Candidate(

        name=name,

        email=email,

        phone=phone,

        skills=", ".join(skills),

        match_score=match_score,

        resume_text=text

    )

    db.session.add(candidate)

    db.session.commit()

    return render_template(
        "result.html",
        name=name,
        email=email,
        phone=phone,
        skills=skills,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        match_score=match_score,
        job=job
    )
