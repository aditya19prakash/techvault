import requests
from bs4 import BeautifulSoup
from django.conf import settings
from google import genai

from aiservice.models import Ai_summary
from resources.models import Resource


GEMINI_MODELS = [
    "models/gemini-2.5-flash",         
    "models/gemini-2.0-flash",          
    "models/gemini-2.5-flash-lite",  
    "models/gemini-2.0-flash-lite",     
    "models/gemini-3-pro",             
    "models/gemini-3-pro-image",     
    "models/gemini-2.5-pro",           
    "models/gemini-2.0-flash-exp"       
]

client = genai.Client(api_key=settings.GEMINI_API_KEY)


def fetch_page_text(url: str) -> str:
    try:
        response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=10,
        )
        response.raise_for_status()
    except:
        return "None"

    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text(separator="\n", strip=True)[:35000]


def ai_summarizer(url: str,i=0) -> str:
    if i >= len(GEMINI_MODELS):
        raise ValueError("All Model Rate limit is exceded")
    page_text = fetch_page_text(url)
    if page_text is "None":
        return "Not summarize  content of this url"
    prompt = f"""
You are given the following webpage content:

{page_text}

Give a **200-word summary** explaining:
- What level of experience is required
- What types of projects can be built
- Basic beginner-level understanding

Write clearly and simply.
"""
    response = None
    try:
       response = client.models.generate_content(
        model=GEMINI_MODELS[i],
        contents=prompt,
      )
       return str(response.text)
    except:
        return ai_summarizer(url,i+1)


def ask_question(question: str, resource_id: int,i=0) -> str:
    resource = Resource.objects.filter(id=resource_id).first()
    if not resource:
        raise ValueError("RESOURCE_NOT_FOUND")

    ai_summary_obj = Ai_summary.objects.filter(resource=resource).first()
    stored_summary = ai_summary_obj.summary if ai_summary_obj else ""

    page_text = fetch_page_text(resource.url)

    prompt = f"""
    You are given the following webpage content:

         {page_text}

         Existing summary:
         {stored_summary}

         User question:
         {question}

         Answer clearly and simply.
         """

    try:
        response = client.models.generate_content(
            model=GEMINI_MODELS[i],
            contents=prompt,
        )
        return str(response.text)

    except Exception:
        return ask_question(question, resource_id,i+1)
