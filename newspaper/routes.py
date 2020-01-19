from flask import render_template, request
from newspaper import application
import pandas as pd
from datetime import date
import glob, os
import plotly
import plotly.graph_objects as go
from newspaper.levels import level1_count,level_2_3_count,level_2_3_filter,level_len,data_level1, data_level2,data_level3
from newspaper.fetch_data import fetch_data



def create_level(df):
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

def create_level_percent(df,color):
    trace = go.Bar(x=df['Newspaper'], text=df.iloc[:,-1], textposition="outside", 
                   y=df.iloc[:,-1], marker_color=color)
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


df_HT = pd.concat(map(pd.read_csv, glob.glob(os.path.join('newspaper/static/datasets/HT', "*.csv"))),sort=False).drop_duplicates(['url'], 'first').dropna()
df_OK = pd.concat(map(pd.read_csv, glob.glob(os.path.join('newspaper/static/datasets/OK', "*.csv"))),sort=False).drop_duplicates(['url'], 'first').dropna()
df_NT = pd.concat(map(pd.read_csv, glob.glob(os.path.join('newspaper/static/datasets/NT', "*.csv"))),sort=False).drop_duplicates(['url'], 'first').dropna()
df_TN = pd.concat(map(pd.read_csv, glob.glob(os.path.join('newspaper/static/datasets/TN', "*.csv"))),sort=False).drop_duplicates(['url'], 'first').dropna()
df_KT = pd.concat(map(pd.read_csv, glob.glob(os.path.join('newspaper/static/datasets/KT', "*.csv"))),sort=False).drop_duplicates(['url'], 'first').dropna()
df_LK = pd.concat(map(pd.read_csv, glob.glob(os.path.join('newspaper/static/datasets/LK', "*.csv"))),sort=False).drop_duplicates(['url'], 'first').dropna()
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

    div1 = create_level(df)
    div2 = create_level_percent(df,color='green')
    div3 = create_pie_chart(df)

    div4 = create_level(df2)
    div5 = create_level_percent(df2,color='indianred')
    
    div6 = create_level(df3)
    div7 = create_level_percent(df3,color='lightsalmon')

    len_data_level_1, len_data_level_2, len_data_level_3 = len(data_level1), len(data_level2), len(data_level3)

    return render_template('index.html', column_names_level1=df.columns.values, row_data_level1=list(df.values.tolist()), div1=div1, div2=div2, div3=div3, div4=div4, div5=div5, div6=div6, div7=div7,\
      len_data_level_1=len_data_level_1, len_data_level_2=len_data_level_2, len_data_level_3=len_data_level_3, total_articles=df['News Articles'].sum(), \
      column_names_level2=df2.columns.values, row_data_level2=list(df2.values.tolist()),\
      column_names_level3=df3.columns.values, row_data_level3=list(df3.values.tolist())
      )

@application.route('/getdata')
def getdata():
    fetch_data()
    return ('done')

