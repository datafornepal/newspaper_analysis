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
    df = df.groupby('newspaper').sum().join(df.groupby('newspaper').size().to_frame('News Articles'))
    df.rename({'level_len': 'Level1', 'level2_len': 'Level2', 'level3_len': 'Level3', 'level_2_3_valid':'Filtered Articles'}, inplace=True, axis=1)

    df['Level1 %'] = (100*df['Level1']/df['News Articles']).map('{:,.1f} %'.format)
    df['Level2 %'] = (100*df['Level2']/df['Filtered Articles']).map('{:,.1f} %'.format)
    df['Level3 %'] = (100*df['Level3']/df['Filtered Articles']).map('{:,.1f} %'.format)


    mapping = pd.DataFrame({'Newspaper': ['The Himalayan Times', 'Katmandu Tribune', 'Lokaantar', 'Nepali Sansar', 'Nepali Times', 'Online Khabar', 'Telegraph Nepal']}, 
             index=['ht', 'kt', 'lk', 'ns', 'nt', 'ok', 'tn'])

    df = df.join(mapping)

    len_data_level_1, len_data_level_2, len_data_level_3 = lengths_of_keywords()
    newspapers = df['Newspaper'].tolist()


    chart1 = [{'name':'Level 1','data':df['Level1'].tolist()},{'name':'Total Articles','data':df['News Articles'].tolist()}]
    chart2 = (df['Level1']/df['News Articles']*100).tolist()

    chart3 = [{'name':'Level 2','data':df['Level2'].tolist()},{'name':'Total Articles','data':df['News Articles'].tolist()}]
    chart4 = (df['Level2']/df['News Articles']*100).tolist()

    chart5 = [{'name':'Level 3','data':df['Level3'].tolist()},{'name':'Total Articles','data':df['News Articles'].tolist()}]
    chart6 = (df['Level3']/df['News Articles']*100).tolist()
    
    level1 = df[['Newspaper', 'Level1', 'News Articles', 'Level1 %']]
    column_names_level1 = level1.columns.values
    row_data_level1 = list(level1.values.tolist())

    level2 = df[['Newspaper', 'Level2', 'Filtered Articles', 'News Articles',  'Level2 %']]
    column_names_level2 = level2.columns.values
    row_data_level2 = list(level2.values.tolist())

    level3 = df[['Newspaper', 'Level3', 'Filtered Articles', 'News Articles', 'Level3 %']]
    column_names_level3 = level3.columns.values
    row_data_level3 = list(level3.values.tolist())

    content = {
        'newspapers': newspapers,
        'chart1': chart1,
        'chart2': chart2,
        'chart3': chart3,
        'chart4': chart4,
        'chart5': chart5,
        'chart6': chart6,
        'column_names_level1' : column_names_level1,
        'row_data_level1' : row_data_level1,
        'column_names_level2' : column_names_level2,
        'row_data_level2' : row_data_level2,
        'column_names_level3' : column_names_level3,
        'row_data_level3' : row_data_level3,
    }

    return render_template ('base.html', **content)



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