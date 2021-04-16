import hmac
import hashlib
import binascii
import os
import time
import requests
import json


REQUEST_METHOD = "POST"
DOMAIN = "https://api-gateway.coupang.com"
URL = "/v2/providers/affiliate_open_api/apis/openapi/v1/deeplink"

# Replace with your own ACCESS_KEY and SECRET_KEY
ACCESS_KEY = "0e3a5476-d2d7-452b-8c34-09ed35687cc4"
SECRET_KEY = "6e872465260407a2c910010a690de8fe9f0dd948"

REQUEST = { "coupangUrls": [
    "https://www.coupang.com/np/search?component=&q=good&channel=user", 
    "https://www.coupang.com/np/coupangglobal"
]}


def generateHmac(method, url, secretKey, accessKey):
    path, *query = url.split("?")
    os.environ["TZ"] = "GMT+0"
    datetime = time.strftime('%y%m%d')+'T'+time.strftime('%H%M%S')+'Z'
    message = datetime + method + path + (query[0] if query else "")

    signature = hmac.new(bytes(secretKey, "utf-8"),
                         message.encode("utf-8"),
                         hashlib.sha256).hexdigest()

    return "CEA algorithm=HmacSHA256, access-key={}, signed-date={}, signature={}".format(accessKey, datetime, signature)


authorization = generateHmac(REQUEST_METHOD, URL, SECRET_KEY, ACCESS_KEY)
url = "{}{}".format(DOMAIN, URL)
resposne = requests.request(method=REQUEST_METHOD, url=url,
                            headers={
                                "Authorization": authorization,
                                "Content-Type": "application/json"
                            },
                            data=json.dumps(REQUEST)
                            )

print(resposne.json())