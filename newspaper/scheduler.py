from flask import render_template
import pandas as pd
import numpy as np
from newspaper import application
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging
from newspaper.fetch_data import fetch_data

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

sched_daily = BackgroundScheduler(daemon=True)

  
@application.route('/scheduler/get_random_df')
def set_random_df():
    df = pd.read_csv('newspaper/static/datasets/scheduler_test.csv')
    table_html = df.to_html()
    return render_template('scheduler_test.html', table_html = table_html)

@application.route('/scheduler/set_random_df')
def get_random_df():
    df = pd.DataFrame(np.random.randint(0, 1000, size=(10, 4)), columns=list('ABCD'))
    df.to_csv('newspaper/static/datasets/scheduler_test.csv', index=False)
    return 'done'

def get_all_csvs():
    try:
        return fetch_data()
    except: 
        return 'failed'

# This route is created so that in cases of emergencies
# the data can be synced manually.
@application.route('/scheduler/main_job')
def main_job():
    # This if for test
    # return get_random_df()
    return get_all_csvs()

# TODO check for conflicts
@application.route('/scheduler/start')
def start_scheduler():
    try:
        sched_daily.add_job(main_job, 'interval', minutes = 180, id='get_csvs')
        sched_daily.start()
        return ("start collecting csvs")
    except:
        return ("The process might have already started")


@application.route('/scheduler/stop')
def stop_scheduler():
    try:
        sched_daily.remove_job('get_csvs')
        return ("stopped")
    except:
        return ("Job not started or already stopped.")

@application.route('/scheduler/status')
def monitor_daemon():
    try:
        chron_status = str(sched_daily.get_job('get_csvs')) 
        return chron_status
    except:
        return ('Check the scheduler')
	
