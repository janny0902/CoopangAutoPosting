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
import Sqlite3Conn

from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods import posts
from wordpress_xmlrpc.methods import media
from wordpress_xmlrpc import WordPressPost


class cupangMgr:
	def __init__(self):

		self.DOMAIN = "https://api-gateway.coupang.com"


		#if not os.path.isdir('imgs'):
		#	os.makedirs('imgs')

		#self.imgpath = os.getcwd() + r"\imgs"

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
		#URL = "/v2/providers/affiliate_open_api/apis/openapi/products/search?keyword=" + urllib.parse.quote(keyword) + "&limit=" + str(limit)
		URL = "/v2/providers/affiliate_open_api/apis/openapi/products/bestcategories/1001?limit=" + str(limit)
		url = "{}{}".format(self.DOMAIN, URL)

		response = requests.request(method=request_method, url=url, headers={ "Authorization": authorization, "Content-Type": "application/json;charset=UTF-8" })
		retdata = json.dumps(response.json(), indent=4).encode('utf-8')
		jsondata = json.loads(retdata)
		data = jsondata['data']
		print(data)
		#productdata = data['productData']

		#return productdata
		return data

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
		content = ''


		for each_img in img:
			src = each_img.get_attribute('src')
			print(src)  ##상품 이미지 url.
			print("------")
			content += '<img src = '+src+'>'
		driver.close()

		return title, producturl, content

	def CreatePost(self,title, content, id , password, category):
		my_blog = Client('http://janny.pe.kr/xmlrpc.php', id, password)
		myposts=my_blog.call(posts.GetPosts())

		post = WordPressPost()
		post.title = title ## 글 제목.
		post.slug='StockTrade'
		post.content = content ## 글 내용.


        # read the binary file and let the XMLRPC library encode it into base64


		post.thumbnail = 531  #어드민 페이지 > 미디어 > 이미지에 마우스 올리면 > 왼쪽밑에 url 에 코드 적혀있음   post = ???? << 이게 아이디
		post.terms_names = {
                            'post_tag' :[category],
                            'category': ["쿠팡 제품 소개"] ## 글을 포함시키고 싶은 카테고리를 넣으면된다.
        }
		post.id = my_blog.call(posts.NewPost(post))
		post.post_status = 'publish'
		my_blog.call(posts.EditPost(post.id, post))

if __name__ == '__main__':

	method = 'GET'				 #정보를 얻는것이기 때문에 GET
	keyword = '노트북' #검색할 키워드, 쿠팡에서 검색하는거랑 결과가 동일합니다.
	limit = 1					 #몇개의 정보를 가져올지 설정. 상위부터 가져옵니다.
	access_key = '#'			#API access key
	secret_key = '#'		#API secret key
	#URL = "/v2/providers/affiliate_open_api/apis/openapi/products/search?keyword=" + urllib.parse.quote(keyword) + "&limit=" + str(limit)
	URL = "/v2/providers/affiliate_open_api/apis/openapi/products/bestcategories/1001?limit=" + str(limit)
	print(URL)
#	https://api-gateway.coupang.com/v2/providers/affiliate_open_api/apis/openapi/products/search?keyword=food&limit=50
#	https://api-gateway.coupang.com/v2/providers/affiliate_open_api/apis/openapi/products/bestcategories/1001?limit=50


	test = cupangMgr()
	authorization = test.generateHmac(method, URL, secret_key, access_key)		# HMAC 생성
	productdata = test.get_productsdata(method, authorization, keyword, limit)	# API 호출

	for each_product in productdata:
		title, producturl,content = test.make_productcontent(each_product)
		print('타이틀 : ', title)
		print('URL : ', producturl)


	title = title + ' 제품 소개'
	category_text = '테스트'
	test.CreatePost(title, content, 'id#' , 'pass#', category_text)

print('program end')