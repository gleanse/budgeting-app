# Budgeting App (FastAPI Version)

This is the **FastAPI version** of a budgeting app built as part of a two-version comparison project. The same app will be built in both **FastAPI** and **Django REST Framework (DRF)** to document and compare the developer experience, code structure, and performance of each framework.

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
fastapi-version/
├── app/
│   ├── core/
│   │   └── auth.py
│   ├── routers/
│   │   ├── auth.py
│   │   ├── income.py
│   │   ├── expense.py
│   │   ├── category.py
│   │   └── balance.py
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── income.py
│   │   ├── expense.py
│   │   └── category.py
│   ├── models.py
│   ├── database.py
│   └── main.py
├── alembic/
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
cd budgeting-app/fastapi-version
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

## API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register` | Register a new user |
| POST | `/login` | Login and receive JWT token |
| POST | `/logout` | Logout current user |

### Category
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/categories` | List all categories |
| POST | `/categories` | Create a new category |
| DELETE | `/categories/{id}` | Delete a category |

### Income
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/incomes` | List all incomes |
| POST | `/incomes` | Create a new income record |
| DELETE | `/incomes/{id}` | Delete an income record |

### Expense
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/expenses` | List all expenses |
| POST | `/expenses` | Create a new expense record |
| DELETE | `/expenses/{id}` | Delete an expense record |

### Balance
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/balance` | Get current balance, total income, and total expenses |

---

## Interactive API Docs

FastAPI provides automatic interactive documentation out of the box:

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

## Known Limitations (v1.0.0)

- No update (PATCH/PUT) endpoints yet — coming in v1.1.0
- No pagination on list endpoints — coming in v1.1.0
- Logout is stateless (token is not blacklisted)

---

## Comparison Project

This is one of two versions of the same budgeting app:

| Version | Framework | Status |
|---------|-----------|--------|
| `fastapi-version/` | FastAPI + SQLModel | v1.0.0 |
| `drf-version/` | Django REST Framework (DRF) | Not yet started |

The goal is to compare developer experience, boilerplate, performance, and trade-offs between the two frameworks.