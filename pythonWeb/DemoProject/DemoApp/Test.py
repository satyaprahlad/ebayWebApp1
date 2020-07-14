import requests
from bs4 import BeautifulSoup
from time import time

from pythonWeb.DemoProject.DemoApp import GoogleSearchService

tic=time();
url = "http://recoil.co.in/googlescrape?domain=" + "google.com" + "&query=" + "how+to+eat";
resp = GoogleSearchService.scrapeGoogle(query="how to eat",googleDomain="google.com" )
#print(list(resp))
toc=time()
print(" tic {tic} and toc {toc} and diff {toc-tic}")
