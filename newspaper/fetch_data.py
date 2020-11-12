from bs4 import BeautifulSoup
import feedparser
from datetime import date
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from newspaper.variables import *
from newspaper.s3_data import read_dataset, write_dataset

stop_words = set(stopwords.words('english'))

def lengths_of_keywords():
    return (len(data_level1), len(data_level2), len(data_level3))


def cleanHTML(raw_html):
    text = BeautifulSoup(raw_html, 'lxml').text
    word_tokens = word_tokenize(text.lower().rstrip())
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    return ' '.join(filtered_sentence)


def performRSSNew(url, newspaper):
    all_links = []
    NewsFeed = feedparser.parse(url)
    entries = NewsFeed.entries
    for entry in entries:
        content = cleanHTML(entry.content[0].value)
        published = entry.published
        temp_dict = {
            'url': entry.link,
            'content': content,
            'newspaper': newspaper,
            'published_date': published,
            }
        all_links.append(temp_dict)
    return all_links


def level1_count(article):
    if article:
        keyword_list = []
        for word in data_level1:
            search_ = r"\b" + word.split()[0] + r"[a-zA-Z]*\s\b" \
                + word.split()[1] + r"[a-zA-Z]*"
            if re.search(search_, article):
                keyword_list.append(word)
        for word in data_level_indicator:
            if word in article:
                keyword_list.append(word)
        return keyword_list
    return []


def level2_count(article, valid):
    if valid == 1:
        keyword_list = []
        for word in data_level2:
            search_ = r"\b" + word + r"[a-zA-Z]*"
            if re.search(search_, article):
                keyword_list.append(word)
        return keyword_list
    return []


def level3_count(article, valid):
    if valid == 1:
        keyword_list = []
        for word in data_level3:
            search_ = r"\b" + word + r"[a-zA-Z]*"
            if re.search(search_, article):
                keyword_list.append(word)
        return keyword_list
    return []


def level_2_3_filter(article):
    for word in filter_list:
        if word in article:
            return 1
    return 0


def level_len(count_list):
    if type(count_list) == str:
        return (1 if len(count_list) > 2 else 0)
    return (1 if len(count_list) > 0 else 0)


def fetch_merge_analyze_data_new(reset_analysis=False):
    
    prev_all = read_dataset()

    for newspaper in newspapers:
        temp = pd.DataFrame(performRSSNew(newspaper[0], newspaper[1]))
        df_ALL = pd.concat([prev_all, temp], sort=False)

    df_ALL = df_ALL.drop_duplicates(subset='url', keep='first'
                                    ).reset_index(drop=True)

    if reset_analysis:
        df_ALL['level1'] = np.nan
        df_ALL['level2'] = np.nan
        df_ALL['level3'] = np.nan

    df_ALL['level1'] = df_ALL.apply(lambda x: (level1_count(x['content'
                                    ]) if pd.isnull(x.level1) else x.level1),
                                    axis=1)
    df_ALL['level_len'] = df_ALL['level1'].apply(level_len)

    df_ALL['level_2_3_valid'] = df_ALL['content'
            ].apply(level_2_3_filter)

    df_ALL['level2'] = df_ALL.apply(lambda x: (level2_count(x['content'
                                    ], x['level_2_3_valid'
                                    ]) if pd.isnull(x.level2) else x.level2),
                                    axis=1)
    df_ALL['level2_len'] = df_ALL.level2.apply(level_len)

    df_ALL['level3'] = df_ALL.apply(lambda x: (level3_count(x['content'
                                    ], x['level_2_3_valid'
                                    ]) if pd.isnull(x.level3) else x.level3),
                                    axis=1)
    df_ALL['level3_len'] = df_ALL.level3.apply(level_len)
    write_dataset(df_ALL)
    return True