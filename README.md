# FastAPI Project

This repository contains a FastAPI application with a PostgreSQL database, Alembic migrations, and tests. It provides endpoints for users, posts, votes, and authentication.

## Features

- FastAPI-based API
- SQLAlchemy ORM models
- OAuth2 authentication
- Alembic migrations for database schema
- Pytest for unit/integration tests

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL database

### Installation

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd Fastapi
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   ```
3. Configure environment variables (see `app/config.py` for required settings).

### Database

Run migrations to create the database schema:
```bash
alembic upgrade head
```

### Running the App

Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

### Testing

Execute tests with pytest:
```bash
pytest
```

### Project Structure

```
app/             - application code
  routers/       - API route definitions
  models.py      - SQLAlchemy models
  schemas.py     - Pydantic schemas
  utils.py       - utility functions
  oauth2.py      - authentication helpers
tests/           - pytest test cases
alembic/         - migration scripts
```

## Contributing

Feel free to open issues or submit pull requests.

## License

[MIT](LICENSE)
