from django.http import HttpResponse
from . import GoogleSearchService


# Create your views here.
def hi(request):
     return HttpResponse('<h1>this is testng</h1>')

def googlescrape(request):
    domain = str(request.GET['domain']).strip()
    query = str(request.GET['query']).strip()
    results= GoogleSearchService.scrapeGoogle(query, domain)
    response= HttpResponse((results),content_type='application/json')
    response.status_code = 200
    return  response


