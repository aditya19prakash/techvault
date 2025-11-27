🚀 TechVault — AI-Enhanced Technical Resource Sharing Platform

TechVault is a modern, scalable, AI-powered resource-sharing platform built using Django, DRF, MySQL, and Google Gemini.
It enables developers to share useful resources, interact via comments and votes, and get AI-generated summaries & answers.

TechVault now includes full JWT Authentication using SimpleJWT, making it suitable for production-ready API development.

✨ Key Features
🔐 User Management + JWT Auth

Fully implemented JWT Authentication (Access & Refresh Tokens)

Login, Logout (token blacklisting), and Token Refresh endpoints

Role-based access: User, Moderator, Admin

Protected routes using IsAuthenticated

📚 Resource Management

Add technical resources (title, URL, category, description, tech stack)

Unique tech stack counting & grouping

Automatic view counter

Clean serializer-driven validation

👍 Voting System

Upvote/downvote for:

Resources

Comments

Prevents duplicate voting (one vote per user per item)

💬 Nested Comments

First-level comments + unlimited nested replies

Vote tracking per comment

🤖 AI Integration (Gemini)

Auto webpage summaries using Gemini 2.5 Flash

Ask-AI feature using Gemini Pro

Smart caching using rapidfuzz (prevents repeated API calls)

Saves summaries + AI answers into the database

📊 Statistics

Resource views tracking

Tech stack grouping API

Vote counts from SQL aggregation

🛠️ Tech Stack
Layer	Technology
Backend	Django 5.x
API	Django REST Framework
Auth	JWT (SimpleJWT)
Database	MySQL
AI/LLM	Google Gemini API
Scraping	Requests + BeautifulSoup
Fuzzy Match	rapidfuzz
🔑 JWT Authentication Endpoints Added
Method	Endpoint	Description
POST	/login/	Generate Access & Refresh tokens
POST	/logout/	Blacklist refresh token (logout)
POST	/refresh/	Generate new access token using refresh token
GET	/	Get all users (protected)

JWT now protects routes using:

@permission_classes([IsAuthenticated])


Logout uses blacklist:

token = RefreshToken(refresh_token)
token.blacklist()

📦 Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/aditya19prakash/techvault.git
cd techvault

2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Environment Variables

Create a .env file:

GEMINI_API_KEY=YOUR_KEY
SECRET_KEY=django-secret

🗄️ Database Setup (MySQL)
CREATE DATABASE techvault;


Update settings.py:

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

Run Migrations
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

▶️ Run Server
python manage.py runserver


API Base: http://127.0.0.1:8000/

📡 API Endpoints Overview
👤 Users + JWT
Method	Endpoint	Description
GET	/	Get all users (JWT protected)
POST	/login/	Login (get access + refresh token)
POST	/logout/	Logout (blacklist token)
POST	/refresh/	Refresh access token
📚 Resources
Method	Endpoint	Description
GET/POST	/resources/	List + create resources
GET/PUT/DELETE	/resources/<id>/	Single resource operations
GET	/resources/techstack/	Group by tech stack
👍 Voting
Method	Endpoint	Description
PUT	/resources/<id>/vote/	Vote resource
PUT	/resources/<id>/comments/vote/	Vote comment
💬 Comments
Method	Endpoint	Description
GET/POST	/resources/<id>/comments/	Add/get comments
POST	/resources/<id>/comments/<comment_id>/reply/	Nested reply
🤖 AI Service
Method	Endpoint	Description
GET	/resources/<id>/summary/	Auto AI summary
POST	/resources/<id>/ask-ai/	Ask question → AI answer
🧠 AI Workflow
1️⃣ Automatic Summaries

Scrapes webpage using requests

Cleans content with BeautifulSoup

Sends to Gemini Flash

Saves summary in DB (Ai_summary table)

2️⃣ Ask-AI Feature

Searches previous answers using rapidfuzz

If similarity ≥ 80% → returns cached answer

Otherwise → uses Gemini Pro and stores result

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

Steps:

Fork repo

Create feature branch

Commit changes

Open PR