import requests as rq
import json


resp=rq.get("http://209.182.239.212:1069/api/hs-codes/d13b89eca2a89a5b22ee")
hstable={}

if resp.status_code==200:
    hsresp=json.loads(resp.text)
    for i in hsresp['HSCodes']:
        hstable[i['FullDescription']]=[i['HSCode'],i['TaxRate']]
