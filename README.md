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
