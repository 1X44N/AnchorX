import re
import random
import json
import os

_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(_DIR, "words.json"), "r", encoding="utf-8") as _f:
    DATA = json.load(_f)

REPS    = DATA["replacements"]
CONS    = DATA["contractions"]
FILLERS = DATA["fillers"]
OPENERS = DATA["openers"]

PATTERNS = [
    (r'[Ii]t is important to (\w+)',        lambda m: m.group(1).capitalize() + "ing this really matters"),
    (r'[Tt]his demonstrates? that',         "This shows that"),
    (r'^\s*[Ii]n conclusion[,.]?\s*',       "So when you step back, "),
    (r'^\s*[Ff]urthermore[,.]?\s*',         "Also, "),
    (r'^\s*[Mm]oreover[,.]?\s*',            "On top of that, "),
    (r'^\s*[Aa]dditionally[,.]?\s*',        "And, "),
    (r'^\s*[Cc]onsequently[,.]?\s*',        "So, "),
    (r'^\s*[Tt]herefore[,.]?\s*',           "So, "),
    (r'^\s*[Hh]ence[,.]?\s*',              "So, "),
    (r'^\s*[Tt]hus[,.]?\s*',              "So, "),
    (r'^\s*[Nn]evertheless[,.]?\s*',       "Still, "),
    (r'^\s*[Nn]onetheless[,.]?\s*',        "Still, "),
    (r'^\s*[Ss]ubsequently[,.]?\s*',       "Then, "),
    (r'[Ii]t is worth noting that\s*',     "Worth mentioning -- "),
    (r'[Tt]his can be seen in',            "You can see this in"),
    (r'plays? a (?:crucial|pivotal|key|vital|significant|major) role in', "really matters when it comes to"),
    (r"[Ii]n today'?s? (?:world|society|era|age|time|climate)", "These days"),
    (r'[Ii]n the (?:modern|contemporary|current) (?:world|era|age|society|times)', "Nowadays"),
    (r'[Oo]ne must consider',              "You really have to think about"),
    (r'[Ii]t can be argued that',          "You could say that"),
    (r'[Tt]his (?:essay|paper|report|study|analysis) (?:will |shall )?(?:explore|discuss|examine|analyze|consider|investigate|address)', "I want to talk about"),
    (r'is an? (?:complex|complicated|multifaceted|intricate) (?:topic|issue|subject|matter)', "is pretty complicated"),
    (r'[Tt]he use of (.+?) has increased significantly', r'More people are using \1 now'),
    (r'serves? as an?\b',                  "works as a"),
    (r'[Tt]here are a number of',          "There are a few"),
    (r'a wide range of',                   "lots of different"),
    (r'a variety of',                      "different kinds of"),
    (r'with the aim of',                   "to"),
    (r'with the purpose of',              "to"),
    (r'in an effort to',                   "trying to"),
    (r'in an attempt to',                  "trying to"),
    (r'[Ii]t is clear that',              "Clearly,"),
    (r'[Ii]t is obvious that',            "Obviously,"),
    (r'[Ii]t is evident that',            "Clearly,"),
    (r'[Ii]t should be noted that',       "Worth noting --"),
    (r'[Ii]t is interesting to note that',"Interestingly,"),
    (r'[Aa]s can be seen',                "As you can see"),
    (r'[Aa]s mentioned (?:above|previously|earlier|before)', "Like I said"),
    (r'has been shown to',                 "seems to"),
    (r'have been shown to',                "seem to"),
    (r'[Rr]esearch (?:shows|suggests|indicates|demonstrates) that', "Studies say that"),
    (r'[Ss]tudies have shown that',        "Research found that"),
    (r'[Aa]ccording to research',          "Based on studies"),
    (r'[Ii]t has been found that',         "People have found that"),
    (r'[Ii]t has been suggested that',     "Some people think that"),
    (r'[Dd]ue to the fact that',           "because"),
    (r'[Ii]n spite of the fact that',      "even though"),
    (r'[Dd]espite the fact that',          "even though"),
    (r'[Ii]n light of the fact that',      "since"),
    (r'[Ww]ith regard to',                 "When it comes to"),
    (r'[Ii]n terms of',                    "when it comes to"),
    (r'[Oo]n the basis of',                "based on"),
    (r'[Bb]y virtue of',                   "because of"),
    (r'[Ii]n the context of',             "in"),
    (r'[Aa]t the same time',              "also"),
    (r'[Ii]n addition[,]?',               "Also,"),
    (r'[Ff]irst and foremost',             "First of all"),
    (r'[Ll]ast but not least',             "And finally"),
    (r'[Aa]ll things considered',          "Overall"),
    (r'[Tt]o put it simply',              "Basically"),
    (r'[Tt]o put it another way',          "In other words"),
    (r'[Ii]n other words',                 "Basically"),
    (r'[Tt]hat being said[,]?',           "But"),
    (r'[Hh]aving said that[,]?',          "But"),
    (r'[Ww]ith that in mind[,]?',         "So"),
    (r'[Nn]eedless to say',                "Obviously"),
    (r'[Ii]t goes without saying (?:that)?', "Obviously"),
    (r'[Ww]ithout a doubt',               "definitely"),
    (r'[Mm]ore often than not',            "usually"),
    (r'[Ff]or all intents and purposes',   "basically"),
    (r'[Ii]n the final analysis',          "in the end"),
    (r'[Ww]hen all is said and done',      "at the end of the day"),
    (r'[Ff]or the most part',             "mostly"),
    (r'[Bb]y and large',                   "mostly"),
    (r'[Aa]s a whole',                     "overall"),
    (r'[Oo]n the whole',                   "overall"),
    (r'[Tt]o a (?:large|great|significant) extent', "mostly"),
    (r'[Tt]o a (?:certain|some) extent',   "kind of"),
    (r'[Ii]t is (?:also )?worth (?:mentioning|highlighting|emphasizing) that', "Also,"),
    (r'[Tt]his (?:highlights|underscores|emphasizes|illustrates|demonstrates)', "This shows"),
    (r'[Aa] (?:key|crucial|vital|critical|essential|fundamental) (?:aspect|element|component|factor|part)', "one important thing"),
    (r'[Tt]here is a (?:growing|increasing|rising) (?:need|demand|concern|awareness)', "more and more people need"),
    (r'[Tt]his is (?:particularly|especially|notably) (?:important|significant|relevant|crucial)', "this really matters"),
    (r'[Ii]t is (?:essential|crucial|vital|necessary|important) (?:to|that)', "you have to"),
    (r'[Oo]ne of the (?:most|key|main|primary|principal) (?:important|significant|crucial|vital)', "one of the biggest"),
    (r'[Hh]as a (?:significant|major|profound|substantial|considerable|dramatic) (?:impact|effect|influence)', "really affects things"),
    (r'[Tt]he (?:importance|significance|relevance|value|role) of', "how important"),
    (r'[Ii]t is widely (?:accepted|recognized|acknowledged|believed|known) that', "most people agree that"),
    (r'[Mm]any (?:experts|researchers|scholars|scientists|analysts) (?:believe|argue|suggest|claim|contend)', "experts think"),
    (r'[Rr]esearch has (?:shown|demonstrated|proven|indicated|suggested) that', "research shows that"),
    (r'[Ss]tudies have (?:shown|demonstrated|proven|indicated|suggested) that', "studies show that"),
    (r'[Ii]t is (?:generally|widely|commonly|broadly|universally) (?:accepted|agreed|recognized|acknowledged)', "most people agree"),
    (r'\butilize[sd]?\b',    "use"),
    (r'\butilizing\b',       "using"),
    (r'\bfacilitate[sd]?\b', "help"),
    (r'\bleverage[sd]?\b',   "use"),
    (r'\bdemonstrate[sd]?\b',"show"),
    (r'\bindicates?\b',      "shows"),
    (r'\bsubstantial\b',     "big"),
    (r'\bnumerous\b',        "many"),
    (r'\bpivotal\b',         "key"),
    (r'\bcrucial\b',         "important"),
    (r'\bvital\b',           "important"),
    (r'\bcritical\b',        "important"),
    (r'\bfundamental\b',     "basic"),
    (r'\bprofound\b',        "deep"),
    (r'\bmyriad\b',          "many"),
    (r'\bplethora\b',        "a lot"),
    (r'\bconsequently\b',    "so"),
    (r'\bsubsequently\b',    "then"),
    (r'\bhence\b',           "so"),
    (r'\bthus\b',            "so"),
    (r'\btherefore\b',       "so"),
    (r'\bnevertheless\b',    "still"),
    (r'\bnonetheless\b',     "still"),
    (r'\bfurthermore\b',     "also"),
    (r'\bmoreover\b',        "also"),
    (r'\badditionally\b',    "and"),
    (r'\bprimarily\b',       "mainly"),
    (r'\bultimately\b',      "in the end"),
    (r'\bspecifically\b',    "exactly"),
    (r'\bparticularly\b',    "especially"),
    (r'\bnotably\b',         "especially"),
    (r'\bcommonly\b',        "usually"),
    (r'\bgenerally\b',       "usually"),
    (r'\bcomprehensive\b',   "full"),
    (r'\bextensive\b',       "large"),
    (r'\bsystematic\b',      "organized"),
    (r'\bconsiderable\b',    "big"),
    (r'\bencompasses?\b',    "covers"),
    (r'\binherent\b',        "built-in"),
    (r'\bexhibits?\b',       "shows"),
    (r'\bobtains?\b',        "gets"),
    (r'\brequires?\b',       "needs"),
    (r'\bpossesses?\b',      "has"),
    (r'\bcommences?\b',      "starts"),
    (r'\bterminates?\b',     "ends"),
    (r'\bascertain\b',       "find out"),
    (r'\bconsequences?\b',   "results"),
    (r'\bimplements?\b',     "uses"),
    (r'\bimplemented\b',     "used"),
    (r'\bestablishes?\b',    "sets up"),
    (r'\bconstitutes?\b',    "makes up"),
]

AI_OPENERS_TO_REMOVE = [
    r'^\s*[Cc]ertainly[!,]?\s*',
    r'^\s*[Oo]f course[!,]?\s*',
    r'^\s*[Ss]ure[!,]?\s*',
    r'^\s*[Aa]bsolutely[!,]?\s*',
    r'^\s*[Gg]reat[!,]?\s*',
    r'^\s*[Hh]ere is (?:the )?(?:rewritten|humanized|revised).*?\n',
    r"^\s*[Hh]ere's (?:the )?(?:rewritten|humanized|revised).*?\n",
    r'^\s*[Rr]ewritten.*?:\s*\n',
    r'^\s*[Bb]elow is.*?\n',
    r'^\s*[Aa]s requested.*?\n',
    r"^\s*[Ii]'d be happy.*?\n",
    r'^\s*[Hh]appy to help.*?\n',
    r'^\s*[Aa]llow me.*?\n',
    r'^\s*[Ll]et me.*?\n',
]

HUMAN_CONNECTORS = [
    "and honestly,", "but here's the thing,",
    "which is kind of interesting,", "and that's actually",
    "but what's crazy is", "so basically,",
    "and i think that's why", "which makes sense when you think about it,",
    "but the thing is,", "and at the end of the day,",
    "and weirdly enough,", "which I didn't expect,",
    "and that kind of surprised me,", "so yeah,",
]

SHORT_PUNCHY = [
    "That's pretty much it.", "Makes sense, right?",
    "It's not that complicated.", "Pretty straightforward.",
    "And that's the main point.", "Simple as that.",
    "That's really all there is to it.", "Not rocket science.",
    "Kind of obvious when you think about it.",
    "That's the whole idea, really.",
    "Anyway, that's the gist of it.",
    "And yeah, that's basically it.",
    "Weird but true.", "Go figure.",
    "Just something worth keeping in mind.",
    "I think that's what it comes down to.",
    "Which, honestly, makes a lot of sense.",
    "And I think that says a lot.",
]

THOUGHT_STARTERS = [
    "I think ", "I feel like ", "I'd say ", "If you ask me, ",
    "Honestly, ", "To be honest, ", "Not gonna lie, ",
    "From what I've seen, ", "In my experience, ",
    "The way I see it, ", "From my perspective, ",
    "Personally, ", "If I'm being real, ",
    "Real talk, ", "Truth is, ",
    "I mean, ", "Look, ", "So here's the thing, ",
    "The thing is, ", "What I've noticed is ",
    "I've always thought ", "If I had to guess, ",
    "Call me biased, but ", "Between you and me, ",
    "I'll be honest, ", "This is just my take, but ",
]

RANDOM_SHORT_SENTENCES = [
    "It's a bit tricky, honestly.",
    "I get why people find it confusing.",
    "That part took me a while to wrap my head around.",
    "Not everyone realizes this.",
    "It's one of those things you don't really think about.",
    "Which is kind of a big deal.",
    "And that matters more than people think.",
    "Sounds simple, but it really isn't.",
    "Worth thinking about.",
    "That's the part most people miss.",
    "Took me a second to get it too.",
    "Which is kind of wild when you think about it.",
    "And that's not something people talk about enough.",
    "I didn't really get this at first either.",
    "It's actually simpler than it sounds.",
    "Once you see it, you can't unsee it.",
    "And I think that's what gets people confused.",
    "Funny how that works.",
    "You'd think it'd be obvious, but it's not.",
    "And honestly, that's kind of the point.",
]

# Synonym pools — randomly swap common words to different synonyms each pass.
# This creates "burstiness": the unpredictable word-choice variation that
# humans naturally have and AI text typically lacks.
SYNONYM_POOLS = [
    (r'\b(also)\b',    ["too", "as well", "plus", "on top of that"]),
    (r'\b(really)\b',  ["actually", "genuinely", "pretty", "quite", "super"]),
    (r'\b(big)\b',     ["huge", "major", "serious", "large", "massive"]),
    (r'\b(good)\b',    ["solid", "decent", "great", "nice", "strong"]),
    (r'\b(bad)\b',     ["rough", "poor", "not great", "messy"]),
    (r'\b(often)\b',   ["a lot", "regularly", "many times", "pretty frequently"]),
    (r'\b(many)\b',    ["a lot of", "tons of", "plenty of", "loads of", "quite a few"]),
    (r'\b(things)\b',  ["stuff", "aspects", "bits", "factors", "parts"]),
    (r'\b(people)\b',  ["folks", "everyone", "most of us", "users"]),
    (r'\b(problem)\b', ["issue", "trouble", "snag", "challenge", "headache"]),
    (r'\b(result)\b',  ["outcome", "effect", "end result", "payoff"]),
    (r'\b(change)\b',  ["shift", "adjustment", "tweak", "difference"]),
    (r'\b(clear)\b',   ["obvious", "plain", "easy to see", "straightforward"]),
    (r'\b(show)\b',    ["reveal", "point to", "make clear", "highlight", "prove"]),
    (r'\b(think)\b',   ["feel", "reckon", "believe", "suspect", "guess"]),
    (r'\b(need)\b',    ["have to", "must", "require"]),
    (r'\b(easy)\b',    ["simple", "not hard", "pretty doable", "a breeze"]),
    (r'\b(hard)\b',    ["tough", "tricky", "not easy", "a challenge"]),
    (r'\b(help)\b',    ["support", "assist", "make it easier", "back up"]),
    (r'\b(start)\b',   ["kick off", "begin", "jump into", "dive in"]),
    (r'\b(end)\b',     ["finish", "wrap up", "close out", "stop"]),
    (r'\b(make)\b',    ["create", "build", "put together", "form"]),
    (r'\b(work)\b',    ["function", "operate", "do the job", "hold up"]),
    (r'\b(get)\b',     ["grab", "pick up", "land", "score", "come by"]),
    (r'\b(use)\b',     ["rely on", "go with", "work with", "apply"]),
]


def strip_ai_openers(text):
    for pattern in AI_OPENERS_TO_REMOVE:
        text = re.sub(pattern, '', text, flags=re.MULTILINE)
    return text.strip()


def clean_symbols(text):
    text = text.replace("\u2014", ",").replace("\u2013", ",")
    text = text.replace("\u2015", ",").replace("\u2212", ",")
    text = text.replace(" - ", ", ").replace("--", ",")
    text = re.sub('["\u201c\u201d\u2018\u2019\u201a\u201e]', '', text)
    text = text.replace("''", "").replace('""', "")
    for b in ["\u2022", "\u00b7", "\u25aa", "\u25b8", "\u25ba", "\u2192",
              "\u2713", "\u2714", "\u2605", "\u25cf", "\u25cb", "\u25e6",
              "\u2023", "\u2043", "\u2219"]:
        text = text.replace(b, "")
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*',     r'\1', text)
    text = re.sub(r'__(.+?)__',     r'\1', text)
    text = re.sub(r'_(.+?)_',       r'\1', text)
    text = re.sub(r'^#{1,6}\s+',    '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*\d+\.\s+',  '', text, flags=re.MULTILINE)
    text = re.sub(r'-{2,}', '', text)
    text = re.sub(r'={2,}', '', text)
    text = text.replace(";", ".")
    text = text.replace("\u2026", "...")
    text = re.sub(r'\.{4,}', '...', text)
    return text


def apply_patterns(text):
    for pattern, replacement in PATTERNS:
        try:
            if callable(replacement):
                text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
            else:
                text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        except Exception:
            pass
    return text


def swap_words(text):
    for phrase, rep in sorted(REPS.items(), key=lambda x: -len(x[0])):
        if ' ' in phrase:
            text = re.sub(re.escape(phrase), rep, text, flags=re.IGNORECASE)
    for word, rep in REPS.items():
        if ' ' not in word:
            def fn(m, r=rep):
                w = m.group(0)
                return r[0].upper() + r[1:] if w[0].isupper() else r
            text = re.sub(r'\b' + re.escape(word) + r'\b', fn, text, flags=re.IGNORECASE)
    return text


def apply_synonym_pools(text):
    """
    Randomly replaces common words with different synonyms on each pass.
    Humans naturally vary their word choices unpredictably (high burstiness).
    AI text reuses the same words in predictable patterns (low burstiness).
    This function fixes that.
    """
    for pattern, synonyms in SYNONYM_POOLS:
        def replacer(m, syns=synonyms):
            if random.random() < 0.60:
                chosen = random.choice(syns)
                orig = m.group(0)
                if orig[0].isupper():
                    return chosen[0].upper() + chosen[1:]
                return chosen
            return m.group(0)
        try:
            text = re.sub(pattern, replacer, text, flags=re.IGNORECASE)
        except Exception:
            pass
    return text


def apply_contractions(text):
    contractions_map = {
        "do not":     "don't",
        "does not":   "doesn't",
        "did not":    "didn't",
        "cannot":     "can't",
        "will not":   "won't",
        "would not":  "wouldn't",
        "should not": "shouldn't",
        "could not":  "couldn't",
        "is not":     "isn't",
        "are not":    "aren't",
        "was not":    "wasn't",
        "were not":   "weren't",
        "have not":   "haven't",
        "has not":    "hasn't",
        "had not":    "hadn't",
        "I am":       "I'm",
        "I have":     "I've",
        "I will":     "I'll",
        "I would":    "I'd",
        "you are":    "you're",
        "you have":   "you've",
        "you will":   "you'll",
        "we are":     "we're",
        "we have":    "we've",
        "we will":    "we'll",
        "they are":   "they're",
        "they have":  "they've",
        "they will":  "they'll",
        "it is":      "it's",
        "it has":     "it's",
        "that is":    "that's",
        "that has":   "that's",
        "there is":   "there's",
        "here is":    "here's",
        "what is":    "what's",
        "who is":     "who's",
        "he is":      "he's",
        "she is":     "she's",
    }
    for formal, short in contractions_map.items():
        text = re.sub(r'\b' + re.escape(formal) + r'\b', short, text)
    if CONS:
        for formal, short in CONS.items():
            text = text.replace(formal, short)
    return text


def vary_sentence_length(sentences):
    result  = []
    lengths = [len(s.split()) for s in sentences]
    has_short = any(l < 8 for l in lengths)

    for i, sentence in enumerate(sentences):
        result.append(sentence)
        if i > 0 and i % random.randint(3, 5) == 0:
            result.append(random.choice(RANDOM_SHORT_SENTENCES))

    if not has_short and len(result) > 2:
        insert_pos = random.randint(1, len(result) - 1)
        result.insert(insert_pos, random.choice(SHORT_PUNCHY))

    return result


def nuclear_sentence_rebuild(text):
    paragraphs        = text.split('\n\n')
    output_paragraphs = []

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        raw       = re.split(r'(?<=[.!?])\s+', para)
        sentences = [s.strip() for s in raw if s.strip()]
        new_sentences = []

        for i, sentence in enumerate(sentences):
            words  = sentence.split()
            length = len(words)

            if length > 22 and random.random() < 0.85:
                split_words = [
                    'and', 'but', 'so', 'because', 'which',
                    'while', 'although', 'since', 'though',
                    'when', 'where', 'if', 'as', 'unless',
                    'until', 'after', 'before', 'whereas',
                    'however', 'yet', 'still',
                ]
                center     = length // 2
                split_done = False
                for offset in range(0, center - 3):
                    for d in [1, -1]:
                        idx = center + offset * d
                        if 5 <= idx <= length - 5:
                            if words[idx].lower() in split_words:
                                first  = ' '.join(words[:idx]).rstrip(',') + '.'
                                second = ' '.join(words[idx:])
                                second = second[0].upper() + second[1:]
                                new_sentences.append(first)
                                new_sentences.append(second)
                                split_done = True
                                break
                    if split_done:
                        break
                if not split_done:
                    mid    = length // 2
                    first  = ' '.join(words[:mid]) + '.'
                    second = ' '.join(words[mid:])
                    second = second[0].upper() + second[1:]
                    new_sentences.append(first)
                    new_sentences.append(second)
                continue

            if i > 0 and length > 5 and random.random() < 0.40:
                starter  = random.choice(THOUGHT_STARTERS)
                sentence = starter + sentence[0].lower() + sentence[1:]
                new_sentences.append(sentence)
                continue

            if length > 8 and random.random() < 0.35:
                filler     = random.choice(FILLERS) if FILLERS else "honestly"
                words_list = sentence.split()
                insert_at  = random.randint(2, min(7, len(words_list) - 2))
                words_list.insert(insert_at, filler + ",")
                sentence   = ' '.join(words_list)
                new_sentences.append(sentence)
                continue

            if i == len(sentences) - 1 and random.random() < 0.35:
                new_sentences.append(sentence)
                new_sentences.append(random.choice(SHORT_PUNCHY))
                continue

            if new_sentences and length < 12 and random.random() < 0.30:
                connector = random.choice(HUMAN_CONNECTORS)
                prev      = new_sentences[-1].rstrip('.')
                merged    = prev + ", " + connector + " " + sentence[0].lower() + sentence[1:]
                new_sentences[-1] = merged
                continue

            new_sentences.append(sentence)

        new_sentences = vary_sentence_length(new_sentences)

        if len(new_sentences) > 4 and random.random() < 0.45:
            mid = random.randint(2, len(new_sentences) - 2)
            p1  = ' '.join(new_sentences[:mid])
            p2  = ' '.join(new_sentences[mid:])
            output_paragraphs.append(p1)
            output_paragraphs.append(p2)
        else:
            output_paragraphs.append(' '.join(new_sentences))

    return '\n\n'.join(output_paragraphs)


def inject_personal_voice(text):
    paragraphs = text.split('\n\n')
    result     = []

    personal_injections = [
        "Honestly, I think ",
        "From what I can tell, ",
        "I've noticed that ",
        "In my view, ",
        "Personally, I feel like ",
        "I'd say ",
        "The way I see it, ",
        "Not gonna lie, ",
        "I mean, ",
        "If I'm being honest, ",
        "Between you and me, ",
        "Real talk, ",
    ]

    casual_transitions = [
        "Anyway, ",
        "So yeah, ",
        "Here's the thing, ",
        "Look, ",
        "And honestly, ",
        "The thing is, ",
        "I mean, ",
        "For what it's worth, ",
        "If you ask me, ",
        "And I think, ",
    ]

    for i, para in enumerate(paragraphs):
        para = para.strip()
        if not para:
            continue

        if i == 0 and not re.search(r'\bI\b', para):
            injection = random.choice(personal_injections)
            para = injection + para[0].lower() + para[1:]
        elif i > 0 and random.random() < 0.55 and not re.search(r'\bI\b', para):
            injection = random.choice(casual_transitions)
            para = injection + para[0].lower() + para[1:]

        result.append(para)

    return '\n\n'.join(result)


def break_paragraph_uniformity(text):
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    if len(paragraphs) < 2:
        return text

    result = []
    i = 0
    while i < len(paragraphs):
        para  = paragraphs[i]
        words = para.split()

        if (len(words) < 30 and i + 1 < len(paragraphs)
                and len(paragraphs[i + 1].split()) < 30
                and random.random() < 0.40):
            merged = para + " " + paragraphs[i + 1]
            result.append(merged)
            i += 2
            continue

        result.append(para)
        i += 1

    return '\n\n'.join(result)


def fix_spaces(text):
    text = re.sub(r' {2,}',       ' ',    text)
    text = re.sub(r'\n{3,}',      '\n\n', text)
    text = re.sub(r' ,',          ',',    text)
    text = re.sub(r' \.',         '.',    text)
    text = re.sub(r',{2,}',       ',',    text)
    text = re.sub(r'\. \.',       '.',    text)
    text = re.sub(r'\s+([.,!?])', r'\1',  text)
    text = re.sub(r'  +',         ' ',    text)
    return text.strip()


def humanize(text):
    if not text or len(text.strip()) < 5:
        return "Please paste some text."

    for _ in range(3):
        text = strip_ai_openers(text)
        text = clean_symbols(text)
        text = apply_patterns(text)
        text = swap_words(text)
        text = apply_contractions(text)
        text = apply_synonym_pools(text)
        text = nuclear_sentence_rebuild(text)
        text = inject_personal_voice(text)
        text = break_paragraph_uniformity(text)
        text = fix_spaces(text)

    return text


def detect_ai(text):
    if not text or len(text.strip()) < 20:
        return {"score": 0, "indicators": ["Text too short to analyze"]}

    indicators = []
    score      = 0
    lower_text = text.lower()

    ai_transitions = [
        'furthermore', 'moreover', 'additionally', 'consequently',
        'nevertheless', 'nonetheless', 'subsequently', 'hence',
        'thus', 'therefore', 'in conclusion', 'first and foremost',
        'last but not least', 'all things considered',
        "it is worth noting", "it is important to note",
        "it is clear that", "it is evident that", "it is obvious that",
        "it goes without saying", "it should be noted that",
        "plays a crucial role", "plays a pivotal role", "plays a vital role",
        "in today's world", "in today's society", "in the modern world",
        "in the contemporary era", "a myriad of", "a plethora of",
        "utilize", "facilitate", "leverage",
        "demonstrates that", "illustrates that",
        "research shows that", "studies have shown that",
        "due to the fact that", "despite the fact that",
        "in spite of the fact that",
        "with regard to", "in terms of",
        "to put it simply", "having said that", "that being said",
        "needless to say", "when all is said and done",
    ]

    transition_count = 0
    for t in ai_transitions:
        matches = re.findall(r'\b' + re.escape(t) + r'\b', lower_text)
        if matches:
            transition_count += len(matches)
            score += len(matches) * 3

    if transition_count > 5:
        indicators.append(f"Found {transition_count} AI-style transition phrases")

    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s for s in sentences if s.strip()]
    if len(sentences) > 3:
        lengths  = [len(s.split()) for s in sentences]
        avg      = sum(lengths) / len(lengths)
        variance = sum((l - avg) ** 2 for l in lengths) / len(lengths)
        std_dev  = variance ** 0.5

        if std_dev < 5 and avg > 15:
            score += 15
            indicators.append("Sentences are unusually uniform in length")
        if avg > 25:
            score += 10
            indicators.append("Average sentence length is very long")
        short = [l for l in lengths if l < 8]
        if not short and len(sentences) > 5:
            score += 12
            indicators.append("No short sentences detected")

    formal = [
        r'\bit is (?:widely|generally|commonly) (?:accepted|recognized|acknowledged)\b',
        r'\b(?:many|several|various) (?:experts|researchers|scholars)\b',
        r'\bresearch (?:has|have) (?:shown|demonstrated|proven|indicated)\b',
        r'\b(?:key|crucial|vital|critical|essential) (?:aspect|element|component)\b',
        r'\b(?:significant|major|profound|substantial) (?:impact|effect|influence)\b',
    ]
    formal_count = 0
    for p in formal:
        matches = re.findall(p, text, re.IGNORECASE)
        formal_count += len(matches)
    if formal_count > 3:
        score += formal_count * 4
        indicators.append(f"Found {formal_count} formal academic phrases")

    contractions = ["don't", "doesn't", "didn't", "can't", "won't",
                    "wouldn't", "shouldn't", "couldn't", "isn't", "aren't",
                    "i'm", "you're", "we're", "they're", "it's", "that's",
                    "here's", "there's", "what's", "who's"]
    has_contraction = any(c in lower_text for c in contractions)
    if not has_contraction and len(text) > 200:
        score += 10
        indicators.append("No contractions found")

    has_personal = bool(re.search(r'\b(i|my|me|we|our|us)\b', text, re.IGNORECASE))
    if not has_personal and len(text) > 300:
        score += 5
        indicators.append("No personal pronouns (I, my, we, our)")

    has_casual = bool(re.search(
        r'\b(honestly|basically|kind of|sort of|you know|i mean|actually|look|anyway|yeah|ngl|real talk)\b',
        text, re.IGNORECASE))
    if not has_casual and len(text) > 500:
        score += 5
        indicators.append("No casual language detected")

    paragraphs = re.split(r'\n\s*\n', text)
    paragraphs = [p for p in paragraphs if p.strip()]
    if len(paragraphs) > 2:
        pl    = [len(p.split()) for p in paragraphs]
        avg_p = sum(pl) / len(pl)
        pv    = sum((l - avg_p) ** 2 for l in pl) / len(pl)
        if pv ** 0.5 < 10:
            score += 8
            indicators.append("Paragraphs are too uniform in length")

    score = min(max(score, 0), 100)

    if score >= 80:
        indicators.append("HIGH: Text appears AI-generated")
    elif score >= 50:
        indicators.append("MEDIUM: Text has mixed characteristics")
    elif score >= 25:
        indicators.append("LOW: Some AI patterns detected")
    else:
        indicators.append("VERY LOW: Text appears mostly human")

    return {"score": round(score), "indicators": indicators}

# ══════════════════════════════════════════════════════════════
#  FIXED IMPROVEMENTS — controlled rates, no stacking
# ══════════════════════════════════════════════════════════════

# ── NEW AI WORD PATTERNS (2024-2025) ──────────────────────────
EXTRA_PATTERNS = [
    (r'\bdelve[sd]?\b',                 "get"),
    (r'\bdelving\b',                    "getting into"),
    (r'\bdelve into\b',                 "look into"),
    (r'\btapestry\b',                   "mix"),
    (r'\bnuanced?\b',                   "complex"),
    (r'\bholistic(?:ally)?\b',          "overall"),
    (r'\brobust\b',                     "strong"),
    (r'\bsynergy\b',                    "working together"),
    (r'\bparadigm\b',                   "model"),
    (r'\bmultifaceted\b',               "complex"),
    (r'\bgroundbreaking\b',             "new"),
    (r'\bunprecedented\b',              "never seen before"),
    (r'\brevolutionary\b',              "major"),
    (r'\btransformative\b',             "big"),
    (r'\binnovative\b',                 "new"),
    (r'\bcutting.edge\b',               "new"),
    (r'\bstate.of.the.art\b',           "modern"),
    (r'\bgame.changing\b',              "important"),
    (r'\bproactive(?:ly)?\b',           "active"),
    (r'\bactionable\b',                 "useful"),
    (r'\bimpactful\b',                  "effective"),
    (r'\bempowers?\b',                  "helps"),
    (r'\bensures?\b',                   "makes sure"),
    (r'\bendeavou?rs?\b',               "tries"),
    (r'\boptimal(?:ly)?\b',             "best"),
    (r'\bstreamlines?\b',               "simplifies"),
    (r'\bfosters?\b',                   "builds"),
    (r'\bcultivates?\b',                "builds"),
    (r'\bnavigates?\b',                 "handles"),
    (r'\bmitigates?\b',                 "reduces"),
    (r'\belucidate[sd]?\b',             "explain"),
    (r'\bpertaining to\b',              "about"),
    (r'\bin conjunction with\b',        "along with"),
    (r'\bin accordance with\b',         "following"),
    (r'\bmoving forward\b',             "from now on"),
    (r'\bgoing forward\b',              "from now on"),
    (r'\bin essence\b',                 "basically"),
    (r'\bat its core\b',                "at heart"),
    (r'\bshed[s]? light on\b',          "explain"),
    (r'\bunderscore[sd]?\b',            "show"),
    (r'\bembark[s]? on\b',              "start"),
    (r'\bprioritize[sd]?\b',            "focus on"),
    (r'\bstakeholders?\b',              "people involved"),
    (r'\bwhereby\b',                    "where"),
    (r'\bwhilst\b',                     "while"),
    (r'\bamidst\b',                     "among"),
    (r'\baforementioned\b',             "mentioned"),
    (r'\bassist(?:s|ed)?\b',            "help"),
    (r'\bin summary[,.]?\s*',           "so basically, "),
    (r'\bto summarize[,.]?\s*',         "in short, "),
    (r'\bto conclude[,.]?\s*',          "to wrap up, "),
    (r'\bquite\b',                      "pretty"),
    (r'\brather\b',                     "pretty"),
    (r'\bextremely\b',                  "super"),
    (r'\bincredibly\b',                 "really"),
    (r'\bremarkably\b',                 "really"),
    (r'\bfascinating\b',                "pretty cool"),
    (r'\bintriguing\b',                 "interesting"),
    (r'\bstunning\b',                   "crazy"),
    (r'\bpurchase[sd]?\b',              "buy"),
    (r'\bobtain[sd]?\b',                "get"),
    (r'\bexamine[sd]?\b',               "look at"),
    (r'\bwitness(?:ed)?\b',             "see"),
    (r'\bencounter(?:ed)?\b',           "run into"),
    (r'\battempt(?:ed|ing)?\b',         "try"),
    (r'\bproceed(?:ed|ing)?\b',         "go"),
    (r'\bconvey(?:ed|ing)?\b',          "say"),
    (r'\bsimply\b',                     "just"),
    (r'\bmerely\b',                     "just"),
    (r'\bapproximately\b',              "around"),
    (r'\btypically\b',                  "usually"),
    (r'\bnormally\b',                   "usually"),
    (r'\bpotentially\b',                "maybe"),
    (r'\bpossibly\b',                   "maybe"),
    (r'\bperhaps\b',                    "maybe"),
    (r'\blikely\b',                     "probably"),
    (r'\bregarding\b',                  "about"),
    (r'\bconcerning\b',                 "about"),
    (r'\bpreviously\b',                 "before"),
    (r'\binitially\b',                  "at first"),
    (r'\beventually\b',                 "at some point"),
    (r'\bimmediately\b',                "right away"),
    (r'\brapidly\b',                    "fast"),
    (r'\bfrequently\b',                 "a lot"),
    (r'\bcurrently\b',                  "right now"),
    (r'\bsubstantially\b',              "a lot"),
    (r'\bsignificantly\b',              "a lot"),
]

# YOUR voice — casual openers (max 1 per paragraph)
YOUR_OPENERS = [
    "Not gonna lie, ",
    "Honestly, ",
    "I feel like ",
    "So basically ",
    "Lowkey ",
    "Ngl, ",
    "The thing is, ",
    "I mean, ",
    "Real talk, ",
    "And I think ",
]

# YOUR short punchy endings (max 1 per output)
YOUR_ENDINGS = [
    "which is pretty cool to me.",
    "not gonna lie that's actually interesting.",
    "lowkey didn't expect that.",
    "which is kind of wild.",
    "and yeah that basically sums it up.",
    "which honestly makes a lot of sense.",
    "pretty straightforward when you think about it.",
    "which is kind of a big deal if you ask me.",
]


def apply_extra_patterns(text):
    """Safe word-for-word replacements only — no structure changes."""
    for pattern, replacement in EXTRA_PATTERNS:
        try:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        except Exception:
            pass
    return text


def inject_voice_once(text):
    """
    Add YOUR voice touches — strictly controlled:
    - Max 1 opener per paragraph
    - Max 1 ending in the whole text
    - Never fires on a sentence that already has a filler/starter
    """
    paragraphs = text.split('\n\n')
    result = []
    ending_used = False

    for para in paragraphs:
        sentences = re.split(r'(?<=[.!?])\s+', para.strip())
        if not sentences:
            result.append(para)
            continue

        opener_used = False
        new_s = []

        for i, s in enumerate(sentences):
            words = s.split()

            # Skip if sentence already has a filler/starter word
            already_modified = any(
                s.lower().startswith(w.lower())
                for w in ['honestly', 'i mean', 'not gonna', 'ngl', 'look,',
                          'real talk', 'the thing', 'so basically', 'lowkey',
                          'i feel', 'i think', 'i\'d say', 'from what',
                          'personally', 'truth is', 'between you']
            )

            # Add opener — only once per paragraph, only on sentences > 6 words
            if (not opener_used
                    and not already_modified
                    and i > 0
                    and len(words) > 6
                    and random.random() < 0.35):
                opener = random.choice(YOUR_OPENERS)
                s = opener + s[0].lower() + s[1:]
                opener_used = True

            # Add ending — only once in entire text, only on last sentence of a para
            if (not ending_used
                    and i == len(sentences) - 1
                    and len(words) > 8
                    and random.random() < 0.40):
                s = s.rstrip('.!?') + ', ' + random.choice(YOUR_ENDINGS)
                ending_used = True

            new_s.append(s)

        result.append(' '.join(new_s))

    return '\n\n'.join(result)


def safe_sentence_rebuild(text):
    """
    Controlled sentence rebuilder — much lower rates than the original.
    Only does two things:
    1. Splits sentences > 25 words (no filler injection)
    2. Adds 1 short punchy sentence per paragraph max
    """
    paragraphs = text.split('\n\n')
    output = []

    for para in paragraphs:
        sentences = re.split(r'(?<=[.!?])\s+', para.strip())
        sentences = [s.strip() for s in sentences if s.strip()]
        new_s = []
        short_added = False

        for s in sentences:
            words = s.split()

            # Split long sentences cleanly
            if len(words) > 25:
                split_words = ['and', 'but', 'so', 'because', 'which',
                               'while', 'although', 'since', 'though']
                center = len(words) // 2
                split_done = False
                for offset in range(0, center - 3):
                    for d in [1, -1]:
                        idx = center + offset * d
                        if 6 <= idx <= len(words) - 6:
                            if words[idx].lower() in split_words:
                                first  = ' '.join(words[:idx]).rstrip(',') + '.'
                                second = ' '.join(words[idx:])
                                second = second[0].upper() + second[1:]
                                new_s.extend([first, second])
                                split_done = True
                                break
                    if split_done:
                        break
                if not split_done:
                    new_s.append(s)
                continue

            new_s.append(s)

        # Add ONE short punchy at the end of the paragraph (30% chance)
        if not short_added and len(new_s) > 2 and random.random() < 0.30:
            punchy = [
                "Pretty interesting when you think about it.",
                "Makes sense, right?",
                "And honestly that's kind of the whole point.",
                "Not that complicated once you get it.",
                "Which is worth knowing.",
                "Kind of a big deal actually.",
            ]
            new_s.append(random.choice(punchy))

        output.append(' '.join(new_s))

    return '\n\n'.join(output)


def humanize(text):
    """
    Clean humanize — runs pipeline ONCE, strict rate limits,
    no stacking, your voice baked in.
    """
    if not text or len(text.strip()) < 5:
        return "Please paste some text."

    # Pass 1 — word-level substitutions only (safe, no structure changes)
    text = strip_ai_openers(text)
    text = clean_symbols(text)
    text = apply_patterns(text)
    text = apply_extra_patterns(text)      # new AI words
    text = swap_words(text)
    text = apply_contractions(text)
    text = apply_synonym_pools(text)

    # Pass 2 — structure (once only)
    text = safe_sentence_rebuild(text)     # controlled splitter

    # Pass 3 — voice injection (once, with strict limits)
    text = inject_voice_once(text)         # your voice, max 1 per para

    # Pass 4 — cleanup
    text = break_paragraph_uniformity(text)
    text = fix_spaces(text)

    return text
