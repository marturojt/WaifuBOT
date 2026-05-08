import os
from dotenv import load_dotenv

load_dotenv()

# Database
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME')

# Telegram
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_BOT_NAME = os.getenv('TELEGRAM_BOT_NAME')

# AI Provider
AI_KEY = os.getenv('AI_KEY')
AI_MODEL = os.getenv('AI_MODEL', 'gpt-4.1-mini')
AI_BASE_URL = os.getenv('AI_BASE_URL') or None  # empty string → None

# Features
KEEP_ALIVE = os.getenv('KEEP_ALIVE', '').lower() == 'true'
