import logging
import openai
import datetime
import json
from .db_interaction import get_waifu_role_by_id, get_chat_log_user, new_chat_log_entry
from data import api_options


# Logging configuration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Set OpenAI API key
openai.api_key = api_options.openai_key
model = "gpt-3.5-turbo"

# Dictionary to store conversation state
conversation_state = {}


async def chat_openai_waifu(message: str, user_name: str, waifu_name: str, waifu_model: int, user_id: int):


    # Get the waifu role configured in the database and replace the placeholders with the user and waifu names
    role_db = get_waifu_role_by_id(waifu_model)
    systemRole = f"{role_db.WaifuRole}".replace(
        "XXXNOVIAXXX", waifu_name).replace("XXXNOVIOXXX", user_name)


    # Create the initial message with the system prompt
    messages = [{"role": "system","content": systemRole},]

    # Get message history and append to message log
    chat_log = get_chat_log_user(user_id)
    if chat_log:
        for log in chat_log:
            # print(log[0])
            json_dict = json.loads(log[0])
            messages.append(json_dict)
        # messages.append(chat_log)

    # print(messages)

    # Append message
    new_message = {"role": "user", "content": message} 
    messages.append(new_message)

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=1,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    text_user = json.dumps(new_message)
    new_chat_log_entry(user_id, text_user, datetime.datetime.now())
    text_response = json.dumps(response["choices"][0]["message"])
    new_chat_log_entry(user_id, text_response, datetime.datetime.now())

    return response["choices"][0]["message"]["content"]

    

    # for attribute, value in vars(waifu_role_db).items():
    #     print(f"{attribute}: {value}")
