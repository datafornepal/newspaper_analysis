from flask import render_template, request
from newspaper import application
import pandas as pd
from newspaper.fetch_data import fetch_merge_analyze_data_new, lengths_of_keywords
from newspaper.level_chart import create_level, create_level_percent, create_pie_chart
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import zipfile
import io
import pathlib
import traceback
import flask
from datetime import date

from flask_basicauth import BasicAuth

basic_auth = BasicAuth(application)

sched_daily = BackgroundScheduler(daemon=True)


@application.route('/')
def index():

    df = pd.read_csv('newspaper/static/datasets/all.csv')
    grouped = df.groupby('newspaper').sum().join(df.groupby('newspaper').size().to_frame('News Articles'))

    grouped['Level1 %'] = (100*grouped['level_len']/grouped['News Articles']).map('{:,.1f} %'.format)
    grouped['Level2 %'] = (100*grouped['level2_len']/grouped['level_2_3_valid']).map('{:,.1f} %'.format)
    grouped['Level3 %'] = (100*grouped['level3_len']/grouped['level_2_3_valid']).map('{:,.1f} %'.format)


    mapping = pd.DataFrame({'Newspaper': ['The Himalayan Times', 'Katmandu Tribune', 'Lokaantar', 'Nepali Sansar', 'Nepali Times', 'Online Khabar', 'Telegraph Nepal']}, 
             index=['ht', 'kt', 'lk', 'ns', 'nt', 'ok', 'tn'])

    grouped = grouped.join(mapping)

    return grouped.to_html()

    # len_data_level_1, len_data_level_2, len_data_level_3 = lengths_of_keywords()

    # chart1 = [{'name':'Level 1','data':df['Level1'].tolist()},{'name':'Total Articles','data':df['News Articles'].tolist()}]
    
    # chart2 = df['Level1']/df['News Articles']*100
    # chart2 = chart2.tolist()
    
    # chart3 = [{'name':'Level 2','data':df2['Level2'].tolist()},{'name':'Total Articles','data':df2['News Articles'].tolist()}]
    
    # chart4 = df2['Level2']/df2['News Articles']*100
    # chart4 = chart4.tolist()
    
    # chart5 = [{'name':'Level 3','data':df3['Level3'].tolist()},{'name':'Total Articles','data':df3['News Articles'].tolist()}]
    
    # chart6 = df3['Level3']/df3['News Articles']*100
    # chart6 = chart6.tolist()
    
    # newspapers = df['Newspaper'].tolist()
    
    # return render_template('base.html', column_names_level1=df.columns.values, row_data_level1=list(df.values.tolist()), \
    #   len_data_level_1=len_data_level_1, len_data_level_2=len_data_level_2, len_data_level_3=len_data_level_3, total_articles=df['News Articles'].sum(), \
    #   column_names_level2=df2.columns.values, row_data_level2=list(df2.values.tolist()),\
    #   column_names_level3=df3.columns.values, row_data_level3=list(df3.values.tolist()), chart1=chart1, newspapers=newspapers, chart2=chart2, chart3=chart3, chart4=chart4, chart5=chart5,chart6=chart6
    #   )


# This route is created so that in cases of emergencies
# the data can be synced manually.
@application.route('/scheduler/main_job')
@basic_auth.required
def main_job_manual():
    # This if for test
    # return get_random_df()
    if (fetch_merge_analyze_data_new()):
        return "done"
    return "check logs"

def main_job():
    # This if for test
    # return get_random_df()
    if (fetch_merge_analyze_data_new()):
        return "done"
    return "check logs"

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

@application.route('/raw_datasets')
@basic_auth.required
def request_zip():
    base_path = pathlib.Path('newspaper/static/datasets/')
    data = io.BytesIO()
    with zipfile.ZipFile(data, mode='w') as z:
        for f_name in base_path.iterdir():
            z.write(f_name)
    data.seek(0)
    return flask.send_file(
        data,
        mimetype='application/zip',
        as_attachment=True,
        attachment_filename=date.today().strftime("%B_%d")+'_datasets.zip'
    )