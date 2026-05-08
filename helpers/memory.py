import asyncio
import json
import logging
import openai
from openai import AsyncOpenAI
from config import AI_KEY, AI_MODEL, AI_BASE_URL

logger = logging.getLogger(__name__)

client = AsyncOpenAI(api_key=AI_KEY, base_url=AI_BASE_URL)

SUMMARIZE_THRESHOLD = 100  # trigger summarization when chat log exceeds this
KEEP_RECENT = 50           # keep this many recent messages after summarization


async def maybe_summarize(user_id: int, waifu_name: str, user_name: str):
    """If the chat log is too long, summarize the oldest messages and prune them."""
    from .db_interaction import (
        count_chat_log_user, get_oldest_chat_logs,
        save_memory_summary, delete_chat_logs_before_id,
    )

    count = await asyncio.to_thread(count_chat_log_user, user_id)
    if count <= SUMMARIZE_THRESHOLD:
        return

    to_summarize = count - KEEP_RECENT
    oldest = await asyncio.to_thread(get_oldest_chat_logs, user_id, to_summarize)
    if not oldest:
        return

    convo_lines = []
    for text, _, _ in oldest:
        try:
            entry = json.loads(text)
            role = "Tú" if entry.get("role") == "assistant" else user_name
            convo_lines.append(f"{role}: {entry.get('content', '')}")
        except Exception:
            continue

    convo_text = "\n".join(convo_lines)

    try:
        response = await client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "Eres un asistente que crea resúmenes concisos de conversaciones para memoria a largo plazo.",
                },
                {
                    "role": "user",
                    "content": (
                        f"Resume en 3-5 oraciones los puntos clave de esta conversación entre "
                        f"{waifu_name} y {user_name}. Incluye hechos importantes, temas discutidos "
                        f"y contexto emocional relevante:\n\n{convo_text}"
                    ),
                },
            ],
            temperature=0.3,
            max_tokens=300,
        )
        summary = response.choices[0].message.content
    except openai.APIError as e:
        logger.error("Failed to generate memory summary for user %s: %s", user_id, e)
        return

    period_start = oldest[0][2]
    period_end = oldest[-1][2]
    last_id = oldest[-1][1]

    await asyncio.to_thread(save_memory_summary, user_id, summary, period_start, period_end)
    await asyncio.to_thread(delete_chat_logs_before_id, user_id, last_id)
    logger.info("Summarized %d messages for user %s", len(oldest), user_id)


async def build_context(user_id: int, system_role: str) -> list:
    """Build the full message list for an LLM call: system + long-term memory + recent chat."""
    from .db_interaction import get_memory_summaries, get_chat_log_user

    messages = [{"role": "system", "content": system_role}]

    summaries = await asyncio.to_thread(get_memory_summaries, user_id)
    if summaries:
        combined = "\n".join(f"- {s}" for s in summaries)
        messages.append({
            "role": "system",
            "content": f"Estos son tus recuerdos de conversaciones anteriores con tu novio:\n{combined}",
        })

    chat_log = await asyncio.to_thread(get_chat_log_user, user_id, KEEP_RECENT)
    for log in chat_log:
        try:
            messages.append(json.loads(log[0]))
        except Exception:
            continue

    return messages
