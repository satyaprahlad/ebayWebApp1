from time import time

import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse


def parse(content, to_scrape = ['h1', 'h2', 'h3','h4','h5']):
   if content.name in to_scrape:
      yield [content.name,"<"+content.name+">"+content.getText()]
   for i in getattr(content, 'contents', []):
      yield from parse(i)

def _scrapPage(url,tagsRequired=["h1","h2","h3","h4","h5"]):
    #url = 'https://karrierebibel.de/bewerbungsschreiben'
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, "html.parser")
    result = list(parse(soup))
    # result= list(parse(inner_content))
    #print(result)
    with open('file.md', 'w') as f:
        f.write('\n'.join(map(str, result)))

    return result

def scrapeGoogle(query,googleDomain):
    #query = "how to make fan"
    query = query.replace(' ', '+')
    #googleDomain="google.co.uk"
    URL = f"https://www."+googleDomain+"/search?q="+query
    # desktop user-agent
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    # mobile user-agent
    headers = {"user-agent" : USER_AGENT}
    resp = requests.get(URL, headers=headers)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "html.parser")
    results = []
    for g in soup.find_all('div', class_='r'):
        anchors = g.find_all('a')
        if anchors:
            link = anchors[0]['href']
            title = g.find('h3').text

            if "youtube" not in link and len(results) < 5:
                item = {
                    "title": title,
                    "link": link,
                    'scarpe':_scrapPage(link)
                }
                results.append(item)

    final = dict()
    final["searchResults"]= results
    return JsonResponse(final, safe=False)



def scrapeGoogle1(query,googleDomain):
    #query = "how to make fan"
    query = query.replace(' ', '+')
    #googleDomain="google.co.uk"
    URL = f"https://www."+googleDomain+"/search?q="+query
    # desktop user-agent
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    # mobile user-agent
    headers = {"user-agent" : USER_AGENT}
    resp = requests.get(URL, headers=headers)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "html.parser")
    results = []
    for g in soup.find_all('div', class_='r'):
        anchors = g.find_all('a')
        if anchors:
            link = anchors[0]['href']
            title = g.find('h3').text

            if "youtube" not in link and len(results) < 5:
                item = {
                    "title": title,
                    "link": link,
                    'scarpe':_scrapPage(link)
                }
                results.append(item)

    final = dict()
    final["searchResults"]= results
    return final


tic=time();
# url = "http://recoil.co.in/googlescrape?domain=" + "google.com" + "&query=" + "how+to+eat";
resp = scrapeGoogle1(query="how to eat",googleDomain="google.com" )
#print(list(resp))
toc=time()
print(" tic {tic} and toc {toc} and diff {tik}",tic,toc,toc-tic)
#
# tic=time();
# url = "http://recoil.co.in/googlescrape?domain=" + "google.com" + "&query=" + "how+to+eat";
# resp = requests.get(url)
# #print(list(resp))
# toc=time()
# print(" tic {tic} and toc {toc} and diff {tik}",tic,toc,toc-tic)

