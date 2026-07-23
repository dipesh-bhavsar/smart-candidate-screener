import json,os
from openai import OpenAI
from pydantic import BaseModel
client=OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
SCHEMA={'name':'parse_resume','description':'Extract resume info','parameters':{'type':'object','properties':{'full_name':{'type':'string'},'email':{'type':'string'},'total_years_experience':{'type':'number'},'skills':{'type':'array','items':{'type':'string'}},'current_title':{'type':'string'},'summary':{'type':'string'}},'required':['full_name','skills','total_years_experience']}}
class ParsedResume(BaseModel):
    full_name:str;email:str='';total_years_experience:float=0;skills:list[str]=[];current_title:str='';summary:str=''
def parse_resume(resume_text):
    r=client.chat.completions.create(model=os.getenv('MODEL','gpt-4o-mini'),messages=[{'role':'user','content':f'Parse resume:\n\n{resume_text[:4000]}'}],functions=[SCHEMA],function_call={'name':'parse_resume'},temperature=0)
    return ParsedResume(**json.loads(r.choices[0].message.function_call.arguments))
