# Noel Caceres
# Quote class
# uses Oanda API v20
# to create a price quote instance

import oandapyV20
from oandapyV20 import API
import oandapyV20.endpoints.pricing as pricing
import simplejson as json


# Price Quote
class Quote:
    # to construct, uses acount ID, instrument symbol, and api token
    def __init__(self, accountID, symbol, token):
        self.__accountID = accountID
        self.__symbol = symbol
        self.__token = token
        self.__ask = float(0)
        self.__bid = float(0)
        self.__timeStamp = ""

        api = API(access_token= self.__token)
        params = { "instruments": self.__symbol }

        r = pricing.PricingInfo(accountID= self.__accountID, params= params)
        rv = api.request(r)

        # to convert time zone hour from utc which is 6 hours difference of my time
        utc = ('00','01','02','03','04','05','06','07','08','09','10','11', \
               '12','13','14','15','16','17','18','19','20','21','22','23')
        cst = ('18','19','20','21','22','23','00','01','02','03','04','05', \
               '06','07','08','09','10','11','12','13','14','15','16','17')
        
        self.__status = rv["prices"][0]["status"]
        tmpDate = rv["prices"][0]["time"]
        
        self.__timeStamp = tmpDate[5:7] + '/' +tmpDate[8:10] + '/' + tmpDate[0:4] + " " \
                        + cst[int(tmpDate[11:13])]+ tmpDate[13:19] 
        self.__ask = (rv["prices"][0]["asks"][0]['price'])
        self.__bid = (rv["prices"][0]["bids"][0]['price'])

    def getStatus(self):
        return self.__status
    def getTimeStamp(self):
        return self.__timeStamp
    def getAsk(self):
        return self.__ask
    def getBid(self):
        return self.__bid
        
                                        
        
