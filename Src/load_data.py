import json
from pathlib import Path
import re


def load_doctors(path="C:/Users/yazdan/Ahd_Task/Doctors_RAG_Chatbot/Data/doctors_500.json"):
    path = Path(path)
    with path.open(encoding="utf-8") as f:
        return json.load(f)

PREFIXES = [
    r"سرکار\s*خانم\s*دکتر",
    r"سرکار\s*خانم",
    r"جناب\s*آقای\s*دکتر",
    r"جناب\s*آقای",
    r"دکتر",
    r"دكتر"
]

PERSIAN_NORMALIZE = {
    "ي": "ی",
    "ى": "ی",
    "ك": "ک",
    "ؤ": "و",
    "إ": "ا",
    "أ": "ا",
    "ۀ": "ه",
    "ة": "ه",
}
def clean_and_normalize(name):

    # Persian character normalization
    for src, dst in PERSIAN_NORMALIZE.items():
        name = name.replace(src, dst)

    # Whitespace cleanup
    name = name.replace("\t", " ").replace("\n", " ")

    # Remove prefixes/titles
    for p in PREFIXES:
        name = re.sub(p, "", name, flags=re.IGNORECASE)

    # Normalize spaces
    name = re.sub(r"\s+", " ", name).strip()

    # Remove leading punctuation
    name = re.sub(r"^[\-\–\:]+", "", name).strip()

    return name

def doctor_to_text(doc):


    text = (
        f"Doctor Name: {clean_and_normalize(doc['name'])}. "
        f"City: {doc['city']}. "
        f"Years of Experience: {doc['experience_years']}. "
        f"Specialization: {doc['specialty']}."
        f"Biography: {clean_and_normalize(doc['biography'])}."
    )
    return text

def prepare_documents(raw_docs):
    return [doctor_to_text(d) for d in raw_docs]
