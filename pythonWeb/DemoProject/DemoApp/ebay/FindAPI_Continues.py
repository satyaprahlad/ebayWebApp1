import copy
import concurrent.futures
import getpass
import sys
from sys import exc_info

from ebaysdk.finding import Connection as Finding
from ebaysdk.shopping import Connection as Shopping
import logging

import threading
import datetime
import time
import gspread.client
from oauth2client.service_account import ServiceAccountCredentials


thread_local=threading.local()

logging.basicConfig(filename="FindAPI.log",

                   filemode='w')
#logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# Creating an object
logger = logging.getLogger()
# Setting the threshold of logger to DEBUG
logger.setLevel(logging.INFO)

def updateToGSheet(data ,error=None,sellerIdFromSheet="",noOfMonths="0"):
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    #creds = ServiceAccountCredentials.from_json_keyfile_name("ebayPractice-f9627f3e653b.json", scope)
    keyFile={
  "type": "service_account",
  "project_id": "ebaypractice",
  "private_key_id": "f9627f3e653b3d76d6ca9ca1d1c76324bed4751b",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDJsmxXyGcMJIgs\nlixgNpwn22gSvo87ruC2vzjTkOCjIblwWuNFSodNt2S3mjZbh7bcYh1fJdpq6+Xj\nwAK8zD6hZxMRBHxZkSGmODHT5IupTowJ68GiiHNLTD/9NktAIwYuvahQQj3/Klsl\nbAIxs6NQ9TQTmyGmqLUDF7n6gjiEnNWz47HX1tFD718hX3fOgthkGHwOOPpcqwgg\nrHl+eKHCrFecZVO65gEQUTC9OsIPfsMAxmocG89D//KRbhPA8qDaFfXU/wM4hf7g\nivarzwSHHgfIb6lcYScsLoY07QcgXNUo79RYUXnnrPFZHBytlx7vqt35+yv/XXTF\nktkemA1PAgMBAAECggEABELNMCOPLb391HdNs7CjpuHnNnIpI3kjzSiIAkwuurOF\nL97zqyySZC1qJsjOuitJTSmTdkWd8iFOp3uQcz2bWxyK1hKyr8+1lsXcI55R5v8+\nTR1aZ10blm0jcu15NH8o68bc7ekgVyolZ8p612L0ocq0UW+3C8bHoCuZpbWnjQGb\ni5ug9bIihrOE+D6dB6Q4lhYmb8BA4UoAf0OKmcuv8fLPMjjmeUlrjqQUycd5atGX\n4wYHEHlPmb3j3TM0MtIScuCPpIVXJAwuwexouYZ5NCsX38NhG0f7fEhQQBj/F115\n+jPQSd8gmgRczqt/NmqJC5eZHMgZsJ3hdVT9LGlD1QKBgQD5cdtIi3u1WHtQPzXD\n2V5Uqyq4XxIxlUWBvZx6CqMOSTQjGP0pKrnt4qUBcGGH/Cu9YwiBgUwFxHBVxYrB\nGOorf7isQKib8FYMQTqIUIIdu48f2QMrXM5jIAWLjE9YSz/QFYkht3Mq11/oY0Y5\nYYASXmDuHCFpBdNOOBLXQUp+8wKBgQDO/1e5BkJ5yfosslmK3JivTYxQyNFtPk/W\nlhbFm4kS2TPy3c6o0XaHGiO9Dh4RP/oLgvJQDvRiZ4ZwrhsXHNevsx3ckC4oKGqZ\nM5Ody/aCRgCdQq0j65ZSd6Br1iYzKDce1jyKj/cXSdASehQJlqcwalcHAHsYi5na\nhIq7EIhnNQKBgAHuAo9GHPfjLlkJlCXmuZcYF+WDPsXJbNc7G0nKaUaEBHY9DEBU\nR0ny1enz7504szHs4TT3RhpJUcEoHRGvWqhpfYk/ms5SBqhjnMtPLCKEv++0IxUj\ny6jyp3hT5o09T8oRUJVFMQvkzKYklnd9LJt3xXIyH4QLen4BawvlQmlHAoGBAKcu\nfeg3EQuSQJdG+KD5p+u2A0Tf3J2RvSPAFuZEx4HMoXNfB+E7Q7K8Pu8bbtdZx5by\njMhyO5kaqe9p/wE8z0rdrJmObWkLs4TGrku9BvySkz5wMqyXQtKaQZu22yVoLpSe\nTUlQGy3Y9M9nf7V60s98o4tJLSJW5c0iTXXmVXSdAoGAUrPzwIA/jHdvFkFciaZ7\n0x7L9e73WZGxMY8jUvKaovcCgzhi4UbqF9705SlM7Y2kUETEqXJcZkREkEFxuGRK\nnN2j7PxGa3PZlbNdbbvRv+q+B2igSHUwL43A0RaWgxlulkl/d+s7AkNsRc9/nje8\ngrPiZjnKwNlz6Qi4w579UpU=\n-----END PRIVATE KEY-----\n",
  "client_email": "ebaytest1@ebaypractice.iam.gserviceaccount.com",
  "client_id": "117154050286596394561",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/ebaytest1%40ebaypractice.iam.gserviceaccount.com"
}

    creds=ServiceAccountCredentials.from_json_keyfile_dict(keyFile,scope)
    client = gspread.authorize(creds)

    outputSheet = client.open("OrderInformationsWork").worksheet("Output")
    allRowsValues = [
                     ['','','','Seller Details : '+str(sellerIdFromSheet)+' For '+str(noOfMonths)+' Month(s)','','','Sheet Last Updated at: '+str(datetime.datetime.now())+' by '+getpass.getuser()],
                     [],
                     ['Title', 'Price', 'Watch','Sold', 'CategoryID','Duration', 'Viewed','TimeLeft before Listing Ends' ]]

    if (error is not None):
        errors = ['Failed to update sheet with reason : ', str(error), ' at ', str(datetime.datetime.now())]
        logger.exception(f"error with {error}")
        outputSheet.clear()
        outputSheet.append_row(errors)
        raise Exception(error)
        return

    #allRowsValues.append(eachRow1)
    for eachItem in data:
        #print(eachItem)
        watchCont=0 if eachItem['listingInfo'].get('watchCount') is None else int(eachItem['listingInfo']['watchCount'])
        QuantitySold=int(eachItem['QuantitySold'])
        HitCount=0 if eachItem.get('HitCount') is None else int(eachItem['HitCount'])
        eachRow = [eachItem.get('title'), float(eachItem['sellingStatus']['currentPrice']['value']),
                   watchCont,
                   QuantitySold,
                   int(eachItem['primaryCategory']['categoryId']),
                   int(eachItem.get('DurationCalc'))
            ,HitCount, eachItem['sellingStatus']['timeLeft']]
        allRowsValues.append(eachRow)

    outputSheet.clear()
    outputSheet.append_rows(allRowsValues)

    #For starting heading
    outputSheet.format("A1:F1", {"textFormat": {"bold": True, "fontSize": 12, "foregroundColor": {
        "red": 1.0,
        "green": 0.0,
        "blue": 0.0
    }}})

    #for each attribute
    outputSheet.format("A3:I3", {"textFormat": {"bold": True, "fontSize": 12, "foregroundColor": {
        "red": 1.0,
        "green": 0.0,
        "blue": 0.0
    }}})
    #to print timestamp at right side of sheet
    outputSheet.format("I1:M1", {"textFormat": {"bold": False, "fontSize": 12, "foregroundColor": {
        "red": 0.0,
        "green": 1.0,
        "blue": 0.0
    }}})#ok
    # reset format

    outputSheet.merge_cells('D1:F1')
    outputSheet.merge_cells('G1:I1')

    inputSheet=client.open("OrderInformationsWork").worksheet("Input")

    inputSheet.format("B4:B4", {"backgroundColor": {
    "red": 1.0,
    "green": 0.8,
    "blue": 0.3
    },"textFormat": {"bold": False, "fontSize": 12}})
    inputSheet.update_cell(4,2,"")
    # clearing input value so that script will not process repeatedly.

def get_session():
    if not hasattr(thread_local, "api"):
        thread_local.api = Shopping(config_file=None, domain='open.api.ebay.com',
                                    appid="SatyaPra-MyEBPrac-PRD-abce464fb-dd2ae5fe",
                                    devid="6c042b69-e90f-4897-9045-060858248665",
                                    certid="PRD-bce464fbd03b-273a-4416-a299-7d41"
                                    )
    return thread_local.api



thread_local_FindingApi_Session=threading.local()
def getFindingApiSession():
    if not hasattr(thread_local_FindingApi_Session,"api"):
        thread_local_FindingApi_Session.api=Finding(config_file=None, domain='svcs.ebay.com', appid="SatyaPra-MyEBPrac-PRD-abce464fb-dd2ae5fe",
                  devid="6c042b69-e90f-4897-9045-060858248665",
                  certid="PRD-bce464fbd03b-273a-4416-a299-7d41"
                  )
    return thread_local_FindingApi_Session.api

def retrieveFromSecondPage(inputObj):
    api=getFindingApiSession()
    response = api.execute('findItemsAdvanced', inputObj).dict()
    #logger.debug(f" thread name {threading.currentThread().name } result is : {response}")
    return response


def main():

        try:
            ebayFunction()
            time.sleep(100)
        except:logger.exception("Exception at processing")

def ebayFunction(userInput):
    api = Finding(config_file=None, domain='svcs.ebay.com', appid="SatyaPra-MyEBPrac-PRD-abce464fb-dd2ae5fe",
                  devid="6c042b69-e90f-4897-9045-060858248665",
                  certid="PRD-bce464fbd03b-273a-4416-a299-7d41"
                  )

    items = list()

    inputObj = {
        "itemFilter": {
            "name": "Seller",
            "value": ""
        },
        "OutputSelector": [
            "Title",
            "itemId",
            "ViewItemURL",
            "SellingStatus",
            "ListingDuration",
            "listingInfo"
            "StartTime",
            "EndTime",
            "WatchCount",
            "ItemsPerPage",
            "PrimaryCategory",
            "HasMoreItems",
            "PageNumber",
            "ReturnedItemCountActual",
            "PaginationResult"
        ],
        "StartTimeFrom": "",
        "StartTimeTo": "",
        "IncludeWatchCount": "true",

        "paginationInput": {
            "entriesPerPage": "100",
            "pageNumber": "0"

        }
    }

    print(userInput)
    startDateTo = datetime.datetime.now()
    startDateFrom = startDateTo - datetime.timedelta(15)
    sellerId=userInput["sellerId"]
    noOfMonths = userInput["noOfMonths"]
    logger.debug(f"seller id fro sheet  {sellerId}")
    logger.debug(f"no of months {str(noOfMonths)}")
    if sellerId is not None and len(sellerId) > 0:

        inputObj["itemFilter"]["value"] =sellerId


        # queryRepeats = int(noOfMonths / 3)
        # if (noOfMonths == 1):  # one month only
        #     queryRepeats = queryRepeats + 1
        #     startDateFrom = startDateTo - datetime.timedelta(30)
        # elif (queryRepeats == 4):  # need to include (4*90) obvious and 6 days for a year
        #     queryRepeats = 5
        tic=time.perf_counter()
        for i in range(int(noOfMonths*2)):
            inputObj["StartTimeTo"] = startDateTo
            inputObj["StartTimeFrom"] = startDateFrom
            inputObj["paginationInput"]["pageNumber"] = 1
            logger.debug(f"iteration number {i}")
            logger.debug(f"sad{inputObj['StartTimeTo']} and {inputObj['StartTimeFrom']}")
            response = api.execute('findItemsAdvanced', inputObj)
            #print(response)
            response=response.dict()
            #print(inputObj)

            if response.get("searchResult") is None:
                logger.debug(f"no result at i {i}")
                break
            elif response.get("searchResult").get("item") is None:
                logger.debug(f"no result:at {i}")
                break
            #print(response["searchResult"])
            currentItems = response["searchResult"]["item"]
            items.extend(currentItems)
                # print("lenght of items , ", len(items))
                # print("page number is ", response["PageNumber"])
                # print("remaining pages", response["PaginationResult"])
                # print("has more number ", response["HasMoreItems"])
            remainingPages = int(response["paginationOutput"]["totalPages"]) - int(
                    response["paginationOutput"]["pageNumber"])

            if remainingPages == 0:
                break
            logger.debug(f"remaining pages: {remainingPages}")
            # query allows only upto max 100 pages
            remainingPages=min(99,remainingPages)
            multiThreadInputObjects=[copy.deepcopy(inputObj) for _ in range(remainingPages)]
            for i in range(remainingPages):
                multiThreadInputObjects[i]["paginationInput"]["pageNumber"]=i+2
            #logger.debug(multiThreadInputObjects)
            with concurrent.futures.ThreadPoolExecutor(max_workers=max(5,remainingPages/20)) as executor:
                searchResults=[]
                searchResults=executor.map(retrieveFromSecondPage,multiThreadInputObjects)
                logger.debug("underr multithread")
                for searchResult in searchResults:

                    items.extend(searchResult["searchResult"]["item"])
                executor.shutdown()

            # if i == 3:
            #     startDateFrom = startDateFrom - datetime.timedelta(6)  # just for last 6 days in 365/366  days
            # else:
            startDateFrom = startDateFrom - datetime.timedelta(15)
            startDateTo = startDateTo - datetime.timedelta(15)

        # print(items, file=open("1.txt", "w"))
        # setting duration count
        for item in items:
            # print("start time and ",item['listingInfo']['startTime']," end time; ", item['listingInfo']['endTime'])
            startTime = datetime.datetime.strptime(item['listingInfo']['startTime'], "%Y-%m-%dT%H:%M:%S.%fZ")
            endTime = datetime.datetime.strptime(item['listingInfo']['endTime'], "%Y-%m-%dT%H:%M:%S.%fZ")
            #item['DurationCalc']= (endTime.__sub__(startTime)).days
            item['DurationCalc'] = (endTime.__sub__(startTime)).days
        toc=time.perf_counter()
        logger.debug(f"search took {toc-tic} time with items: {len(items)}")
        logger.debug("now adding details like hit count and quantity sold")
        items=getGood(items)

        updateToGSheet(items, None, sellerId, noOfMonths)
        logger.debug("completed")


def getGood(items):
    logger.debug("shopping")
    itemIdSet = set(map(lambda x: x['itemId'], items))
    noDuplicates = list()
    print("set size is ",len(itemIdSet))
    for x in items:
        if x['itemId'] in itemIdSet:
            itemIdSet.remove(x['itemId'])
            noDuplicates.append(x)

    logger.debug(f"no of duplicates: {len(items)-len(noDuplicates)}")
    items = noDuplicates
    inputObj = {"ItemID": [], "IncludeSelector": "Details"}
    inputObjects = []
    j = 0
    _ = 0
    for item in items:
        # print("start time and ",item['listingInfo']['startTime']," end time; ", item['listingInfo']['endTime'])
        startTime = datetime.datetime.strptime(item['listingInfo']['startTime'], "%Y-%m-%dT%H:%M:%S.%fZ")
        endTime = datetime.datetime.strptime(item['listingInfo']['endTime'], "%Y-%m-%dT%H:%M:%S.%fZ")
        item['DurationCalc'] = (endTime.__sub__(startTime)).days
        item['QuantitySold']=0
        item['HitCount']=0
        logger.debug(item['itemId'])
    tic = time.perf_counter()
    while _ < (len(items)):
        logger.debug(f"{_} out of {len(items)}")
        if _ + 20 > len(items):
            j = len(items)
        else:
            j = _ + 20
        inputObj["ItemID"] = list(map(lambda x: x['itemId'], items[_:j]))

        # print("before adding sold, hitcount ",items[_:j])
        try:
            response = get_session().execute('GetMultipleItems', inputObj).dict()
        # print("response after executing multiple api call: ",response)

        except ConnectionError as err:
            logger.debug("got exception while getmultipleitems",exc_info=True)
            print("exception at connection",err)
            print(err.response().dict())
            break
        except:
            print("exception at connection")
            logger.exception("got exeption not ConnectionError")
            break
        else:
            if type(response.get('Item'))==list:
                for i in range(len(response['Item'])):
                    items[_ + i]['QuantitySold'] = response['Item'][i].get('QuantitySold')
                    items[_ + i]['HitCount'] = response['Item'][i].get('HitCount')
            elif type(response.get('Item')) == dict:
                    print(items[_:j])
                    print(response['Item'])
                    items[_]['QuantitySold'] = response['Item'].get('QuantitySold')
                    items[_]['HitCount'] = response['Item'].get('HitCount')
            else:
                print("Din't get any response due to time out.")
                print(response.get('Errors'))
                break

        _ = j

        # print("remaining items to process ",len(items)-i)
    # correcting duration to start and end dates diff
        # print("duration is , ",item['DurationCalc'])
    toc = time.perf_counter()
    logger.debug(f"stopwatch: {toc-tic}")
    #logger.debug(f"lengthof input {len(inputObjects)}")
    return items


if __name__ == "__main__":
    main()