import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timezone, timedelta

from config import SECRET_KEY, ALGORITHM, TOKEN_FILE, ACCESS_TOKEN_EXPIRE_MINUTES


def create_token(data: dict) -> None:
    """Create a JWT token with the given data."""
    if TOKEN_FILE.exists():
        TOKEN_FILE.unlink()
    token = jwt.encode({
        "email": data.email,
        "password": data.hashed_password,
        "role": data.role,
        "exp": datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        }, SECRET_KEY, algorithm=ALGORITHM)
    with open(TOKEN_FILE, 'w') as token_file:
        token_file.write(token)

def load_token() -> str:
    """Load the JWT token from a file."""
    if not TOKEN_FILE.exists():
        raise Exception("You must log in first.")
    with open(TOKEN_FILE, 'r') as token_file:
        token = token_file.read().strip()
    if not token:
        raise Exception("Token file is empty. You must log in first.")
    return token

def decode_token(token: str) -> dict:
    """Decode the JWT token and return its payload."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        TOKEN_FILE.unlink(missing_ok=True)  # Clear token file if expired
        raise Exception("Token has expired. Please log in again.")
    except InvalidTokenError:
        raise Exception("Invalid token. Please log in again.")

def clear_token() -> None:
    """Clear the JWT token by deleting the token file."""
    if TOKEN_FILE.exists():
        TOKEN_FILE.unlink()
    else:
        raise Exception("No token file found to clear.")
