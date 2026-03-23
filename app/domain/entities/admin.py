from dataclasses import dataclass
import uuid

@dataclass
class Admin:
    id: str
    email: str
    password_hash: str

    @classmethod
    def create(cls, email: str, password_hash: str) -> "Admin":
        return cls(
            id=str(uuid.uuid4()),
            email=email,
            password_hash=password_hash
        )
