import pandas
import ast
import getmac
import typing 
from datetime import datetime
######################


class Myhash ():
    ENCRYPTDICT = {'Key': {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'a', 11: 'b', 12: 'c', 13: 'd', 14: 'e', 15: 'f', 16: 'g', 17: 'h', 18: 'i', 19: 'j', 20: 'k', 21: 'l', 22: 'm', 23: 'n', 24: 'o', 25: 'p', 26: 'q', 27: 'r', 28: 's', 29: 't', 30: 'u', 31: 'v', 32: 'w', 33: 'x', 34: 'y', 35: 'z', 36: 'A', 37: 'B', 38: 'C', 39: 'D', 40: 'E', 41: 'F', 42: 'G', 43: 'H', 44: 'I', 45: 'J', 46: 'K', 47: 'L', 48: 'M', 49: 'N', 50: 'O', 51: 'P', 52: 'Q', 53: 'R', 54: 'S', 55: 'T', 56: 'U',57: 'V', 58: 'W', 59: 'X', 60: 'Y', 61: 'Z', 62: '!', 63: '$', 64: '%', 65: '&', 66: '*', 67: '+', 68: '-', 69: '/', 70: ':', 71: ';', 72: '<', 73: '=', 74: '>', 75: '?', 76: '@', 77: '[', 78: ']', 79: '^', 80: '_', 81: '`', 82: '{', 83: '|', 84: '}', 85:'~', 86: "'", 87: '"', 88: ' ', 89: ',',90:'\n'},
                  'value': {0: 'Rq?', 1: 'rK4', 2: '?NJ', 3: 'iN}', 4: ':}C', 5: '7a1', 6: '`k<', 7: '5GG', 8: 'tB[', 9: '*+=', 10: 'V0l', 11: 'cTj', 12: 'h;D', 13: '_rU', 14: 'S}`', 15: 'y{t', 16: 'j3{', 17: 'go*', 18: 'l$I', 19: 'o&7', 20: 'z*v', 21: 'D&r', 22: 'K:3', 23: '2]M', 24: 'Mav', 25: '^^p', 26: 'QYO', 27: 'U~{', 28: 'V}M', 29: '-^{', 30: '*P&', 31: 'Adu', 32: 'cZa', 33: '<Hj', 34:'e%g', 35: 'q|^', 36: 'o[Z', 37: 'MfK', 38: '/`C', 39: '6]K', 40: 'Ja1', 41: '[Hv', 42: 'bjk', 43: 'LE`', 44: 'FPl', 45: 'SOQ',46: 'H=_', 47: '/7w', 48: 'Sl!', 49: '?ub', 50: 'tQ:', 51: '5~M', 52: '[pe', 53: 'hNM', 54: 'Rvg', 55: '75g', 56: 'w1/', 57: 'qD5', 58: 'HGW', 59: 'yut', 60: '3~`', 61: 'Emi', 62: '_QH', 63: 'ZJ[', 64: 'OlN', 65: 'J]x', 66: 'b%6', 67: 'nvb', 68: 'B`w', 69: '4d:', 70: '-T>', 71: 'a~G', 72: 'tBp', 73: 'x_E', 74: '0oB', 75: '<Kd', 76: 'rMj', 77: ';dt', 78: 'T=!', 79: '}Z?', 80: 'xD0', 81: 'L@+', 82: 'JFO', 83: 'ZLl', 84: 'n[=', 85: 'eR&', 86: 'nji', 87: 'bhu', 88: '][p', 89: 'tsb',90:'nq9'}}
    def __init__(self):
        self.username = ""
        self.dataframe = pandas.DataFrame().from_dict(data=self.ENCRYPTDICT)

    def encoder(self, text: str):
        """
        No # in text
        """
        values = []
        for i in text:
            index = self.dataframe[self.dataframe["Key"] == i].index
            value = self.dataframe["value"].iloc[index].values[0]
            values.append(value)
        return "".join(values)

    def decoder(self, text: str):
        keys = []
        try:
            for i in range(0, len(text), 3):
                index = self.dataframe[self.dataframe["value"]== text[i:i+3]].index
                value = self.dataframe["Key"].iloc[index].values[0]
                keys.append(value)
        except Exception as e:
            print(f"Can't decode ---{e}---")
        result = "".join(keys)
        return result

    def enlayers(self, text: str, num_of_layers: int) -> str :
        for i in range(num_of_layers):
            text = self.encoder(text)
        return text

    def delayers(self, text: str, num_of_layers: int) -> str :
        for i in range(num_of_layers):
            text = self.decoder(text)
        return text

    def delayersIntoRequest(self, text: str, num_of_layers: int):
        return ast.literal_eval( self.delayers(text, num_of_layers))

    def Timeing(self,current:datetime , resDate:dict):
        return True if current.year <= int(resDate['year']) and current.month <= int(resDate['month']) and current.day <= int(resDate['day']) else False

    def checkMAC(self,MAC:str):
        return True if MAC == self.getCurrentMAC() else False
        
    def  getCurrentMAC(self)-> str:
        return getmac.get_mac_address()      


    @typing.overload
    def checkValidation(self, txtfilepath:str , layers:int )->bool:
        ...
    @typing.overload
    def checkValidation(self,data:str)->bool:
        ...
    @typing.overload
    def checkValidation(self,data:dict)->bool:
        ...

    def checkValidation(self,layers:int,txtfilepath:str = None , data = None ):
        current = datetime.now()
        
        if txtfilepath != None :
            with open(txtfilepath,"r") as file :
                code = file.readline()
                file.close()
                response = self.delayersIntoRequest(
                    text = code ,
                    num_of_layers = layers ,
                )
                self.username = response['username']
                if self.username == "K7Hesham": # Admin
                    return True
                else:
                    return True if self.Timeing(current,response['to']) and self.checkMAC(response['mac']) else False
        elif data != None :
            if data is str :
                response = self.delayersIntoRequest(
                    text = data , 
                    num_of_layers = layers , 
                )
                self.username = response['username']
                if self.username == "K7Hesham":
                    return True
                else:
                    return self.Timeing(current,response['to'])
            elif data is dict:
                if response['username'] == "K7Hesham":
                    return True
                else:
                    return True if self.Timeing(current,data['to']) and self.checkMAC(data['mac']) else False   
        else:
            return False

    def getUserName(self):
        return self.username
