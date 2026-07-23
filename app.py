import os,tempfile,pandas as pd
import streamlit as st
from src.extractor import extract_text
from src.jd_parser import parse_jd
from src.resume_parser import parse_resume
from src.scorer import score_candidate
st.set_page_config(page_title='Smart Candidate Screener',layout='wide')
st.title('Smart Candidate Screener')
col1,col2=st.columns(2)
with col1:
    st.subheader('Job Description')
    jd_file=st.file_uploader('Upload JD',type=['pdf','docx','txt'],key='jd')
    jd_text_input=st.text_area('Or paste JD',height=200)
with col2:
    st.subheader('Resumes')
    resume_files=st.file_uploader('Upload resumes',type=['pdf','docx'],accept_multiple_files=True)
if st.button('Screen Candidates',type='primary'):
    jd_text=''
    if jd_file:
        with tempfile.NamedTemporaryFile(suffix=jd_file.name,delete=False) as f: f.write(jd_file.read()); jd_text=extract_text(f.name)
    elif jd_text_input: jd_text=jd_text_input
    if not jd_text: st.error('Provide a JD.'); st.stop()
    if not resume_files: st.error('Upload resumes.'); st.stop()
    with st.spinner('Parsing JD...'): parsed_jd=parse_jd(jd_text)
    st.success(f'JD: {parsed_jd.title} | {len(parsed_jd.required_skills)} required skills')
    results=[];progress=st.progress(0)
    for i,rf in enumerate(resume_files):
        with tempfile.NamedTemporaryFile(suffix=rf.name,delete=False) as f: f.write(rf.read()); rt=extract_text(f.name)
        with st.spinner(f'Scoring {rf.name}...'): results.append(score_candidate(parsed_jd,parse_resume(rt)))
        progress.progress((i+1)/len(resume_files))
    results.sort(key=lambda r:r.total_score,reverse=True)
    df=pd.DataFrame([{'Rank':i+1,'Candidate':r.candidate_name,'Score':r.total_score,'Matched':','.join(r.matched_skills),'Missing':','.join(r.missing_skills)} for i,r in enumerate(results)])
    st.dataframe(df,use_container_width=True)
    st.download_button('Download CSV',df.to_csv(index=False),'shortlist.csv','text/csv')
