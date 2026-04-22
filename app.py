from flask import Flask, render_template, request
import re
import pronouncing
import os

app = Flask(__name__)

def words(text):
    return re.findall(r"[a-zA-Z]+", text.lower())

def syllable(word):
    phones = pronouncing.phones_for_word(word)
    if not phones:
        return 1
    return pronouncing.syllable_count(phones[0])

def analyze(text):
    w = words(text)
    if not w:
        return None

    total_words = len(w)
    total_syllables = sum(syllable(x) for x in w)
    avg_syll = total_syllables / total_words

    vocab = len(set(w)) / total_words * 100
    multi = sum(1 for x in w if syllable(x) >= 3)

    rhyme = min(vocab * 0.9, 100)
    flow = max(0, 100 - abs(avg_syll - 2.4) * 18)
    structure = min(100, (total_words / 60) * 100)

    language = vocab * 0.6 + (100 - abs(avg_syll - 2.2) * 10) * 0.4
    impact = min(100, (multi * 2.2) + (vocab * 0.3))

    score = (rhyme + flow + language + structure + impact) / 5

    good = []
    bad = []

    if vocab > 65:
        good.append("strong vocabulary diversity")
    else:
        bad.append("increase vocabulary variety")

    if multi > 10:
        good.append("strong multisyllable usage")
    else:
        bad.append("add more multisyllable rhymes")

    if flow > 70:
        good.append("consistent flow control")
    else:
        bad.append("flow needs improvement")

    if structure > 70:
        good.append("good structure")
    else:
        bad.append("improve structure")

    if impact > 70:
        good.append("strong lyrical impact")
    else:
        bad.append("add punchlines / imagery")

    if score >= 90:
        label = "ELITE LEVEL"
    elif score >= 75:
        label = "RADIO READY"
    elif score >= 50:
        label = "DEVELOPING ARTIST"
    else:
        label = "BASIC LEVEL"

    return {
        "score": round(score, 1),
        "label": label,
        "words": total_words,
        "syllables": total_syllables,
        "avg_syllables": round(avg_syll, 2),
        "multi": multi,
        "rhyme": round(rhyme, 1),
        "flow": round(flow, 1),
        "language": round(language, 1),
        "structure": round(structure, 1),
        "impact": round(impact, 1),
        "good": good,
        "bad": bad
    }

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        text = request.form.get("verse", "")
        result = analyze(text)
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
