import logging
import openai
from openai import AsyncOpenAI
from config import AI_KEY

logger = logging.getLogger(__name__)

# Always uses OpenAI directly — DALL-E 3 is not available on other providers
_client = AsyncOpenAI(api_key=AI_KEY)

# Default appearance per role description keyword — all explicitly female
_ROLE_APPEARANCES = {
    'estudiante': 'cute 18-year-old girl, long hair, casual university outfit, warm smile',
    'trabajadora': 'elegant 30-year-old woman, business casual attire, confident expression',
    'artista': 'bohemian young woman with paint-stained fingers, colorful creative style',
    'deportista': 'fit athletic young woman in sports attire, energetic happy expression',
    'gamer': 'cute young woman with headphones, cozy hoodie, playful gamer expression',
    'misteriosa': 'mysterious young woman, dark elegant aesthetic, alluring expression',
}
_DEFAULT_APPEARANCE = 'beautiful young woman with warm eyes and a gentle smile'


def _get_default_appearance(role_description: str) -> str:
    desc_lower = role_description.lower() if role_description else ''
    for keyword, appearance in _ROLE_APPEARANCES.items():
        if keyword in desc_lower:
            return appearance
    return _DEFAULT_APPEARANCE


async def generate_selfie(waifu_name: str, role_description: str, appearance: str | None = None) -> str:
    """Generate a selfie via DALL-E 3. Returns the image URL."""
    base_appearance = appearance or _get_default_appearance(role_description)
    prompt = (
        f"Anime style selfie portrait of a young woman named {waifu_name}. "
        f"She is a {base_appearance}. Female character, girl. "
        f"Close-up phone camera selfie perspective, natural lighting, high quality, detailed."
    )
    try:
        response = await _client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        return response.data[0].url
    except openai.APIError as e:
        logger.error("DALL-E image generation failed: %s", e)
        raise
