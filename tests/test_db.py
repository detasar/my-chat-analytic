# tests/test_db.py

import asyncio
import pytest
from src.db import Database

@pytest.mark.asyncio
async def test_database_init_and_insert(tmp_path):
    """
    Tests database initialization and record insertion.
    We use a temporary SQLite DB file to avoid polluting the real logs.db.
    """
    # Construct an in-memory or temporary DB URL
    db_url = f"sqlite+aiosqlite:///{tmp_path}/test_logs.db"
    db = Database(db_url)

    # 1) Initialize DB
    await db.init_db()

    # 2) Insert a sample record
    await db.insert_log(
        role="agent",
        text="Test message",
        sentiment="neutral",
        intent="greeting"
    )

    # 3) Check if the record was inserted
    # We'll open a new async session to query the logs table.
    async with db.async_session() as session:
        result = await session.execute("SELECT COUNT(*) FROM logs")
        count = result.scalar()
        assert count == 1, "Expected exactly 1 record in the logs table"
