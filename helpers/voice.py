import io
import logging
import openai
from openai import AsyncOpenAI
from config import AI_KEY, AI_BASE_URL

logger = logging.getLogger(__name__)

client = AsyncOpenAI(api_key=AI_KEY, base_url=AI_BASE_URL)

VALID_VOICE_STYLES = ('alloy', 'echo', 'fable', 'nova', 'onyx', 'shimmer')


async def transcribe_voice(voice_bytes: io.BytesIO) -> str:
    """Transcribe a Telegram voice note using Whisper."""
    voice_bytes.seek(0)
    result = await client.audio.transcriptions.create(
        model="whisper-1",
        file=("voice.ogg", voice_bytes, "audio/ogg"),
    )
    return result.text


async def generate_voice(text: str, voice_style: str = "nova") -> bytes:
    """Generate speech from text using OpenAI TTS. Returns opus audio bytes."""
    style = voice_style if voice_style in VALID_VOICE_STYLES else "nova"
    response = await client.audio.speech.create(
        model="tts-1",
        voice=style,
        input=text,
        response_format="opus",
    )
    return response.content
