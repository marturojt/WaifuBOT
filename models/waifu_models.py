from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Users(Base):
    __tablename__ = "tb_users"

    idUser = Column(Integer, primary_key=True)
    name = Column(String(length=255))
    telegram_id = Column(String(length=255))
    email = Column(String(length=255))


class ChatLog(Base):
    __tablename__ = "tb_chat_log"

    idChatLog = Column(Integer, primary_key=True)
    relIdUser = Column(Integer)
    text = Column(Text)
    timestamp = Column(String(length=25))


