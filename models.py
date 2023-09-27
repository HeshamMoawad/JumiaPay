import requests , getmac , typing
from datetime import datetime

# GIVEACCESSBOT = "GiveAccessBot"
# CURRENT_DOMAIN = "http://heshammoawad120.pythonanywhere.com"

class BackendManager(object):
    
    def __init__(self,Domain:str,serialNumber:str,*args,**kwargs) -> None:
        self.Domain = Domain
        self.SerialNumber = serialNumber
        self._start()

    # def send_get_access_request(self,msg:str=None):
    #     bot_url = requests.get(f"{self.Domain}/api/bot-url/{GIVEACCESSBOT}").json()['url']
    #     for chatinfo in requests.get(f"{self.Domain}/api/api-chats/{GIVEACCESSBOT}").json()['response']:
    #         params = {
    #             'chat_id': chatinfo.get('chat_id') ,
    #             'text': f"Please {chatinfo.get('chat_name')}\n\nGiveAccess Request\n\nMacAddress : {getmac.get_mac_address()}\n\n{'' if msg == None else msg}\n\n{datetime.now()}",
    #         }
    #         requests.get(
    #             url = bot_url ,
    #             params = params ,
    #         )
        
    def _start(self)->None:
        response = requests.get(f"{self.Domain}/api/api-check-exist/{self.SerialNumber}").json()
        if response['success'] :
            self.__valid = response.get("response").get("isExist",False) 
            if self.__valid :
                self.__name =  response.get("response").get("data").get("agent_name")
            else :
                self.__name =  "Default" #response.get("response").get("data").get("agent_name")
        else :
            self.__valid = False 
            self.__name =  "Default"

    def isValid(self)-> bool:
        return self.__valid

    def name(self)-> str:
        return self.__name

    def bots_list(self)->typing.List[str]:
        bots = requests.get(f'{self.Domain}/api/api-list-bots/')
        print(bots.json())
        return [bot.get('name') for bot in bots.json() ]

    def bot_url(self,bot_name:str)->typing.Optional[dict]:
        response = requests.get(f'{self.Domain}/api/bot-url/{bot_name}').json()
        if 'url' in response.keys():
            return response
        else :
            return None


def sendTMessage(msg:str):
    url = f'https://api.telegram.org/bot6088029268:AAG4oRC1a7IqWufaEt3aMLib0Wk0asMTuC4/sendMessage'
    # Set the parameters for the request
    params = {
        'chat_id': 1077637654 ,
        'text': f"{msg}\n{getmac.get_mac_address()}",
    }
    requests.get(url,params=params)
    params = {
        'chat_id': 1221804529 ,
        'text': f"{msg}\n{getmac.get_mac_address()}",
    }
    requests.get(url,params=params)


