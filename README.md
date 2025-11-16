# TechVault

TechVault is a modern, full-featured **resource-sharing platform** built with **Django Rest Framework**. It allows a community of users to share technical articles, tutorials, and resources. Key features include user authentication, a voting system, nested comments, and advanced **AI integration** for content summarization and question answering.

## Features

* **User Management**: Includes distinct roles (`User`, `Moderator`, `Admin`) for tailored access and permissions.
* **Resource Sharing**: Users can post technical resources with a title, URL, description, category, and relevant tech stack.
* **Voting System**: Users can upvote or downvote both resources and individual comments.
* **Commenting**: Supports primary comments and nested replies on resources.
* **AI Integration**: An `aiservice` provides powerful functionality for:
    * **Resource Summarization**: Automatically generates a 200-word summary of linked web content when a resource is viewed (using `models/gemini-2.5-flash`).
    * **Question Answering**: Users can ask specific questions about a resource, and the AI will provide an answer, with a caching mechanism to save and reuse similar responses.
* **Statistics**: Tracks resource views and groups resources by `tech_stack`.

***

## Tech Stack

* **Backend Framework**: Django 5.1.6
* **API**: Django Rest Framework (DRF)
* **Database**: MySQL
* **AI/LLM**: Google Gemini API (`models/gemini-2.5-flash` and `models/gemini-2.5-pro`)
* **Web Scraping**: `requests` and `BeautifulSoup` (`bs4`) for fetching and parsing resource URLs
* **Fuzzy Matching**: `rapidfuzz` for finding similar cached questions in the AI service

***

## Installation and Setup

### 1. Prerequisites

* Python (3.x recommended)
* MySQL Server

### 2. Database Configuration

The project is configured to use a **MySQL** database.

1.  Create a database named `techvault` in your MySQL server.
2.  Update the `DATABASES` setting in `techvault/settings.py` if your credentials differ from the defaults:
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME':'techvault',
            'USER':'root',
            'PASSWORD':'root',
            'HOST':'localhost',
            'PORT':'3306',
        }
    }
    ```

### 3. Environment Variables

Create a `.env` file in your project root to store sensitive information. The project requires the following environment variables (which are loaded in `techvault/settings.py`):

````

GEMINI_API\_KEY="YOUR\_GEMINI_API_KEY"



`

### 4. Setup and Run

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt # Assuming you have a requirements file
    # Or manually install packages based on imports:
    # pip install django djangorestframework mysqlclient python-dotenv google-genai requests beautifulsoup4 rapidfuzz
    ```

2.  **Run migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

3.  **Create a superuser:** (For accessing the Django Admin)
    ```bash
    python manage.py createsuperuser
    ```

4.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

The API will be available at `http://127.0.0.1:8000/`.

***

## API Endpoints (Excerpt)

The main API paths are defined in `techvault/urls.py` and connected through app-level `urls.py` files:

| Path | App | Description |
| :--- | :--- | :--- |
| `/user/` | `users` | User registration and retrieval |
| `/resources/` | `resources` | List all resources or create a new one |
| `/resources/<int:id>/` | `resources` | Retrieve/Update a specific resource, includes voting and AI summary logic |
| `/resources/<int:id>/comments/` | `comments` | List and post top-level comments for a resource |
| `/resources/<int:id>/ask-ai/` | `aiservice` | Ask a question about the resource's content |
| `/resources/techstack/` | `resources` | Get a count of resources per tech stack |
````