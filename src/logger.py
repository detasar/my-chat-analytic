from src.db import Database

class AsyncLogger:
    """
    The AsyncLogger handles asynchronous logging to the database.
    """
    def __init__(self, db: Database):
        self.db = db

    async def log_message(
        self,
        role: str,
        text: str,
        sentiment: str,
        intent: str
    ) -> None:
        """
        Logs a single message asynchronously by calling insert_log on the database.
        """
        await self.db.insert_log(
            role=role,
            text=text,
            sentiment=sentiment,
            intent=intent
        )
