import requests

r = requests.get("https://api.coinlore.net/api/ticker/?id=90")
print(r.json()[0]["price_usd"])