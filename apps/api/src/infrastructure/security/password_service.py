import re

import bcrypt


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    password_bytes = plain_password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def validate_password(password: str) -> list[str]:
    """
    Validate password strength.

    Returns a list of error messages. Empty list means password is valid.

    Requirements:
    - At least 8 characters
    - At least one letter
    - At least one number
    """
    errors = []

    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")

    if not re.search(r"[a-zA-Z]", password):
        errors.append("Password must contain at least one letter")

    if not re.search(r"\d", password):
        errors.append("Password must contain at least one number")

    return errors
