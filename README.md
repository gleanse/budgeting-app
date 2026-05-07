# Budgeting App

A budgeting app API built with FastAPI and SQLModel. This project demonstrates JWT authentication, database migrations, and versioned endpoints.

> Main repo: [github.com/gleanse/budgeting-app](https://github.com/gleanse/budgeting-app)

---

## Tech Stack

- **FastAPI** - web framework
- **SQLModel** - ORM (built on SQLAlchemy + Pydantic)
- **PostgreSQL** - database
- **Alembic** - database migrations
- **Docker** - containerized database
- **python-decouple** - environment variable management
- **bcrypt** - password hashing
- **python-jose** - JWT authentication

---

## Project Structure

```
.
├── app/
│   ├── core/
│   │   ├── auth_core.py
│   │   └── dependencies.py
│   ├── routers/
│   │   └── v1/
│   ├── schemas/
│   │   └── v1/
│   ├── services/
│   │   └── v1/
│   ├── repositories/
│   ├── models.py
│   ├── database.py
│   └── main.py
├── alembic/
│   └── versions/
├── postman/
│   └── budgeting-fastapi-v1.0.0.json
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/gleanse/budgeting-app.git
cd budgeting-app
```

### 2. Create your environment file

```bash
# Linux/Mac/WSL
cp .env.example .env

# Windows
copy .env.example .env
```

Then fill in your values in `.env`:

```env
DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<database_name>
JWT_KEY=your-secret-jwt-key-here
```

### 3. Start the database

```bash
docker compose up -d
```

### 4. Create a virtual environment and install dependencies

```bash
python -m venv venv

# Linux/Mac/WSL
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

### 5. Run database migrations

```bash
alembic upgrade head
```

### 6. Start the server
```bash
# recommended
fastapi dev app/main.py

# or with uvicorn directly
uvicorn app.main:app --reload

# custom host/port if needed
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

---

## Interactive API Docs

FastAPI provides automatic interactive documentation out of the box. All endpoints are currently versioned under `/api/v1/`.

- **Swagger UI** → `http://<host>:<port>/docs`
- **ReDoc** → `http://<host>:<port>/redoc`

---

## Postman Collection

A Postman collection is included at `postman/budgeting-fastapi-v1.0.0.json`.

Import it into Postman and set up an environment with:

| Variable | Value |
|----------|-------|
| `base_url` | `http://<host>:<port>` |

The collection includes pre-request and post-response scripts that automatically handle token saving and ID tracking across requests.

---

## Testing

### Sync the test database schema

The test database (`budgeting_fastapi_db_test`) is created automatically on container init via `init.sql`. To apply migrations to it, override `DATABASE_URL` when running alembic:

```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/budgeting_fastapi_db_test alembic upgrade head
```

---

## Known Limitations (v1.0.0)

- No update (PATCH/PUT) endpoints yet — coming in v1.1.0
- No pagination on list endpoints — coming in v1.1.0
- Logout is stateless (token is not blacklisted)
