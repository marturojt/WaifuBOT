import asyncio
import logging

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.chat_action import ChatActionSender

from helpers import (
    keep_alive,
    search_user, new_user, update_user,
    update_user_waifu_name, update_user_waifu_role,
    get_waifu_role_descriptions, get_waifu_role_descriptions_with_id,
    chat_openai_waifu,
    delete_chat_log_user, delete_memory_summaries,
    is_rate_limited,
    update_user_last_active, toggle_user_voice, update_user_voice_style,
    update_user_appearance, toggle_user_proactive,
    transcribe_voice, generate_voice, VALID_VOICE_STYLES,
    generate_selfie,
    start_scheduler,
)
from config import TELEGRAM_TOKEN, KEEP_ALIVE

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


class Form(StatesGroup):
    get_user_name = State()
    get_girlfriend_name = State()
    get_girlfriend_model = State()
    get_appearance = State()


# CONFIGURATION FUNCTIONALITY

@dp.message(Command('start', 'help'))
async def send_welcome(message: types.Message, state: FSMContext):
    await message.answer("Hola, Soy tu novia virtual y estare encantada en complacerte!")
    user_db = await asyncio.to_thread(search_user, message.from_user.id)

    if user_db:
        markup = types.ReplyKeyboardMarkup(
            keyboard=[[types.KeyboardButton(text="/config")]],
            resize_keyboard=True,
        )
        await message.answer(
            "Ya haz hecho la configuracion inicial, puedes empezar a hablar conmigo!\n"
            "Si quieres cambiar algo usa /config.",
            reply_markup=markup,
        )
    else:
        await message.answer("Pero antes de empezar, necesito conocerte un poco mejor")
        await config_user_name(message, state)


@dp.message(Command('config_actual'))
async def actual_config(message: types.Message):
    user_db = await asyncio.to_thread(search_user, message.from_user.id)
    waifu_roles = await asyncio.to_thread(get_waifu_role_descriptions_with_id)

    if user_db:
        markup = types.ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton(text="/my_name"), types.KeyboardButton(text="/waifu_name"), types.KeyboardButton(text="/waifu_role")],
                [types.KeyboardButton(text="/finalizar")],
            ],
            resize_keyboard=True,
        )
        role_desc = waifu_roles[user_db.selected_waifu_role - 1][0] if user_db.selected_waifu_role else "Sin configurar"
        voice_status = f"{'✅' if user_db.voice_enabled else '❌'} ({user_db.voice_style or 'nova'})"
        proactive_status = "✅" if user_db.proactive_enabled else "❌"
        await message.answer(
            f"Tu configuracion actual es:\n"
            f"Tu nombre: <b>{user_db.name}</b>\n"
            f"Mi nombre: <b>{user_db.waifu_name}</b>\n"
            f"Rol: <b>{role_desc}</b>\n"
            f"Voz: {voice_status}\n"
            f"Mensajes proactivos: {proactive_status}\n\n"
            f"Comandos: /voice · /selfie · /notifications · /reset",
            parse_mode="HTML",
            reply_markup=markup,
        )


@dp.message(Command('config'))
async def general_configuration(message: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardRemove()
    await message.answer("Vamos a revisar tu configuracion", reply_markup=markup)
    user_db = await asyncio.to_thread(search_user, message.from_user.id)

    if user_db:
        await actual_config(message)
    else:
        await config_user_name(message, state)


@dp.message(StateFilter('*'), Command('cancel', 'finalizar'))
@dp.message(StateFilter('*'), F.text.casefold() == 'cancel')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        markup = types.ReplyKeyboardRemove()
        await message.answer('Podemos platicar si gustas', reply_markup=markup)
        return
    await state.clear()
    await message.reply('Accion cancelada')


@dp.message(Command('my_name'))
async def config_user_name(message: types.Message, state: FSMContext):
    if await asyncio.to_thread(search_user, message.from_user.id):
        await message.answer("Ya nos conocemos, pero si gustas puedo llamarte de otra forma.\n¿Cómo quieres que te llame ahora?")
    else:
        await message.answer("Primero quiero conocerte, dime tu nombre por favor:")
    await state.set_state(Form.get_user_name)


@dp.message(Form.get_user_name)
async def process_name(message: types.Message, state: FSMContext):
    user_name = message.text
    user_db = await asyncio.to_thread(search_user, message.from_user.id)
    if user_db:
        await asyncio.to_thread(update_user, message.from_user.id, user_name)
    else:
        await asyncio.to_thread(new_user, message.from_user.id, user_name)

    await state.clear()
    await message.reply(f"Genial, ahora te llamaré {user_name}")

    if user_db is None:
        await config_waifu_name(message, state)
    else:
        await actual_config(message)


@dp.message(Command('waifu_name'))
async def config_waifu_name(message: types.Message, state: FSMContext):
    user_db = await asyncio.to_thread(search_user, message.from_user.id)
    if user_db is None:
        await message.answer("Primero tengo que saber como te llamas")
        await config_user_name(message, state)
    else:
        await message.answer("Dime como quieres que me llame:")
    await state.set_state(Form.get_girlfriend_name)


@dp.message(Form.get_girlfriend_name)
async def process_waifu_name(message: types.Message, state: FSMContext):
    waifu_name = message.text
    if await asyncio.to_thread(search_user, message.from_user.id):
        await asyncio.to_thread(update_user_waifu_name, message.from_user.id, waifu_name)
    else:
        await asyncio.to_thread(new_user, message.from_user.id, waifu_name)

    await state.clear()
    await message.reply(f"Genial, ahora me llamaré {waifu_name}")

    user_db = await asyncio.to_thread(search_user, message.from_user.id)
    if user_db.selected_waifu_role is None:
        await config_waifu_role(message, state)
    else:
        await actual_config(message)


@dp.message(Command('waifu_role'))
async def config_waifu_role(message: types.Message, state: FSMContext):
    available_roles = await asyncio.to_thread(get_waifu_role_descriptions)
    keyboard = [[types.KeyboardButton(text=role)] for role in available_roles]
    markup = types.ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, selective=True)
    await message.answer("¿Qué rol quieres que tenga?", reply_markup=markup)
    await state.set_state(Form.get_girlfriend_model)


@dp.message(Form.get_girlfriend_model)
async def process_waifu_role(message: types.Message, state: FSMContext):
    available_roles = await asyncio.to_thread(get_waifu_role_descriptions)
    if message.text not in available_roles:
        return await message.reply("Rol invalido. Elige un rol de la lista.")

    waifu_roles_with_id = await asyncio.to_thread(get_waifu_role_descriptions_with_id)
    for description, role_id in waifu_roles_with_id:
        if description == message.text:
            await asyncio.to_thread(update_user_waifu_role, message.from_user.id, role_id)
            break

    markup = types.ReplyKeyboardRemove()
    await message.answer("Rol actualizado!", reply_markup=markup)
    await state.clear()
    await actual_config(message)


@dp.message(Command('reset'))
async def reset_conversation(message: types.Message):
    user_db = await asyncio.to_thread(search_user, message.from_user.id)
    if not user_db:
        await message.answer("Aún no tenemos conversaciones guardadas 😊")
        return
    await asyncio.to_thread(delete_chat_log_user, message.from_user.id)
    await asyncio.to_thread(delete_memory_summaries, message.from_user.id)
    await message.answer("Listo, borré todos nuestros recuerdos 🥺 Empecemos de cero...")


# VOICE COMMANDS

@dp.message(Command('voice'))
async def toggle_voice(message: types.Message):
    user_db = await asyncio.to_thread(search_user, message.from_user.id)
    if not user_db:
        await message.answer("Primero necesito conocerte. Usa /start")
        return

    new_state = not (user_db.voice_enabled or False)
    await asyncio.to_thread(toggle_user_voice, message.from_user.id, new_state)

    if new_state:
        styles_list = " · ".join(VALID_VOICE_STYLES)
        await message.answer(
            f"🔊 Respuestas de voz activadas con estilo <b>{user_db.voice_style or 'nova'}</b>.\n"
            f"Estilos disponibles: {styles_list}\n"
            f"Cambia el estilo con: <code>/voice_style nova</code>",
            parse_mode="HTML",
        )
    else:
        await message.answer("🔇 Respuestas de voz desactivadas.")


@dp.message(Command('voice_style'))
async def set_voice_style(message: types.Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2 or parts[1].strip() not in VALID_VOICE_STYLES:
        await message.answer(f"Estilos válidos: {' · '.join(VALID_VOICE_STYLES)}")
        return
    style = parts[1].strip()
    await asyncio.to_thread(update_user_voice_style, message.from_user.id, style)
    await message.answer(f"Voz cambiada a <b>{style}</b> 🎙️", parse_mode="HTML")


# VOICE MESSAGE HANDLER

@dp.message(F.voice)
async def handle_voice_message(message: types.Message, state: FSMContext):
    user_db = await asyncio.to_thread(search_user, message.from_user.id)
    if user_db is None or user_db.name is None or user_db.waifu_name is None or user_db.selected_waifu_role is None:
        await general_configuration(message, state)
        return

    if is_rate_limited(message.from_user.id):
        await message.answer("Dame un respiro, estoy un poco abrumada 💕")
        return

    try:
        async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
            voice_bytes = await bot.download(message.voice)
            transcribed = await transcribe_voice(voice_bytes)

        await message.answer(f"🎤 _{transcribed}_", parse_mode="Markdown")

        async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
            response_txt = await chat_openai_waifu(
                transcribed, user_db.name, user_db.waifu_name,
                user_db.selected_waifu_role, message.from_user.id,
            )

        if user_db.voice_enabled:
            audio_bytes = await generate_voice(response_txt, user_db.voice_style or 'nova')
            await message.answer_voice(types.BufferedInputFile(audio_bytes, "response.ogg"))
        else:
            await message.answer(response_txt)

        await asyncio.to_thread(update_user_last_active, message.from_user.id)

    except Exception as e:
        logger.error("Error in voice handler for user %s: %s", message.from_user.id, e)
        await message.answer("Tuve problemas con el audio, intenta de nuevo 🥺")


# SELFIE COMMANDS

@dp.message(Command('selfie'))
async def send_selfie(message: types.Message):
    user_db = await asyncio.to_thread(search_user, message.from_user.id)
    if not user_db or not user_db.waifu_name or not user_db.selected_waifu_role:
        await message.answer("Primero completa la configuración con /start")
        return

    waifu_roles = await asyncio.to_thread(get_waifu_role_descriptions_with_id)
    role_desc = next(
        (desc for desc, rid in waifu_roles if rid == user_db.selected_waifu_role),
        ""
    )

    await message.answer("Un momento, me estoy arreglando para la foto... 📸")
    try:
        async with ChatActionSender.upload_photo(bot=bot, chat_id=message.chat.id):
            image_url = await generate_selfie(
                user_db.waifu_name,
                role_desc,
                user_db.appearance_description,
            )
        await message.answer_photo(image_url, caption=f"¿Te gusta? 😊")
    except Exception as e:
        logger.error("Selfie generation failed for user %s: %s", message.from_user.id, e)
        await message.answer("No pude tomar la foto ahora mismo 🥺 Intenta más tarde.")


@dp.message(Command('appearance'))
async def set_appearance(message: types.Message, state: FSMContext):
    await message.answer(
        "Descríbeme cómo quieres que me vea en las fotos. Por ejemplo:\n"
        "<i>'cabello largo negro, ojos verdes, estilo casual elegante'</i>",
        parse_mode="HTML",
    )
    await state.set_state(Form.get_appearance)


@dp.message(Form.get_appearance)
async def process_appearance(message: types.Message, state: FSMContext):
    await asyncio.to_thread(update_user_appearance, message.from_user.id, message.text)
    await state.clear()
    await message.answer("Guardado ✅ Usa /selfie para verme así 📸")


# NOTIFICATIONS

@dp.message(Command('notifications'))
async def toggle_notifications(message: types.Message):
    user_db = await asyncio.to_thread(search_user, message.from_user.id)
    if not user_db:
        await message.answer("Primero necesito conocerte. Usa /start")
        return

    new_state = not (user_db.proactive_enabled if user_db.proactive_enabled is not None else True)
    await asyncio.to_thread(toggle_user_proactive, message.from_user.id, new_state)

    if new_state:
        await message.answer("🔔 Te voy a escribir cuando te extrañe 💕")
    else:
        await message.answer("🔕 De acuerdo, no te molestaré si no me escribes primero.")


# CHATGPT FUNCTIONALITY

@dp.message()
async def gpt(message: types.Message, state: FSMContext):
    if not message.text:
        await message.answer("Por ahora solo puedo leer mensajes de texto 😊")
        return
    if len(message.text) > 2000:
        await message.answer("Tu mensaje es muy largo, ¿puedes resumirlo un poco? 🥺")
        return

    if is_rate_limited(message.from_user.id):
        await message.answer("Dame un respiro, estoy un poco abrumada 💕")
        return

    user_db = await asyncio.to_thread(search_user, message.from_user.id)

    if user_db is None or user_db.name is None or user_db.waifu_name is None or user_db.selected_waifu_role is None:
        await general_configuration(message, state)
        return

    try:
        async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
            response_txt = await chat_openai_waifu(
                message.text, user_db.name, user_db.waifu_name,
                user_db.selected_waifu_role, message.from_user.id,
            )

        if user_db.voice_enabled:
            audio_bytes = await generate_voice(response_txt, user_db.voice_style or 'nova')
            await message.answer_voice(types.BufferedInputFile(audio_bytes, "response.ogg"))
        else:
            await message.answer(response_txt)

        await asyncio.to_thread(update_user_last_active, message.from_user.id)

    except Exception as e:
        logger.error("Unhandled error in gpt handler for user %s: %s", message.from_user.id, e)
        await message.answer("Algo salió mal, intenta de nuevo 💕")


async def main():
    if KEEP_ALIVE:
        keep_alive()
    start_scheduler(bot)

    await bot.set_my_commands([
        types.BotCommand(command="start",         description="Bienvenida e inicio"),
        types.BotCommand(command="config_actual", description="Ver tu configuración actual"),
        types.BotCommand(command="config",        description="Editar configuración"),
        types.BotCommand(command="selfie",        description="📸 Genera una foto de tu waifu"),
        types.BotCommand(command="voice",         description="🔊 Activar/desactivar respuestas de voz"),
        types.BotCommand(command="voice_style",   description="🎙️ Cambiar estilo de voz (ej: /voice_style nova)"),
        types.BotCommand(command="appearance",    description="🎨 Describir apariencia para las fotos"),
        types.BotCommand(command="notifications", description="🔔 Activar/desactivar mensajes proactivos"),
        types.BotCommand(command="reset",         description="🗑️ Borrar historial de conversación"),
        types.BotCommand(command="my_name",       description="Cambiar tu nombre"),
        types.BotCommand(command="waifu_name",    description="Cambiar el nombre de tu waifu"),
        types.BotCommand(command="waifu_role",    description="Cambiar personalidad"),
        types.BotCommand(command="finalizar",     description="Cancelar acción actual"),
    ])

    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
