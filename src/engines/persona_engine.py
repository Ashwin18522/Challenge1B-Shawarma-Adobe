import spacy
from functools import lru_cache

class ZeroShotPersonaEngine:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    @lru_cache(maxsize=32)
    def analyze_persona(self, persona):
        doc = self.nlp(persona)
        expertise = [token.text for token in doc if token.pos_ in ('NOUN', 'PROPN', 'ADJ')]
        profile = {
            "role": persona.split(" in ")[0] if " in " in persona else persona,
            "domain": persona.split(" in ")[1] if " in " in persona else "",
            "expertise_areas": expertise,
            "knowledge_level": "expert" if "phd" in persona.lower() or "senior" in persona.lower() else "intermediate",
        }
        return profile

    # @lru_cache(maxsize=32)
    def parse_job_to_be_done(self, job, persona_profile):
        doc = self.nlp(job.lower())
        information_types = []
        if "literature review" in job.lower(): information_types += ["methodologies", "datasets", "benchmarks"]
        if "summarize" in job.lower(): information_types += ["summary", "main points"]
        return {
            "primary_goals": [chunk.text for chunk in doc.noun_chunks],
            "information_types_needed": information_types or [token.text for token in doc if token.pos_ == "NOUN"],
            "deliverable": job,
        }

    def generate_relevance_criteria(self, persona_profile, job_requirements):
        keywords = []
        keywords += persona_profile.get('expertise_areas', [])
        keywords += job_requirements.get('information_types_needed', [])
        keywords = list(set(k.lower() for k in keywords))
        return {
            "keyword_priorities": keywords,
            "section_types_important": ["Methodology", "Dataset", "Benchmark", "Summary"]
        }
