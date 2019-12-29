from flask import render_template, request
from newspaper import application
import feedparser
import pandas as pd
from bs4 import BeautifulSoup
from datetime import date
import glob, os
import plotly
import plotly.graph_objects as go

links = [
 '/about-town',
 '/analysis',
 '/business',
 '/commentary',
 '/current_affairs',
 '/editorial',
 '/editorials',
 '/education',
 '/entertainment',
 '/finance',
 '/governance',
 '/headline',
 '/here-now',
 '/international',
 '/interview',
 '/kathmandu',
 '/latest',
 '/lifestyle',
 '/multimedia',
 '/national',
 '/nepal',
 '/opinion',
 '/political',
 '/science-technology',
 '/sports',
 '/travel',
 '/world']

data_level1 = [
'population census', 
'household survey', 
'geospatial data', 
'statistics', 
'data', 
'study', 'research', 
'report',
'data literacy']

data_level2 = ['GDP', 
'CPI']

data_level3 = ['sample size', 
'regression', 
'correlation']

def level1_count(article):
    count_list = []
    for word in data_level1:
        word_count = article.count(word)
        if word_count > 0:
            count_list.append({word:word_count})
    return count_list


def cleanHTML(raw_html):
    return BeautifulSoup(raw_html, "lxml").text

def performRSS(url, categories):
    all_links = []
    for category in categories:
        NewsFeed = feedparser.parse(url.format(category))
        entries = NewsFeed.entries
        for entry in entries:
            temp_dict = {'url': entry.link, 'content': cleanHTML(entry.content[0].value), 'category': category, 'published_date':entry.published}
            all_links.append(temp_dict)        
    return all_links

def level1_len(count_list):
    return len(count_list)

def create_level1(df):
    traces = []
    for i in df.columns[1:]:
        trace = go.Bar(x=df['Newspaper'], y=df[i], name=i, text=df[i], textposition="outside")
        traces.append(trace)
    data = traces
    layout = go.Layout(barmode='group')
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(font=dict(size=9), legend=dict(x=-.1, y=1.2), legend_orientation="h")
    div = plotly.offline.plot(fig, include_plotlyjs=False, output_type='div', config={"displayModeBar": False})
    return div


@application.route('/')
def index():
    df_HT = pd.concat(map(pd.read_csv, glob.glob(os.path.join('newspaper/static/datasets/HT', "*.csv")))).drop_duplicates(['url'], 'first')
    df_OK = pd.concat(map(pd.read_csv, glob.glob(os.path.join('newspaper/static/datasets/OK', "*.csv")))).drop_duplicates(['url'], 'first')
    df_NT = pd.concat(map(pd.read_csv, glob.glob(os.path.join('newspaper/static/datasets/NT', "*.csv")))).drop_duplicates(['url'], 'first')
    df_TN = pd.concat(map(pd.read_csv, glob.glob(os.path.join('newspaper/static/datasets/TN', "*.csv")))).drop_duplicates(['url'], 'first')
    df_KT = pd.concat(map(pd.read_csv, glob.glob(os.path.join('newspaper/static/datasets/KT', "*.csv")))).drop_duplicates(['url'], 'first')
    df_LK = pd.concat(map(pd.read_csv, glob.glob(os.path.join('newspaper/static/datasets/LK', "*.csv")))).drop_duplicates(['url'], 'first')
    df_HT['level1'] = df_HT.content.apply(level1_count)
    df_OK['level1'] = df_OK.content.apply(level1_count)
    df_NT['level1'] = df_NT.content.apply(level1_count)
    df_TN['level1'] = df_TN.content.apply(level1_count)
    df_KT['level1'] = df_KT.content.apply(level1_count)
    df_LK['level1'] = df_LK.content.apply(level1_count)
    df_HT['level1_len'] = df_HT.level1.apply(level1_len)
    df_OK['level1_len'] = df_OK.level1.apply(level1_len)
    df_NT['level1_len'] = df_NT.level1.apply(level1_len)
    df_TN['level1_len'] = df_TN.level1.apply(level1_len)
    df_KT['level1_len'] = df_KT.level1.apply(level1_len)
    df_LK['level1_len'] = df_LK.level1.apply(level1_len)
    data = [
    ['The Himalayan Times', df_HT.level1_len.sum(), df_HT.shape[0]],
    ['Online Khabar', df_OK.level1_len.sum(), df_OK.shape[0]],
    ['Nepali Times', df_NT.level1_len.sum(), df_NT.shape[0]],
    ['Telegraph Nepal', df_TN.level1_len.sum(), df_TN.shape[0]],
    ['Katmandu Tribune', df_KT.level1_len.sum(), df_KT.shape[0]],
    ['Lokaantar', df_LK.level1_len.sum(), df_LK.shape[0]]
       ] 
    df = pd.DataFrame(data, columns = ['Newspaper', 'Level1', 'News Articles']) 
    div = create_level1(df)
    len_data_level_1, len_data_level_2, len_data_level_3 = len(data_level1), len(data_level2), len(data_level3)
    return render_template('index.html', column_names_level1=df.columns.values, row_data_level1=list(df.values.tolist()), div=div,\
      len_data_level_1=len_data_level_1, len_data_level_2=len_data_level_2, len_data_level_3=len_data_level_3)

@application.route('/getdata')
def getdata():
    today = date.today().strftime("%b-%d-%Y")
    himalayan_times_url = "https://thehimalayantimes.com/category{}/feed/"
    raw_HT = performRSS(himalayan_times_url, links)
    df_HT = pd.DataFrame(raw_HT).drop_duplicates()
    df_HT.to_csv('newspaper/static/datasets/HT/'+today+'.csv')
    online_khabar_url = "https://english.onlinekhabar.com/category{}/feed/"
    raw_OK = performRSS(online_khabar_url, links)
    df_OK = pd.DataFrame(raw_OK).drop_duplicates()
    df_OK.to_csv('newspaper/static/datasets/OK/'+today+'.csv') 
    nepali_times_url = "https://www.nepalitimes.com/nt{}/feed/"
    raw_NT = performRSS(nepali_times_url, links)
    df_NT = pd.DataFrame(raw_NT).drop_duplicates()
    df_NT.to_csv('newspaper/static/datasets/NT/'+today+'.csv') 
    telegraph_nepal_url = "http://telegraphnepal.com/category{}/feed/"
    raw_TN = performRSS(telegraph_nepal_url, links)
    df_TN = pd.DataFrame(raw_TN).drop_duplicates()
    df_TN.to_csv('newspaper/static/datasets/TN/'+today+'.csv') 
    kathmandu_tribune_url = "https://kathmandutribune.com/category{}/feed/"
    raw_KT = performRSS(kathmandu_tribune_url, links)
    df_KT = pd.DataFrame(raw_KT).drop_duplicates()
    df_KT.to_csv('newspaper/static/datasets/KT/'+today+'.csv') 
    lokaantar_url = "http://english.lokaantar.com/category{}/feed/"
    raw_LK = performRSS(lokaantar_url, links)
    df_LK = pd.DataFrame(raw_LK).drop_duplicates()
    df_LK.to_csv('newspaper/static/datasets/LK/'+today+'.csv') 
    return ('done')

