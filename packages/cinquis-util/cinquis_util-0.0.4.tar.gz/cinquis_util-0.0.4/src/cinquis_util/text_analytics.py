# import spacy
# import spacy.cli
# spacy.cli.download("en_core_web_lg")
import numpy as np
import matplotlib.pyplot as plt
import wordcloud
from sklearn.feature_extraction.text import CountVectorizer
from scipy.stats import zipf
from nltk import FreqDist
import en_core_web_lg
nlp = en_core_web_lg.load()


def cleanText(dirty_text):
    # first process the text with spacy;
    # this does a lot of things we aren't using right here
    nlp_string = nlp(dirty_text)
    lowercase_words = []
    for word in nlp_string:
        if word.is_alpha:
            if not word.is_punct:
                lowercase_words.append(word.lower_)
    return nlp(' '.join(lowercase_words))


def cleanerText(dirty_text):
    # first process the text with spacy; this does a lot of things we aren't
    # using right here
    nlp_string = nlp(dirty_text)
    lowercase_words = []
    for word in nlp_string:
        if word.is_alpha and not word.is_stop:
            if not word.is_punct:
                lowercase_words.append(word.lower_)
    return nlp(' '.join(lowercase_words))


def removeStop(dirty_text):
    nlp_string = nlp(dirty_text)
    lowercase_words = []
    for word in nlp_string:
        if not word.is_stop:
            if not word.is_punct:
                lowercase_words.append(word.lower_)
    return nlp(' '.join(lowercase_words))


def makeZipfPlot(text):
    fd = FreqDist(text.split())
    # adapted from here:
    # https://finnaarupnielsen.wordpress.com/2013/10/22/zipf-plot-for-word-counts-in-brown-corpus/
    # get counts for x and y
    counts = np.array(list(fd.values()))
    # tokens = list(fd.keys())
    ranks = np.arange(1, len(counts) + 1)
    indices = np.argsort(-counts)
    # frequencies = counts[indices]
    normalized_frequencies = counts[indices] / sum(counts)

    # make plot
    # f = plt.figure(figsize=(10, 10))
    plt.loglog(ranks, normalized_frequencies, marker=".")
    # add the expected Zipfian distribution from the equation
    plt.loglog(ranks, [z for z in zipf.pmf(ranks, 1.07)])

    # add labels for clarity
    plt.title("Zipf plot for Brown corpus tokens")
    plt.xlabel("Frequency rank of token")
    plt.ylabel("Absolute frequency of token")

    ax = plt.gca()  # get current axis
    ax.set_aspect('equal')  # make the plot square
    plt.grid(True)

    # add text labels -- not strictly necessary,
    # but a nice adaptation from the example
    last_freq = None
    for i in list(np.logspace(-0.5, np.log10(len(counts) - 1),
                              10).astype(int)):
        # ensure words don't overlap and make sure y-val is differnt
        if last_freq != normalized_frequencies[i]:
            # dummy = plt.text(ranks[i],
            #                  normalized_frequencies[i],
            #                  " " + tokens[indices[i]],
            #                  verticalalignment="bottom",
            #                  horizontalalignment="left")
            last_freq = normalized_frequencies[i]


def makeWordClouds(text, x, y, h, w):
    text_clean = cleanerText(text)
    vectorizer = CountVectorizer(ngram_range=(x, y))
    counts = vectorizer.fit_transform([text_clean.text])
    story_counts = np.array(counts.todense()).flatten()
    freq_dict = {}
    for v, i in vectorizer.vocabulary_.items():
        freq_dict[v] = story_counts[i]
    wc = wordcloud.WordCloud()
    plt.figure(figsize=(h, w))
    plt.imshow(wc.generate_from_frequencies(freq_dict))


def getNER(text):
    people = [" "]
    dates = [" "]
    orgs = [" "]

    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            for p in people:
                if ent.text not in people:
                    people.append(ent.text)
        if ent.label_ == 'DATE':
            for d in dates:
                if ent.text not in dates:
                    dates.append(ent.text)
        if ent.label_ == 'ORG':
            for o in orgs:
                if ent.text not in orgs:
                    orgs.append(ent.text)
    print("People:", people)
    print("Dates:", dates)
    print("Orgs :", orgs)


# def autoAnalyze(text):
#     makeZipfPlot(text)
#     makeWordClouds(text,2,2)
    # makeWordClouds(text,3,3)

def main():
    print('hello text analytics')


if __name__ == "__main__":
    main()
