import asyncio
from typing import Optional
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Table, MetaData

# Define metadata for the logs table
metadata = MetaData()

# Table definition
LogsTable = Table(
    "logs",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("role", String, nullable=False),
    Column("text", String, nullable=False),
    Column("sentiment", String, nullable=False),
    Column("intent", String, nullable=False)
)

class Database:
    """
    Database class managing the async connection and operations using SQLAlchemy.
    """
    def __init__(self, db_url: str):
        """
        Constructor for Database.

        :param db_url: Async DB URL (e.g., sqlite+aiosqlite:///./logs.db)
        """
        self.engine = create_async_engine(db_url, echo=False)
        self.async_session = sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def init_db(self) -> None:
        """
        Initializes the database by creating tables if they do not exist.
        """
        async with self.engine.begin() as conn:
            await conn.run_sync(metadata.create_all)

    async def insert_log(
        self,
        role: str,
        text: str,
        sentiment: str,
        intent: str
    ) -> None:
        """
        Inserts a single record into the logs table.
        """
        async with self.async_session() as session:
            stmt = LogsTable.insert().values(
                role=role,
                text=text,
                sentiment=sentiment,
                intent=intent
            )
            await session.execute(stmt)
            await session.commit()
