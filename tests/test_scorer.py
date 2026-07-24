from src.jd_parser import ParsedJD
from src.resume_parser import ParsedResume
from src.scorer import score_candidate
JD=ParsedJD(title='SWE',required_skills=['Python','FastAPI','PostgreSQL'],min_years_experience=3,key_responsibilities=['Build REST APIs'])
def test_full_match_high(): assert score_candidate(JD,ParsedResume(full_name='A',skills=['Python','FastAPI','PostgreSQL'],total_years_experience=5,summary='Python dev')).total_score>=70
def test_no_skill_zero(): assert score_candidate(JD,ParsedResume(full_name='B',skills=['Java'],total_years_experience=5,summary='Java dev')).skill_match_score==0
def test_matched_found(): r=score_candidate(JD,ParsedResume(full_name='C',skills=['Python'],total_years_experience=2,summary='dev')); assert 'Python' in r.matched_skills and 'FastAPI' in r.missing_skills
def test_exp_capped(): assert score_candidate(JD,ParsedResume(full_name='D',skills=[],total_years_experience=100,summary='')).experience_score<=30
