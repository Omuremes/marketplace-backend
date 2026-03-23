import bcrypt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Truncate plain_password to 72 bytes to match bcrypt's hard limit
    password_bytes = plain_password.encode('utf-8')[:72]
    try:
        return bcrypt.checkpw(password_bytes, hashed_password.encode('utf-8'))
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    # Truncate password to 72 bytes to match bcrypt's hard limit
    password_bytes = password.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode('utf-8')
