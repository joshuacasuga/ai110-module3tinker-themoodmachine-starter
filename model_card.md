Model Card: Mood Machine

This card covers both versions of the classifier: the rule based model in
mood_analyzer.py and the machine learning model in ml_experiments.py. Both were
run on the same 14 posts in dataset.py.


1. Model Overview

Model type: I built and compared both models.

Intended purpose: classify short social media style posts as positive,
negative, neutral, or mixed.

How it works: The rule based model scores text by counting positive and
negative signals. Each positive word adds 1 and each negative word subtracts 1.
A negation word like not or never flips the next signal. Emojis and emoticons
count as signals too. The total score becomes the label: above zero is positive,
below zero is negative, zero is neutral. The ML model turns each post into a
bag of word counts with CountVectorizer and fits a logistic regression on the
labels, so it learns which words tend to go with which label instead of being
told.


2. Data

Dataset description: I started with 6 posts and added 8 more for a total of 14.
The new ones use realistic language: slang (lowkey, highkey, no cap), emojis and
emoticons, sarcasm, and mixed feelings.

Labeling process: I labeled by the meaning a person would read, not the words
on the page. That is why I absolutely love getting stuck in traffic is labeled
negative even though it contains love. A few were genuinely hard. idk lowkey sad
but whatever could be negative or mixed depending on how much weight you give
whatever. it is not the worst thing ever could be neutral or mixed.

Important characteristics: contains slang, emojis, sarcasm, and several posts
that mix one positive and one negative feeling in the same sentence.

Possible issues: the dataset is tiny (14 posts) and leans toward casual young
internet English. There are more mixed examples than a real feed would have,
because I was deliberately probing edge cases.


3. How the Rule Based Model Works

Scoring rules: positive word +1, negative word -1. preprocess lowercases,
strips punctuation off normal words, keeps emoticons like :) and :( whole, and
splits emoji characters into their own tokens. score_text loops the tokens and
adds up the signals. The enhancement I chose was negation handling plus emoji
and emoticon signals: not bad scores +1, and :( or an angry emoji counts as
negative. I also added three slang positives (fire, lit, sick) to the word list
after testing.

Strengths: predictable and easy to explain. It does well on direct statements
with a clear keyword, like Today was a terrible day or no cap this is the best
day ever, and the negation rule correctly handles I am not happy about this.

Weaknesses: it cannot do sarcasm, it ignores any word not in the list, and a
single score cannot represent mixed. It scored 0.64 on the 14 posts, and every
miss was a mixed or sarcastic post.


4. How the ML Model Works

Features: bag of words counts from CountVectorizer.

Training data: trained on all 14 SAMPLE_POSTS and TRUE_LABELS.

Training behavior: it reached 1.00 accuracy, but this is training accuracy
measured on the exact posts it learned from, so it is mostly memorization. With
only 14 examples it can fit them perfectly without learning anything general.

Strengths and weaknesses: it picks up patterns on its own, including the mixed
posts the rule based model could not handle. The weakness is that it is fragile
and label dependent. A new post with words it has never seen will fall back to
whatever those words happened to mean in the tiny training set.


5. Evaluation

How evaluated: both models were run on the 14 labeled posts in dataset.py.
Rule based accuracy was 0.64. ML training accuracy was 1.00.

Correct predictions (rule based): I love this class so much went positive on the
word love. Today was a terrible day went negative on terrible. I am not happy
about this went negative because the negation rule flipped happy.

Incorrect predictions (rule based): Lowkey stressed but kind of proud of myself
was predicted negative but is mixed, because stressed scores -1 and proud is not
in the word list, so only the negative half is seen. kinda nervous kinda hyped
for tomorrow was predicted neutral but is mixed, because neither nervous nor
hyped is in the lists, so the score stays 0. The ML model got both of these
right because it learned them directly from the labels.


6. Limitations

The dataset is very small, so any accuracy number is shaky. The rule based model
cannot detect sarcasm: I absolutely love getting stuck in traffic scores +1 and
is called positive when it is clearly negative. It also depends entirely on the
word list, so unfamiliar slang scores 0. A single sentiment score cannot express
mixed feelings at all. The ML model looks perfect only because it was tested on
its own training data; it has not been shown to generalize.

Note on breakers: in Part 4 the slang fix helped (sick and fire went from
neutral to positive with no regressions on the other posts), but adding sick is
risky. It is positive as slang but negative literally, so a sentence like I am
home sick and miserable would now get a wrong positive bump. Fixing one case
quietly created the conditions for a future one.


7. Ethical Considerations

Mood detection on personal messages is sensitive. Misreading a distressed
message as neutral or positive could matter if a tool used this to decide who
needs help. There is also a bias and scope problem. My dataset is casual,
emoji heavy, English internet slang, so the model is optimized for people who
write that way. It would likely misread more formal writing, other dialects,
non English text, or older users who do not use these slang terms and emojis.
Words like sick or fire mean the opposite of their dictionary meaning only
inside one cultural context, and the model bakes that assumption in. Analyzing
private messages at all raises consent and privacy questions.


8. Ideas for Improvement

Add far more labeled data and split it into separate train and test sets so the
ML accuracy is honest. Track positive and negative hits separately so the rule
based model can actually output mixed. Try TF IDF instead of raw counts. Build a
real lexicon for slang and emojis with weights. Handle context for ambiguous
words like sick. None of these solve sarcasm, which needs a model that
understands context rather than counting words.


Comparison summary

The two models failed in different ways. The rule based model is transparent and
you can read exactly why it chose a label, but it is blind to anything outside
its word list and cannot represent mixed, so it landed at 0.64. The ML model fit
all 14 posts including the mixed ones and hit 1.00, but that number is
misleading because it was graded on its own training data. It did fix the mixed
failures without me writing any rules, which is the appeal of learning from
examples. It also introduced a new risk: it is only as good as my 14 labels, and
it would likely break on any wording it has not seen. Neither model handles
sarcasm.
