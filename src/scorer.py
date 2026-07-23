from dataclasses import dataclass,field
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from src.jd_parser import ParsedJD
from src.resume_parser import ParsedResume
_model=None
def _get():
    global _model
    if _model is None: _model=SentenceTransformer('all-MiniLM-L6-v2')
    return _model
@dataclass
class ScoreResult:
    candidate_name:str;total_score:float;skill_match_score:float;experience_score:float;semantic_score:float;matched_skills:list=field(default_factory=list);missing_skills:list=field(default_factory=list)
def score_candidate(jd:ParsedJD,resume:ParsedResume)->ScoreResult:
    rl={s.lower() for s in resume.skills}
    matched=[s for s in jd.required_skills if s.lower() in rl]
    missing=[s for s in jd.required_skills if s.lower() not in rl]
    skill_score=(len(matched)/len(jd.required_skills)*40) if jd.required_skills else 20
    exp_ratio=min(resume.total_years_experience/max(jd.min_years_experience,1),1.5) if jd.min_years_experience else 0.7
    exp_score=min(exp_ratio*30,30)
    embs=_get().encode([' '.join(jd.required_skills+jd.key_responsibilities),resume.summary+' '+' '.join(resume.skills)])
    sem_score=float(cosine_similarity([embs[0]],[embs[1]])[0][0])*30
    total=round(min(skill_score+exp_score+sem_score,100),1)
    return ScoreResult(resume.full_name,total,round(skill_score,1),round(exp_score,1),round(sem_score,1),matched,missing)
