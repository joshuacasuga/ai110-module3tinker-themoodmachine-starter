"""
Shared data for the Mood Machine lab.

This file defines:
  - POSITIVE_WORDS: starter list of positive words
  - NEGATIVE_WORDS: starter list of negative words
  - SAMPLE_POSTS: short example posts for evaluation and training
  - TRUE_LABELS: human labels for each post in SAMPLE_POSTS
"""

# ---------------------------------------------------------------------
# Starter word lists
# ---------------------------------------------------------------------

POSITIVE_WORDS = [
    "happy",
    "great",
    "good",
    "love",
    "excited",
    "awesome",
    "fun",
    "chill",
    "relaxed",
    "amazing",
    # Slang positives (added to fix the "sick"/"fire" breaker failure).
    # NOTE: "sick" is risky — it's positive as slang ("that's sick!") but
    # negative literally ("I feel sick"). Watch for that regression.
    "fire",
    "lit",
    "sick",
]

NEGATIVE_WORDS = [
    "sad",
    "bad",
    "terrible",
    "awful",
    "angry",
    "upset",
    "tired",
    "stressed",
    "hate",
    "boring",
]

# ---------------------------------------------------------------------
# Starter labeled dataset
# ---------------------------------------------------------------------

# Short example posts written as if they were social media updates or messages.
SAMPLE_POSTS = [
    "I love this class so much",
    "Today was a terrible day",
    "Feeling tired but kind of hopeful",
    "This is fine",
    "So excited for the weekend",
    "I am not happy about this",
    "Lowkey stressed but kind of proud of myself",
    "I absolutely love getting stuck in traffic",
    "no cap this is the best day ever :)",
    "highkey not okay today :(",
    "this song hits different 😂",
    "idk lowkey sad but whatever",
    "this meeting could've been an email 💀",
    "kinda nervous kinda hyped for tomorrow 🥲",
]

# Human labels for each post above.
# Allowed labels in the starter:
#   - "positive"
#   - "negative"
#   - "neutral"
#   - "mixed"
TRUE_LABELS = [
    "positive",  # "I love this class so much"
    "negative",  # "Today was a terrible day"
    "mixed",     # "Feeling tired but kind of hopeful"
    "neutral",   # "This is fine"
    "positive",  # "So excited for the weekend"
    "negative",  # "I am not happy about this"
    "mixed",     # "Lowkey stressed but kind of proud of myself" — "stressed" (neg) + "proud" (pos) in one breath
    "negative",  # "I absolutely love getting stuck in traffic" — sarcasm; "love" looks positive but means the opposite
    "positive",  # "no cap this is the best day ever :)" — slang + ":)" + "best ever" all point positive
    "negative",  # "highkey not okay today :(" — "not okay" + ":(" ; "okay" could fool a keyword model via negation
    "positive",  # "this song hits different 😂" — "hits different" = strong praise; no dictionary keyword to match on
    "mixed",     # "idk lowkey sad but whatever" — EDGE CASE: "sad" (neg) softened by dismissive "whatever"; could argue negative
    "negative",  # "this meeting could've been an email 💀" — dry complaint; 💀 + no positive words
    "mixed",     # "kinda nervous kinda hyped for tomorrow 🥲" — "nervous" (neg) and "hyped" (pos) held together
]

# TODO: Add 5-10 more posts and labels.
#
# Requirements:
#   - For every new post you add to SAMPLE_POSTS, you must add one
#     matching label to TRUE_LABELS.
#   - SAMPLE_POSTS and TRUE_LABELS must always have the same length.
#   - Include a variety of language styles, such as:
#       * Slang ("lowkey", "highkey", "no cap")
#       * Emojis (":)", ":(", "🥲", "😂", "💀")
#       * Sarcasm ("I absolutely love getting stuck in traffic")
#       * Ambiguous or mixed feelings
#
# Tips:
#   - Try to create some examples that are hard to label even for you.
#   - Make a note of any examples that you and a friend might disagree on.
#     Those "edge cases" are interesting to inspect for both the rule based
#     and ML models.
#
# Example of how you might extend the lists:
#
# SAMPLE_POSTS.append("Lowkey stressed but kind of proud of myself")
# TRUE_LABELS.append("mixed")
#
# Remember to keep them aligned:
#   len(SAMPLE_POSTS) == len(TRUE_LABELS)
