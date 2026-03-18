from dataclasses import dataclass
import uuid

@dataclass
class Seller:
    id: str
    name: str
    rating: float

    @classmethod
    def create(cls, name: str, rating: float) -> "Seller":
        return cls(
            id=str(uuid.uuid4()),
            name=name,
            rating=rating
        )
