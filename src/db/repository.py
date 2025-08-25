from sqlalchemy import create_engine, select, update, delete
from sqlalchemy.orm import sessionmaker
from datetime import date, timedelta
from .models import Base, Account

from typing import List, Optional

class Repository:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url, connect_args={"check_same_thread": False})
        self.Session = sessionmaker(bind=self.engine, expire_on_commit=False)
        Base.metadata.create_all(self.engine)

    # --- CRUD ---
    def add_account(self, user_id: int, email: str, days_left: int) -> None:
        """
        days_left: сколько дней до обновления (N).
        date_start = today - (30 - N)  (или: date_end - 30), date_end = date_start + 30 дней.
        """
        today = date.today()
        if days_left < 0 or days_left > 31:  # sanity cap (31 день)
            raise ValueError("days_left should be >=0 and <= 31")
        date_end = today + timedelta(days=days_left)
        date_start = date_end - timedelta(days=30)
        s = self.Session()
        try:
            existing = s.get(Account, (user_id, email))
            if existing:
                raise ValueError(f"Account with email={email} already exists")
            else:
                acc = Account(
                    user_id=user_id,
                    email=email,
                    date_start=date_start.isoformat(),
                    date_end=date_end.isoformat(),
                    is_used=0,
                )
                s.add(acc)
            s.commit()
        finally:
            s.close()

    def list_accounts(self, user_id: int) -> List[Account]:
        s = self.Session()
        try:
            q = s.query(Account).filter_by(user_id=user_id).order_by(Account.date_end.asc())
            return q.all()
        finally:
            s.close()

    def mark_used(self, user_id: int, email: str) -> bool:
        s = self.Session()
        try:
            acc = s.get(Account, (user_id, email))
            if not acc:
                return False
            acc.is_used = 1
            s.commit()
            return True
        finally:
            s.close()

    def delete_account(self, user_id: int, email: str) -> bool:
        s = self.Session()
        try:
            acc = s.get(Account, (user_id, email))
            if not acc:
                return False
            s.delete(acc)
            s.commit()
            return True
        finally:
            s.close()

    def find_free(self, user_id: int) -> Optional[Account]:
        s = self.Session()
        try:
            q = s.query(Account).filter_by(user_id=user_id, is_used=0).order_by(Account.date_end.asc()).limit(1)
            res = q.first()
            return res
        finally:
            s.close()

    def refresh_expired(self) -> int:
        """
        Проходится по всем записям, у которых date_end <= today.
        Для каждой такой записи:
            - is_used := 0
            - date_start := today
            - date_end := today + 30 days
        Возвращает количество обновлённых записей.
        """
        s = self.Session()
        try:
            today = date.today()
            accounts = s.query(Account).filter(Account.date_end < today.isoformat()).all()
            updated = 0
            for acc in accounts:
                acc.is_used = 0
                acc.date_start = today.isoformat()
                acc.date_end = (today + timedelta(days=30)).isoformat()
                updated += 1
            s.commit()
            return updated
        finally:
            s.close()
