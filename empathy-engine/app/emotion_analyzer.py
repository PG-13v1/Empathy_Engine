# app/emotion_analyzer.py

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class EmotionAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def detect_emotion(self, text: str) -> str:
        """
        Analyzes text and returns emotional category: 'positive', 'negative', or 'neutral'
        
        Args:
            text (str): Input text to analyze
            
        Returns:
            str: Emotional category
        """
        if not text.strip():
            return "neutral"
            
        # Get sentiment scores
        scores = self.analyzer.polarity_scores(text)
        compound = scores['compound']
        
        # Map compound score to emotional categories
        if compound >= 0.05:
            return "positive"
        elif compound <= -0.05:
            return "negative"
        else:
            return "neutral"

# Create singleton instance
_analyzer = None

def detect_emotion(text: str) -> str:
    """
    Helper function to use singleton analyzer instance
    """
    global _analyzer
    if _analyzer is None:
        _analyzer = EmotionAnalyzer()
    return _analyzer.detect_emotion(text)