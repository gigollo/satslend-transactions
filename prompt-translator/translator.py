"""
Prompt translation layer: compresses user prompts before sending to main model,
then expands compressed responses back to natural language.

Token savings come from:
- Sending shorter prompts to the (expensive) main model
- Instructing the main model to respond in dense/compressed format
- Using cheap Haiku for translation overhead
"""
import anthropic
from dataclasses import dataclass, field
from typing import AsyncIterator


HAIKU_MODEL = "claude-haiku-4-5"

COMPRESS_SYSTEM = """\
You are a prompt compressor. Rewrite text in the most token-efficient form while preserving ALL semantic meaning.

Rules:
- Remove articles (a, an, the) when context is clear
- Remove filler phrases: "I would like to", "Could you please", "I was wondering"
- Use abbreviations: w/=with, w/o=without, re:=regarding, impl=implementation, config=configuration, info=information
- Use symbols: &=and, +=also/plus
- Compress verbose sentences to minimal noun phrases
- List items with bullets instead of prose
- Keep technical terms, names, numbers, code exact
- Output ONLY the compressed text, no explanation"""

EXPAND_SYSTEM = """\
You are a response expander. Receive a compressed, telegraphic AI response and rewrite it as fluent, natural, professional text.

Rules:
- Restore articles, conjunctions, and prepositions
- Expand abbreviations to full words
- Make sentences grammatically complete and readable
- Preserve all technical accuracy and information
- Format code blocks, lists, headers correctly
- Add smooth transitions between ideas
- Output ONLY the expanded text, no explanation"""

DENSE_RESPONSE_INSTRUCTION = """\

[RESPONSE FORMAT: Use compressed, token-efficient style. Omit articles when meaning is clear. Use abbreviations: impl, config, info, w/, w/o. Write telegraphically. Use bullets for lists. Skip filler phrases. Be precise.]"""


@dataclass
class TokenStats:
    original_input_tokens: int = 0
    compressed_input_tokens: int = 0
    original_output_tokens: int = 0
    compressed_output_tokens: int = 0
    translator_tokens: int = 0

    @property
    def main_model_tokens_saved(self) -> int:
        input_saved = self.original_input_tokens - self.compressed_input_tokens
        output_saved = self.original_output_tokens - self.compressed_output_tokens
        return input_saved + output_saved

    @property
    def net_savings_tokens(self) -> int:
        return self.main_model_tokens_saved - self.translator_tokens

    def to_dict(self) -> dict:
        return {
            "original_input_tokens": self.original_input_tokens,
            "compressed_input_tokens": self.compressed_input_tokens,
            "original_output_tokens": self.original_output_tokens,
            "compressed_output_tokens": self.compressed_output_tokens,
            "translator_tokens": self.translator_tokens,
            "main_model_tokens_saved": self.main_model_tokens_saved,
            "net_savings_tokens": self.net_savings_tokens,
        }


class PromptTranslator:
    def __init__(self, api_key: str | None = None):
        self.client = anthropic.Anthropic(api_key=api_key) if api_key else anthropic.Anthropic()

    def compress_prompt(self, text: str) -> tuple[str, int]:
        """Compress user prompt. Returns (compressed_text, tokens_used)."""
        response = self.client.messages.create(
            model=HAIKU_MODEL,
            max_tokens=2048,
            system=COMPRESS_SYSTEM,
            messages=[{"role": "user", "content": text}],
        )
        compressed = response.content[0].text
        tokens_used = response.usage.input_tokens + response.usage.output_tokens
        return compressed, tokens_used

    def expand_response(self, compressed_text: str) -> tuple[str, int]:
        """Expand compressed model response. Returns (expanded_text, tokens_used)."""
        response = self.client.messages.create(
            model=HAIKU_MODEL,
            max_tokens=4096,
            system=EXPAND_SYSTEM,
            messages=[{"role": "user", "content": compressed_text}],
        )
        expanded = response.content[0].text
        tokens_used = response.usage.input_tokens + response.usage.output_tokens
        return expanded, tokens_used

    def count_tokens(self, text: str, model: str, system: str | None = None) -> int:
        """Count tokens for a text using the target model."""
        try:
            params = {
                "model": model,
                "messages": [{"role": "user", "content": text}],
            }
            if system:
                params["system"] = system
            result = self.client.messages.count_tokens(**params)
            return result.input_tokens
        except Exception:
            return len(text) // 4

    async def stream_translated_chat(
        self,
        user_message: str,
        conversation_history: list[dict],
        main_model: str,
        system_prompt: str | None,
        translation_enabled: bool = True,
    ) -> AsyncIterator[dict]:
        """
        Full pipeline:
        1. Count original tokens
        2. Compress user message (if enabled)
        3. Stream response from main model (with dense-response instruction)
        4. Collect compressed response, expand it
        5. Yield events: stats, compressed_prompt, streaming_text, final_stats
        """
        stats = TokenStats()

        # Count original input tokens
        stats.original_input_tokens = self.count_tokens(
            user_message, main_model, system_prompt
        )

        if translation_enabled:
            # Step 1: compress user prompt
            compressed_prompt, compress_tokens = self.compress_prompt(user_message)
            stats.compressed_input_tokens = self.count_tokens(
                compressed_prompt, main_model, system_prompt
            )
            stats.translator_tokens += compress_tokens
        else:
            compressed_prompt = user_message
            stats.compressed_input_tokens = stats.original_input_tokens

        yield {"type": "compressed_prompt", "text": compressed_prompt}
        yield {"type": "stats_update", "stats": stats.to_dict()}

        # Build messages for main model
        messages = list(conversation_history)
        messages.append({"role": "user", "content": compressed_prompt})

        # Build system with dense-response instruction
        if translation_enabled:
            effective_system = (system_prompt or "") + DENSE_RESPONSE_INSTRUCTION
        else:
            effective_system = system_prompt or ""

        # Step 2: stream from main model
        compressed_response_parts = []

        try:
            with self.client.messages.stream(
                model=main_model,
                max_tokens=8192,
                system=effective_system if effective_system else None,
                messages=messages,
                thinking={"type": "adaptive"} if "opus" in main_model else None,
            ) as stream:
                for text_chunk in stream.text_stream:
                    compressed_response_parts.append(text_chunk)
                    if not translation_enabled:
                        yield {"type": "response_chunk", "text": text_chunk}

                final_message = stream.get_final_message()
                stats.compressed_output_tokens = final_message.usage.output_tokens

        except anthropic.BadRequestError:
            # Retry without thinking if model doesn't support it
            with self.client.messages.stream(
                model=main_model,
                max_tokens=8192,
                system=effective_system if effective_system else None,
                messages=messages,
            ) as stream:
                for text_chunk in stream.text_stream:
                    compressed_response_parts.append(text_chunk)
                    if not translation_enabled:
                        yield {"type": "response_chunk", "text": text_chunk}

                final_message = stream.get_final_message()
                stats.compressed_output_tokens = final_message.usage.output_tokens

        compressed_response = "".join(compressed_response_parts)

        if translation_enabled:
            # Step 3: expand the compressed response
            expanded_response, expand_tokens = self.expand_response(compressed_response)
            stats.translator_tokens += expand_tokens
            stats.original_output_tokens = len(expanded_response) // 4  # estimate

            # Stream the expanded response character by character for smooth UX
            chunk_size = 8
            for i in range(0, len(expanded_response), chunk_size):
                yield {"type": "response_chunk", "text": expanded_response[i:i + chunk_size]}

            final_response = expanded_response
        else:
            stats.original_output_tokens = stats.compressed_output_tokens
            final_response = compressed_response

        yield {
            "type": "done",
            "stats": stats.to_dict(),
            "compressed_response": compressed_response if translation_enabled else None,
            "final_response": final_response,
        }
