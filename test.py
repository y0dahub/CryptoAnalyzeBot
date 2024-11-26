import requests

a = requests.get("https://2ip.io", proxies={"http": "127.0.0.1:2080"})
print(a.text)