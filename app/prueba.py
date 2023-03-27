import requests

url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=turix&inputtype=textquery&locationbias=circle%3A2000%19.4323763%2C-99.1948132&fields=place_id&key=AIzaSyBcDJUy0pFP_bRlNgfW9f49q6hr1G56rfQ"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)