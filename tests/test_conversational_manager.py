# tests/test_conversational_manager.py

import asyncio
import pytest
from unittest.mock import patch
from src.conversational_manager import ConversationalManager
from src.logger import AsyncLogger
from src.db import Database
from src.sentiment_intent_analyzer import ZeroShotAnalyzer

@pytest.mark.asyncio
async def test_conversational_manager_context(tmp_path):
    """
    Test that the ConversationalManager builds context properly
    and calls the analyzer & logger with correct parameters.
    """
    db_url = f"sqlite+aiosqlite:///{tmp_path}/test_logs.db"
    db = Database(db_url)
    await db.init_db()
    logger = AsyncLogger(db)

    # We'll mock out the ZeroShotAnalyzer's analyze_message
    # so we can verify how it's called with context.
    with patch.object(ZeroShotAnalyzer, 'analyze_message', return_value={
        "role": "customer",
        "text": "Hello",
        "sentiment": "positive",
        "intent": "greeting"
    }) as mock_analyze:
        analyzer = ZeroShotAnalyzer("fake-model", "cpu")
        conv_manager = ConversationalManager(analyzer, logger, context_window=2)

        # Simulate two messages in a conversation:
        await conv_manager.process_utterance("customer", "Hello, I'd like to upgrade.")
        await conv_manager.process_utterance("agent", "Sure, can I have your account number?")

        # Check that 'analyze_message' was called with context
        assert mock_analyze.call_count == 2, "Expected two calls to analyze_message"
        # The second call should have included the first turn in context
        # Because context_window=2, it should combine the last message with the current text
        args_list = mock_analyze.call_args_list
        # The last call (2nd message)
        _, kwargs_second = args_list[-1]
        # The 'text' passed is the combined context
        context_text = kwargs_second["text"]
        assert "customer: Hello, I'd like to upgrade." in context_text
        assert "current_user: Sure, can I have your account number?" in context_text

    # Verify we inserted two logs
    async with db.async_session() as session:
        result = await session.execute("SELECT COUNT(*) FROM logs")
        count = result.scalar()
        assert count == 2, f"Expected 2 records in logs, got {count}"
