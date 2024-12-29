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

**Actions** covered:

- **Action 1**: Build a codebase that reads conversation data, performs sentiment & intent detection with zero-shot learning, and logs results in a DB.
- **Action 2**: Propose quick solutions to adapt the system into a more conversational AI approach (while keeping the BART model the same).

---

## Project Structure
```bash
my-chat-analytic/
├── README.md
├── requirements.txt
├── setup.py
├── config
│   └── model_config.ini
├── data
│   └── conversation.json
├── resources
│   └── README.md
├── src
│   ├── __init__.py
│   ├── db.py
│   ├── logger.py
│   ├── sentiment_intent_analyzer.py
│   ├── main.py
│   └── conversational_manager.py   <-- (Advanced conversation logic)
└── notebooks
    └── task2_conversational_demo.ipynb  <-- (Jupyter Notebook)
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
### TASK 1
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
### TASK 2

1. Start Jupyter:
```bash
jupyter notebook
```
2. Open notebooks/task2_conversational_demo.ipynb.
3. Run the cells in order. The notebook will demonstrate how we can add a simple context window, maintain session data, and classify each message with a more “conversational” approach (still using facebook/bart-large-mnli zero-shot classification).


## Task 2: Quick Solutions (Recap)
1. Context Window
Combine the last N user or agent messages with the current one for classification, providing a short conversation history.

2. State Machine / Rule-based
A simple state machine or set of rules can guide the conversation flow based on the zero-shot-detected intent.

3. Session-based Memory
Track which user session is active and store relevant context or conversation history in memory or a DB.

4. Keyword/Rule Hybrid
If zero-shot occasionally misfires, a small library of domain-specific keywords can confirm or override intent predictions.

All of these are optional expansions beyond the core zero-shot classification approach. The notebook in notebooks/task2_conversational_demo.ipynb showcases how to apply them in code.

## Contributing

1. Fork the repository.
2. Create a new branch (git checkout -b feature/awesome-feature).
3. Commit your changes (git commit -m "Add awesome feature").
4. Push to the branch (git push origin feature/awesome-feature).
5. Open a Pull Request.

## License
MIT License

Feel free to adapt or extend the code as needed.
