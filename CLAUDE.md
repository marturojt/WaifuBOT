# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the bot

```bash
cp .env.example .env      # fill in credentials
uv sync                   # create .venv and install all dependencies
uv run python main.py     # run inside the venv
```

Requires MariaDB/MySQL running locally. On macOS: `brew services start mariadb`.

Credentials live in `.env` (git-ignored). See `.env.example` for all required variables. `config.py` loads them via `python-dotenv` and exposes them as module-level constants imported by the rest of the codebase.

## Architecture

The bot is a Telegram chatbot built with **aiogram 3.x** that uses an OpenAI-compatible API to simulate a virtual girlfriend persona.

### Request flow

1. User sends a Telegram message → `main.py` handler
2. If user is not configured → FSM guides through setup (name → waifu name → personality role)
3. If configured → `chat_openai_waifu()` in `helpers/chat.py`:
   - Loads system prompt from `tb_waifu_roles`, replaces name placeholders
   - Injects relationship stage context from `helpers/relationship.py`
   - Calls `maybe_summarize()` — if chat log > 100 msgs, summarizes oldest into `tb_memory_summaries`
   - Calls `build_context()` — system prompt + long-term summaries + last 50 msgs
   - Calls AI API and persists both messages to DB
   - Increments relationship message count

### Key design decisions

- **Personality system**: Roles stored in `tb_waifu_roles` as full system prompts with `XXXNOVIAXXX` (waifu name) and `XXXNOVIOXXX` (user name) placeholders replaced at chat time.
- **Memory system**: Two-tier — last 50 raw messages (short-term) + LLM-generated summaries of older batches (long-term). Both injected on every call.
- **Relationship progression**: `tb_relationship_state` tracks total messages per user. 4 stages (stranger → conocidos → saliendo → comprometidos) injected into system prompt.
- **Session management**: `helpers/db_connection.py` exports `SessionLocal` (SQLAlchemy `sessionmaker`). Every DB function in `db_interaction.py` opens its own session via `with SessionLocal() as session:`.
- **Async DB**: All synchronous DB calls are wrapped with `asyncio.to_thread()` at call sites to avoid blocking the event loop.
- **AI provider**: Configured entirely via `.env` (`AI_KEY`, `AI_MODEL`, `AI_BASE_URL`). Supports OpenAI, Gemini, and Groq without code changes. DALL-E 3 (selfies) always uses OpenAI directly.
- **Keep-alive server**: Flask server on port 8080, only starts if `KEEP_ALIVE=true` in `.env`.

### Configuration

Variables loaded from `.env` via `config.py`. To switch AI provider, change only `AI_KEY`, `AI_MODEL`, and `AI_BASE_URL` in `.env`. See `.env.example` for provider examples (OpenAI, Gemini, Groq).

### FSM states (`main.py`)

Four states in `Form`: `get_user_name` → `get_girlfriend_name` → `get_girlfriend_model` → `get_appearance`. Commands `/my_name`, `/waifu_name`, `/waifu_role`, `/appearance` trigger individual states outside onboarding.

### Helpers overview

| File | Responsibility |
|---|---|
| `helpers/chat.py` | Core AI call — builds context, calls API, persists messages |
| `helpers/memory.py` | `build_context()` and `maybe_summarize()` — long-term memory logic |
| `helpers/relationship.py` | Stage thresholds and context string for system prompt |
| `helpers/voice.py` | Whisper STT (`transcribe_voice`) and OpenAI TTS (`generate_voice`) |
| `helpers/image_gen.py` | DALL-E 3 selfie generation |
| `helpers/scheduler.py` | APScheduler — proactive messages for inactive users |
| `helpers/rate_limiter.py` | In-memory sliding window rate limiter (20 msg/min) |
| `helpers/db_interaction.py` | All DB CRUD — users, chat log, memory summaries, relationships |
| `helpers/db_connection.py` | SQLAlchemy engine, session factory, table creation, role seeding |

### Database tables

| Table | Purpose |
|---|---|
| `tb_users` | User profiles, voice/appearance/notification preferences |
| `tb_waifu_roles` | Personality system prompts (seeded on first run) |
| `tb_chat_log` | Raw message history (JSON per entry) |
| `tb_memory_summaries` | LLM-generated long-term memory summaries |
| `tb_relationship_state` | Message count and relationship stage per user |
