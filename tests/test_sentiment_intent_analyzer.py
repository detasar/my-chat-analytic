# tests/test_sentiment_intent_analyzer.py

import pytest
from unittest.mock import patch
from src.sentiment_intent_analyzer import ZeroShotAnalyzer

@pytest.mark.parametrize(
    "text_input, expected_sentiment_label",
    [
        ("I love this product!", "positive"),
        ("This is awful, I hate it", "negative"),
        ("It is okay, not good, not bad", "neutral")
    ]
)
def test_predict_sentiment_mocked(text_input, expected_sentiment_label):
    """
    Test the ZeroShotAnalyzer's predict_sentiment with a mock pipeline.
    We don't want to load the real model in unit tests for speed.
    """
    with patch("src.sentiment_intent_analyzer.pipeline") as mock_pipeline:
        # Setup mock return
        mock_pipeline.return_value = lambda text, labels: {
            "labels": [expected_sentiment_label]
        }

        analyzer = ZeroShotAnalyzer(model_name="fake-model", device="cpu")
        sentiment = analyzer.predict_sentiment(text_input)
        assert sentiment == expected_sentiment_label

@pytest.mark.parametrize(
    "text_input, expected_intent_label",
    [
        ("How much does it cost?", "ask_price"),
        ("I want to upgrade my plan.", "upgrade"),
        ("Thank you for your help!", "thank_you"),
    ]
)
def test_predict_intent_mocked(text_input, expected_intent_label):
    """
    Test the ZeroShotAnalyzer's predict_intent with a mock pipeline.
    """
    with patch("src.sentiment_intent_analyzer.pipeline") as mock_pipeline:
        mock_pipeline.return_value = lambda text, labels: {
            "labels": [expected_intent_label]
        }

        analyzer = ZeroShotAnalyzer(model_name="fake-model", device="cpu")
        intent = analyzer.predict_intent(text_input)
        assert intent == expected_intent_label
