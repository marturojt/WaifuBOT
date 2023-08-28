from .db_connection import db_session
from models.waifu_models import Users, ChatLog, WaifuRoles

db_session = db_session()

users = db_session.query(Users).all()
print(users)

# USER OPERATIONS

# Search for a user in the database
def search_user(user_id):
    user = db_session.query(Users).filter(Users.telegram_id == user_id).first()
    db_session.close()
    return user

# Create a new user in the database
def new_user(telegram_id, name):
    new_user = Users(telegram_id=telegram_id, name=name)
    db_session.add(new_user)
    db_session.commit()
    db_session.close()

# Update user name
def update_user(telegram_id, name):
    existing_user = db_session.query(Users).filter(Users.telegram_id == telegram_id).first()
    if (existing_user):
        existing_user.name = name
        db_session.commit()
    db_session.close()

# Update user waifu name
def update_user_waifu_name(telegram_id, waifu_name):
    existing_user = db_session.query(Users).filter(Users.telegram_id == telegram_id).first()
    if (existing_user):
        existing_user.waifu_name = waifu_name
        db_session.commit()
    db_session.close()

# Update user waifu role
def update_user_waifu_role(telegram_id, waifu_role):
    existing_user = db_session.query(Users).filter(Users.telegram_id == telegram_id).first()
    if (existing_user):
        existing_user.selected_waifu_role = waifu_role
        db_session.commit()
    db_session.close()

# CHAT CONFIG OPERATIONS

# Get waifu role by id
def get_waifu_role_by_id(waifu_role_id):
    waifu_role = db_session.query(WaifuRoles).filter(WaifuRoles.idWaifuRole == waifu_role_id).first()
    db_session.close()
    return waifu_role

# Get a list of WaifuRoles Descriptions paired with id
def get_waifu_role_descriptions_with_id():
    waifu_roles = db_session.query(WaifuRoles).all()
    waifu_roles_descriptions = []
    for waifu_role in waifu_roles:
        waifu_roles_descriptions.append([waifu_role.WaifuRoleDescription, waifu_role.idWaifuRole])
    db_session.close()
    return waifu_roles_descriptions

# Get a list of WaifuRoles Descriptions
def get_waifu_role_descriptions():
    waifu_roles = db_session.query(WaifuRoles).all()
    waifu_roles_descriptions = []
    for waifu_role in waifu_roles:
        waifu_roles_descriptions.append(waifu_role.WaifuRoleDescription)
    db_session.close()
    return waifu_roles_descriptions

# CHAT LOG OPERATIONS

# Obtain the chat log for a user
def get_chat_log_user(user_id):
    chat_log = db_session.query(ChatLog).filter(ChatLog.relIdUser == user_id).all()
    chat_log_parsed = []
    for chat in chat_log:
        chat_log_parsed.append([chat.text])
    db_session.close()
    return chat_log_parsed

# Add a new chat log entry
def new_chat_log_entry(user_id, text, timestamp):
    new_chat_log_entry = ChatLog(relIdUser=user_id, text=text, timestamp=timestamp)
    db_session.add(new_chat_log_entry)
    db_session.commit()
    db_session.close()