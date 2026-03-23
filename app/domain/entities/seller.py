from dataclasses import dataclass
import uuid

@dataclass
class Seller:
    id: str
    name: str
    email: str
    password_hash: str
    rating: float

    @classmethod
    def create(cls, name: str, email: str, password_hash: str, rating: float = 0.0) -> "Seller":
        return cls(
            id=str(uuid.uuid4()),
            name=name,
            email=email,
            password_hash=password_hash,
            rating=rating
        )
