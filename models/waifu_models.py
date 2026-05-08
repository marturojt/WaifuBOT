from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Users(Base):
    __tablename__ = "tb_users"

    idUser = Column(Integer, primary_key=True)
    name = Column(String(length=255))
    telegram_id = Column(String(length=255), index=True)
    email = Column(String(length=255))
    waifu_name = Column(String(length=255))
    selected_waifu_role = Column(Integer)
    # Voice
    voice_enabled = Column(Boolean, default=False)
    voice_style = Column(String(length=20), default='nova')
    # Selfie
    appearance_description = Column(Text)
    # Proactive messages
    last_active = Column(DateTime)
    proactive_enabled = Column(Boolean, default=True)


class ChatLog(Base):
    __tablename__ = "tb_chat_log"

    idChatLog = Column(Integer, primary_key=True)
    relIdUser = Column(Integer, index=True)
    text = Column(Text)
    timestamp = Column(String(length=50))


class WaifuRoles(Base):
    __tablename__ = "tb_waifu_roles"

    idWaifuRole = Column(Integer, primary_key=True)
    WaifuRole = Column(Text)
    WaifuRoleDescription = Column(String(length=255))


class MemorySummary(Base):
    __tablename__ = "tb_memory_summaries"

    idSummary = Column(Integer, primary_key=True)
    relIdUser = Column(Integer, index=True)
    summary = Column(Text)
    period_start = Column(DateTime)
    period_end = Column(DateTime)
    created_at = Column(DateTime)


class RelationshipState(Base):
    __tablename__ = "tb_relationship_state"

    idRelationship = Column(Integer, primary_key=True)
    relIdUser = Column(Integer, index=True, unique=True)
    total_messages = Column(Integer, default=0)
    first_interaction = Column(DateTime)
