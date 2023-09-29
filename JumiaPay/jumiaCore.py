import typing 

import re
# as per recommendation from @freylis, compile once only # '<.*?>'
CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});') 

def removeHTML(text):
  return re.sub(CLEANR, '', text)



class LeadObjectFirst(object):
    def __init__(self,Response:dict) -> None:
        self.Response = Response
        self.goNext = True
        self.statusOfResponse = Response["code"]  # "SUCCESS"
        try:
            self.Price = Response["response"]["elements"][0]["label"].split("EGP")[0].split(" ")[-2]
        except Exception as e :
            try:
                self.Price = Response["response"]["elements"][0]["label"]
                print(f"error in and fixed  {e} with response {self.Price}")
            except Exception as e :
                print(f"error in {e} with response {self.Response}")
                self.Price = "can't get Price"
        self.ServerMsg = Response["response"]["elements"][0]["label"]
        self.AreaCode = Response['AreaCode']
        self.PhoneNumber = Response['PhoneNumber']
        self.HasUnpaidInvoices = 'يوجد فاتورة' 
        self.TimeScraping = str(round(Response['TimeScraping'],ndigits =2)) # Response['TimeScraping'] 
        

    def __str__(self) -> str:
        return str(self.dictOfObject)
        
    @property
    def dictOfObject(self)->dict:
        return self.__dict__

############################################

class LeadObjectSec(object):
    def __init__(self,Response:dict) -> None:
        self.Response = Response
        self.goNext = True
        self.statusOfResponse = Response["code"]  # "SUCCESS"
        self.Price = str(Response["response"]['payment_details'][0]['raw_value'])
        self.ServerMsg = 'Redirect Page' #Response["response"]["elements"][0]["label"]
        self.AreaCode = Response['AreaCode']
        self.PhoneNumber = Response['PhoneNumber']
        self.HasUnpaidInvoices = 'يوجد فاتورة' 
        self.TimeScraping = str(round(Response['TimeScraping'],ndigits =2)) # Response['TimeScraping'] 

    def __str__(self) -> str:
        return str(self.dictOfObject)
        
    @property
    def dictOfObject(self)->dict:
        return self.__dict__

############################################

class LeadObjectNoClient(object):
    def __init__(self,Response:dict) -> None:
        self.Response = Response
        self.goNext = True
        self.statusOfResponse = Response["code"]  # "INVALID_FIELDS"
        self.Price = str(None)
        self.ServerMsg = Response['response'] #Response["response"]["elements"][0]["label"]
        self.AreaCode = Response['AreaCode']
        self.PhoneNumber = Response['PhoneNumber']
        self.HasUnpaidInvoices = 'لايوجد'
        self.TimeScraping = str(round(Response['TimeScraping'],ndigits =2)) # Response['TimeScraping'] 

    def __str__(self) -> str:
        return str(self.dictOfObject)
        
    @property
    def dictOfObject(self)->dict:
        return self.__dict__

############################################

class LeadObjectUndefined(object):
    def __init__(self,Response:dict) -> None:
        self.Response = Response
        self.goNext = True
        self.statusOfResponse = f'Undefined-{Response}'  # "INVALID_FIELDS"
        self.Price = str(None)
        self.ServerMsg = Response["response"] if 'response' in Response.keys() else "Undefined Message"   #Response["response"]["elements"][0]["label"]
        self.AreaCode = Response['AreaCode']
        self.PhoneNumber = Response['PhoneNumber']
        self.HasUnpaidInvoices = "Undefined"
        self.TimeScraping = str(round(Response['TimeScraping'],ndigits =2)) # Response['TimeScraping'] 

    def __str__(self) -> str:
        return str(self.dictOfObject)
        
    @property
    def dictOfObject(self)->dict:
        return self.__dict__

###############################################################



                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
#     print("SECOUND")
# else :
#     print("Not Found Instance")

# l = "B48FA4B0712495394276362E62465E6220230422312040A914D4C153C2E02965E1B8A6C667E42E"
# print(len(l))

# gen = Generator()


# print(gen.genText(78).upper())