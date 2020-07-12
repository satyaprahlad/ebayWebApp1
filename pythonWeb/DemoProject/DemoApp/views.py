from django.shortcuts import render
from django.http import HttpResponse
import time
from .ebay import  FindAPI_Continues
# Create your views here.
# def hi(request):
#     return HttpResponse('<h1>this is testng</h1>')
def hi(request):
    return render(request,'DemoApp/home1.html')

def googlescrape(request):
    sellerId = str(request.GET['domain']).strip()
    noOfMonths = str(request.GET['query'])
    return []

def bye(request):
    mydict=dict()
    mydict['name1']='satya'
    response=HttpResponse((mydict),content_type='application/json')
    response.status_code=200

    return response

def homePage(request):
    return render(request,'DemoApp/sellerInput.html')

def sellerSearch(request):
    inputs=dict()
    sellerId=str(request.GET['sellerId']).strip()
    noOfMonths=int(request.GET['noOfMonths'])
    print(f"request parameters are {sellerId} and {noOfMonths}")
    inputs['sellerId'] = sellerId
    inputs['noOfMonths']=noOfMonths
    FindAPI_Continues.ebayFunction(inputs)
    response=HttpResponse(str({'result':'success'}),content_type='application/json')
    response.status_code=200
    return response
