import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from django.conf import settings
from aiservice.models import Ai_summary
from resources.models import Resource
from rest_framework.response import Response

genai.configure(api_key=settings.GEMINI_API_KEY)# type: ignore

def ai_summarizer(url:str):
    model = genai.GenerativeModel("models/gemini-2.5-flash")# type: ignore
    html = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).text
    soup = BeautifulSoup(html, "html.parser")
    page_text = soup.get_text(separator="\n", strip=True)
    prompt = f"""
You are given the following webpage content:
{page_text[:35000]}   # prevents token limit crash
Give a **200-word summary** explaining:
- What level of experience is required   
- What types of projects can be built  
- Basic beginner-level understanding  
Write clearly and simply.
"""
    response = model.generate_content(prompt)
    return response.text

flag = True
count = 0
def ask_question(question,id):
    global flag 
    global count
    if count == 5: 
        return "Model was busy try after sometime"
    response = None
    model = None
    if flag:
       model = genai.GenerativeModel("models/gemini-2.5-pro")# type: ignore
    else:
        model = genai.GenerativeModel("models/gemini-2.5-flash")# type: ignore
        flag=True
    resource=None
    ai_summary_obj = None
    try:
      resource = Resource.objects.get(id=id)
    except:
        return Response({"ERROR_MESSAGE":"RESOURCE_NOT_FOUND"})
    try:
        ai_summary_obj = Ai_summary.objects.get(resource=resource)
    except Ai_summary.DoesNotExist:
        ai_summary_obj = None
    html = requests.get(resource.url, headers={"User-Agent": "Mozilla/5.0"}).text
    soup = BeautifulSoup(html, "html.parser")
    page_text = soup.get_text(separator="\n", strip=True)
    summary = ai_summary_obj.summary if ai_summary_obj is not None else None
    prompt = f"""
    You are given the following webpage content:
    {page_text[:35000]}   # prevents token limit crash
    i also a attach a summary of this project {summary }
    Write clearly and simply.
    """
    try:
       response = model.generate_content(prompt)
    except:
        flag=False
        count+=1
        return ask_question(question,id)
    return response.text








