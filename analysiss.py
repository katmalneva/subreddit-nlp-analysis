import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer

def cleaning():
    with open('ucsc_newest_reddit_post.csv', 'r') as f:
        text = f.read()
    #text = "Natural language processing is an exciting area."

    #breaks it up into single word strings
    #print(word_tokenize(text))

    text = nltk.re.sub(r"[^a-zA-Z0-9]", " ", text.lower())
    words = text.split()
    # makes string all lowercase
    #print(words)


    #takes out unnecessary words
    #print(words)

    words: list[str] = nltk.word_tokenize(text)
    words = [w for w in words if w not in stopwords.words("english")]
    fd = nltk.FreqDist(words)
    #shows most frequent words in string

    print(fd.most_common(10))
    words_str = ' '.join(map(str, words))
    sia = SentimentIntensityAnalyzer()
    # sentiment analysis :)
    print(sia.polarity_scores(words_str))


if __name__ == '__main__':
    cleaning()