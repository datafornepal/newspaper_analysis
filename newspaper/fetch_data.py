from bs4 import BeautifulSoup
import feedparser
from datetime import date
import pandas as pd
import re  
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

newspapers = [('https://thehimalayantimes.com/feed/', 'ht'), 
              ('https://english.onlinekhabar.com/feed', 'ok'),
              ('https://www.nepalitimes.com/feed/', 'nt'),
              ('https://kathmandutribune.com/feed/', 'kt'),
              ('http://english.lokaantar.com/feed/', 'lk'),
              ('https://www.nepalisansar.com/feed/', 'ns'),
              ('http://telegraphnepal.com/feed/', 'tn'),
              ]

stop_words = set(stopwords.words('english'))      

data_level1=['arabl land','avail data','bureau statist','busi survey','cens publi','cens pop','children employ','civil registr','collect method','commerci export','complet rate','consum electr','consum energ','data access','data collect','data compil','data entri','data manag','data releas','data standard','data user','demograph data','densit popul','develop data','difusion dat','direct statist','disaggreg data','electr access','electr consumpt','energi consumpt','establish survey','exchang rate','extern debt','fertil rate','food import','food product','gender gap','govern debt','govern statist','gross domest','gross nation','health expenditur','health survey','import marchandis','improv data','improv statist','indic measur','indic preci','inflat rate','institut statist','interest payment','intern tourism','irrig land','land use','life expect','livestock product','merchandis export','merchandis trade','model statist','mortal rate','multilater debt','nation account','nation statist','nation survey','national brut','national statist','open data','part revenus','pay gap','popul census','popul growth','popul rate','price index','produccion aliment','purchas power','qualiti data','receit fiscal','releas data','revenu fiscal','rural popul','servic export','statist agenc','statist author','statist avail','statist committe','statist data','statist depart','statist national','statist offic','statist servic','statist studi','survey catalogu','tax payment','tax revenu','trade balanc','unemploy rate','use data','water suppli','youth unemploy']

data_level2=['accur','adequ','ambigu','ambígu','apropi','bancal','bias','confiabl','correct','deceit','deceiv','decept','defectu','delud','engan','equivoc','erreur','erro','erron','errone','error','exact','exat','fake','fallaci','faux','fiabl','generaliz','illus','imparcial','impartial','imprecis','improp','inaccur','incorrect','inexact','invalid','limit','manipul','mislead','mistaken','parcial','prec','precis','proper','reliabl','rigor','rigour','scientif','sol','solid','som','son','sound','spurious','tromp','trompeur','unbias','unreli','unscientif','unsound','vag','vagu','val','valid',]

data_level3=['data manipul','lead question','manipul dat','report bias','sampl select','sampl size']

data_level_indicator = [' cpi ', ' fdi ', ' gdp ', ' gnp ', ' hdi ', ' wdi ']

filter_list=[' data ',' record ',' research ',' statistics ',' study ']

def lengths_of_keywords():
    return len(data_level1), len(data_level2), len(data_level3)

def cleanHTML(raw_html):
    text = BeautifulSoup(raw_html, "lxml").text
    word_tokens = word_tokenize(text.lower().rstrip()) 
    filtered_sentence = [w for w in word_tokens if not w in stop_words] 
    return ' '.join(filtered_sentence)

def performRSSNew(url, newspaper):
    all_links = []
    NewsFeed = feedparser.parse(url)
    entries = NewsFeed.entries
    for entry in entries:
            content =  cleanHTML(entry.content[0].value)
            published = entry.published
            temp_dict = ({'url': entry.link, 
            'content': content , 
            'newspaper': newspaper,
            'published_date': published})
            all_links.append(temp_dict)    
    return all_links

def level1_count(article):
    if article:
        keyword_list = []
        for word in data_level1:
            search_ = (r"\b"+word.split()[0]+r"[a-zA-Z]*\s\b"+word.split()[1]+"[a-zA-Z]*")
            if re.search(search_, article):
                keyword_list.append(word)
        for word in data_level_indicator:
            if (word in article):
                keyword_list.append(word)
        return keyword_list
    return []

def level2_count(article, valid):
    if valid==1:
        keyword_list = []
        for word in data_level2:
            search_ = (r"\b"+word+r"[a-zA-Z]*")
            if re.search(search_, article):
                keyword_list.append(word)
        return keyword_list
    return []

def level3_count(article, valid):
    if valid==1:
        keyword_list = []
        for word in data_level3:
            search_ = (r"\b"+word+r"[a-zA-Z]*")
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
        return 1 if len(count_list)>2 else 0
    return 1 if len(count_list)>0 else 0


def fetch_merge_analyze_data_new(reset_analysis = False):
    start = time.time()
    prev_all = pd.read_csv('newspaper/static/datasets/all.csv')

    for newspaper in newspapers:
        temp = pd.DataFrame(performRSSNew(newspaper[0], newspaper[1]))
        df_ALL = pd.concat([prev_all, temp], sort=False)
    
    df_ALL = df_ALL.drop_duplicates(subset='url', keep="first").reset_index(drop=True) 
     
    print ('fetch_data and compile_data', time.time() - start)
    
    if (reset_analysis):
        df_ALL['level1'] = np.nan
        df_ALL['level2'] = np.nan
        df_ALL['level3'] = np.nan
        print ('reset_data', time.time() - start)
    
 
    df_ALL['level1'] = df_ALL.apply(lambda x: level1_count(x['content']) if pd.isnull(x.level1) else x.level1, axis=1)
    df_ALL['level_len'] = df_ALL['level1'].apply(level_len)
    
    print ('level_1_analysis', time.time() - start)
    
    df_ALL['level_2_3_valid'] = df_ALL['content'].apply(level_2_3_filter)
    print ('level_2_filter ', time.time() - start)
    
    df_ALL['level2'] =  df_ALL.apply(lambda x: level2_count(x['content'], x['level_2_3_valid']) if pd.isnull(x.level2) else x.level2, axis=1)
    df_ALL['level2_len'] = df_ALL.level2.apply(level_len)
    print ('level_2_analysis ', time.time() - start)
    
    df_ALL['level3'] =  df_ALL.apply(lambda x: level3_count(x['content'], x['level_2_3_valid']) if pd.isnull(x.level3) else x.level3, axis=1)
    df_ALL['level3_len'] = df_ALL.level3.apply(level_len)
    print ('level_3_analysis ', time.time() - start)
    
    df_ALL.to_csv('newspaper/static/datasets/all.csv', index=False)
    return df_ALL