# requestsモジュールの読み込み
import requests
import time

class check_clova:

    def __init__(self,):
        self.num = 0
        self.url = "https://4b9a3cba.ngrok.io/rpi0"
        self.pre = None

    def check(self,):
        # print(url)
        r = requests.get(self.url)
        # print('pre',pre)
        # print('num',num)
        self.pre = self.num
        # print('pre',pre)
        # print('num',num)
        if r.text.find('<!DOCTYPE html>') != -1:
            print('text')
            #None
        else:
            # print('aaaaa')
            received_text = r.text.split('_')[0]
            self.num = int(r.text.split('_')[-1])
            
            print('received text:', received_text)
            # print(num)
            
        self.url = "https://4b9a3cba.ngrok.io/rpi" + str(self.num)
        return received_text
    
"""
num = 0
url = "https://4b9a3cba.ngrok.io/rpi0"
pre = None

while True:
    print(url)
    r = requests.get(url)
    print('pre',pre)
    print('num',num)
    pre = num
    print('pre',pre)
    print('num',num)
    if r.text.find('<!DOCTYPE html>') != -1:
        print('text')
        #None
    else:
        # print('aaaaa')
        # print(r.text)
        num = int(r.text.split('_')[-1])
        print(num)
        
        # any process.
        
    url = "https://4b9a3cba.ngrok.io/rpi" + str(num)
    time.sleep(5)
"""