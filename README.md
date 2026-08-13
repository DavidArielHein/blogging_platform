# Personal Blogging Platform

API for managing posts in a personal blog. It allows you to create, list, search, update, and delete posts using FastAPI and SQLite.

Project link: https://roadmap.sh/projects/blogging-platform-api

---

## Description

This application exposes a REST API for managing content in a personal blog. Each post includes:

- title
- content
- category
- tags
- creation and update dates

The API is built with FastAPI and stores data in SQLite using SQLAlchemy.

---

## Requirements

- Python 3.10 or higher
- pip
- virtual environment recommended

---

## How to download the project

```bash
git clone https://github.com/your-username/blogging_platform.git
cd blogging_platform
```

If the project is already downloaded on your local machine, simply open the folder:

```bash
cd /path/to/project/blogging_platform
```

---

## How to install and use

1. Create the virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -e .
```

3. Run the API:

```bash
uvicorn src.main:app --reload
```

The API will be available at:

- http://127.0.0.1:8000
- Interactive documentation: http://127.0.0.1:8000/docs
- Alternative documentation: http://127.0.0.1:8000/redoc

---

## How the API works

The API is used to manage personal blog content from an HTTP client. You can make requests using tools such as:

- curl
- Postman
- Thunder Client
- browser with Swagger documentation

---

## Endpoints

### GET /

Returns a welcome message from the API.

```json
"Welcome to the API of your personal blog!"
```

### GET /posts

Lists all available posts.

It also accepts an optional search parameter:

```bash
GET /posts?term=python
```

This filter searches for matches in `title`, `content`, and `category`.

### GET /posts/{post_id}

Gets a specific post by its ID.

If it does not exist, it returns a 404 error.

### POST /posts

Creates a new post.

Example body:

```json
{
  "title": "My first post",
  "content": "This is the content of my publication.",
  "category": "Technology",
  "tags": ["python", "api", "fastapi"]
}
```

### PUT /posts/{post_id}

Updates an existing post by its ID.

The same body format as `POST` is used, but only the sent fields will be modified.

### DELETE /posts/{post_id}

Deletes a post by its ID.

Returns a 204 status code with no content if deleted successfully.

---

## Notes

- The database is stored in `src/database.db`.
- When the application starts, FastAPI creates the tables automatically if they do not exist.
- The API includes automatic Swagger documentation at `/docs`.
