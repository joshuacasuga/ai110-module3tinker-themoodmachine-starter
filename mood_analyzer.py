# mood_analyzer.py
"""
Rule based mood analyzer for short text snippets.

This class starts with very simple logic:
  - Preprocess the text
  - Look for positive and negative words
  - Compute a numeric score
  - Convert that score into a mood label
"""

import string
from typing import List, Dict, Tuple, Optional

from dataset import POSITIVE_WORDS, NEGATIVE_WORDS


class MoodAnalyzer:
    """
    A very simple, rule based mood classifier.
    """

    # Emoticons made of punctuation. We list them explicitly so preprocess
    # keeps them intact instead of stripping the ":" and ")" as punctuation.
    POSITIVE_EMOTICONS = {":)", ":-)", ":d", ";)", ":p"}
    NEGATIVE_EMOTICONS = {":(", ":-(", ":'(", ":/"}

    # Single-character emoji signals. Kept simple and explicit on purpose.
    POSITIVE_EMOJI = {"😂", "🎉", "💪", "🌱", "🥰", "😊", "❤"}
    NEGATIVE_EMOJI = {"😩", "💀", "😭", "😡", "😞"}

    # Words that flip the meaning of the word right after them ("not happy").
    NEGATIONS = {"not", "no", "never", "dont", "don't", "isnt", "isn't",
                 "cant", "can't", "wasnt", "wasn't", "aint", "ain't"}

    def __init__(
        self,
        positive_words: Optional[List[str]] = None,
        negative_words: Optional[List[str]] = None,
    ) -> None:
        # Use the default lists from dataset.py if none are provided.
        positive_words = positive_words if positive_words is not None else POSITIVE_WORDS
        negative_words = negative_words if negative_words is not None else NEGATIVE_WORDS

        # Store as sets for faster lookup.
        self.positive_words = set(w.lower() for w in positive_words)
        self.negative_words = set(w.lower() for w in negative_words)

    # ---------------------------------------------------------------------
    # Preprocessing
    # ---------------------------------------------------------------------

    def preprocess(self, text: str) -> List[str]:
        """
        Convert raw text into a list of tokens the model can work with.

        TODO: Improve this method.

        Right now, it does the minimum:
          - Strips leading and trailing whitespace
          - Converts everything to lowercase
          - Splits on spaces

        Ideas to improve:
          - Remove punctuation
          - Handle simple emojis separately (":)", ":-(", "🥲", "😂")
          - Normalize repeated characters ("soooo" -> "soo")

        This version:
          - lowercases and splits on whitespace
          - keeps known emoticons (":)", ":(") as whole tokens
          - peels emoji characters off into their own tokens
          - strips surrounding punctuation from ordinary words
        """
        cleaned = text.strip().lower()
        tokens: List[str] = []

        for raw in cleaned.split():
            # Keep emoticons exactly as-is; their punctuation IS the signal.
            if raw in self.POSITIVE_EMOTICONS or raw in self.NEGATIVE_EMOTICONS:
                tokens.append(raw)
                continue

            # Walk the characters, splitting emojis out as standalone tokens.
            word_chars: List[str] = []
            for ch in raw:
                if self._is_emoji(ch):
                    word = "".join(word_chars).strip(string.punctuation)
                    if word:
                        tokens.append(word)
                    word_chars = []
                    tokens.append(ch)
                else:
                    word_chars.append(ch)

            word = "".join(word_chars).strip(string.punctuation)
            if word:
                tokens.append(word)

        return tokens

    @staticmethod
    def _is_emoji(ch: str) -> bool:
        """Rough check: is this character a pictographic emoji?"""
        code = ord(ch)
        return (
            0x1F300 <= code <= 0x1FAFF  # symbols, pictographs, emoticons, supplemental
            or 0x2600 <= code <= 0x27BF  # misc symbols & dingbats
            or code == 0x2764            # heavy black heart ❤
        )

    # ---------------------------------------------------------------------
    # Scoring logic
    # ---------------------------------------------------------------------

    def score_text(self, text: str) -> int:
        """
        Compute a numeric "mood score" for the given text.

        Positive words increase the score.
        Negative words decrease the score.

        TODO: You must choose AT LEAST ONE modeling improvement to implement.
        For example:
          - Handle simple negation such as "not happy" or "not bad"
          - Count how many times each word appears instead of just presence
          - Give some words higher weights than others (for example "hate" < "annoyed")
          - Treat emojis or slang (":)", "lol", "💀") as strong signals
        """
        tokens = self.preprocess(text)
        score = 0
        negate = False  # set True right after a negation word like "not"

        for token in tokens:
            # A negation word flips the NEXT scoring token, then we move on.
            if token in self.NEGATIONS:
                negate = True
                continue

            # Decide this token's raw contribution: +1, -1, or 0.
            value = 0
            if token in self.positive_words or token in self.POSITIVE_EMOTICONS \
                    or token in self.POSITIVE_EMOJI:
                value = 1
            elif token in self.negative_words or token in self.NEGATIVE_EMOTICONS \
                    or token in self.NEGATIVE_EMOJI:
                value = -1

            if value != 0:
                if negate:
                    value = -value  # "not happy" -> -1, "not bad" -> +1
                score += value

            # Negation only reaches across one token, so always reset it here.
            negate = False

        return score

    # ---------------------------------------------------------------------
    # Label prediction
    # ---------------------------------------------------------------------

    def predict_label(self, text: str) -> str:
        """
        Turn the numeric score for a piece of text into a mood label.

        The default mapping is:
          - score > 0  -> "positive"
          - score < 0  -> "negative"
          - score == 0 -> "neutral"

        TODO: You can adjust this mapping if it makes sense for your model.
        For example:
          - Use different thresholds (for example score >= 2 to be "positive")
          - Add a "mixed" label for scores close to zero
        Just remember that whatever labels you return should match the labels
        you use in TRUE_LABELS in dataset.py if you care about accuracy.
        """
        score = self.score_text(text)

        if score > 0:
            return "positive"
        if score < 0:
            return "negative"
        return "neutral"

    # ---------------------------------------------------------------------
    # Explanations (optional but recommended)
    # ---------------------------------------------------------------------

    def explain(self, text: str) -> str:
        """
        Return a short string explaining WHY the model chose its label.

        TODO:
          - Look at the tokens and identify which ones counted as positive
            and which ones counted as negative.
          - Show the final score.
          - Return a short human readable explanation.

        Example explanation (your exact wording can be different):
          'Score = 2 (positive words: ["love", "great"]; negative words: [])'

        The current implementation is a placeholder so the code runs even
        before you implement it.
        """
        tokens = self.preprocess(text)

        positive_hits: List[str] = []
        negative_hits: List[str] = []
        score = 0
        negate = False

        # Mirror score_text so the explanation matches the actual prediction.
        for token in tokens:
            if token in self.NEGATIONS:
                negate = True
                continue

            value = 0
            if token in self.positive_words or token in self.POSITIVE_EMOTICONS \
                    or token in self.POSITIVE_EMOJI:
                value = 1
            elif token in self.negative_words or token in self.NEGATIVE_EMOTICONS \
                    or token in self.NEGATIVE_EMOJI:
                value = -1

            if value != 0:
                if negate:
                    value = -value
                    token = f"not+{token}"  # show that negation flipped it
                score += value
                if value > 0:
                    positive_hits.append(token)
                else:
                    negative_hits.append(token)

            negate = False

        return (
            f"Score = {score} "
            f"(positive: {positive_hits or '[]'}, "
            f"negative: {negative_hits or '[]'})"
        )
