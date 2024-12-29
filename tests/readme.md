# Testing Notes

- All tests use `pytest` plus `pytest-asyncio` for asynchronous test functions.
- We frequently use Python's `unittest.mock.patch` to avoid loading the
  large `facebook/bart-large-mnli` model in unit tests, which helps
  keep tests fast and isolated.
- For **integration testing** or **system testing**, you could remove
  the mocks so that the real model pipeline is loaded. However, be aware
  these tests may be slower and require GPU/CPU resources.

## With these tests:

`test_db.py` and `test_logger.py` confirm our asynchronous DB logging logic.
`test_sentiment_intent_analyzer.py` ensures correct sentiment/intent labels (mocked pipeline).
`test_conversational_manager.py` ensures the new context-based approach (Task 2) works and logs properly.

How to Run the Tests
Make sure pytest is installed:
```bash
pip install pytest
```
From the root of your project (the same level as tests/ and src/), run:
```bash
pytest tests
```
You should see all tests pass.
* If you want more detail, use: `pytest -v --asyncio-mode=auto`
* Or for coverage: `coverage run -m pytest tests` then `coverage report -m`.
