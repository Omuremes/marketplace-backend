from dataclasses import dataclass

@dataclass(frozen=True)
class Money:
    amount: float
    currency: str

    def to_dict(self):
        return {"amount": self.amount, "currency": self.currency}
