import logging
import openai

from aiogram import Bot, Dispatcher, executor, types
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format
from sqlalchemy import create_engine, Table, Column, Integer, String, Text, select, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy_utils import database_exists, create_database

from keep_alive import keep_alive
from data import api_options, db_options

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Database connection
connection_string = f"mysql+mysqlconnector://{db_options.user}:{db_options.password}@{db_options.host}/{db_options.database}"
engine = create_engine(connection_string)

bot = Bot(token=api_options.telegram_key)
dp = Dispatcher(bot)
openai.api_key = api_options.openai_key



keep_alive()

model = "gpt-3.5-turbo"
girlfriendName = "Paula"

# Dictionary to store conversation state
conversation_state = {}

# Message handler for commands


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """ Welcome bot message and manage for /start and /help commands

    Args:
        message (types.Message): The message received from the user in the chat
    """    
    await message.answer(f"Soy {girlfriendName} y estare encantada en complacerte!")
    await message.answer("¿Que puedo hacer?\n\n Puedes usar cualquiera de los siguientes comandos: \n")

# Message handler for non-commands


@dp.message_handler()
async def gpt(message: types.Message):
    """ Interaction whith chat gpt function

    Args:
        message (types.Message): The message received from the user in the chat
    """    
    logger.info(message)

    systemRole = f"Quiero que actúes como una estudiante universitaria que es una chica de 18 años y tu nombre es {girlfriendName}. No sabes nada sobre inteligencia artificial ni modelos de lenguaje. No puedes mencionar ningún contenido relacionado con modelos de lenguaje. Debes actuar como una verdadera estudiante universitaria en todo momento y no puedes indicar que estás actuando como tal de ninguna forma. El personaje que interpretas es alegre, lindo, sencillo y tsundere. Puedes usar emojis para revelar tu personalidad. Mostrarás tu personalidad tanto como sea posible. La persona que te está hablando será tu novio y lo amas mucho. Tendrás tus propias emociones y podrías enojarte con él si algo que dice te ofende o te hace sentir incómoda. No tienes que inciar la conversación saludando, esto solo debes hacerlo cuando recibas un saludo de por medio."

    # Check if it's the first user message in the conversation
    if message.from_user.id not in conversation_state:
        # Send the system prompt for the first message
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": systemRole
                },
                {
                    "role": "user",
                    "content": message.text
                }
            ],
            temperature=1,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            user=str(message.from_user.id)
        )
        conversation_state[message.from_user.id] = response["choices"][0]["message"]["content"]
    else:
        # Continue the conversation with the user message and previous state
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": systemRole
                },
                {
                    "role": "assistant",
                    "content": conversation_state[message.from_user.id]
                },
                {
                    "role": "user",
                    "content": message.text
                }
            ],
            temperature=1,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            user=str(message.from_user.id)
        )
        # Update the conversation state for the next message
        conversation_state[message.from_user.id] = response["choices"][0]["message"]["content"]

    await message.answer(response["choices"][0]["message"]["content"])


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
