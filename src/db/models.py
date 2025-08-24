from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Account(Base):
    __tablename__ = "accounts"
    user_id = Column(Integer, primary_key=True)
    email = Column(String, primary_key=True)  # composite PK (user_id, email)
    date_start = Column(String, nullable=False)  # YYYY-MM-DD
    date_end = Column(String, nullable=False)    # YYYY-MM-DD
    is_used = Column(Integer, nullable=False, default=0)  # 0 or 1

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "email": self.email,
            "date_start": self.date_start,
            "date_end": self.date_end,
            "is_used": bool(self.is_used),
        }
