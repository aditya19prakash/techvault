import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from django.conf import settings
from aiservice.models import Ai_summary
from resources.models import Resource
from rest_framework.response import Response
from rapidfuzz import fuzz
from .models import Ai_saved_answer


genai.configure(api_key=settings.GEMINI_API_KEY)

def ai_summarizer(url:str):
    model = genai.GenerativeModel("models/gemini-2.5-flash")

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

def ask_question(question,id):
    global flag
    model = None
    if flag:
       model = genai.GenerativeModel("models/gemini-2.5-pro")
    else:
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        flag=True
    resource=None
    ai_summary_obj = None
    try:
      resource = Resource.objects.get(id=id)
    except:
        return Response({"ERROR_MESSAGE":"RESOURCE_NOT_FOUND"})
    try:
        ai_summary_obj = Ai_summary.objects.get(resource=resource)
    except:
        pass
    html = requests.get(resource.url, headers={"User-Agent": "Mozilla/5.0"}).text
    soup = BeautifulSoup(html, "html.parser")
    page_text = soup.get_text(separator="\n", strip=True)
    prompt = f"""
    You are given the following webpage content:
    {page_text[:35000]}   # prevents token limit crash
    i also a attach a summary of this project {ai_summary_obj.summary}
    i give a question:{question}
    Write clearly and simply.
    """
    try:
       response = model.generate_content(prompt)
    except:
        flag=False
        ask_question(question,id)
    return response.text

def find_similar_answer(user_question):
    saved = Ai_saved_answer.objects.all()
    best_score = 0
    best_answer = None
    for item in saved:
        score = fuzz.token_sort_ratio(user_question.lower(), item.question.lower())
        if score > best_score:
            best_score = score
            best_answer = item.answer
    if best_score >= 70:
        return best_answer
    return None

import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

def email_message_creation(data: dict):
    model = genai.GenerativeModel("models/gemini-2.5-flash")

    url = data["url"]
    logo_url = data["logo_url"]  # GitHub image link

    html = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).text
    soup = BeautifulSoup(html, "html.parser")
    page_text = soup.get_text(separator="\n", strip=True)
    cleaned_text = page_text[:25000]

    prompt = f"""
    Generate a professional HTML email summary for this project.

    Include this logo at the top, centered:
    <img src="{logo_url}" alt="TechVault Logo" 
         style="width:160px; margin:0 auto 20px; display:block;" />

    End with:
    <p>Sincerely,<br>TechVault Team</p>

    Project Content:
    {cleaned_text}
    """

    response = model.generate_content(prompt)

    try:
        return response.text
    except:
        return "".join([c.text for c in response.candidates])


