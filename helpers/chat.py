import asyncio
import logging
import datetime
import json
import openai
from openai import AsyncOpenAI
from .db_interaction import get_waifu_role_by_id, new_chat_log_entry, increment_relationship_messages, get_relationship_total
from .memory import build_context, maybe_summarize
from .relationship import get_stage_context
from config import AI_KEY, AI_MODEL, AI_BASE_URL


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

client = AsyncOpenAI(api_key=AI_KEY, base_url=AI_BASE_URL)


async def chat_openai_waifu(message: str, user_name: str, waifu_name: str, waifu_model: int, user_id: int):

    role_db = await asyncio.to_thread(get_waifu_role_by_id, waifu_model)
    base_role = role_db.WaifuRole.replace("XXXNOVIAXXX", waifu_name).replace("XXXNOVIOXXX", user_name)

    # Inject relationship stage context into system prompt
    total_msgs = await asyncio.to_thread(get_relationship_total, user_id)
    system_role = base_role + get_stage_context(total_msgs)

    # Summarize old messages if needed, then build full context
    await maybe_summarize(user_id, waifu_name, user_name)
    messages = await build_context(user_id, system_role)

    new_message = {"role": "user", "content": message}
    messages.append(new_message)

    try:
        response = await client.chat.completions.create(
            model=AI_MODEL,
            messages=messages,
            temperature=1,
            max_tokens=300,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
    except openai.RateLimitError:
        logger.warning("OpenAI rate limit reached for user %s", user_id)
        return "Estoy un poco ocupada ahora mismo, intenta de nuevo en un momento 💕"
    except openai.APIConnectionError:
        logger.error("OpenAI connection error for user %s", user_id)
        return "Parece que hay problemas de conexión, intenta de nuevo pronto 🥺"
    except openai.APIError as e:
        logger.error("OpenAI API error for user %s: %s", user_id, e)
        return "Tuve un pequeño problema, ¿puedes repetirlo? 😊"

    now = datetime.datetime.now()
    try:
        await asyncio.to_thread(new_chat_log_entry, user_id, json.dumps(new_message), now)
        assistant_message = response.choices[0].message
        assistant_dict = {"role": assistant_message.role, "content": assistant_message.content}
        await asyncio.to_thread(new_chat_log_entry, user_id, json.dumps(assistant_dict), now)
        await asyncio.to_thread(increment_relationship_messages, user_id)
    except Exception as e:
        logger.error("Failed to persist chat log for user %s: %s", user_id, e)
        assistant_message = response.choices[0].message

    return assistant_message.content
