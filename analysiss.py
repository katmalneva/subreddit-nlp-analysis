import datetime

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
from nltk.corpus import words
import bs4 as bs
import urllib.request
import nltk
import re
import numpy as np


def set_up():
    df = pd.DataFrame()
    pd.options.display.max_colwidth = 700
    df = pd.read_csv('newest')

    # text = df.to_string()
    # breaks it up into single word strings
    # print(word_tokenize(text))

    # text = nltk.re.sub(r"[^a-zA-Z0-9]", " ", text.lower())
    # words = text.split()
    # # makes string all lowercase

    #
    # words: list[str] = nltk.word_tokenize(text)
    # words = [w for w in words if w not in stopwords.words("english")]
    # fd = nltk.FreqDist(words)
    # #shows most frequent words in string
    #
    #
    # #print(fd.most_common(10))
    # words_str = ' '.join(map(str, words))
    # sia = SentimentIntensityAnalyzer()
    # # sentiment analysis :)
    # #print(sia.polarity_scores(words_str))

    #highest_post = dates_posted(df)

    # df.iloc[:, 7] = df.iloc[:, 7].astype(str) + '-'
    # self_text = df.iloc[:, 7].to_string()
    # cleaned_self_text = clean_text(self_text)



    # df.iloc[:, 9] = df.iloc[:, 9].astype(str) + '-'
    # titles = df.iloc[:, 9].to_string()
    # cleaned_titles = clean_text(titles)
    #
    # common_words_self_text = most_common_words(cleaned_self_text)
    # common_words_titles = most_common_words(cleaned_titles)
    #
    # for i in range(len(common_words_self_text)):
    #     scores = analyze_posts_with_popular_posts(common_words_self_text[i][0], self_text)
    #     print(str(i) + ". " + str(common_words_self_text[i][0]) + ": " + str(scores))
    #
    # for j in range(len(common_words_titles)):
    #     scores = analyze_posts_with_popular_posts(common_words_titles[j][0], self_text)
    #     print(str(j) + ". " + str(common_words_titles[j][0]) + ": " + str(scores))

    # text_from_most_posted_day = get_posts_from_most_posted_date("05-17", df)
    # print(text_from_most_posted_day)
    #
    posts = hacky_posts_from_most_popular_date()
    summary = text_summary(posts)


def text_summary(scraped_data):

    sentence_list = nltk.sent_tokenize(scraped_data)
    stopwords = nltk.corpus.stopwords.words('english')

    word_frequencies = {}
    for word in nltk.word_tokenize(scraped_data):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
        maximum_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word] / maximum_frequency)
        sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]
    import heapq
    summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

    summary = ' '.join(summary_sentences)
    print(summary)
    return summary

def hacky_posts_from_most_popular_date():
    f = open("may-17th", "r")
    posts = f.read()
    " ".join(posts)
    return posts


def get_posts_from_most_posted_date(date, df):
    day = date[3] + date[4]
    month = date[1]
    parsed_date = datetime.datetime(2022, int(month), int(day))

    title_post = []

    df_dates = df.iloc[:, 1]
    for i in range(len(list(df_dates))):
        curr_date = df_dates[i]
        curr_day = curr_date[8] + curr_date[9]
        curr_month = curr_date[6]
        curr_parsed_date = datetime.datetime(2022, int(curr_month), int(curr_day))
        if curr_parsed_date == parsed_date:
            # posts.append(df.iloc[i:, 7].to_string())
            # titles.append(df.iloc[i:, 9].to_string())
            text = df.iloc[i:, 7].to_string() + df.iloc[i:, 9].to_string()
            cleaned_text = clean_text(text)
            title_post.append(cleaned_text)
    " ".join(title_post)

    return title_post


def analyze_posts_with_popular_posts(popular_word, text):
    posts = []
    split_text = text.split("-")

    for i in split_text:
        post = i
        post = post.split()
        post = set(post)
        if popular_word in post:
            post = " ".join(post)
            if post not in posts:
                posts.append(post)

    words_str = ' '.join(map(str, posts))
    sia = SentimentIntensityAnalyzer()
    scores = sia.polarity_scores(words_str)

    return scores


def most_common_words(cleaned_text):
    text: list[str] = nltk.word_tokenize(cleaned_text)
    fd = nltk.FreqDist(text)
    common = fd.most_common(15)
    cleaned_common = []
    for i in range(len(common)):
        if len(common[i][0]) > 1:
            cleaned_common.append(common[i])

    return cleaned_common


def dates_posted(df):
    dates = df.iloc[:, 1].to_string()
    dates_only = []

    for line in dates.splitlines():
        x = line.split(" ")
        dates_only.append(x[4])

    count = 0
    d = []
    for date in dates_only:
        x = date.split("T")
        if x[0] != "":
            reduced_string = re.sub(r'.', '', x[0], count=5)
            d.append(reduced_string)

    frequency = {}

    # iterating over the list
    for item in d:
        # checking the element in dictionary
        if item in frequency:
            # incrementing the counr
            frequency[item] += 1
        else:
            # initializing the count
            frequency[item] = 1

    x = frequency.keys()
    y = frequency.values()

    highest_posts = max(frequency, key=frequency.get)
    print("Highest number of posts on: " + str(highest_posts))
    # plotting the points

    plt.scatter(x, y, c="blue")
    plt.xticks(fontsize=5)
    axes = plt.gca()
    axes.xaxis.label.set_size(10)
    axes.yaxis.label.set_size(10)
    # naming the x axis
    plt.xlabel('Dates')
    # naming the y axis
    plt.ylabel('Number of Posts')

    # giving a title to my graph
    plt.title('Frequency of Posting')
    # function to show the plot
    plt.show()

    return highest_posts


def clean_text(text):
    posts = []
    words = set(nltk.corpus.words.words())

    for index, line in enumerate(text.splitlines()):
        x = line.split(" ")
        while ("" in x):
            x.remove("")
        while ("NaN" in x):
            x.remove("NaN")
        while ("\n" in x):
            x.remove("\n")
        while ("\\n" in x):
            x.remove("\\n")
        while ("\\n" in x):
            x.remove("\\n")
        while ("..." in x):
            x.remove("...")
        pattern = '[0-9]'
        x = [re.sub(pattern, '', i) for i in x]
        pattern = r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*'
        x = [re.sub(pattern, '', i) for i in x]

        x.remove(x[0])
        if len(x) > 1:
            ' '.join(x)
            for i in range(len(x)):
                x[i] = x[i].lower()
                if len(x[i]) > 2 and x[i] in words and x[i] not in stopwords.words("english"):
                    posts.append(x[i])

    # posts = [w for w in posts if w not in stopwords.words("english")]
    posts = " ".join(posts)
    #posts = nltk.re.sub(r"[^a-zA-Z0-9]", " ", posts.lower())

    return posts


if __name__ == '__main__':
    set_up()
