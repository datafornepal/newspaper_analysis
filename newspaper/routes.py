from flask import render_template, request
from newspaper import application
import pandas as pd
from newspaper.fetch_data import fetch_merge_analyze_data, lengths_of_keywords
from newspaper.level_chart import create_level, create_level_percent, create_pie_chart
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import traceback

from flask_basicauth import BasicAuth

basic_auth = BasicAuth(application)

# logging.basicConfig()
# logging.getLogger('apscheduler').setLevel(logging.DEBUG)

sched_daily = BackgroundScheduler(daemon=True)


@application.route('/')
def index():
    df = pd.read_csv('newspaper/static/datasets/level1.csv')
    df2 = pd.read_csv('newspaper/static/datasets/level2.csv')
    df3 = pd.read_csv('newspaper/static/datasets/level3.csv')

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

    len_data_level_1, len_data_level_2, len_data_level_3 = lengths_of_keywords()

    return render_template('index.html', column_names_level1=df.columns.values, row_data_level1=list(df.values.tolist()), div1=div1, div2=div2, div3=div3, div4=div4, div5=div5, div6=div6, div7=div7,\
      len_data_level_1=len_data_level_1, len_data_level_2=len_data_level_2, len_data_level_3=len_data_level_3, total_articles=df['News Articles'].sum(), \
      column_names_level2=df2.columns.values, row_data_level2=list(df2.values.tolist()),\
      column_names_level3=df3.columns.values, row_data_level3=list(df3.values.tolist())
      )

@application.route('/getdata')
def getdata():
    fetch_merge_analyze_data()
    return ('done')


@application.route('/scheduler/get_random_df')
@basic_auth.required
def get_random_df():
    df = pd.read_csv('newspaper/static/datasets/scheduler_test.csv')
    table_html = df.to_html()
    return render_template('scheduler_test.html', table_html = table_html)

@application.route('/scheduler/set_random_df')
@basic_auth.required
def set_random_df():
    df = pd.DataFrame(np.random.randint(0, 1000, size=(10, 4)), columns=list('ABCD'))
    df.to_csv('newspaper/static/datasets/scheduler_test.csv', index=False)
    return 'done'


# This route is created so that in cases of emergencies
# the data can be synced manually.
@application.route('/scheduler/main_job')
@basic_auth.required
def main_job():
    # This if for test
    # return get_random_df()
    return fetch_data

# TODO check for conflicts
@application.route('/scheduler/start')
@basic_auth.required
def start_scheduler():
    try:
        sched_daily.add_job(main_job, 'interval', minutes = 180, id='get_csvs')
        sched_daily.start()
        return ("start collecting csvs")
    except:
        return ("The process might have already started")


@application.route('/scheduler/stop')
@basic_auth.required
def stop_scheduler():
    try:
        sched_daily.remove_job('get_csvs')
        return ("stopped")
    except:
        return ("Job not started or already stopped.")

@application.route('/scheduler/status')
@basic_auth.required
def monitor_daemon():
    try:
        chron_status = str(sched_daily.get_job('get_csvs')) 
        return chron_status
    except:
        return ('Check the scheduler')