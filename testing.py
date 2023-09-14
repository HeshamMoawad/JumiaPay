# #!/usr/bin/python

# from PyQt5 import QtNetwork 
# from PyQt5.QtCore import QByteArray ,QJsonDocument 
# from PySide2.QtWebEngineCore import QWebEngineHttpRequest
# from PyQt5.QtCore import QCoreApplication, QUrl
# from PyQt5.QtNetwork import QHttpMultiPart , QHttpPart 
# import sys , json

# requestargs = QtNetwork.QNetworkRequest.KnownHeaders

# class Example:

#     def __init__(self):

#         self.doRequest()
    

#     def postRequest(self):
#         self.url = QUrl()
#         self.req = QWebEngineHttpRequest()

#         self.url.setScheme("http")
#         self.url.setHost("stackoverflow")
#         # self.url.setPath("/something/somethingelse")

#         self.req.setUrl(self.url)
#         self.req.setMethod(QWebEngineHttpRequest.Post)
#         self.req.setHeader(QByteArray(b'Content-Type'),QByteArray(b'application/json'))

#         params = json.loads('json\payloads.json')['WE']

#         self.req.setPostData(bytes(json.dumps(params), 'utf-8')) 
        
#         return self.req



#     def setheaders(self): 
#         raw = """{"service_key":"internet.postpaid.wehome@aman","payload":{"phone_number":"EG_+2035242441"},"form_segments":[{"service_key":"internet.postpaid.etisalat@aman","elements":[{"key":"phone_number","label":"Phone Number","options":[{"form_elements":[],"icon":"","label":"Egypt","message":"","option_value":"EG_+20","preselected":false}],"template":"phone_with_country","title":"What is your phone number?","validators":[{"message":"Phone Number is required","options":[],"type":"required"},{"message":"Invalid phone number","options":[],"type":"phoneNumber"}]}],"step":1,"step_count":2,"payload":[],"integrity_key":"1d1ae883953a3d6d3dca01523dfa4599b14f29ee"}]}"""       
#         js = QJsonDocument(raw)
#         print(js.toJson())
#         header = {
#             'accept': 'application/json, text/plain, */*' ,
#             'accept-encoding': 'gzip, deflate, br' ,
#             'accept-language': 'en' ,
#             'content-length': '890' ,
#             'content-type': 'application/json;charset=UTF-8' ,
#             'origin': 'https://pay.jumia.com.eg' ,
#             'referer': 'https://pay.jumia.com.eg/services/internet-bills' ,
#             'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36' ,
#             }

#         datapart = QHttpPart()
#         datapart.setHeader(requestargs.ContentLengthHeader,'890')
#         datapart.setHeader(requestargs.ContentTypeHeader,'application/json;charset=UTF-8')
#         datapart.setHeader(requestargs.UserAgentHeader,'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36')
#         # arr = QByteArray()
#         datapart.setBody(raw)
        
#         return datapart


#     def doRequest(self):

#         url = "https://pay.jumia.com.eg/api/v3/utilities/service-form-type/internet.postpaid.wehome@aman"

#         # url = 'https://billing.te.eg/ar-EG'
#         req = QtNetwork.QNetworkRequest(QUrl(url))

#         self.nam = QtNetwork.QNetworkAccessManager()
#         self.nam.finished.connect(self.handleResponse)
#         self.setheaders()
#         self.nam.post(req)

#     def handleResponse(self, reply:QtNetwork.QNetworkReply):
#         print("-"*30)
#         er = reply.error()
#         print(type(reply))

#         if er == QtNetwork.QNetworkReply.NetworkError.NoError:

#             bytes_string = reply.readAll()
#             print(str(bytes_string, 'utf-8'))

#         else:
#             print("Error occured: ", er)
#             print(reply.errorString())

#         QCoreApplication.quit()


# def main():

#     app = QCoreApplication([])
#     ex = Example()
#     sys.exit(app.exec())


# if __name__ == '__main__':
#     main()

import sys

from PyQt5.QtCore import QByteArray, QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineCore import QWebEngineHttpRequest
from PyQt5.QtWebEngineWidgets import QWebEnginePage


class Render(QWebEnginePage):
    def __init__(self, url):
        app = QApplication(sys.argv)
        QWebEnginePage.__init__(self)
        self.loadFinished.connect(self._loadFinished)

        self._html = ""
        header = {
            'accept': 'application/json, text/plain, */*' ,
            'accept-encoding': 'gzip, deflate, br' ,
            'accept-language': 'en' ,
            'content-length': '890' ,
            'content-type': 'application/json;charset=UTF-8' ,
            'origin': 'https://pay.jumia.com.eg' ,
            'referer': 'https://pay.jumia.com.eg/services/internet-bills' ,
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36' ,
            }


        # username = "username"
        # password = "password"
        # base64string = QByteArray(("%s:%s" % (username, password)).encode()).toBase64()
        request = QWebEngineHttpRequest(QUrl.fromUserInput(url))
        # request.setHeader()
        self.makeheader(request,header)
        request.setMethod(request.Method.Post)
        request.setPostData(b"""{"service_key":"internet.postpaid.wehome@aman","payload":{"phone_number":"EG_+2035242441"},"form_segments":[{"service_key":"internet.postpaid.etisalat@aman","elements":[{"key":"phone_number","label":"Phone Number","options":[{"form_elements":[],"icon":"","label":"Egypt","message":"","option_value":"EG_+20","preselected":false}],"template":"phone_with_country","title":"What is your phone number?","validators":[{"message":"Phone Number is required","options":[],"type":"required"},{"message":"Invalid phone number","options":[],"type":"phoneNumber"}]}],"step":1,"step_count":2,"payload":[],"integrity_key":"1d1ae883953a3d6d3dca01523dfa4599b14f29ee"}]}""")
        self.load(request)
        app.exec_()

    def makeheader(self,req:QWebEngineHttpRequest,header:dict):
        for key , value in header.items():
            req.setHeader(bytes(str(key).encode()),bytes(str(value).encode()))
        

    @property
    def html(self):
        return self._html

    def _loadFinished(self):
        self.toHtml(self.handle_to_html)

    def handle_to_html(self, html):
        self._html = html
        QApplication.quit()


def main():
    url = "https://pay.jumia.com.eg/api/v3/utilities/service-form-type/internet.postpaid.wehome@aman"
    r = Render(url)
    print(r.html)


if __name__ == "__main__":
    main()
