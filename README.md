# my-chat-analytic

**Author**: Emre Tasar (GitHub: [detasar](https://github.com/detasar))  
**Purpose**: Demonstration of **Zero-Shot Sentiment** and **Intent** analysis on a conversation regarding purchasing an iPhone14.

---

## Overview

This repository implements:
1. A simulated conversation (approx. 20 steps) in **JSON** format between a customer and an agent.
2. A zero-shot classification pipeline using **Hugging Face**'s `facebook/bart-large-mnli` model:
   - **Sentiment**: `positive`, `negative`, `neutral`
   - **Intent**: e.g., `upgrade`, `ask_price`, `buy`, etc.
3. **Asynchronous** logging of conversation data (role, text, sentiment, intent) to a database (SQLite in this example).
4. A Python packaging structure including `setup.py`, allowing easy installation and distribution.

**Tasks** covered:

- **Task 1**: Build a codebase that reads conversation data, performs sentiment & intent detection with zero-shot learning, and logs results in a DB.
- **Task 2**: Propose quick solutions to adapt the system into a more conversational AI approach (while keeping the BART model the same).

---

## Project Structure
```bash
my-chat-analytic/
├── README.md                      # This README file
├── requirements.txt               # Required dependencies
├── setup.py                       # Makes the project installable as a Python package
├── config
│   └── model_config.ini           # Model & DB configuration
├── data
│   └── conversation.json          # Simulated conversation data
├── resources
│   └── README.md                  # Additional notes about the model
└── src
    ├── __init__.py
    ├── db.py                      # Async DB logic (SQLAlchemy)
    ├── logger.py                  # Async logger to insert logs into DB
    ├── sentiment_intent_analyzer.py   # Zero-shot pipeline logic
    └── main.py                    # Main script that orchestrates the flow
```


### How It Works

1. **`main.py`** reads configuration from `config/model_config.ini`, which tells it:
   - Which Hugging Face model to load (default: `facebook/bart-large-mnli`)
   - Whether to use CPU or GPU
   - Which async DB URL to connect to
2. **`main.py`** then reads `data/conversation.json`, which contains a 20-step dialogue.
3. For each message, we use `sentiment_intent_analyzer.ZeroShotAnalyzer`:
   - **Sentiment**: Zero-shot classification among `positive`, `negative`, `neutral`.
   - **Intent**: Zero-shot classification among specified custom labels (e.g. `upgrade`, `ask_price`, `buy`, etc.).
4. **`logger.py`** asynchronously logs each record (role, text, sentiment, intent) to a database table named `logs`.
5. Console output indicates completion, and a `logs.db` file is created locally (if SQLite is used).

---

## Installation

1. **Clone** this repository:
   ```bash
   git clone https://github.com/detasar/my-chat-analytic.git
2. **Install** the required packages:
```bash
pip install -r requirements.txt
```
3. **(Optional)** Build & install as a local package:
```bash
python setup.py sdist bdist_wheel
pip install dist/my_chat_analytic-0.1.0-py3-none-any.whl
```

## Usage
1. Ensure you have your model_config.ini in config/ and your conversation data in data/conversation.json.
2. Run the application:
```bash
python -m src.main
```
3. You should see:
```css
Conversation analysis complete and logged to DB!
```
4. A logs.db file (SQLite) will be created in your project folder. You can inspect it using any SQLite client:
```sql
SELECT * FROM logs;
```

## Quick Solutions for a More Conversational AI

1. Context Window: Pass not just the current utterance but also the previous 1-3 messages as a single text block into the zero-shot classifier. This helps the model interpret context more accurately (though BART MNLI is not fine-tuned for multi-turn).
2. State Machine / Rule-based enhancements: Maintain a simple state machine or set of rules that, if the user’s intent is ask_price, you trigger a “pricing” flow. If the user’s intent is upgrade, you trigger an “upgrade plan” flow, etc.
3. Session-based Memory: Maintain a session ID for each user to accumulate conversation history. Even if the zero-shot model is stateless, you can keep relevant info in memory or a database and pass partial context on each inference.
4. Hybrid Approach: Combine zero-shot results with keyword or regex triggers to catch domain-specific phrases (e.g., “iPhone 14”, “change plan”). This can override or confirm the zero-shot classification.

## Contributing

1. Fork the repository.
2. Create a new branch (git checkout -b feature/awesome-feature).
3. Commit your changes (git commit -m "Add awesome feature").
4. Push to the branch (git push origin feature/awesome-feature).
5. Open a Pull Request.

## License
MIT License

Feel free to adapt or extend the code as needed.
