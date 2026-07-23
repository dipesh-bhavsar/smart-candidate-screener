import json,os
from openai import OpenAI
from pydantic import BaseModel
client=OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
SCHEMA={'name':'parse_job_description','description':'Extract JD requirements','parameters':{'type':'object','properties':{'title':{'type':'string'},'required_skills':{'type':'array','items':{'type':'string'}},'nice_to_have_skills':{'type':'array','items':{'type':'string'}},'min_years_experience':{'type':'integer'},'key_responsibilities':{'type':'array','items':{'type':'string'}}},'required':['title','required_skills','min_years_experience']}}
class ParsedJD(BaseModel):
    title:str;required_skills:list[str];nice_to_have_skills:list[str]=[];min_years_experience:int=0;key_responsibilities:list[str]=[]
def parse_jd(jd_text):
    r=client.chat.completions.create(model=os.getenv('MODEL','gpt-4o-mini'),messages=[{'role':'user','content':f'Parse this JD:\n\n{jd_text}'}],functions=[SCHEMA],function_call={'name':'parse_job_description'},temperature=0)
    return ParsedJD(**json.loads(r.choices[0].message.function_call.arguments))
