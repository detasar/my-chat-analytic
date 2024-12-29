from typing import Dict
from transformers import pipeline

class ZeroShotAnalyzer:
    """
    This class encapsulates a zero-shot classification pipeline
    for both sentiment and intent analysis.
    """
    def __init__(self, model_name: str = "facebook/bart-large-mnli", device: str = "cpu"):
        """
        Initialize the zero-shot classification pipeline.

        :param model_name: The name of the Hugging Face model to load.
        :param device: 'cpu' or 'cuda' for GPU usage.
        """
        # By default, Hugging Face uses device index: -1 for CPU, 0 for GPU.
        device_index = -1 if device.lower() == "cpu" else 0

        self.classifier = pipeline(
            "zero-shot-classification",
            model=model_name,
            device=device_index
        )

    def predict_sentiment(self, text: str) -> str:
        """
        Predict sentiment (positive, negative, neutral) using zero-shot classification.
        """
        candidate_labels = ["positive", "negative", "neutral"]
        result = self.classifier(text, candidate_labels)
        return result["labels"][0]  # Highest-scored label

    def predict_intent(self, text: str) -> str:
        """
        Predict intent from a custom set of candidate labels using zero-shot classification.
        """
        candidate_labels = [
            "upgrade",
            "ask_price",
            "buy",
            "change_package",
            "greeting",
            "ask_color",
            "thank_you"
        ]
        result = self.classifier(text, candidate_labels)
        return result["labels"][0]  # Highest-scored label

    def analyze_message(self, role: str, text: str) -> Dict[str, str]:
        """
        Analyze a single message for sentiment and intent.
        """
        sentiment = self.predict_sentiment(text)
        intent = self.predict_intent(text)
        return {
            "role": role,
            "text": text,
            "sentiment": sentiment,
            "intent": intent
        }
