from datetime import datetime
from sqlalchemy import select, Table, Column, Integer, String, MetaData, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    telegram_id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=True)
    balance = Column(Integer, default=0)
    is_blocked = Column(Boolean, default=False)

    def __repr__(self):
        user = self.username if self.username else self.telegram_id
        return f"<User {user}>"

    def __str__(self):
        user = self.username if self.username else self.telegram_id
        return f'Пользователь {user}'


class Payments(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True)
    qiwi_id = Column(String)
    telegram_id = Column(Integer, ForeignKey('user.telegram_id'))
    datetime = Column(DateTime, default=datetime.now())
    amount = Column(Integer)
    is_completed = Column(Boolean, default=False)

    def __str__(self):
        return f'qiwi_id={self.qiwi_id}, сумма={self.amount}'


