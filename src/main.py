import asyncio
import configparser
import json
import os
import sys

from src.db import Database
from src.logger import AsyncLogger
from src.sentiment_intent_analyzer import ZeroShotAnalyzer

async def main() -> None:
    """
    Main async entry point for Task 1 approach.
    - Reads config, DB, conversation data
    - Does zero-shot classification per utterance
    - Logs to DB
    """
    # 1) READ CONFIG
    config = configparser.ConfigParser()
    config_path = os.path.join("config", "model_config.ini")
    if not os.path.exists(config_path):
        print(f"Error: {config_path} not found.")
        sys.exit(1)
    config.read(config_path)

    model_name = config["DEFAULT"].get("model_name", "facebook/bart-large-mnli")
    device = config["DEFAULT"].get("device", "cpu")
    db_url = config["DEFAULT"].get("db_url", "sqlite+aiosqlite:///./logs.db")

    # 2) INIT DATABASE
    db = Database(db_url)
    await db.init_db()
    logger = AsyncLogger(db)

    # 3) CREATE ZERO-SHOT ANALYZER
    analyzer = ZeroShotAnalyzer(model_name=model_name, device=device)

    # 4) LOAD CONVERSATION DATA
    data_path = os.path.join("data", "conversation.json")
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found.")
        sys.exit(1)

    with open(data_path, "r", encoding="utf-8") as f:
        conversation_data = json.load(f)

    conversation = conversation_data.get("conversation", [])
    if not conversation:
        print(f"No conversation data found in {data_path}.")
        sys.exit(1)

    # 5) PROCESS EACH UTTERANCE & LOG
    for turn in conversation:
        role = turn.get("role", "unknown")
        text = turn.get("text", "")

        if not text:
            continue

        analysis = analyzer.analyze_message(role, text)
        await logger.log_message(
            role=analysis["role"],
            text=analysis["text"],
            sentiment=analysis["sentiment"],
            intent=analysis["intent"]
        )

    print("Conversation analysis complete and logged to DB!")

if __name__ == "__main__":
    asyncio.run(main())
