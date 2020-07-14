import concurrent.futures
import traceback
from time import time

import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse


to_scrape = ['h1', 'h2', 'h3','h4','h5']

def parse(content ):
   if content.name in to_scrape:
      yield [content.name,"<"+content.name+">"+content.getText()]
   for i in getattr(content, 'contents', []):
      yield from parse(i)

def _scrapPage(item):
    reqs = requests.get(item['link'])
    soup = BeautifulSoup(reqs.text, "html.parser")
    result = list(parse(soup))
    item2=dict()
    item2['link']=item['link']
    item2['title']=item['title']
    item2['scarpe']=result
    return item2

def scrapeGoogle(query,googleDomain):
    query = query.replace(' ', '+')
    URL = f"https://www."+googleDomain+"/search?q="+query
    # desktop user-agent
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    # mobile user-agent
    headers = {"user-agent" : USER_AGENT}
    resp = requests.get(URL, headers=headers)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "html.parser")
    links = []
    titles=[]
    items=[]
    for g in soup.find_all('div', class_='r'):
        anchors = g.find_all('a')
        if anchors:
            link = anchors[0]['href']
            title = g.find('h3').text
            if "youtube" not in link and len(items) < 5:
                item = {
                    "title": title,
                    "link": link
                }
                items.append(item)

    #tic = time.perf_counter()
    results=[]
    #print(links)
    #print(titles)
    with concurrent.futures.ThreadPoolExecutor(5) as executor:
        results = [executor.submit(_scrapPage, item) for item in items]
        for future in results:
            try:
                yield future.result()
            except:
                traceback.print_exc()
    final = dict()
    final["searchResults"]= results
    return final

tic=time();
resp = scrapeGoogle(query="how to eat",googleDomain="google.com" )
resp=list(resp)
#print(resp)
print(len(resp))
#print(list(resp))
toc=time()
print(" tic {tic} and toc {toc} and diff {tik}",tic,toc,toc-tic)
#
# tic=time();
# resp = scrapeGoogle1(query="how to eat",googleDomain="google.com" )
# #print(list(resp))
# toc=time()
# print(" tic {tic} and toc {toc} and diff {tik}",tic,toc,toc-tic)

tic=time();
url = "http://recoil.co.in/googlescrape?domain=" + "google.com" + "&query=" + "how+to+eat";
resp = requests.get(url)
#print(list(resp))
toc=time()
print(" tic {tic} and toc {toc} and diff {tik}",tic,toc,toc-tic)

# tic=time();
# resp = scrapeGoogle2(query="how to eat",googleDomain="google.com" )
# #print(list(resp))
# toc=time()
# print(" tic {tic} and toc {toc} and diff {tik}",tic,toc,toc-tic)