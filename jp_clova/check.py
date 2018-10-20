# requestsモジュールの読み込み
import requests
import time
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
    url = "https://4b9a3cba.ngrok.io/rpi" + str(num)
    time.sleep(5)
