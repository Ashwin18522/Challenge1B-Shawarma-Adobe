from sentence_transformers import SentenceTransformer
import numpy as np

class SemanticMatchingEngine:
    def __init__(self, model_name="models/all-MiniLM-L6-v2"):
        self.encoder = SentenceTransformer(model_name)
        self.vector_cache = {}

    def batch_encode_sections(self, doc_sections):
        texts, keys = [], []
        for pdf, sections in doc_sections.items():
            for i, sec in enumerate(sections):
                key = (pdf, i)
                text = sec.get("content", "")[:800]
                texts.append(text)
                keys.append(key)
        embs = self.encoder.encode(texts, batch_size=32, show_progress_bar=False, normalize_embeddings=True)
        return {k: v for k, v in zip(keys, embs)}

    def create_persona_job_vector(self, persona_profile, job_reqs):
        text = (
            persona_profile.get("role", "") + " " +
            persona_profile.get("domain", "") + " " +
            " ".join(persona_profile.get("expertise_areas", [])) + " " +
            " ".join(job_reqs.get("information_types_needed", []))
        )
        emb = self.encoder.encode([text], normalize_embeddings=True)[0]
        return emb

    def score_relevance_fast(self, section_embeddings, target_embedding, scoring_criteria):
        keywds = scoring_criteria.get("keyword_priorities", [])
        relevance = {}
        for (pdf, idx), vec in section_embeddings.items():
            sim = np.dot(vec, target_embedding)
            keyword_boost = 0.0
            for kw in keywds:
                if kw in str(pdf).lower():
                    keyword_boost += 0.05
            relevance[(pdf, idx)] = float(sim) + keyword_boost
        return relevance
