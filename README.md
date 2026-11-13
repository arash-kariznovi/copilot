# FastAPI Server

## Run locally

Install dependencies and start the development server:

```bash
python3 -m pip install -r requirements.txt
python3 -m uvicorn main:app --reload
```

The server runs at <http://127.0.0.1:8000>. Interactive API documentation is available at <http://127.0.0.1:8000/docs>.

## Endpoints

- `GET /` returns a greeting.
- `GET /health` returns the server health status.
- `GET /auth` serves the sign-in page.
- `POST /token` accepts the login form and returns a JWT.
- `GET /protected` requires a bearer token.

## Authentication

The local demo credentials are `admin` / `admin`. Set `AUTH_SECRET_KEY` to a strong secret before using this outside local development.

After signing in, send the returned token as an `Authorization: Bearer <token>` header when calling `/protected`.
