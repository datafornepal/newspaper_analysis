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


def fetch_merge_analyze_data_new():
    # Fetch and Merge data
    himalayan_times_url = "https://thehimalayantimes.com/feed/"
    raw_HT = pd.DataFrame(performRSSNew(himalayan_times_url)) 
    prev_HT = pd.read_csv('newspaper/static/datasets/ht.csv')
    df_HT = pd.concat([prev_HT, raw_HT], sort=False).drop_duplicates(subset='url', keep="first") 
    df_HT.to_csv('newspaper/static/datasets/ht.csv', index=False)
    
    online_khabar_url = "https://english.onlinekhabar.com/feed"
    raw_OK = pd.DataFrame(performRSSNew(online_khabar_url)) 
    prev_OK = pd.read_csv('newspaper/static/datasets/ok.csv')
    df_OK = pd.concat([prev_OK, raw_OK], sort=False).drop_duplicates(subset='url', keep="first") 
    df_OK.to_csv('newspaper/static/datasets/ok.csv', index=False)
    
    
    nepali_times_url = "https://www.nepalitimes.com/feed/"
    raw_NT = pd.DataFrame(performRSSNew(nepali_times_url)) 
    prev_NT = pd.read_csv('newspaper/static/datasets/nt.csv')
    df_NT = pd.concat([prev_NT, raw_NT], sort=False).drop_duplicates(subset='url', keep="first") 
    df_NT.to_csv('newspaper/static/datasets/nt.csv', index=False)
    
    
    telegraph_nepal_url = "http://telegraphnepal.com/feed/"
    raw_TN = pd.DataFrame(performRSSNew(telegraph_nepal_url)) 
    prev_TN = pd.read_csv('newspaper/static/datasets/tn.csv')
    df_TN = pd.concat([prev_TN, raw_TN], sort=False).drop_duplicates(subset='url', keep="first") 
    df_TN.to_csv('newspaper/static/datasets/tn.csv', index=False)
    
    
    kathmandu_tribune_url = "https://kathmandutribune.com/feed/"
    raw_KT = pd.DataFrame(performRSSNew(kathmandu_tribune_url)) 
    prev_KT = pd.read_csv('newspaper/static/datasets/kt.csv')
    df_KT = pd.concat([prev_KT, raw_KT], sort=False).drop_duplicates(subset='url', keep="first") 
    df_KT.to_csv('newspaper/static/datasets/kt.csv', index=False)
    
    lokaantar_url = "http://english.lokaantar.com/feed/"
    raw_LK = pd.DataFrame(performRSSNew(lokaantar_url)) 
    prev_LK = pd.read_csv('newspaper/static/datasets/lk.csv')
    df_LK = pd.concat([prev_LK, raw_LK], sort=False).drop_duplicates(subset='url', keep="first") 
    df_LK.to_csv('newspaper/static/datasets/lk.csv', index=False)

    ratopati_url = "http://english.ratopati.com/feed/"
    raw_RP = pd.DataFrame(performRSSNew(ratopati_url)) 
    prev_RP = pd.read_csv('newspaper/static/datasets/rp.csv')
    df_RP = pd.concat([prev_RP, raw_RP], sort=False).drop_duplicates(subset='url', keep="first") 
    df_RP.to_csv('newspaper/static/datasets/rp.csv', index=False)

    nepali_sansar_url = "https://www.nepalisansar.com/feed/"
    raw_NS = pd.DataFrame(performRSSNew(nepali_sansar_url)) 
    prev_NS = pd.read_csv('newspaper/static/datasets/ns.csv')
    df_NS = pd.concat([prev_NS, raw_NS], sort=False).drop_duplicates(subset='url', keep="first") 
    df_NS.to_csv('newspaper/static/datasets/ns.csv', index=False)
    
    df_HT = pd.read_csv('newspaper/static/datasets/ht.csv').dropna(subset=['url', 'content'])
    df_OK = pd.read_csv('newspaper/static/datasets/ok.csv').dropna(subset=['url', 'content']) 
    df_NT = pd.read_csv('newspaper/static/datasets/nt.csv').dropna(subset=['url', 'content']) 
    df_TN = pd.read_csv('newspaper/static/datasets/tn.csv').dropna(subset=['url', 'content']) 
    df_KT = pd.read_csv('newspaper/static/datasets/kt.csv').dropna(subset=['url', 'content']) 
    df_LK = pd.read_csv('newspaper/static/datasets/lk.csv').dropna(subset=['url', 'content']) 
    df_RP = pd.read_csv('newspaper/static/datasets/rp.csv').dropna(subset=['url', 'content']) 
    df_NS = pd.read_csv('newspaper/static/datasets/ns.csv').dropna(subset=['url', 'content']) 

    # Perform analysis
    df_HT['level1'] = df_HT['content'].apply(level1_count)
    df_OK['level1'] = df_OK['content'].apply(level1_count)
    df_NT['level1'] = df_NT['content'].apply(level1_count)
    df_TN['level1'] = df_TN['content'].apply(level1_count)
    df_KT['level1'] = df_KT['content'].apply(level1_count)
    df_LK['level1'] = df_LK['content'].apply(level1_count)
    df_RP['level1'] = df_RP['content'].apply(level1_count)
    df_NS['level1'] = df_NS['content'].apply(level1_count)

    df_HT['level_len'] = df_HT['level1'].apply(level_len)
    df_OK['level_len'] = df_OK['level1'].apply(level_len)
    df_NT['level_len'] = df_NT['level1'].apply(level_len)
    df_TN['level_len'] = df_TN['level1'].apply(level_len)
    df_KT['level_len'] = df_KT['level1'].apply(level_len)
    df_LK['level_len'] = df_LK['level1'].apply(level_len)
    df_RP['level_len'] = df_RP['level1'].apply(level_len)
    df_NS['level_len'] = df_NS['level1'].apply(level_len)

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
    df_RP['level_2_3_valid'] = df_RP['content'].apply(level_2_3_filter)
    df_RP_level_2_3 = df_RP[df_RP['level_2_3_valid']==1].reset_index(drop=True)
    df_NS['level_2_3_valid'] = df_NS['content'].apply(level_2_3_filter)
    df_NS_level_2_3 = df_NS[df_NS['level_2_3_valid']==1].reset_index(drop=True)


    df_HT_level_2_3['level2'] = df_HT_level_2_3['content'].apply(lambda x:level_2_3_count(x,data_level2))
    df_OK_level_2_3['level2'] = df_OK_level_2_3['content'].apply(lambda x:level_2_3_count(x,data_level2))
    df_NT_level_2_3['level2'] = df_NT_level_2_3['content'].apply(lambda x:level_2_3_count(x,data_level2))
    df_TN_level_2_3['level2'] = df_TN_level_2_3['content'].apply(lambda x:level_2_3_count(x,data_level2))
    df_KT_level_2_3['level2'] = df_KT_level_2_3['content'].apply(lambda x:level_2_3_count(x,data_level2))
    df_LK_level_2_3['level2'] = df_LK_level_2_3['content'].apply(lambda x:level_2_3_count(x,data_level2))
    df_RP_level_2_3['level2'] = df_RP_level_2_3['content'].apply(lambda x:level_2_3_count(x,data_level2))
    df_NS_level_2_3['level2'] = df_NS_level_2_3['content'].apply(lambda x:level_2_3_count(x,data_level2))

    df_HT_level_2_3['level2_len'] = df_HT_level_2_3.level2.apply(level_len)
    df_OK_level_2_3['level2_len'] = df_OK_level_2_3.level2.apply(level_len)
    df_NT_level_2_3['level2_len'] = df_NT_level_2_3.level2.apply(level_len)
    df_TN_level_2_3['level2_len'] = df_TN_level_2_3.level2.apply(level_len)
    df_KT_level_2_3['level2_len'] = df_KT_level_2_3.level2.apply(level_len)
    df_LK_level_2_3['level2_len'] = df_LK_level_2_3.level2.apply(level_len)
    df_RP_level_2_3['level2_len'] = df_RP_level_2_3.level2.apply(level_len)
    df_NS_level_2_3['level2_len'] = df_NS_level_2_3.level2.apply(level_len)

    df_HT_level_2_3['level3'] = df_HT_level_2_3['content'].apply(lambda x:level_2_3_count(x,data_level3))
    df_OK_level_2_3['level3'] = df_OK_level_2_3['content'].apply(lambda x:level_2_3_count(x,data_level3))
    df_NT_level_2_3['level3'] = df_NT_level_2_3['content'].apply(lambda x:level_2_3_count(x,data_level3))
    df_TN_level_2_3['level3'] = df_TN_level_2_3['content'].apply(lambda x:level_2_3_count(x,data_level3))
    df_KT_level_2_3['level3'] = df_KT_level_2_3['content'].apply(lambda x:level_2_3_count(x,data_level3))
    df_LK_level_2_3['level3'] = df_LK_level_2_3['content'].apply(lambda x:level_2_3_count(x,data_level3))
    df_RP_level_2_3['level3'] = df_RP_level_2_3['content'].apply(lambda x:level_2_3_count(x,data_level3))
    df_NS_level_2_3['level3'] = df_NS_level_2_3['content'].apply(lambda x:level_2_3_count(x,data_level3))

    df_HT_level_2_3['level3_len'] = df_HT_level_2_3['level3'].apply(level_len)
    df_OK_level_2_3['level3_len'] = df_OK_level_2_3['level3'].apply(level_len)
    df_NT_level_2_3['level3_len'] = df_NT_level_2_3['level3'].apply(level_len)
    df_TN_level_2_3['level3_len'] = df_TN_level_2_3['level3'].apply(level_len)
    df_KT_level_2_3['level3_len'] = df_KT_level_2_3['level3'].apply(level_len)
    df_LK_level_2_3['level3_len'] = df_LK_level_2_3['level3'].apply(level_len)
    df_RP_level_2_3['level3_len'] = df_RP_level_2_3['level3'].apply(level_len)
    df_NS_level_2_3['level3_len'] = df_NS_level_2_3['level3'].apply(level_len)

    data1 = [
    ['The Himalayan Times', df_HT.level_len.sum(), df_HT.shape[0]],
    ['Online Khabar', df_OK.level_len.sum(), df_OK.shape[0]],
    ['Nepali Times', df_NT.level_len.sum(), df_NT.shape[0]],
    ['Telegraph Nepal', df_TN.level_len.sum(), df_TN.shape[0]],
    ['Katmandu Tribune', df_KT.level_len.sum(), df_KT.shape[0]],
    ['Lokaantar', df_LK.level_len.sum(), df_LK.shape[0]],
    ['Ratopati', df_RP.level_len.sum(), df_RP.shape[0]],
    ['Nepali Sansar', df_NS.level_len.sum(), df_NS.shape[0]]
    ] 

    data2 = [
    ['The Himalayan Times', df_HT_level_2_3.level2_len.sum(), df_HT_level_2_3.shape[0]],
    ['Online Khabar', df_OK_level_2_3.level2_len.sum(), df_OK_level_2_3.shape[0]],
    ['Nepali Times', df_NT_level_2_3.level2_len.sum(), df_NT_level_2_3.shape[0]],
    ['Telegraph Nepal', df_TN_level_2_3.level2_len.sum(), df_TN_level_2_3.shape[0]],
    ['Katmandu Tribune', df_KT_level_2_3.level2_len.sum(), df_KT_level_2_3.shape[0]],
    ['Lokaantar', df_LK_level_2_3.level2_len.sum(), df_LK_level_2_3.shape[0]],
    ['Ratopati', df_RP_level_2_3.level2_len.sum(), df_RP_level_2_3.shape[0]],
    ['Nepali Sansar', df_NS_level_2_3.level2_len.sum(), df_NS_level_2_3.shape[0]]
    ] 


    data3 = [
    ['The Himalayan Times', df_HT_level_2_3.level3_len.sum(), df_HT_level_2_3.shape[0]],
    ['Online Khabar', df_OK_level_2_3.level3_len.sum(), df_OK_level_2_3.shape[0]],
    ['Nepali Times', df_NT_level_2_3.level3_len.sum(), df_NT_level_2_3.shape[0]],
    ['Telegraph Nepal', df_TN_level_2_3.level3_len.sum(), df_TN_level_2_3.shape[0]],
    ['Katmandu Tribune', df_KT_level_2_3.level3_len.sum(), df_KT_level_2_3.shape[0]],
    ['Lokaantar', df_LK_level_2_3.level3_len.sum(), df_LK_level_2_3.shape[0]],
    ['Ratopati', df_RP_level_2_3.level3_len.sum(), df_RP_level_2_3.shape[0]],
    ['Nepali Sansar', df_NS_level_2_3.level3_len.sum(), df_NS_level_2_3.shape[0]]
    ] 

        
    pd.DataFrame(data1, columns = ['Newspaper', 'Level1', 'News Articles']).to_csv('newspaper/static/datasets/level1.csv', index=False) 
    pd.DataFrame(data2, columns = ['Newspaper', 'Level2', 'News Articles']).to_csv('newspaper/static/datasets/level2.csv', index=False)  
    pd.DataFrame(data3, columns = ['Newspaper', 'Level3', 'News Articles']).to_csv('newspaper/static/datasets/level3.csv', index=False)  
    
    return True
