import re  
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 



stop_words = set(stopwords.words('english'))      

data_level1=['arabl land','avail data','bureau statist','busi survey','cens publi','cens pop','children employ','civil registr','collect method','commerci export','complet rate','consum electr','consum energ','data access','data collect','data compil','data entri','data manag','data releas','data standard','data user','demograph data','densit popul','develop data','difusion dat','direct statist','disaggreg data','electr access','electr consumpt','energi consumpt','establish survey','exchang rate','extern debt','fertil rate','food import','food product','gender gap','govern debt','govern statist','gross domest','gross nation','health expenditur','health survey','import marchandis','improv data','improv statist','indic measur','indic preci','inflat rate','institut statist','interest payment','intern tourism','irrig land','land use','life expect','livestock product','merchandis export','merchandis trade','model statist','mortal rate','multilater debt','nation account','nation statist','nation survey','national brut','national statist','open data','part revenus','pay gap','popul census','popul growth','popul rate','price index','produccion aliment','purchas power','qualiti data','receit fiscal','releas data','revenu fiscal','rural popul','servic export','statist agenc','statist author','statist avail','statist committe','statist data','statist depart','statist national','statist offic','statist servic','statist studi','survey catalogu','tax payment','tax revenu','trade balanc','unemploy rate','use data','water suppli','youth unemploy']

data_level2=['accur','adequ','ambigu','ambígu','apropi','bancal','bias','confiabl','correct','deceit','deceiv','decept','defectu','delud','engan','equivoc','erreur','erro','erron','errone','error','exact','exat','fake','fallaci','faux','fiabl','generaliz','illus','imparcial','impartial','imprecis','improp','inaccur','incorrect','inexact','invalid','limit','manipul','mislead','mistaken','parcial','prec','precis','proper','reliabl','rigor','rigour','scientif','sol','solid','som','son','sound','spurious','tromp','trompeur','unbias','unreli','unscientif','unsound','vag','vagu','val','valid',]

data_level3=['data manipul','lead question','manipul dat','report bias','sampl select','sampl size']

data_level_indicator = [' cpi ', ' fdi ', ' gdp ', ' gnp ', ' hdi ', ' wdi ']

filter_list=[' data ',' record ',' research ',' statistics ',' study ']


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