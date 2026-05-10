"""
LLM Chat with Prompt Translation
Compresses user prompts and expands model responses to save tokens.
"""
import asyncio
import json
import os
from pathlib import Path

import anthropic
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from translator import PromptTranslator

app = FastAPI(title="LLM Chat – Prompt Translator")

STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


def get_translator(api_key: str | None = None) -> PromptTranslator:
    key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    return PromptTranslator(api_key=key)


@app.get("/")
async def index():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/models")
async def list_models():
    """Return supported Claude models."""
    return JSONResponse([
        {"id": "claude-opus-4-7", "name": "Claude Opus 4.7 (best)"},
        {"id": "claude-opus-4-6", "name": "Claude Opus 4.6"},
        {"id": "claude-sonnet-4-6", "name": "Claude Sonnet 4.6"},
        {"id": "claude-haiku-4-5", "name": "Claude Haiku 4.5 (fastest)"},
    ])


@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()

    conversation_history: list[dict] = []
    api_key: str | None = None
    main_model = "claude-opus-4-7"
    system_prompt: str | None = None
    translation_enabled = True

    try:
        while True:
            raw = await websocket.receive_text()
            msg = json.loads(raw)
            msg_type = msg.get("type")

            if msg_type == "config":
                api_key = msg.get("api_key") or None
                main_model = msg.get("model", "claude-opus-4-7")
                system_prompt = msg.get("system_prompt") or None
                translation_enabled = msg.get("translation_enabled", True)
                await websocket.send_json({"type": "config_ok", "model": main_model})

            elif msg_type == "clear":
                conversation_history = []
                await websocket.send_json({"type": "cleared"})

            elif msg_type == "message":
                user_text = msg.get("text", "").strip()
                if not user_text:
                    continue

                try:
                    translator = get_translator(api_key)
                except Exception as exc:
                    await websocket.send_json({"type": "error", "message": str(exc)})
                    continue

                # Stream the translation pipeline
                final_response = ""
                compressed_prompt = user_text

                async def run_translation():
                    nonlocal final_response, compressed_prompt
                    # Run sync generator in thread pool
                    loop = asyncio.get_event_loop()

                    def collect():
                        events = []
                        for event in translator.stream_translated_chat(
                            user_message=user_text,
                            conversation_history=conversation_history,
                            main_model=main_model,
                            system_prompt=system_prompt,
                            translation_enabled=translation_enabled,
                        ):
                            events.append(event)
                        return events

                    return await loop.run_in_executor(None, collect)

                try:
                    events = await run_translation()
                except anthropic.AuthenticationError:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Invalid API key. Please check your ANTHROPIC_API_KEY."
                    })
                    continue
                except anthropic.RateLimitError:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Rate limited. Please wait a moment and try again."
                    })
                    continue
                except Exception as exc:
                    await websocket.send_json({
                        "type": "error",
                        "message": f"Error: {exc}"
                    })
                    continue

                for event in events:
                    await websocket.send_json(event)
                    if event["type"] == "done":
                        final_response = event["final_response"]
                        if event.get("compressed_response"):
                            compressed_prompt = event.get("compressed_response", user_text)

                # Update conversation history with compressed versions for efficiency
                if translation_enabled and compressed_prompt != user_text:
                    history_user_content = compressed_prompt
                    history_assistant_content = (
                        events[-1].get("compressed_response") or final_response
                        if events else final_response
                    )
                else:
                    history_user_content = user_text
                    history_assistant_content = final_response

                if final_response:
                    conversation_history.append({"role": "user", "content": history_user_content})
                    conversation_history.append({"role": "assistant", "content": history_assistant_content})

                    # Keep history bounded to last 20 turns to avoid context overflow
                    if len(conversation_history) > 40:
                        conversation_history = conversation_history[-40:]

    except WebSocketDisconnect:
        pass
    except Exception as exc:
        try:
            await websocket.send_json({"type": "error", "message": str(exc)})
        except Exception:
            pass
