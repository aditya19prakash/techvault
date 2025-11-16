🚀 TechVault — AI-Enhanced Technical Resource Sharing Platform

TechVault is a modern, scalable resource-sharing and knowledge discovery platform built with Django REST Framework.
It enables developers to share helpful technical resources, collaborate through comments and votes, and leverage AI-powered summarization and Q&A using Google Gemini.

TechVault is designed for performance, clean architecture, and extensibility, making it ideal for both learning and real-world use.

✨ Key Features
🔐 User Management

Role-based access: User, Moderator, Admin

JWT-ready authentication design (can be added easily)

Secure resource interactions

📚 Resource Sharing

Add resources with title, URL, category, description, and tech stack

Automatic view counter

Tech stack grouping statistics (e.g., Python: 14 resources)

👍 Voting System

Upvote/downvote support for:

Resources

Individual comments

Prevents duplicate voting per user

💬 Comments + Nested Replies

First-level comments

Unlimited nested replies

Vote tracking for each comment

🤖 AI Integration (Gemini)

Built using Google Gemini 2.5 Flash & Pro

📝 Automatic Resource Summaries

Scrapes webpage content

Generates 200-word AI summaries

Saves/updates summary in DB

❓ Ask-AI Feature

Users can ask questions about the resource content

AI answers using Gemini Pro

Smart caching using rapidfuzz similarity matching

Prevents repeated API calls → reduces cost

📊 Statistics

Tracks resource views

Aggregates resources by tech_stack

🛠️ Tech Stack
Layer	Technology
Backend	Django 5.x
API	Django REST Framework
Database	MySQL
AI/LLM	Google Gemini API
Web Scraping	requests, BeautifulSoup
Fuzzy Matching	rapidfuzz
Auth	Django auth (JWT-ready)
📦 Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/YOUR_USERNAME/techvault.git
cd techvault

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate     # Linux / Mac
venv\Scripts\activate        # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Configure Environment Variables

Create a .env file in your project root:

GEMINI_API_KEY="YOUR_GEMINI_KEY"

🗄️ Database Setup (MySQL)

Create a MySQL database:

CREATE DATABASE techvault;


Configure in techvault/settings.py:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'techvault',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


Run migrations:

python manage.py makemigrations
python manage.py migrate


Create superuser:

python manage.py createsuperuser

▶️ Run the Server
python manage.py runserver


API Base URL → http://127.0.0.1:8000/

📡 API Endpoints Overview
👤 User Module
Method	Endpoint	Description
POST	/user/register/	Register
POST	/user/login/	Login
GET	/user/	Get all users
📚 Resources
Method	Endpoint	Description
GET/POST	/resources/	List or create resource
GET/PUT/DELETE	/resources/<id>/	Single resource operations
GET	/resources/techstack/	Group by tech stack
👍 Votes
Method	Endpoint	Description
PUT	/resources/<id>/vote/	Upvote/Downvote resource
PUT	/resources/<id>/comments/vote/	Vote a comment
💬 Comments
Method	Endpoint	Description
GET/POST	/resources/<id>/comments/	Add or get comments
POST	/resources/<id>/comments/<comment_id>/reply/	Add nested comment
🤖 AI Service
Method	Endpoint	Description
GET	/resources/<id>/summary/	Auto summary
POST	/resources/<id>/ask-ai/	Ask a question → AI answer
🧠 AI Features Workflow
1️⃣ AI Summary Generation

Fetch HTML using requests

Parse content via BeautifulSoup

Generate summary using Gemini Flash

Save to Ai_summary table

2️⃣ AI Question Answering

Search previous questions using rapidfuzz similarity

If match ≥ 80% → return cached answer

Else → call Gemini Pro

Save result in Ai_saved_answer

This design optimizes cost, speed, and efficiency.

🧪 Testing

Run Django tests:

python manage.py test

📁 Project Structure
techvault/
│── aiservice/
│── comments/
│── resources/
│── users/
│── votes/
│── techvault/settings.py
│── techvault/urls.py
│── manage.py

🤝 Contributing

Pull requests are welcome!
Follow these steps:

Fork the repo

Create feature branch

Commit changes

Submit a PR