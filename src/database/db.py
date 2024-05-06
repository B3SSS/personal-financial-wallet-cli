from datetime import date
from enum import Enum
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


engine = create_engine(url="sqlite:///wallet.db", echo=False)
session_factory = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass

# Категория транзакции: доходы - income, расходы - expense
class Category(Enum):
    income = "income"
    expense = "expense"

# Таблица транзакций
class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[date] = mapped_column(default=date.today)
    category: Mapped[Category]
    sum: Mapped[float]
    description: Mapped[Optional[str]]
    
# Таблица текущего баланса кошелька
class Balance(Base):
    __tablename__ = "balance"

    id: Mapped[int] = mapped_column(primary_key=True)
    balance: Mapped[float] = mapped_column(default=0.00)


def create_db() -> None:
    """Функция создания БД и таблиц"""
    Base.metadata.create_all(engine)
