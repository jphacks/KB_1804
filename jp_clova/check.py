# requestsモジュールの読み込み
import requests

r = requests.get("https://cce58712.ngrok.io/rpi")

print(r.text)
