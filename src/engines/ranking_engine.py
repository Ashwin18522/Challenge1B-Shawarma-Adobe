class IntelligentRanker:
    def __init__(self):
        self.ranking_weights = {
            'semantic_similarity': 0.5,
            'keyword_relevance': 0.3,
            'section_importance': 0.2,
        }

    def calculate_importance_rank(self, doc_sections, rel_scores, persona_profile, top_k=7):
        all_sections = []
        for pdf, sections in doc_sections.items():
            for i, sec in enumerate(sections):
                score = rel_scores.get((pdf, i), 0.0)
                all_sections.append({
                    "document": pdf,
                    "page_number": sec.get("page_number", 0),
                    "section_title": sec.get("section_title", "")[:90],
                    "importance_rank": 0,
                    "relevance_score": round(score, 3)
                })
        ranked = sorted(all_sections, key=lambda d: d["relevance_score"], reverse=True)[:top_k]
        for k, sec in enumerate(ranked):
            sec["importance_rank"] = k+1
        return ranked

    def extract_refined_subsections(self, ranked_sections, job_requirements, doc_sections=None):
        analysis = []
        info_types = set(job_requirements.get("information_types_needed", []))
        for sec in ranked_sections:
            ref_text = sec["section_title"]
            if doc_sections:
                idx = None
                for i, s in enumerate(doc_sections[sec["document"]]):
                    if s.get("section_title", "") == sec["section_title"]:
                        idx = i
                        break
                if idx is not None:
                    orig_text = doc_sections[sec["document"]][idx].get("content", "")
                    found = False
                    for it in info_types:
                        if it in orig_text.lower():
                            ref_text = orig_text
                            found = True
                            break
                    if not found:
                        ref_text = ". ".join(orig_text.split(".")[:3])
            analysis.append({
                "document": sec["document"],
                "section_title": sec["section_title"],
                "refined_text": ref_text[:400].strip(),
                "page_number": sec["page_number"],
                "importance_rank": sec["importance_rank"]
            })
        return analysis

    def validate_output_quality(self, extracted_sections, persona_profile):
        return True, extracted_sections
