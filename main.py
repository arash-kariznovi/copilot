import os
from datetime import datetime, timedelta, timezone

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

app = FastAPI(title="FastAPI Server")

SECRET_KEY = os.getenv("AUTH_SECRET_KEY", "development-only-change-me")
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30
DEMO_USERNAME = "admin"
DEMO_PASSWORD = "admin"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/", response_model=dict[str, str])
async def read_root() -> dict[str, str]:
    return {"message": "Hello, World!"}


@app.get("/health", response_model=dict[str, str])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/auth", response_class=HTMLResponse)
async def auth_page() -> str:
    return """<!doctype html>
<html lang="en">
  <head><meta charset="utf-8"><title>Sign in</title></head>
  <body>
    <main>
      <h1>Sign in</h1>
      <form action="/token" method="post">
        <label>Username <input name="username" required></label><br>
        <label>Password <input name="password" type="password" required></label><br>
        <button type="submit">Sign in</button>
      </form>
    </main>
  </body>
</html>"""


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> dict[str, str]:
    if form_data.username != DEMO_USERNAME or form_data.password != DEMO_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    expires_at = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    token = jwt.encode(
        {"sub": form_data.username, "exp": expires_at}, SECRET_KEY, algorithm=ALGORITHM
    )
    return {"access_token": token, "token_type": "bearer"}


async def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
    except JWTError as exc:
        raise credentials_error from exc
    if username != DEMO_USERNAME:
        raise credentials_error
    return username


@app.get("/protected", response_model=dict[str, str])
async def protected_route(username: str = Depends(get_current_user)) -> dict[str, str]:
    return {"message": f"Welcome, {username}!"}
