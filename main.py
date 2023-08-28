# Import general libraries
import logging
import openai

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

# Import functions from helpers package
from helpers import keep_alive, search_user, new_user, update_user, update_user_waifu_name, update_user_waifu_role, get_waifu_role_by_id, get_waifu_role_descriptions, get_waifu_role_descriptions_with_id, chat_openai_waifu
from data import api_options, db_options

# Logging configuration
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot and OpenAI connection
bot = Bot(token=api_options.telegram_key)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
# openai.api_key = api_options.openai_key

keep_alive()


# States
class Form(StatesGroup):
    get_user_name = State()
    get_girlfriend_name = State()
    get_girlfriend_model = State()

# CONFIGURATION FUNCTIONALITY

# Message handler for commands /start and /help
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """ Welcome bot message and manage for /start and /help commands

    Args:
        message (types.Message): The message received from the user in the chat
    """
    await message.answer("Hola, Soy tu novia virtual y estare encantada en complacerte!")

    user_db = search_user(message.from_user.id)

    if (user_db):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        config_btn = types.KeyboardButton("/config")
        markup.add(config_btn)
        await message.answer("Ya haz hecho la configuracion inicial, puedes empezar a hablar conmigo!\nSi quieres cambiar algo de la configuracion puedes usar el comando de configuración, o directamente presionar el boton de abajo.", reply_markup=markup)
    else: 
        await message.answer("Pero antes de empezar, necesito conocerte un poco mejor")
        await general_configuration(message)

# Send actual config into message
@dp.message_handler(commands=['config_actual'])
async def actual_config(message: types.Message):
    user_db = search_user(message.from_user.id)
    waifu_roles = get_waifu_role_descriptions_with_id()

    if (user_db):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        user_name_btn = types.KeyboardButton("/my_name")
        waifu_name_btn = types.KeyboardButton("/waifu_name")
        waifu_role_btn = types.KeyboardButton("/waifu_role")
        cancel_handler_btn = types.KeyboardButton("/finalizar")
        markup.add(user_name_btn, waifu_name_btn, waifu_role_btn)
        markup.add(cancel_handler_btn)
    

        
        await bot.send_message(
        message.chat.id,
        md.text(
            md.text('Tu configuracion actual es:'),
            md.text('Tu nombre:', md.bold(user_db.name)),
            md.text('Mi nombre (waifu):', md.bold(user_db.waifu_name)),
            md.text('Rol de novia:', md.bold(waifu_roles[user_db.selected_waifu_role - 1][0])),
            md.text('Si deseas cambiar algo, puedes usar los siguientes comandos:'),
            sep='\n',
        ),
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN,
    )

# Message handler for command /config
@dp.message_handler(commands=['config'])
async def general_configuration(message: types.Message):
    """ General configuration for the bot

    Args:
        message (types.Message): The message received from the user in the chat
    """
    markup = types.ReplyKeyboardRemove()
    await message.answer("Vamos a revisar tu configuracion", reply_markup=markup)
    user_db = search_user(message.from_user.id)
    waifu_roles = get_waifu_role_descriptions_with_id()

    if (user_db):
        await actual_config(message)
    else:    
        await config_user_name(message)

# Message handler for command /cancel (to cancel any State)
@dp.message_handler(state='*', commands=['cancel', 'finalizar'])
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """Allow user to cancel action via /cancel command

    Args:
        message (types.Message): The message received from the user in the chat
        state: The state of the user
    """
    current_state = await state.get_state()

    if current_state is None:
        # User is not in any state, ignoring
        markup = types.ReplyKeyboardRemove()
        await message.answer('Podemos platicar si gustas', reply_markup=markup)
        return

    # Cancel state and inform user about it
    await state.finish()
    await message.reply('Accion cancelada')

# Message handler for command /my_name
@dp.message_handler(commands=['my_name'])
async def config_user_name(message: types.Message):
    """ Ask the user for his name and save it or update it in the database

    Args:
        message (types.Message): The message received from the user in the chat
    """
    if (search_user(message.from_user.id)):
        await message.answer("Ya nos conocemos, pero si gustas puedo llamarte de otra forma \nComo quieres que te llame ahora:")
    else:
        await message.answer("Primero quiero conocerte, dime tu nombre por favor:")
    await Form.get_user_name.set()

# Set user name after /my_name command is executed
@dp.message_handler(state=Form.get_user_name)
async def process_name(message: types.Message, state: FSMContext):
    """Save user name and finish the state

    Args:
        message (types.Message): The message received from the user in the chat
        state (FSMContext): The state of the user
    """    
    user_name = message.text
    user_db = search_user(message.from_user.id)
    if (user_db):
        update_user(message.from_user.id, user_name)
    else:
        new_user(message.from_user.id, user_name)
    
    await state.finish()
    await message.reply(f"Genial, ahora te llamaré {user_name}")

    # Set waifu name if it's not set
    if (user_db is None):
        await config_waifu_name(message)
    else:
        await actual_config(message)

# Message handler for command /waifu_name
@dp.message_handler(commands=['waifu_name'])
async def config_waifu_name(message: types.Message):
    """ Ask the user for his waifu name and save it or update it in the database

    Args:
        message (types.Message): The message received from the user in the chat
    """
    user_db = search_user(message.from_user.id)
    if (user_db is None):
        await message.answer("Primero tengo que saber como te llamas")
        await config_user_name(message)
    else:
        await message.answer("Dime como quieres que me llame:")
    await Form.get_girlfriend_name.set()

# Set waifu name after /waifu_name command is executed
@dp.message_handler(state=Form.get_girlfriend_name)
async def process_waifu_name(message: types.Message, state: FSMContext):
    """Save waifu name and finish the state

    Args:
        message (types.Message): The message received from the user in the chat
        state (FSMContext): The state of the user
    """    
    waifu_name = message.text
    if (search_user(message.from_user.id)):
        update_user_waifu_name(message.from_user.id, waifu_name)
    else:
        new_user(message.from_user.id, waifu_name)
    
    await state.finish()
    await message.reply(f"Genial, ahora me llamaré {waifu_name}")

    user_db = search_user(message.from_user.id)
    if (user_db.selected_waifu_role is None):
        await config_waifu_role(message)
    else:
        await actual_config(message)

# Message handler for waifu role configuration
@dp.message_handler(commands=['waifu_role'])
async def config_waifu_role(message: types.Message):
    """ Ask the user for his waifu role and save it or update it in the database

    Args:
        message (types.Message): The message received from the user in the chat
    """
    available_roles = get_waifu_role_descriptions()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(*available_roles)
    await message.answer("Que rol quieres que tenga?", reply_markup=markup)
    await Form.get_girlfriend_model.set()

# Set waifu role after /waifu_role command is executed
@dp.message_handler(lambda message: message.text not in get_waifu_role_descriptions(), state=Form.get_girlfriend_model)
async def process_waifu_role_invalid(message: types.Message):
    return await message.reply("Rol invalido. Elige un rol de la lista.")
@dp.message_handler(state=Form.get_girlfriend_model)
async def process_waifu_role(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['waifu_role'] = message.text

    # Remove keyboard
    markup = types.ReplyKeyboardRemove()

    waifu_roles_with_id = get_waifu_role_descriptions_with_id()
    for waifu_roles_description in waifu_roles_with_id:
        # print(waifu_roles_description)
        if waifu_roles_description[0] == message.text:
            update_user_waifu_role(message.from_user.id, waifu_roles_description[1])
            break
    await state.finish()
    
    # print actual config
    await actual_config(message)




# CHATGPT FUNCTIONALITY

# Message handler for non-commands
@dp.message_handler()
async def gpt(message: types.Message):
    """ Interaction whith chat gpt function

    Args:
        message (types.Message): The message received from the user in the chat
    """    
    logger.info(message)

    # Evaluate if the user exists in the database 
    user_db = search_user(message.from_user.id)
    # print(user_db)
    
    if (user_db is None): 
        await general_configuration(message)
    elif(user_db.name is None or user_db.waifu_name is None or user_db.selected_waifu_role is None):
        await general_configuration(message)
    else:
        response_txt = await chat_openai_waifu(message.text, user_db.name, user_db.waifu_name, user_db.selected_waifu_role, message.from_user.id)
        await message.answer(response_txt)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
