import glob, json, time, os
from src.engines.document_processor import ParallelDocumentProcessor
from src.engines.persona_engine import ZeroShotPersonaEngine
from src.engines.semantic_engine import SemanticMatchingEngine
from src.engines.ranking_engine import IntelligentRanker

def main(input_json):
    t0 = time.time()
    docs = input_json["documents"]
    persona = input_json["persona"]
    job = input_json["job_to_be_done"]

    doc_proc = ParallelDocumentProcessor(max_workers=4)
    doc_sections = doc_proc.process_documents_parallel(docs)

    persona_engine = ZeroShotPersonaEngine()
    persona_profile = persona_engine.analyze_persona(persona)
    job_reqs = persona_engine.parse_job_to_be_done(job, persona_profile)
    scoring_criteria = persona_engine.generate_relevance_criteria(persona_profile, job_reqs)
    print("persona_engine instance:", persona_engine)
    print("persona_profile:", persona_profile)
    print("job description:", job)

    matcher = SemanticMatchingEngine(model_name="models/all-MiniLM-L6-v2")
    embeddings = matcher.batch_encode_sections(doc_sections)
    target_emb = matcher.create_persona_job_vector(persona_profile, job_reqs)
    rel_scores = matcher.score_relevance_fast(embeddings, target_emb, scoring_criteria)

    ranker = IntelligentRanker()
    ranked_sections = ranker.calculate_importance_rank(doc_sections, rel_scores, persona_profile)
    subsections = ranker.extract_refined_subsections(ranked_sections, job_reqs, doc_sections)

    runtime = time.time() - t0
    output = {
        "metadata": {
            "input_documents": docs,
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": time.strftime("%Y-%m-%d"),
            "processing_time_seconds": round(runtime, 2)
        },
        "extracted_sections": ranked_sections,
        "sub_section_analysis": subsections
    }
    return output

if __name__ == "__main__":
    input_dir = "./input"
    output_dir = "./output"
    doc_files = sorted(glob.glob(os.path.join(input_dir, "*.pdf")))
    persona_job_path = os.path.join(input_dir, "persona_job.json")
    if not doc_files or not os.path.exists(persona_job_path):
        raise RuntimeError("No PDF or persona_job.json in input/")
    inp = json.load(open(persona_job_path))
    inp["documents"] = doc_files
    out = main(inp)
    with open(os.path.join(output_dir, "output.json"), 'w') as f:
        json.dump(out, f, indent=2)
