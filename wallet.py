from models import Transaction
from storage import FileStorage


class Wallet:
    """ Основной класс управления кошельком (бизнес-логика). """

    def __init__(self, storage: FileStorage = None):
        self.storage = storage or FileStorage()
        self.transactions: list[Transaction] = []
        self._load_transactions()

    def _load_transactions(self) -> None:
        raw_data = self.storage.load_data()
        self.transactions = [Transaction.from_dict(item) for item in raw_data]

    def _save_transactions(self) -> None:
        raw_data = [t.to_dict() for t in self.transactions]
        self.storage.save_data(raw_data)

    def _generate_id(self) -> int:
        if not self.transactions:
            return 1
        return max(t.id for t in self.transactions) + 1

    def add_transaction(self, t_type: str, amount: float, category: str, description: str = "") -> Transaction:
        if amount <= 0:
            raise ValueError("Сумма должна быть больше нуля!")
        if t_type not in ("income", "expense"):
            raise ValueError("Тип транзакции должен быть 'income' или 'expense'!")

        new_id = self._generate_id()
        transaction = Transaction(
            transaction_id=new_id,
            transaction_type=t_type,
            amount=amount,
            category=category,
            description=description
        )
        self.transactions.append(transaction)
        self._save_transactions()
        return transaction

    def get_balance(self) -> dict:
        total_income = sum(t.amount for t in self.transactions if t.type == "income")
        total_expense = sum(t.amount for t in self.transactions if t.type == "expense")
        return {
            "income": total_income,
            "expense": total_expense,
            "balance": total_income - total_expense
        }

    def get_transactions(self, t_type: str = None, category: str = None) -> list[Transaction]:
        result = self.transactions
        if t_type:
            result = [t for t in result if t.type == t_type]
        if category:
            result = [t for t in result if t.category.lower() == category.lower()]
        return result

    def get_category_stats(self, t_type: str = "expense") -> dict[str, float]:
        stats = {}
        for t in self.transactions:
            if t.type == t_type:
                stats[t.category] = stats.get(t.category, 0.0) + t.amount
        return stats

    def delete_transaction(self, transaction_id: int) -> bool:
        initial_length = len(self.transactions)
        self.transactions = [t for t in self.transactions if t.id != transaction_id]

        if len(self.transactions) < initial_length:
            self._save_transactions()
            return True
        return False