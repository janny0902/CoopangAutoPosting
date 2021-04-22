import hmac
import hashlib
import os
import time
import requests
import json
import urllib.request
from selenium import webdriver
import secrets
from urllib.parse import urlencode
from PIL import Image
from io import BytesIO

__author__ = "Jaejin Jang<jaejin_me@naver.com>"

class cupangMgr:
	def __init__(self):
		self.DOMAIN = "https://api-gateway.coupang.com"

		if not os.path.isdir('imgs'):
			os.makedirs('imgs')

		self.imgpath = os.getcwd() + r"\imgs"

		self.options = webdriver.ChromeOptions()
		self.options.add_argument('headless')
		self.options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36")
		self.options.add_argument("lang=ko_KR")
		self.webdriverpath = os.getcwd() + r"\chromedriver.exe"

	def generateHmac(self, method, url, secretKey, accessKey):
		path, *query = url.split("?")
		os.environ["TZ"] = "GMT+0"
		datetime = time.strftime('%y%m%d')+'T'+time.strftime('%H%M%S')+'Z'
		message = datetime + method + path + (query[0] if query else "")
		signature = hmac.new(bytes(secretKey, "utf-8"), message.encode("utf-8"), hashlib.sha256).hexdigest()

		return "CEA algorithm=HmacSHA256, access-key={}, signed-date={}, signature={}".format(accessKey, datetime, signature)

	def get_productsdata(self, request_method, authorization, keyword, limit):
		URL = "/v2/providers/affiliate_open_api/apis/openapi/products/search?keyword=" + urllib.parse.quote(keyword) + "&limit=" + str(limit)
		url = "{}{}".format(self.DOMAIN, URL)

		response = requests.request(method=request_method, url=url, headers={ "Authorization": authorization, "Content-Type": "application/json;charset=UTF-8" })
		retdata = json.dumps(response.json(), indent=4).encode('utf-8')
		jsondata = json.loads(retdata)
		data = jsondata['data']
		productdata = data['productData']

		return productdata

	def make_productcontent(self, each_product):
		driver = webdriver.Chrome(self.webdriverpath, options=self.options)
		time.sleep(5)

		producturl = each_product['productUrl'] 
		driver.get(producturl)
		driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5]}})")
		driver.execute_script("Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}})")
		driver.execute_script("const getParameter = WebGLRenderingContext.getParameter;WebGLRenderingContext.prototype.getParameter = function(parameter) {if (parameter === 37445) {return 'NVIDIA Corporation'} if (parameter === 37446) {return 'NVIDIA GeForce GTX 980 Ti OpenGL Engine';}return getParameter(parameter);};")
		time.sleep(5)

		title = driver.find_element_by_class_name("prod-buy-header__title").text
		img = driver.find_elements_by_xpath("//*[@class='detail-item']//img")

		images = []

		for each_img in img:
			src = each_img.get_attribute('src')
			if 'vendor_inventory' not in src and ('thumbnail' not in src or 'remote' not in src):
				continue
			fname = secrets.token_hex(16)[0:10] + ".png" 
			fnamefull = self.imgpath + "\\" + fname
			urllib.request.urlretrieve(src, fnamefull)
			images.append(('image', (fname, open(fnamefull, 'rb'), 'image/png')))
		driver.close()

		return title, producturl, images

	
if __name__ == '__main__':
	method = 'GET'				 #정보를 얻는것이기 때문에 GET
	keyword = '노트북' #검색할 키워드, 쿠팡에서 검색하는거랑 결과가 동일합니다.
	limit = 1					 #몇개의 정보를 가져올지 설정. 상위부터 가져옵니다.
	access_key = '0e3a5476-d2d7-452b-8c34-09ed35687cc4'			#API access key
	secret_key = '6e872465260407a2c910010a690de8fe9f0dd948'		#API secret key
	URL = "/v2/providers/affiliate_open_api/apis/openapi/products/search?keyword=" + urllib.parse.quote(keyword) + "&limit=" + str(limit)

	test = cupangMgr()
	authorization = test.generateHmac(method, URL, secret_key, access_key)		# HMAC 생성
	productdata = test.get_productsdata(method, authorization, keyword, limit)	# API 호출

	for each_product in productdata:
		title, producturl, images = test.make_productcontent(each_product)
		print('타이틀 : ', title)
		print('URL : ', producturl)
		print('이미지파일 : ', images)

print('program end')