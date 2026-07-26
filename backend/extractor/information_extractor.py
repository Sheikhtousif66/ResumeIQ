import re
import spacy

nlp = spacy.load("en_core_web_sm")

SKILLS = [
    "python",
    "java",
    "c",
    "c++",
    "sql",
    "mysql",
    "oracle",
    "html",
    "css",
    "javascript",
    "flask",
    "git",
    "github",
    "opencv",
    "rest api",
    "rest apis"
]


def extract_name(text):

    lines = text.split("\n")

    for line in lines[:10]:

        line = line.strip()

        if (
            len(line.split()) >= 2
            and "@" not in line
            and "+" not in line
        ):
            return line

    return None


def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS:

        # Special handling for C++
        if skill == "c++":

            if "c++" in text:
                found_skills.append(skill)

            continue

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text):

            found_skills.append(skill)

    return found_skills
