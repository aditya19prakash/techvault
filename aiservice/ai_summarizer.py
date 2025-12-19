import requests
from bs4 import BeautifulSoup
from django.conf import settings
from google import genai

from aiservice.models import Ai_summary
from resources.models import Resource


# ============================================================
# Gemini Client (NEW SDK – REQUIRED)
# ============================================================

client = genai.Client(api_key=settings.GEMINI_API_KEY)


# ============================================================
# Utility: Fetch webpage text safely
# ============================================================

def fetch_page_text(url: str) -> str:
    """
    Fetch webpage content and extract visible text.
    Limits size to avoid token overflow.
    """
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


# ============================================================
# Generate AI Summary for a Resource URL
# ============================================================

def ai_summarizer(url: str) -> str:
    """
    Generates a 200-word beginner-friendly summary
    for the given resource URL.
    """

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

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return str(response.text)


# ============================================================
# Ask a Question about a Resource (with fallback logic)
# ============================================================

def ask_question(question: str, resource_id: int) -> str:
    """
    Answers a user question based on:
    - Webpage content
    - Stored AI summary (if exists)
    """

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
        # Primary (higher quality)
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=prompt,
        )
        return str(response.text)

    except Exception:
        # Fallback (faster & cheaper)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return str(response.text)
