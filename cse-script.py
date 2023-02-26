from googleapiclient.discovery import build
from bs4 import BeautifulSoup
from itertools import count
from requests.exceptions import HTTPError

import configparser
import time, random
import requests
import pandas as pd

# %%
def get_urls(calls, search_query, api_key, cse_id):
    ''' Number of calls is linked to expected number of results. Limit is that a function call can only 
        return a maximum of 100 results and returns 10 results per call. So, if a total of 65 results
        are expected, then calls must be equal to 7. 
    '''
    urls = set()
    start_ = 1
    
    service = build('customsearch', 'v1', developerKey = api_key).cse()
    
    # I switch the default start of itertools.count because I find it easier to start counting from 1.
    for i in count(1):
        if i > calls:
            break
        try:    
            result = service.list(q=search_query, cx=cse_id, start=start_).execute()
            for item in result['items']:
                urls.add(item['link'])
        except HTTPError:
            pass
            
        start_ += 10
        time.sleep(random.uniform(1,2))
        
    return urls
        

# %%
def get_article_text(**kwargs):
    urls = kwargs['urls']
    article_tag = kwargs['article_tag']
    article_class = kwargs['article_class']
    
    article_texts = []
    
    for url in urls:
        url_text = requests.get(url).text
        soup = BeautifulSoup(url_text, 'lxml')
        
        try:
            article_text = soup.find(article_tag, class_ = article_class).text
        except AttributeError:
            pass
        
        article_texts.append(article_text)
            
        time.sleep(random.uniform(1,2))
        
    return article_texts

# %%
def save_results(urls, article_texts, site):
    data = {'Link': list(urls), 'Link-text': article_texts} 
    df = pd.DataFrame(data)
    df.to_excel(f'{site}_data.xlsx')

    return df

# %%
# Read in access details from config file
config = configparser.ConfigParser()
config.read("config.ini")

# cse api key
api_key = config["cse"]["API_key"]

# cse ids for the 2 news sites
three_news_id = config["cse"]["three_news_id"]
myjoyonline_id = config["cse"]["myjoyonline_id"]

# search query
search_query = "ghana water company limited after:2020-01-01"

# three news
three_news_text_tag = config['cse']['three_news_text_tag']
three_news_text_class = config['cse']['three_news_text_class']

myjoyonline_text_tag = config['cse']['myjoyonline_text_tag']
myjoyonline_text_class = config['cse']['myjoyonline_text_class']

# %%
# First do a manual google search to determine the total number of returned search results
# google cse returns max 100 results so calls argument will be max 10 since each cse call returns 10 results
# if the manual google search returns 56 results for example, then calls argument will have to be 6



# %%
# Search from 3news.com

links = get_urls(calls=10, search_query=search_query, api_key=api_key, cse_id=three_news_id)

article_texts = get_article_text(urls=links, article_tag=three_news_text_tag, article_class=three_news_text_class)

save_results(links, article_texts, site="three_news")

# %%
# Search from 3news.com
links = get_urls(calls=10, search_query=search_query, api_key=api_key, cse_id=three_news_id)

article_texts = get_article_text(urls=links, article_tag=myjoyonline_text_tag, article_class=myjoyonline_text_class)

save_results(links, article_texts, site="myjoyonline")

# %%
# Search from myjoyonline.com
links = get_urls(calls=10, search_query=search_query, api_key=api_key, cse_id=myjoyonline_news_id)

article_texts = get_article_text(urls=links, article_tag=myjoyonline_text_tag, article_class=myjoyonline_text_class)

save_results(links, article_texts, site="myjoyonline")

# %%



