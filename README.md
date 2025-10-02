# To-Do App

Full-stack task manager built with a FastAPI backend and a Vue 3 (Vite) frontend. Users can register, log in, and manage their personal to-do list with create, edit, bulk-complete, and delete actions.

## Features

- User registration, login, and token-based session persistence (`backend/app/endpoints/user_ep.py`).
- Task creation, editing, completion, and deletion with ownership checks (`backend/app/endpoints/task_ep.py`).
- Bulk mark-as-complete and delete-completed utilities (`frontend/src/components/ToDoCard.vue`).
- Persisted auth state with Pinia + localStorage (`frontend/src/stores/authStore.js`).
- Toast notifications and simple validation flows on the client.

## Tech Stack

- **Frontend:** Vue 3, Vite, Pinia, Vue Router, VeeValidate, Tailwind utility classes, Axios, Vue Toastification.
- **Backend:** FastAPI, SQLAlchemy, Alembic, PostgreSQL, Passlib for hashing, JWT via python-jose.
- **Tooling:** Node >= 18, npm >= 9, Python >= 3.11.

## Project Structure

```
backend/
  app/
    core/
    crud/
    endpoints/
    models/
    schemas/
  alembic/
  requirements.txt
  .env.template
frontend/
  src/
    components/
    pages/
    routes/
    services/
    stores/
  package.json
  .env.template
```

## Prerequisites

- Python 3.11+
- Node.js 18+ and npm 9+
- PostgreSQL database instance.
- Optional: virtualenv/venv and `alembic` CLI.

## Backend Setup

1. Copy `.env.template` to `.env` and fill in the values:

   ```env
   DATABASE_URL=postgres:postgres@localhost:5432/todo_db
   BACKEND_CORS_ORIGINS=http://localhost:5173
   SECRET_KEY=change-me
   ALGORITHM=HS256
   ```

2. Install dependencies:

   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Apply migrations:

   ```bash
   alembic upgrade head
   ```

4. Run the API:

   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   Swagger UI is available at `http://localhost:8000/docs`.

## Frontend Setup

1. Copy `.env.template` to `.env`:

   ```env
   VITE_BASE_URL=http://localhost:8000
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Run the dev server:

   ```bash
   npm run dev
   ```

   The app runs on `http://localhost:5173` by default.

## Running the Full Stack

- Start the FastAPI server (`uvicorn ...`) in one terminal.
- Start the Vite dev server (`npm run dev`) in another.
- Navigate to `http://localhost:5173`, register, and log in to begin managing tasks.

## API Overview

| Method | Endpoint                     | Description                        | Auth |
|--------|------------------------------|------------------------------------|------|
| POST   | /auth/create                 | Register a new user                | No   |
| POST   | /auth/token                  | Obtain JWT access token            | No   |
| GET    | /auth/me                     | Retrieve current user profile      | Yes  |
| POST   | /tasks/create                | Create a task                      | Yes  |
| GET    | /tasks/                      | List all tasks (admin/debug)       | No   |
| GET    | /tasks/get-from-user/{id}    | List tasks for the current user    | Yes  |
| PUT    | /tasks/update/{task_id}      | Update a task                      | Yes  |
| DELETE | /tasks/delete/{task_id}      | Delete a task                      | Yes  |
| DELETE | /tasks/delete_completed      | Bulk delete completed tasks        | Yes  |
| GET    | /health                      | Health check                       | No   |

> Endpoints marked "Yes" require an `Authorization: Bearer <token>` header obtained via `/auth/token`.

## Database Migrations

- Create a migration after model changes:

  ```bash
  alembic revision --autogenerate -m "describe change"
  alembic upgrade head
  ```

- The migration scripts live in `backend/alembic/versions/`.

## Testing & Troubleshooting

- Automated tests are not yet configured; consider adding PyTest coverage for the API and component/integration tests for the UI.
- Ensure CORS origins in `.env` matches the frontend URL to avoid blocked requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

