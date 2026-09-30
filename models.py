from datetime import datetime


class Transaction:
    """ Класс, описывающий отдельную финансовую операцию (доход или расход). """

    def __init__(
        self,
        transaction_id: int,
        transaction_type: str,
        amount: float,
        category: str,
        description: str = "",
        date: str = None
    ):
        self.id = transaction_id
        self.type = transaction_type.lower()
        self.amount = float(amount)
        self.category = category.strip()
        self.description = description.strip()
        self.date = date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> dict:
        """ Превращает объект в словарь для сохранения в JSON. """
        return {
            "id": self.id,
            "type": self.type,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date
        }

    @classmethod
    def from_dict(cls, data: dict):
        """ Создает объект Transaction из словаря, загруженного из JSON. """
        return cls(
            transaction_id=data["id"],
            transaction_type=data["type"],
            amount=data["amount"],
            category=data["category"],
            description=data.get("description", ""),
            date=data.get("date")
        )

    def __str__(self) -> str:
        symbol = "+" if self.type == "income" else "-"
        return f"[{self.date}] ID:{self.id} | {symbol}{self.amount:,.2f} ₽ | {self.category} ({self.description})"