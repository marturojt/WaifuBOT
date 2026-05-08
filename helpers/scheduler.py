import asyncio
import datetime
import logging
import openai
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from openai import AsyncOpenAI
from config import AI_KEY, AI_MODEL, AI_BASE_URL

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()

INACTIVE_HOURS = 6  # hours without activity before sending a proactive message


def start_scheduler(bot):
    scheduler.add_job(
        _check_inactive_users,
        'interval',
        hours=1,
        args=[bot],
        id='proactive_check',
        replace_existing=True,
    )
    scheduler.start()
    logger.info("Proactive message scheduler started")


async def _check_inactive_users(bot):
    from .db_interaction import get_active_proactive_users, update_user_last_active, get_waifu_role_by_id

    cutoff = datetime.datetime.now() - datetime.timedelta(hours=INACTIVE_HOURS)
    users = await asyncio.to_thread(get_active_proactive_users, cutoff)

    for user in users:
        try:
            hours_inactive = (datetime.datetime.now() - user.last_active).total_seconds() / 3600
            msg = await _generate_proactive_message(user, int(hours_inactive))
            await bot.send_message(user.telegram_id, msg)
            await asyncio.to_thread(update_user_last_active, user.telegram_id)
            logger.info("Sent proactive message to user %s", user.telegram_id)
        except Exception as e:
            logger.error("Failed to send proactive message to user %s: %s", user.telegram_id, e)


async def _generate_proactive_message(user, hours_inactive: int) -> str:
    from .db_interaction import get_waifu_role_by_id

    role_db = await asyncio.to_thread(get_waifu_role_by_id, user.selected_waifu_role)
    system_role = role_db.WaifuRole.replace("XXXNOVIAXXX", user.waifu_name).replace("XXXNOVIOXXX", user.name)

    client = AsyncOpenAI(api_key=AI_KEY, base_url=AI_BASE_URL)
    try:
        response = await client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "system", "content": system_role},
                {
                    "role": "user",
                    "content": (
                        f"Tu novio {user.name} no te ha escrito en {hours_inactive} horas. "
                        f"Envíale un mensaje espontáneo y natural, como si lo extrañaras o quisieras saber cómo está. "
                        f"Solo escribe el mensaje, sin explicaciones."
                    ),
                },
            ],
            temperature=1,
            max_tokens=150,
        )
        return response.choices[0].message.content
    except openai.APIError as e:
        logger.error("Failed to generate proactive message: %s", e)
        return f"Oye {user.name}, ¿todo bien? Te extraño 💕"
