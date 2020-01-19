from bs4 import BeautifulSoup
import feedparser


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

def fetch_data():    
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
