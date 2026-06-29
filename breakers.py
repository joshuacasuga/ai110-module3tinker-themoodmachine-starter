"""
Breaker sentences: realistic language designed to confuse the Mood Machine.

Run with:  python breakers.py
"""

from mood_analyzer import MoodAnalyzer

# (sentence, what a human would say, why it's hard)
BREAKERS = [
    ("I love getting stuck in traffic",        "negative", "sarcasm hiding behind 'love'"),
    ("That movie was sick",                     "positive", "slang: 'sick' = great"),
    ("This party is fire",                       "positive", "slang: 'fire' = great"),
    ("wicked good show tonight",                 "positive", "slang: 'wicked' = very"),
    ("I'm fine 🙂",                              "neutral",  "flat words + ambiguous emoji"),
    ("I'm exhausted but proud of myself",        "mixed",    "two opposite feelings"),
    ("not bad at all honestly",                  "positive", "double negation -> positive"),
    ("great. just great.",                       "negative", "sarcastic repetition of a positive word"),
]


def main() -> None:
    analyzer = MoodAnalyzer()
    print("=== Breaker Run ===\n")
    for text, human, why in BREAKERS:
        predicted = analyzer.predict_label(text)
        reason = analyzer.explain(text)
        flag = "OK " if predicted == human else "MISS"
        print(f"[{flag}] {text!r}")
        print(f"       predicted={predicted}  human={human}  ({why})")
        print(f"       {reason}\n")


if __name__ == "__main__":
    main()
