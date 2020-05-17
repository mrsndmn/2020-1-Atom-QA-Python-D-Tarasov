
from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'test_users'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, autoincrement=True)
    username = Column(String(16))
    password = Column(String(255), nullable=False)
    email = Column(String(64), nullable=False)
    access = Column(Boolean)
    active = Column(Boolean)
    start_active_time = Column(Date)

    def __repr__(self):
        return f"<User(" \
                f"id='{self.id}'" \
                f"username='{self.username}'" \
                f"password='{self.password}'" \
                f"email='{self.email}'" \
                f"access='{self.access}'" \
                f"active='{self.active}'" \
                f"start_active_time='{self.start_active_time}'" \
               f")>"


