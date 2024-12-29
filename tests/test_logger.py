# tests/test_logger.py

import asyncio
import pytest
from src.db import Database
from src.logger import AsyncLogger

@pytest.mark.asyncio
async def test_async_logger(tmp_path):
    """
    Tests the AsyncLogger to ensure it correctly calls DB insertion.
    """
    db_url = f"sqlite+aiosqlite:///{tmp_path}/test_logs.db"
    db = Database(db_url)
    await db.init_db()

    logger = AsyncLogger(db)

    # Insert a sample log
    await logger.log_message(
        role="customer",
        text="Hello, I'd like an upgrade.",
        sentiment="positive",
        intent="upgrade"
    )

    # Verify
    async with db.async_session() as session:
        result = await session.execute("SELECT role, text, sentiment, intent FROM logs")
        row = result.fetchone()
        assert row is not None, "Expected a log entry"
        assert row.role == "customer"
        assert row.text == "Hello, I'd like an upgrade."
        assert row.sentiment == "positive"
        assert row.intent == "upgrade"
