import asyncio
from typing import List, Dict
from src.sentiment_intent_analyzer import ZeroShotAnalyzer
from src.logger import AsyncLogger

class ConversationalManager:
    """
    An example manager that shows how to handle multi-turn context.
    For each new utterance, we combine the last N utterances as context
    before calling the zero-shot pipeline.
    """

    def __init__(self, analyzer: ZeroShotAnalyzer, logger: AsyncLogger, context_window: int = 2):
        """
        :param analyzer: A ZeroShotAnalyzer instance.
        :param logger: An AsyncLogger instance.
        :param context_window: Number of previous utterances to include as context.
        """
        self.analyzer = analyzer
        self.logger = logger
        self.context_window = context_window
        self.memory: List[Dict[str, str]] = []  # Stores past messages (role, text)

    async def process_utterance(self, role: str, text: str) -> Dict[str, str]:
        """
        Creates a context-based utterance, classifies, and logs it asynchronously.
        Returns the classification result dict.
        """

        # Build a context string from the last N messages + current
        context_text = self._build_context_text(text)

        # Perform zero-shot classification on the combined context
        analysis = self.analyzer.analyze_message(role, context_text)

        # Store to memory
        self.memory.append({"role": role, "text": text})

        # Log the classification
        await self.logger.log_message(
            role=role,
            text=text,
            sentiment=analysis["sentiment"],
            intent=analysis["intent"]
        )

        return analysis

    def _build_context_text(self, current_text: str) -> str:
        """
        Build a short context window by combining the last N utterances
        with the current user utterance. This is a simplistic approach:
        e.g., "Prev1 || Prev2 || Current"
        """
        # Take the last self.context_window utterances
        recent_messages = self.memory[-self.context_window:]
        # Combine them into a single string
        context_parts = [m["role"] + ": " + m["text"] for m in recent_messages]
        context_parts.append("current_user: " + current_text)

        # Return combined text. You could add separators or formatting as needed.
        return " || ".join(context_parts)
