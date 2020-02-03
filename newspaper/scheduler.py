from flask import render_template
import pandas as pd
import numpy as np
from newspaper import application
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

sched_daily = BackgroundScheduler(daemon=True)

def fetch_data():    
    today = date.today().strftime("%b-%d-%Y")
    himalayan_times_url = "https://thehimalayantimes.com/category{}/feed/"
    raw_HT = performRSS(himalayan_times_url, links)
    df_HT = pd.DataFrame(raw_HT).drop_duplicates()
    df_HT.to_csv('newspaper/static/datasets/HT/'+today+'.csv', index=False)
    online_khabar_url = "https://english.onlinekhabar.com/category{}/feed/"
    raw_OK = performRSS(online_khabar_url, links)
    df_OK = pd.DataFrame(raw_OK).drop_duplicates()
    df_OK.to_csv('newspaper/static/datasets/OK/'+today+'.csv', index=False) 
    nepali_times_url = "https://www.nepalitimes.com/nt{}/feed/"
    raw_NT = performRSS(nepali_times_url, links)
    df_NT = pd.DataFrame(raw_NT).drop_duplicates()
    df_NT.to_csv('newspaper/static/datasets/NT/'+today+'.csv', index=False) 
    telegraph_nepal_url = "http://telegraphnepal.com/category{}/feed/"
    raw_TN = performRSS(telegraph_nepal_url, links)
    df_TN = pd.DataFrame(raw_TN).drop_duplicates()
    df_TN.to_csv('newspaper/static/datasets/TN/'+today+'.csv', index=False) 
    kathmandu_tribune_url = "https://kathmandutribune.com/category{}/feed/"
    raw_KT = performRSS(kathmandu_tribune_url, links)
    df_KT = pd.DataFrame(raw_KT).drop_duplicates()
    df_KT.to_csv('newspaper/static/datasets/KT/'+today+'.csv', index=False) 
    lokaantar_url = "http://english.lokaantar.com/category{}/feed/"
    raw_LK = performRSS(lokaantar_url, links)
    df_LK = pd.DataFrame(raw_LK).drop_duplicates()
    df_LK.to_csv('newspaper/static/datasets/LK/'+today+'.csv', index=False) 
    return True
  
@application.route('/scheduler/set_random_df')
def set_random_df():
    df = pd.read_csv('newspaper/static/datasets/scheduler_test.csv')
    table_html = df.to_html()
    return render_template('scheduler_test.html', table_html = table_html)

@application.route('/scheduler/get_random_df')
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
    if (get_all_csvs()):
        


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
	
