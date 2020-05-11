from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class NginxLog(Base):
    __tablename__ = 'nginxlogs'
    __table_args__ = {'mysql_charset': 'UTF8MB4'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(64), nullable=False)
    method = Column(String(16), nullable=False)
    path = Column(String(1024), nullable=False)
    status = Column(Integer, nullable=False)
    size = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<NginxLog(" \
               f"id='{self.id}'," \
               f"ip='{self.ip}', " \
               f"method='{self.method}', " \
               f"path='{self.path}', "\
               f"status='{self.status}', " \
               f"size='{self.size}'" \
               f")>"

