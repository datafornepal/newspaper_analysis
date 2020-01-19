from flask import render_template, request
from newspaper import application
import pandas as pd
from newspaper.levels import data_level1, data_level2,data_level3
from newspaper.prepare_dataframe import prepare_dataframe
from newspaper.fetch_data import fetch_data
from newspaper.level_chart import create_level,create_level_percent,create_pie_chart


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

