import re
from .config import settings


def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Validate password strength based on security requirements.

    Args:
        password: Plain text password to validate

    Returns:
        Tuple of (is_valid, error_message)
        If valid: (True, "")
        If invalid: (False, "Error message explaining why")
    """
    if len(password) < settings.PASSWORD_MIN_LENGTH:
        return False, f"Password must be at least {settings.PASSWORD_MIN_LENGTH} characters long"

    if settings.PASSWORD_REQUIRE_UPPERCASE and not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"

    if settings.PASSWORD_REQUIRE_LOWERCASE and not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"

    if settings.PASSWORD_REQUIRE_DIGITS and not re.search(r"\d", password):
        return False, "Password must contain at least one digit"

    if settings.PASSWORD_REQUIRE_SPECIAL and not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>)"

    return True, ""


def is_strong_password(password: str) -> bool:
    """
    Check if password meets strength requirements.

    Args:
        password: Plain text password to validate

    Returns:
        True if password is strong, False otherwise

    Raises:
        ValueError: If password does not meet requirements
    """
    is_valid, error_message = validate_password_strength(password)
    if not is_valid:
        raise ValueError(error_message)
    return True
