from bs4 import BeautifulSoup
import feedparser
from datetime import date
import pandas as pd
import re  
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

stop_words = set(stopwords.words('english'))      

data_level1=['arabl land','avail data','bureau statist','busi survey','cens publi','cens pop','children employ','civil registr','collect method','commerci export','complet rate','consum electr','consum energ','data access','data collect','data compil','data entri','data manag','data releas','data standard','data user','demograph data','densit popul','develop data','difusion dat','direct statist','disaggreg data','electr access','electr consumpt','energi consumpt','establish survey','exchang rate','extern debt','fertil rate','food import','food product','gender gap','govern debt','govern statist','gross domest','gross nation','health expenditur','health survey','import marchandis','improv data','improv statist','indic measur','indic preci','inflat rate','institut statist','interest payment','intern tourism','irrig land','land use','life expect','livestock product','merchandis export','merchandis trade','model statist','mortal rate','multilater debt','nation account','nation statist','nation survey','national brut','national statist','open data','part revenus','pay gap','popul census','popul growth','popul rate','price index','produccion aliment','purchas power','qualiti data','receit fiscal','releas data','revenu fiscal','rural popul','servic export','statist agenc','statist author','statist avail','statist committe','statist data','statist depart','statist national','statist offic','statist servic','statist studi','survey catalogu','tax payment','tax revenu','trade balanc','unemploy rate','use data','water suppli','youth unemploy']

data_level2=['accur','adequ','ambigu','ambígu','apropi','bancal','bias','confiabl','correct','deceit','deceiv','decept','defectu','delud','engan','equivoc','erreur','erro','erron','errone','error','exact','exat','fake','fallaci','faux','fiabl','generaliz','illus','imparcial','impartial','imprecis','improp','inaccur','incorrect','inexact','invalid','limit','manipul','mislead','mistaken','parcial','prec','precis','proper','reliabl','rigor','rigour','scientif','sol','solid','som','son','sound','spurious','tromp','trompeur','unbias','unreli','unscientif','unsound','vag','vagu','val','valid',]

data_level3=['data manipul','lead question','manipul dat','report bias','sampl select','sampl size']

data_level_indicator = [' cpi ', ' fdi ', ' gdp ', ' gnp ', ' hdi ', ' wdi ']

filter_list=[' data ',' record ',' research ',' statistics ',' study ']

links=(['/about-town','/analysis','/business',
'/commentary','/current_affairs','/editorial',
'/editorials','/education','/entertainment',
'/finance','/governance','/headline','/here-now',
'/international','/interview','/kathmandu','/latest',
'/lifestyle','/multimedia','/national','/nepal','/opinion',
'/political','/science-technology','/sports','/travel','/world'])

def lengths_of_keywords():
    return len(data_level1), len(data_level2), len(data_level3)

def cleanHTML(raw_html):
    return BeautifulSoup(raw_html, "lxml").text

def performRSS(url, categories):
    all_links = []
    for category in categories:
        NewsFeed = feedparser.parse(url.format(category))
        entries = NewsFeed.entries
        for entry in entries:
            temp_dict = ({'url': entry.link, 
            'content': cleanHTML(entry.content[0].value), 
            'category': category, 
            'published_date':entry.published})
            all_links.append(temp_dict)        
    return all_links

def level1_count(article):
    word_tokens = word_tokenize(article.lower().rstrip()) 
    filtered_sentence = [w for w in word_tokens if not w in stop_words] 
    
    article = ' '.join(filtered_sentence)  
    keyword_list = []
    for word in data_level1:
        search_ = (r"\b"+word.split()[0]+r"[a-zA-Z]*\s\b"+word.split()[1]+"[a-zA-Z]*")
        if re.search(search_, article):
            keyword_list.append(word)
    for word in data_level_indicator:
        if (word in article):
            keyword_list.append(word)
    return keyword_list

def level_2_3_count(article, data):
    word_tokens = word_tokenize(article.lower().rstrip()) 
    filtered_sentence = [w for w in word_tokens if not w in stop_words] 
    

    article = ' '.join(filtered_sentence)  
    keyword_list = []
    for word in data:
        search_ = (r"\b"+word+r"[a-zA-Z]*")
        if re.search(search_, article):
            keyword_list.append(word)
    return keyword_list

def level_2_3_filter(article):
    article = article.lower().rstrip()
    for word in filter_list:
        if word in article:
            return 1
    return 0


def level_len(count_list):
    return 1 if len(count_list)>0 else 0

def fetch_merge_analyze_data():
    # Fetch and Merge data
    himalayan_times_url = "https://thehimalayantimes.com/category{}/feed/"
    raw_HT = pd.DataFrame(performRSS(himalayan_times_url, links)).dropna()
    prev_HT = pd.read_csv('newspaper/static/datasets/ht.csv')
    df_HT = pd.concat([prev_HT, raw_HT], sort=False).drop_duplicates(subset='url', keep="first").dropna()
    df_HT.to_csv('newspaper/static/datasets/ht.csv', index=False)
    
    online_khabar_url = "https://english.onlinekhabar.com/category{}/feed/"
    raw_OK = pd.DataFrame(performRSS(online_khabar_url, links)).dropna()
    prev_OK = pd.read_csv('newspaper/static/datasets/ok.csv')
    df_OK = pd.concat([prev_OK, raw_OK], sort=False).drop_duplicates(subset='url', keep="first").dropna()
    df_OK.to_csv('newspaper/static/datasets/ok.csv', index=False)
    
    
    nepali_times_url = "https://www.nepalitimes.com/nt{}/feed/"
    raw_NT = pd.DataFrame(performRSS(nepali_times_url, links)).dropna()
    prev_NT = pd.read_csv('newspaper/static/datasets/nt.csv')
    df_NT = pd.concat([prev_NT, raw_NT], sort=False).drop_duplicates(subset='url', keep="first").dropna()
    df_NT.to_csv('newspaper/static/datasets/nt.csv', index=False)
    
    
    telegraph_nepal_url = "http://telegraphnepal.com/category{}/feed/"
    raw_TN = pd.DataFrame(performRSS(telegraph_nepal_url, links)).dropna()
    prev_TN = pd.read_csv('newspaper/static/datasets/tn.csv')
    df_TN = pd.concat([prev_TN, raw_TN], sort=False).drop_duplicates(subset='url', keep="first").dropna()
    df_TN.to_csv('newspaper/static/datasets/tn.csv', index=False)
    
    
    kathmandu_tribune_url = "https://kathmandutribune.com/category{}/feed/"
    raw_KT = pd.DataFrame(performRSS(kathmandu_tribune_url, links)).dropna()
    prev_KT = pd.read_csv('newspaper/static/datasets/kt.csv')
    df_KT = pd.concat([prev_KT, raw_KT], sort=False).drop_duplicates(subset='url', keep="first").dropna()
    df_KT.to_csv('newspaper/static/datasets/kt.csv', index=False)
    
    lokaantar_url = "http://english.lokaantar.com/category{}/feed/"
    raw_LK = pd.DataFrame(performRSS(lokaantar_url, links)).dropna()
    prev_LK = pd.read_csv('newspaper/static/datasets/lk.csv')
    df_LK = pd.concat([prev_LK, raw_LK], sort=False).drop_duplicates(subset='url', keep="first").dropna()
    df_LK.to_csv('newspaper/static/datasets/lk.csv', index=False)
    
    df_HT = pd.read_csv('newspaper/static/datasets/ht.csv').dropna()
    df_OK = pd.read_csv('newspaper/static/datasets/ok.csv').dropna()
    df_NT = pd.read_csv('newspaper/static/datasets/nt.csv').dropna()
    df_TN = pd.read_csv('newspaper/static/datasets/tn.csv').dropna()
    df_KT = pd.read_csv('newspaper/static/datasets/kt.csv').dropna()
    df_LK = pd.read_csv('newspaper/static/datasets/lk.csv').dropna()

    # Perform analysis
    df_HT['level1'] = df_HT['content'].apply(level1_count)
    df_OK['level1'] = df_OK['content'].apply(level1_count)
    df_NT['level1'] = df_NT['content'].apply(level1_count)
    df_TN['level1'] = df_TN['content'].apply(level1_count)
    df_KT['level1'] = df_KT['content'].apply(level1_count)
    df_LK['level1'] = df_LK['content'].apply(level1_count)

    df_HT['level_len'] = df_HT['level1'].apply(level_len)
    df_OK['level_len'] = df_OK['level1'].apply(level_len)
    df_NT['level_len'] = df_NT['level1'].apply(level_len)
    df_TN['level_len'] = df_TN['level1'].apply(level_len)
    df_KT['level_len'] = df_KT['level1'].apply(level_len)
    df_LK['level_len'] = df_LK['level1'].apply(level_len)

    df_HT['level_2_3_valid'] = df_HT['content'].apply(level_2_3_filter)
    df_HT_level_2_3 = df_HT[df_HT['level_2_3_valid']==1].reset_index(drop=True)
    df_OK['level_2_3_valid'] = df_OK['content'].apply(level_2_3_filter)
    df_OK_level_2_3 = df_OK[df_OK['level_2_3_valid']==1].reset_index(drop=True)
    df_NT['level_2_3_valid'] = df_NT['content'].apply(level_2_3_filter)
    df_NT_level_2_3 = df_NT[df_NT['level_2_3_valid']==1].reset_index(drop=True)
    df_TN['level_2_3_valid'] = df_TN['content'].apply(level_2_3_filter)
    df_TN_level_2_3 = df_TN[df_TN['level_2_3_valid']==1].reset_index(drop=True)
    df_KT['level_2_3_valid'] = df_KT['content'].apply(level_2_3_filter)
    df_KT_level_2_3 = df_KT[df_KT['level_2_3_valid']==1].reset_index(drop=True)
    df_LK['level_2_3_valid'] = df_LK['content'].apply(level_2_3_filter)
    df_LK_level_2_3 = df_LK[df_LK['level_2_3_valid']==1].reset_index(drop=True)


    df_HT_level_2_3['level2'] = df_HT_level_2_3['content'].apply(lambda x:level_2_3_count(x,data_level2))
    df_OK_level_2_3['level2'] = df_OK_level_2_3['content'].apply(lambda x:level_2_3_count(x,data_level2))
    df_NT_level_2_3['level2'] = df_NT_level_2_3['content'].apply(lambda x:level_2_3_count(x,data_level2))
    df_TN_level_2_3['level2'] = df_TN_level_2_3['content'].apply(lambda x:level_2_3_count(x,data_level2))
    df_KT_level_2_3['level2'] = df_KT_level_2_3['content'].apply(lambda x:level_2_3_count(x,data_level2))
    df_LK_level_2_3['level2'] = df_LK_level_2_3['content'].apply(lambda x:level_2_3_count(x,data_level2))

    df_HT_level_2_3['level2_len'] = df_HT_level_2_3.level2.apply(level_len)
    df_OK_level_2_3['level2_len'] = df_OK_level_2_3.level2.apply(level_len)
    df_NT_level_2_3['level2_len'] = df_NT_level_2_3.level2.apply(level_len)
    df_TN_level_2_3['level2_len'] = df_TN_level_2_3.level2.apply(level_len)
    df_KT_level_2_3['level2_len'] = df_KT_level_2_3.level2.apply(level_len)
    df_LK_level_2_3['level2_len'] = df_LK_level_2_3.level2.apply(level_len)

    df_HT_level_2_3['level3'] = df_HT_level_2_3['content'].apply(lambda x:level_2_3_count(x,data_level3))
    df_OK_level_2_3['level3'] = df_OK_level_2_3['content'].apply(lambda x:level_2_3_count(x,data_level3))
    df_NT_level_2_3['level3'] = df_NT_level_2_3['content'].apply(lambda x:level_2_3_count(x,data_level3))
    df_TN_level_2_3['level3'] = df_TN_level_2_3['content'].apply(lambda x:level_2_3_count(x,data_level3))
    df_KT_level_2_3['level3'] = df_KT_level_2_3['content'].apply(lambda x:level_2_3_count(x,data_level3))
    df_LK_level_2_3['level3'] = df_LK_level_2_3['content'].apply(lambda x:level_2_3_count(x,data_level3))

    df_HT_level_2_3['level3_len'] = df_HT_level_2_3['level3'].apply(level_len)
    df_OK_level_2_3['level3_len'] = df_OK_level_2_3['level3'].apply(level_len)
    df_NT_level_2_3['level3_len'] = df_NT_level_2_3['level3'].apply(level_len)
    df_TN_level_2_3['level3_len'] = df_TN_level_2_3['level3'].apply(level_len)
    df_KT_level_2_3['level3_len'] = df_KT_level_2_3['level3'].apply(level_len)
    df_LK_level_2_3['level3_len'] = df_LK_level_2_3['level3'].apply(level_len)

    data1 = [
    ['The Himalayan Times', df_HT.level_len.sum(), df_HT.shape[0]],
    ['Online Khabar', df_OK.level_len.sum(), df_OK.shape[0]],
    ['Nepali Times', df_NT.level_len.sum(), df_NT.shape[0]],
    ['Telegraph Nepal', df_TN.level_len.sum(), df_TN.shape[0]],
    ['Katmandu Tribune', df_KT.level_len.sum(), df_KT.shape[0]],
    ['Lokaantar', df_LK.level_len.sum(), df_LK.shape[0]]
    ] 

    data2 = [
    ['The Himalayan Times', df_HT_level_2_3.level2_len.sum(), df_HT_level_2_3.shape[0]],
    ['Online Khabar', df_OK_level_2_3.level2_len.sum(), df_OK_level_2_3.shape[0]],
    ['Nepali Times', df_NT_level_2_3.level2_len.sum(), df_NT_level_2_3.shape[0]],
    ['Telegraph Nepal', df_TN_level_2_3.level2_len.sum(), df_TN_level_2_3.shape[0]],
    ['Katmandu Tribune', df_KT_level_2_3.level2_len.sum(), df_KT_level_2_3.shape[0]],
    ['Lokaantar', df_LK_level_2_3.level2_len.sum(), df_LK_level_2_3.shape[0]]
    ] 


    data3 = [
    ['The Himalayan Times', df_HT_level_2_3.level3_len.sum(), df_HT_level_2_3.shape[0]],
    ['Online Khabar', df_OK_level_2_3.level3_len.sum(), df_OK_level_2_3.shape[0]],
    ['Nepali Times', df_NT_level_2_3.level3_len.sum(), df_NT_level_2_3.shape[0]],
    ['Telegraph Nepal', df_TN_level_2_3.level3_len.sum(), df_TN_level_2_3.shape[0]],
    ['Katmandu Tribune', df_KT_level_2_3.level3_len.sum(), df_KT_level_2_3.shape[0]],
    ['Lokaantar', df_LK_level_2_3.level3_len.sum(), df_LK_level_2_3.shape[0]]
    ] 

        
    pd.DataFrame(data1, columns = ['Newspaper', 'Level1', 'News Articles']).to_csv('newspaper/static/datasets/level1.csv', index=False) 
    pd.DataFrame(data2, columns = ['Newspaper', 'Level2', 'News Articles']).to_csv('newspaper/static/datasets/level2.csv', index=False)  
    pd.DataFrame(data3, columns = ['Newspaper', 'Level3', 'News Articles']).to_csv('newspaper/static/datasets/level3.csv', index=False)  
    
    return True