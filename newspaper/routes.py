from flask import render_template, request
from newspaper import application
import feedparser
import pandas as pd
from bs4 import BeautifulSoup
from datetime import date
import glob, os
import plotly
import plotly.graph_objects as go
from newspaper.levels import level1_count,level_2_3_count,level_2_3_filter,level_len,data_level1, data_level2,data_level3,data_level_indicator,filter_list
# import re
# from nltk.corpus import stopwords 
# from nltk.tokenize import word_tokenize 


# stop_words = set(stopwords.words('english')) 

links=['/about-town','/analysis','/business','/commentary','/current_affairs','/editorial','/editorials','/education','/entertainment','/finance','/governance','/headline','/here-now','/international','/interview','/kathmandu','/latest','/lifestyle','/multimedia','/national','/nepal','/opinion','/political','/science-technology','/sports','/travel','/world']


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



def create_level1(df):
    traces = []
    for i in df.columns[1:-1]:
        trace = go.Bar(x=df['Newspaper'], y=df[i], name=i, text=df[i], textposition="outside")
        traces.append(trace)
    data = traces
    layout = go.Layout(barmode='group')
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(font=dict(size=9), legend=dict(x=-.1, y=1.2), legend_orientation="h", margin=dict(t=5,b=5,l=5,r=5))
    div = plotly.offline.plot(fig, include_plotlyjs=False, output_type='div', config={"displayModeBar": False})
    return div

def create_level1_percent(df):
    trace = go.Bar(x=df['Newspaper'], text=df['Level1 %'], textposition="outside", 
                   y=df['Level1 %'], marker_color='green')
    data = [trace]
    layout = go.Layout(margin=dict(t=5,b=5,l=5,r=5))
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(font=dict(size=9))
    div = plotly.offline.plot(fig, include_plotlyjs=False,
                              output_type='div', config={"displayModeBar": False})
    return div


def create_level2_percent(df):
    trace = go.Bar(x=df['Newspaper'], text=df['Level2 %'], textposition="outside", 
                   y=df['Level2 %'], marker_color='indianred')
    data = [trace]
    layout = go.Layout(margin=dict(t=5,b=5,l=5,r=5))
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(font=dict(size=9))
    div = plotly.offline.plot(fig, include_plotlyjs=False,
                              output_type='div', config={"displayModeBar": False})
    return div

def create_level3_percent(df):
    trace = go.Bar(x=df['Newspaper'], text=df['Level3 %'], textposition="outside", 
                   y=df['Level3 %'], marker_color='lightsalmon')
    data = [trace]
    layout = go.Layout(margin=dict(t=5,b=5,l=5,r=5))
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(font=dict(size=9))
    div = plotly.offline.plot(fig, include_plotlyjs=False,
                              output_type='div', config={"displayModeBar": False})
    return div

def create_pie_chart(df):
    data=[go.Pie(labels=df['Newspaper'], values=df['News Articles'], hole=.3)]
    layout = go.Layout(margin=dict(t=5,b=5,l=5,r=5))
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(font=dict(size=9), legend=dict(x=-.1, y=1.2), legend_orientation="h")
    div = plotly.offline.plot(fig, include_plotlyjs=False,
                              output_type='div', config={"displayModeBar": False})
    return div


df_HT = pd.concat(map(pd.read_csv, glob.glob(os.path.join('newspaper/static/datasets/HT', "*.csv")))).drop_duplicates(['url'], 'first').dropna()
df_OK = pd.concat(map(pd.read_csv, glob.glob(os.path.join('newspaper/static/datasets/OK', "*.csv")))).drop_duplicates(['url'], 'first').dropna()
df_NT = pd.concat(map(pd.read_csv, glob.glob(os.path.join('newspaper/static/datasets/NT', "*.csv")))).drop_duplicates(['url'], 'first').dropna()
df_TN = pd.concat(map(pd.read_csv, glob.glob(os.path.join('newspaper/static/datasets/TN', "*.csv")))).drop_duplicates(['url'], 'first').dropna()
df_KT = pd.concat(map(pd.read_csv, glob.glob(os.path.join('newspaper/static/datasets/KT', "*.csv")))).drop_duplicates(['url'], 'first').dropna()
df_LK = pd.concat(map(pd.read_csv, glob.glob(os.path.join('newspaper/static/datasets/LK', "*.csv")))).drop_duplicates(['url'], 'first').dropna()
df_HT['level1'] = df_HT.content.apply(level1_count)
df_OK['level1'] = df_OK.content.apply(level1_count)
df_NT['level1'] = df_NT.content.apply(level1_count)
df_TN['level1'] = df_TN.content.apply(level1_count)
df_KT['level1'] = df_KT.content.apply(level1_count)
df_LK['level1'] = df_LK.content.apply(level1_count)

df_HT['level_len'] = df_HT.level1.apply(level_len)
df_OK['level_len'] = df_OK.level1.apply(level_len)
df_NT['level_len'] = df_NT.level1.apply(level_len)
df_TN['level_len'] = df_TN.level1.apply(level_len)
df_KT['level_len'] = df_KT.level1.apply(level_len)
df_LK['level_len'] = df_LK.level1.apply(level_len)

df_HT['level_2_3_valid'] = df_HT.content.apply(level_2_3_filter)
df_HT_level_2_3 = df_HT[df_HT['level_2_3_valid']==1].reset_index(drop=True)
df_OK['level_2_3_valid'] = df_OK.content.apply(level_2_3_filter)
df_OK_level_2_3 = df_OK[df_OK['level_2_3_valid']==1].reset_index(drop=True)
df_NT['level_2_3_valid'] = df_NT.content.apply(level_2_3_filter)
df_NT_level_2_3 = df_NT[df_NT['level_2_3_valid']==1].reset_index(drop=True)
df_TN['level_2_3_valid'] = df_TN.content.apply(level_2_3_filter)
df_TN_level_2_3 = df_TN[df_TN['level_2_3_valid']==1].reset_index(drop=True)
df_KT['level_2_3_valid'] = df_KT.content.apply(level_2_3_filter)
df_KT_level_2_3 = df_KT[df_KT['level_2_3_valid']==1].reset_index(drop=True)
df_LK['level_2_3_valid'] = df_LK.content.apply(level_2_3_filter)
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

df_HT_level_2_3['level3_len'] = df_HT_level_2_3.level3.apply(level_len)
df_OK_level_2_3['level3_len'] = df_OK_level_2_3.level3.apply(level_len)
df_NT_level_2_3['level3_len'] = df_NT_level_2_3.level3.apply(level_len)
df_TN_level_2_3['level3_len'] = df_TN_level_2_3.level3.apply(level_len)
df_KT_level_2_3['level3_len'] = df_KT_level_2_3.level3.apply(level_len)
df_LK_level_2_3['level3_len'] = df_LK_level_2_3.level3.apply(level_len)

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


@application.route('/')
def index():
    df = pd.DataFrame(data1, columns = ['Newspaper', 'Level1', 'News Articles']) 
    df2 = pd.DataFrame(data2, columns = ['Newspaper', 'Level2', 'News Articles']) 
    df3 = pd.DataFrame(data3, columns = ['Newspaper', 'Level3', 'News Articles']) 

    df['Level1 %'] = round(df['Level1']/df['News Articles']*100).map('{:,.0f} %'.format)
    df2['Level2 %'] = round(df2['Level2']/df2['News Articles']*100).map('{:,.0f} %'.format)
    df3['Level3 %'] = round(df3['Level3']/df3['News Articles']*100).map('{:,.0f} %'.format)

    div1 = create_level1(df)
    div2 = create_level1_percent(df)
    div3 = create_pie_chart(df)

    div4 = create_level1(df2)
    div5 = create_level2_percent(df2)
    
    div6 = create_level1(df3)
    div7 = create_level3_percent(df3)

    len_data_level_1, len_data_level_2, len_data_level_3 = len(data_level1), len(data_level2), len(data_level3)

    return render_template('index.html', column_names_level1=df.columns.values, row_data_level1=list(df.values.tolist()), div1=div1, div2=div2, div3=div3, div4=div4, div5=div5, div6=div6, div7=div7,\
      len_data_level_1=len_data_level_1, len_data_level_2=len_data_level_2, len_data_level_3=len_data_level_3, total_articles=df['News Articles'].sum(), \
      column_names_level2=df2.columns.values, row_data_level2=list(df2.values.tolist()),\
      column_names_level3=df3.columns.values, row_data_level3=list(df3.values.tolist())
      )

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

