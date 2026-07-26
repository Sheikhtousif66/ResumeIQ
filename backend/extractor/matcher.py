from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def calculate_match_score(
    resume_text,
    job_description
):

    resume_embedding = model.encode(
        resume_text
    )

    jd_embedding = model.encode(
        job_description
    )

    similarity = cos_sim(
        resume_embedding,
        jd_embedding
    )

    score = float(
        similarity[0][0]
    ) * 100

    return round(score, 2)


def compare_skills(
    resume_skills,
    job_skills
):

    resume_set = {
        skill.strip().lower()
        for skill in resume_skills
    }

    job_set = {
        skill.strip().lower()
        for skill in job_skills.split(",")
    }

    matched_skills = sorted(
        resume_set & job_set
    )

    missing_skills = sorted(
        job_set - resume_set
    )

    return (
        matched_skills,
        missing_skills
    )
