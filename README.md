<a name="readme-top"></a>

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/marturojt/WaifuBOT">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">WaifuBOT</h3>

  <p align="center">
    An AI-powered virtual girlfriend Telegram bot. Personalized, always available, with voice, selfies, memory, and relationship progression.
    <br />
    <br />
    <a href="https://github.com/marturojt/WaifuBOT/issues">Report Bug</a>
    ·
    <a href="https://github.com/marturojt/WaifuBOT/issues">Request Feature</a>
  </p>
</div>

---

## About The Project

WaifuBOT is a Telegram chatbot that simulates a virtual girlfriend powered by OpenAI. Users can customize the waifu's name, personality, and appearance — and the bot remembers their conversations over time.

**Key features:**
- 7 built-in personalities (student, working woman, bohemian artist, athlete, gamer, mysterious)
- Long-term memory system — summarizes old conversations so the waifu never truly forgets
- Voice messages — send audio, receive audio (OpenAI Whisper + TTS)
- AI-generated selfies via DALL-E 3
- Proactive messaging — the bot messages you when you've been away too long
- Relationship progression — the waifu's behavior evolves as the relationship grows
- Easy AI provider switching (OpenAI, Gemini, Groq) via `.env`

### Built With

[![Python][Python.org]][Python-url] [![uv][uv-badge]][uv-url]

---

## Getting Started

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager
- MariaDB or MySQL server
- Telegram bot token (via [@BotFather](https://t.me/botfather))
- OpenAI API key

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/marturojt/WaifuBOT
   cd WaifuBOT
   ```

2. Install `uv` if you don't have it
   ```sh
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. Install dependencies (creates `.venv` automatically)
   ```sh
   uv sync
   ```

4. Copy and fill the environment file
   ```sh
   cp .env.example .env
   ```

   | Variable | Description |
   |---|---|
   | `DB_USER` / `DB_PASSWORD` / `DB_HOST` / `DB_NAME` | MySQL/MariaDB credentials |
   | `TELEGRAM_TOKEN` | Bot token from BotFather |
   | `TELEGRAM_BOT_NAME` | Bot username (e.g. `@MyBot`) |
   | `AI_KEY` | API key for your AI provider |
   | `AI_MODEL` | Model name (e.g. `gpt-4.1-mini`) |
   | `AI_BASE_URL` | Leave empty for OpenAI, set URL for Gemini/Groq |
   | `KEEP_ALIVE` | `true` only on platforms like Replit |

5. Start MariaDB/MySQL and run the bot
   ```sh
   brew services start mariadb   # macOS
   uv run python main.py
   ```

   The database and all tables are created automatically on first run.

### Switching AI Provider

Only change `.env` — no code changes needed:

| Provider | `AI_MODEL` | `AI_BASE_URL` |
|---|---|---|
| OpenAI | `gpt-4.1-mini` | *(empty)* |
| Gemini | `gemini-2.5-flash` | `https://generativelanguage.googleapis.com/v1beta/openai/` |
| Groq | `llama-3.3-70b-versatile` | `https://api.groq.com/openai/v1` |

---

## Bot Commands

| Command | Description |
|---|---|
| `/start` | Welcome and initial setup |
| `/config_actual` | View current configuration |
| `/config` | Edit configuration |
| `/selfie` | Generate an AI photo of your waifu |
| `/appearance` | Describe how you want your waifu to look |
| `/voice` | Toggle voice responses (TTS) |
| `/voice_style` | Change TTS voice (alloy, echo, fable, nova, onyx, shimmer) |
| `/notifications` | Toggle proactive messages |
| `/reset` | Clear conversation history and memory |
| `/my_name` | Change your name |
| `/waifu_name` | Change your waifu's name |
| `/waifu_role` | Change personality |
| `/finalizar` | Cancel current action |

---

## Roadmap

- [x] Basic bot with FSM onboarding
- [x] Persistent conversation history
- [x] Custom names and personalities
- [x] Migrated to aiogram 3.x and openai v1.x
- [x] Environment-based config (.env)
- [x] uv package manager + venv
- [x] Long-term memory with LLM summarization
- [x] 7 built-in personalities
- [x] Rate limiting
- [x] Typing indicator
- [x] Voice messages (Whisper STT + TTS)
- [x] AI selfie generation (DALL-E 3)
- [x] Proactive messaging (APScheduler)
- [x] Relationship progression system
- [x] Telegram command menu
- [ ] Monetization via Telegram Stars
- [ ] Premium / VIP tiers
- [ ] Multi-language support (English)
- [ ] Custom personality builder
- [ ] Voice quality upgrade — `tts-1-hd` (drop-in improvement) or ElevenLabs integration (near-human quality)

---

## Contributing

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'feat: add AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## License

Distributed under the MIT License. See `LICENSE` for more information.

---

## Contact

Arturo Jiménez — [@_systemctl](https://twitter.com/_systemctl)

WaifuBOT: [https://github.com/marturojt/WaifuBOT](https://github.com/marturojt/WaifuBOT)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/marturojt/WaifuBOT?style=for-the-badge
[contributors-url]: https://github.com/marturojt/WaifuBOT/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/marturojt/WaifuBOT?style=for-the-badge
[forks-url]: https://github.com/marturojt/WaifuBOT/network/members
[stars-shield]: https://img.shields.io/github/stars/marturojt/WaifuBOT?style=for-the-badge
[stars-url]: https://github.com/marturojt/WaifuBOT/stargazers
[issues-shield]: https://img.shields.io/github/issues/marturojt/WaifuBOT?style=for-the-badge
[issues-url]: https://github.com/marturojt/WaifuBOT/issues
[license-shield]: https://img.shields.io/github/license/marturojt/WaifuBOT?style=for-the-badge
[license-url]: https://github.com/marturojt/WaifuBOT/blob/dev/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/marturojt
[product-screenshot]: images/screenshot.png
[Python.org]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://python.org/
[uv-badge]: https://img.shields.io/badge/uv-package%20manager-DE5FE9?style=for-the-badge
[uv-url]: https://docs.astral.sh/uv/
