import asyncio
from .db_interaction import get_relationship_total, increment_relationship_messages

# (min_messages, stage_key, context injected into system prompt)
STAGES = [
    (0,   'stranger',      "Acaban de conocerse, hay curiosidad mutua pero todavía cierta distancia."),
    (10,  'conocidos',     "Ya se conocen bien, hay confianza y comodidad entre ellos."),
    (50,  'saliendo',      "Están saliendo juntos, el afecto es claro y abierto."),
    (200, 'comprometidos', "Son una pareja comprometida y muy cercana, con una conexión profunda."),
]


def get_stage_context(total_messages: int) -> str:
    context = STAGES[0][2]
    for threshold, _, description in STAGES:
        if total_messages >= threshold:
            context = description
    return f"\n\nContexto de la relación: {context} Han tenido {total_messages} intercambios juntos."


async def track_message(user_id: int) -> int:
    """Increment the message count and return the new total."""
    return await asyncio.to_thread(increment_relationship_messages, user_id)


async def get_total_messages(user_id: int) -> int:
    return await asyncio.to_thread(get_relationship_total, user_id)
