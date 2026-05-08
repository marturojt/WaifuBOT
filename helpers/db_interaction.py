import datetime
from .db_connection import SessionLocal
from models.waifu_models import Users, ChatLog, WaifuRoles, MemorySummary, RelationshipState


# USER OPERATIONS

def search_user(user_id):
    with SessionLocal() as session:
        return session.query(Users).filter(Users.telegram_id == user_id).first()

def new_user(telegram_id, name):
    with SessionLocal() as session:
        user = Users(telegram_id=telegram_id, name=name)
        session.add(user)
        session.commit()

def update_user(telegram_id, name):
    with SessionLocal() as session:
        existing_user = session.query(Users).filter(Users.telegram_id == telegram_id).first()
        if existing_user:
            existing_user.name = name
            session.commit()

def update_user_waifu_name(telegram_id, waifu_name):
    with SessionLocal() as session:
        existing_user = session.query(Users).filter(Users.telegram_id == telegram_id).first()
        if existing_user:
            existing_user.waifu_name = waifu_name
            session.commit()

def update_user_waifu_role(telegram_id, waifu_role):
    with SessionLocal() as session:
        existing_user = session.query(Users).filter(Users.telegram_id == telegram_id).first()
        if existing_user:
            existing_user.selected_waifu_role = waifu_role
            session.commit()

def update_user_last_active(telegram_id):
    with SessionLocal() as session:
        existing_user = session.query(Users).filter(Users.telegram_id == telegram_id).first()
        if existing_user:
            existing_user.last_active = datetime.datetime.now()
            session.commit()

def toggle_user_voice(telegram_id, enabled: bool):
    with SessionLocal() as session:
        existing_user = session.query(Users).filter(Users.telegram_id == telegram_id).first()
        if existing_user:
            existing_user.voice_enabled = enabled
            session.commit()

def update_user_voice_style(telegram_id, style: str):
    with SessionLocal() as session:
        existing_user = session.query(Users).filter(Users.telegram_id == telegram_id).first()
        if existing_user:
            existing_user.voice_style = style
            session.commit()

def update_user_appearance(telegram_id, description: str):
    with SessionLocal() as session:
        existing_user = session.query(Users).filter(Users.telegram_id == telegram_id).first()
        if existing_user:
            existing_user.appearance_description = description
            session.commit()

def toggle_user_proactive(telegram_id, enabled: bool):
    with SessionLocal() as session:
        existing_user = session.query(Users).filter(Users.telegram_id == telegram_id).first()
        if existing_user:
            existing_user.proactive_enabled = enabled
            session.commit()

def get_active_proactive_users(cutoff: datetime.datetime) -> list:
    """Return fully configured users with proactive enabled and inactive since cutoff."""
    with SessionLocal() as session:
        users = (
            session.query(Users)
            .filter(
                Users.proactive_enabled == True,
                Users.last_active != None,
                Users.last_active < cutoff,
                Users.name != None,
                Users.waifu_name != None,
                Users.selected_waifu_role != None,
            )
            .all()
        )
        return users


# WAIFU ROLE OPERATIONS

def get_waifu_role_by_id(waifu_role_id):
    with SessionLocal() as session:
        return session.query(WaifuRoles).filter(WaifuRoles.idWaifuRole == waifu_role_id).first()

def get_waifu_role_descriptions_with_id():
    with SessionLocal() as session:
        waifu_roles = session.query(WaifuRoles).all()
        return [[role.WaifuRoleDescription, role.idWaifuRole] for role in waifu_roles]

def get_waifu_role_descriptions():
    with SessionLocal() as session:
        waifu_roles = session.query(WaifuRoles).all()
        return [role.WaifuRoleDescription for role in waifu_roles]


# CHAT LOG OPERATIONS

def get_chat_log_user(user_id, limit: int = 50):
    with SessionLocal() as session:
        chat_log = (
            session.query(ChatLog)
            .filter(ChatLog.relIdUser == user_id)
            .order_by(ChatLog.idChatLog.desc())
            .limit(limit)
            .all()
        )
        return [[chat.text] for chat in reversed(chat_log)]

def count_chat_log_user(user_id) -> int:
    with SessionLocal() as session:
        return session.query(ChatLog).filter(ChatLog.relIdUser == user_id).count()

def get_oldest_chat_logs(user_id, limit: int):
    with SessionLocal() as session:
        chat_log = (
            session.query(ChatLog)
            .filter(ChatLog.relIdUser == user_id)
            .order_by(ChatLog.idChatLog.asc())
            .limit(limit)
            .all()
        )
        return [(chat.text, chat.idChatLog, chat.timestamp) for chat in chat_log]

def new_chat_log_entry(user_id, text, timestamp):
    with SessionLocal() as session:
        entry = ChatLog(relIdUser=user_id, text=text, timestamp=timestamp)
        session.add(entry)
        session.commit()

def delete_chat_log_user(user_id):
    with SessionLocal() as session:
        session.query(ChatLog).filter(ChatLog.relIdUser == user_id).delete()
        session.commit()

def delete_chat_logs_before_id(user_id, before_id: int):
    with SessionLocal() as session:
        session.query(ChatLog).filter(
            ChatLog.relIdUser == user_id,
            ChatLog.idChatLog <= before_id,
        ).delete()
        session.commit()


# MEMORY SUMMARY OPERATIONS

def get_memory_summaries(user_id) -> list[str]:
    with SessionLocal() as session:
        summaries = (
            session.query(MemorySummary)
            .filter(MemorySummary.relIdUser == user_id)
            .order_by(MemorySummary.period_start.asc())
            .all()
        )
        return [s.summary for s in summaries]

def save_memory_summary(user_id, summary: str, period_start, period_end):
    def _to_dt(val):
        if isinstance(val, datetime.datetime):
            return val
        try:
            return datetime.datetime.fromisoformat(str(val).split('.')[0])
        except Exception:
            return datetime.datetime.now()

    with SessionLocal() as session:
        entry = MemorySummary(
            relIdUser=user_id,
            summary=summary,
            period_start=_to_dt(period_start),
            period_end=_to_dt(period_end),
            created_at=datetime.datetime.now(),
        )
        session.add(entry)
        session.commit()

def delete_memory_summaries(user_id):
    with SessionLocal() as session:
        session.query(MemorySummary).filter(MemorySummary.relIdUser == user_id).delete()
        session.commit()


# RELATIONSHIP OPERATIONS

def get_relationship_total(user_id) -> int:
    with SessionLocal() as session:
        rel = session.query(RelationshipState).filter(RelationshipState.relIdUser == user_id).first()
        return rel.total_messages if rel else 0

def increment_relationship_messages(user_id) -> int:
    with SessionLocal() as session:
        rel = session.query(RelationshipState).filter(RelationshipState.relIdUser == user_id).first()
        if not rel:
            rel = RelationshipState(
                relIdUser=user_id,
                total_messages=1,
                first_interaction=datetime.datetime.now(),
            )
            session.add(rel)
        else:
            rel.total_messages = (rel.total_messages or 0) + 1
        session.commit()
        return rel.total_messages
