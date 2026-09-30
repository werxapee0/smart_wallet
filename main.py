import sys
from wallet import Wallet


def print_divider(char="=", lenght=50):
    print(char * lenght)


def get_float_input(prompt: str) -> float:
    while True:
        try:
            val = float(input(prompt).replace(",", ".").strip())
            if val <= 0:
                print("⚠️ Сумму необходимо ввести больше 0. Попробуйте снова.")
                continue
            return val
        except ValueError:
            print("⚠️ Ошибка: введите числовое значение (например, 250 или 640.50).")


def get_non_empty_string(prompt: str) -> str:
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print("⚠️ Это поле не может быть пустым. Попробуйте снова.")


def show_balance(wallet: Wallet):
    balance_info = wallet.get_balance()
    print_divider()
    print("💰 ТЕКУЩИЙ БАЛАНС")
    print_divider("-")
    print(f"  🟢 Всего доходов : +{balance_info['income']:,.2f} ₽")
    print(f"  🔴 Всего расходов: -{balance_info['expense']:,.2f} ₽")
    print_divider("-")
    balance = balance_info["balance"]
    prefix = "+" if balance >= 0 else ""
    print(f"  💼 ЧИСТЫЙ ИТОГ   : {prefix}{balance:,.2f} ₽")
    print_divider()


def add_transaction_flow(wallet: Wallet, t_type: str):
    title = "ДОХОДА" if t_type == "income" else "РАСХОДА"
    print_divider()
    print(f"➕ ДОБАВЛЕНИЕ {title}")
    print_divider("-")

    amount = get_float_input("Введите сумму (₽): ")
    category = get_non_empty_string("Введите категорию (например, Еда, Зарплата, Такси): ")
    description = input("Описание / комментарий (опционально): ").strip()

    t = wallet.add_transaction(t_type, amount, category, description)
    print(f"\n✅ Успешно добавлено: {t}")


def list_transactions_flow(wallet: Wallet):
    print_divider()
    print("📜 ИСТОРИЯ ОПЕРАЦИЙ")
    print("  1. Показать все операции")
    print("  2. Только доходы")
    print("  3. Только расходы")
    print("  4. Фильтр по названию категории")
    print_divider("-")
    choice = input("Выберите вариант (1-4): ").strip()

    t_type = None
    category = None

    if choice == "2":
        t_type = "income"
    elif choice == "3":
        t_type = "expense"
    elif choice == "4":
        category = get_non_empty_string("Введите название категории: ")

    transactions = wallet.get_transactions(t_type=t_type, category=category)

    if not transactions:
        print("\n📭 Записей по вашему запросу не найдено.")
        return

    print_divider("-")
    for t in transactions:
        print(t)
    print_divider()
    print(f"Всего найденных записей: {len(transactions)}")


def show_statistics_flow(wallet: Wallet):
    print_divider()
    print("📊 СТАТИСТИКА РАСХОДОВ ПО КАТЕГОРИЯМ")
    print_divider("-")

    stats = wallet.get_category_stats(t_type="expense")
    total_expense = sum(stats.values())

    if not stats or total_expense == 0:
        print("📭 Нет данных о расходах для построения статистики.")
        return

    for cat, amount in sorted(stats.items(), key=lambda x: x[1], reverse=True):
        percent = (amount / total_expense) * 100
        print(f"  • {cat:<15}: {amount:>10.2f} ₽ ({percent:>5.1f}%)")
    print_divider("-")
    print(f"  ИТОГО РАСХОДОВ  : {total_expense:>10.2f} ₽")


def delete_transaction_flow(wallet: Wallet):
    print_divider()
    print("❌ УДАЛЕНИЕ ЗАПИСИ")
    print_divider("-")

    try:
        t_id = int(input("Введите ID записи для удаления: ").strip())
    except ValueError:
        print("⚠️ Ошибка: ID должен быть целым числом.")
        return

    if wallet.delete_transaction(t_id):
        print(f"✅ Запись с ID {t_id} успешно удалена.")
    else:
        print(f"⚠️ Запись с ID {t_id} не найдена.")



def main():
    wallet = Wallet()

    menu = """
==================================================
           💼 УМНЫЙ КОШЕЛЕК (CLI)
==================================================
  1. 💰 Посмотреть баланс
  2. ➕ Добавить доход
  3. ➖ Добавить расход
  4. 📜 История операций (с фильтрами)
  5. 📊 Статистика по категориям
  6. ❌ Удалить запись
  0. 🚪 Выйти
--------------------------------------------------"""

    while True:
        print(menu)
        choice = input("Выберите действие (0-6): ").strip()

        if choice == "1":
            show_balance(wallet)
        elif choice == "2":
            add_transaction_flow(wallet, "income")
        elif choice == "3":
            add_transaction_flow(wallet, "expense")
        elif choice == "4":
            list_transactions_flow(wallet)
        elif choice == "5":
            show_statistics_flow(wallet)
        elif choice == "6":
            delete_transaction_flow(wallet)
        elif choice == "0":
            print("\n👋 Спасибо за использование Smart Wallet. До свидания!")
            sys.exit(0)
        else:
            print("⚠️ Неизвестная команда. Введите цифру от 0 до 6.")

if __name__ == "__main__":
    main()