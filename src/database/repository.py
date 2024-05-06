from sqlalchemy import insert, update, delete, select

from .db import Balance, Category, Transaction, session_factory


class BalanceRepository:

    @classmethod
    def insert(cls) -> None:
        """
        Функция для добавления записи в таблицу balance.
        Применяется единожды (при отсутствии файла wallet.db).
        """
        with session_factory() as session:
            balance = Balance()
            session.add(balance)
            session.commit()

    @classmethod
    def update(cls, money: float) -> None:
        """Функция для изменения баланса"""
        with session_factory() as session:
            balance = session.get(Balance, 1)
            balance.balance += money
            session.commit()

    @classmethod
    def get(cls) -> float:
        """Функция для получения баланса"""
        with session_factory() as session:
            stmt = select(Balance).filter_by(id=1)
            balance = session.execute(stmt).scalar_one()
            return balance.balance

class TransactionRepository:

    @classmethod
    def find_all(cls, limit: int = 5, offset: int = 0, **filters) -> list[list]:
        """Функция взятия списка транзакций из БД, предварительно отфильтрованных"""
        with session_factory() as session:
            stmt = select(Transaction).filter_by(**filters).limit(limit).offset(offset)
            transactions = session.execute(stmt).scalars().all()
            return [[tr.id, tr.created_at, tr.sum, tr.description] for tr in transactions]
        
    @classmethod
    def add_one(cls, **values) -> None:
        """Функция добавления транзакции в БД"""
        with session_factory() as session:
            balance = session.get(Balance, 1)
            balance.balance += values["sum"] if values["category"] == Category.income.value else -values["sum"]
            session.execute(insert(Transaction).values(**values))
            session.commit()

    @classmethod
    def find_one(cls, id: int) -> list:
        """Функция взятия транзакции из БД по id"""
        with session_factory() as session:
            stmt = select(Transaction).filter_by(id=id)
            tr = session.execute(stmt).scalar_one_or_none()
            return [tr.id, tr.created_at, tr.sum, tr.description]
        
    @classmethod
    def pop(cls, id: int) -> None:
        """Функция удаления транзакции из БД по id"""
        with session_factory() as session:
            category = session.get(Transaction, id).category.value
            summa = TransactionRepository.find_one(id=id)[2]
        
            balance = session.get(Balance, 1)
            balance.balance -= summa if category == Category.income.value else -summa

            session.execute(delete(Transaction).where(Transaction.id == id))
            session.commit()

    @classmethod
    def change_data(cls, id: int, **values) -> None:
        """Функция изменения данных транзакции по id"""
        if values == {}:
            return 
        with session_factory() as session:
            trans = session.get(Transaction, id)

            changed_sum = values.get("sum", None)
            if changed_sum:
                balance = session.get(Balance, 1)
                if trans.sum > changed_sum:
                    balance.balance -= trans.sum - changed_sum if trans.category.value == Category.income.value else changed_sum - trans.sum
                else:                  
                    balance.balance += changed_sum - trans.sum if trans.category.value == Category.income.value else trans.sum - changed_sum

            stmt = update(Transaction).where(Transaction.id == id).values(**values)
            session.execute(stmt)
            session.commit()