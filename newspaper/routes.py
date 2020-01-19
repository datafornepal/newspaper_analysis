from flask import render_template, request
from newspaper import application
import pandas as pd
from datetime import date
import plotly
import plotly.graph_objects as go
from newspaper.levels import data_level1, data_level2,data_level3
from newspaper.prepare_dataframe import prepare_dataframe
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




@application.route('/')
def index():
    data1,data2,data3=prepare_dataframe()
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

