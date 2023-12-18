from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine("postgresql://postgres:12345@localhost/modul5", echo=True)

Base = declarative_base()
metadata = Base.metadata
Session = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = 'user_table'
    id = Column(Integer, primary_key=True)
    user_telegram_id = Column(String, unique=True)
    username = Column(String)
    created = Column(DateTime)


class Message_(Base):
    __tablename__ = 'user_message'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    created = Column(DateTime)
    user_id = Column(String, ForeignKey('user_table.user_telegram_id'))  # userdagi id ga foregn qilingan


Base.metadata.create_all(engine)
