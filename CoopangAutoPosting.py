import hmac
import hashlib
import os
import time
import requests
import json
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
import secrets
from urllib.parse import urlencode
from PIL import Image
from io import BytesIO
import chatGPT
import Sqlite3Conn
import re



#카테고리 코드

#Id	이름
#1001	여성패션
#1002	남성패션
#1010	뷰티
#1011	출산/유아동
#1012	식품
#1013	주방용품
#1014	생활용품
#1015	홈인테리어
#1016	가전디지털
#1017	스포츠/레저
#1018	자동차용품
#1019	도서/음반/DVD
#1020	완구/취미
#1021	문구/오피스
#1024	헬스/건강식품
#1025	국내여행
#1026	해외여행
#1029	반려동물용품
#1030	유아동패션

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

	def get_productsdata(self, request_method, authorization, keyword, limit, proCode):
		#URL = "/v2/providers/affiliate_open_api/apis/openapi/products/search?keyword=" + urllib.parse.quote(keyword) + "&limit=" + str(limit)
		URL = "/v2/providers/affiliate_open_api/apis/openapi/products/bestcategories/"+proCode+"?limit=" + str(limit)
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

		title = driver.find_element(By.CLASS_NAME,"prod-buy-header__title").text
		img = driver.find_element(By.CLASS_NAME, 'prod-image__detail')
		cost =  driver.find_element(By.CLASS_NAME, 'total-price')
		print(img.get_attribute("outerHTML"))
		#img = driver.find_elements(By.XPATH,"//*[@class='detail-item']//img")

		# title = 'test'
		# img=''
		imgPath = img.get_attribute("outerHTML")
		price = cost.get_attribute("innerHTML").replace(" " , "").replace("\n","").strip('</strong>''<string>')

		# for each_img in img:
		# 	src = each_img.get_attribute('src')
		# 	print(src)  ##상품 이미지 url.
		# 	print("------")
		# 	content += '<img src = '+src+'>'
		driver.close()

		return title, producturl, imgPath, price

	def CreatePost(self,title, content, id , password, category):
		my_blog = Client('#', id, password)
		# myposts=my_blog.call(posts.GetPosts())

		post = WordPressPost()
		post.title = title ## 글 제목.
		post.slug='StockTrade'
		post.content = content ## 글 내용.


        # read the binary file and let the XMLRPC library encode it into base64


		post.thumbnail = 948  #어드민 페이지 > 미디어 > 이미지에 마우스 올리면 > 왼쪽밑에 url 에 코드 적혀있음   post = ???? << 이게 아이디
		post.terms_names = {
                            'post_tag' :[category],
                            'category': ["쿠팡 제품 소개"] ## 글을 포함시키고 싶은 카테고리를 넣으면된다.
        }
		post.id = my_blog.call(posts.NewPost(post))
		post.post_status = 'publish'
		my_blog.call(posts.EditPost(post.id, post))

if __name__ == '__main__':
	proCode = '1015'
	method = 'GET'				 #정보를 얻는것이기 때문에 GET
	keyword = '노트북' #검색할 키워드, 쿠팡에서 검색하는거랑 결과가 동일합니다.
	limit = 1					 #몇개의 정보를 가져올지 설정. 상위부터 가져옵니다.
	access_key = '#'			#API access key
	secret_key = '#'		#API secret key
	blogID = '#'
	blogPW = '#'
	#URL = "/v2/providers/affiliate_open_api/apis/openapi/products/search?keyword=" + urllib.parse.quote(keyword) + "&limit=" + str(limit)
	URL = "/v2/providers/affiliate_open_api/apis/openapi/products/bestcategories/"+proCode+"?limit=" + str(limit)
	print(URL)
#	https://api-gateway.coupang.com/v2/providers/affiliate_open_api/apis/openapi/products/search?keyword=food&limit=50
#	https://api-gateway.coupang.com/v2/providers/affiliate_open_api/apis/openapi/products/bestcategories/1001?limit=50


	test = cupangMgr()
	authorization = test.generateHmac(method, URL, secret_key, access_key)		# HMAC 생성
	productdata = test.get_productsdata(method, authorization, keyword, limit, proCode)	# API 호출

	print(URL)
	for each_product in productdata:
		title, producturl,imgPath,price = test.make_productcontent(each_product)
		print('타이틀 : ', title)
		print('URL : ', producturl)
		print('price : ', price)
		print('content', imgPath)  #chat gpt 연결해서 내용 만들기~
		openAIchat = chatGPT.chatGPTMethod
		ChatGPTan = openAIchat.questionFunction(title+" 제품 "+price+" 광고글 작성해줘")
		print("answn:"+ChatGPTan)
		#ChatGPTan ='안녕하세요! 감사합니다.'
		producturl = "'"+producturl+"'"
	title = title + ' 제품 소개'
	category_text = keyword
	content = "<div>  </div>"
	content +="<h2>"+title+"</h2><div>  </div>"
	content += '<div OnClick="location.href='+producturl+'"><span style="width: 45%;" !important>'+imgPath +'</img></span><span style="width:15%;color: red;font-weight: bold;font-size: 40px;" !important>'+price+'</span></div>'

	res = re.split('[!.]+', ChatGPTan)
	for i in res:

		content += "<div>"+i+".</div><div>  </div>"

	content += '<div OnClick="location.href='+producturl+'">구매하기 링크 !!  ☜☜☜☜☜☜ 클릭</div>'
	#content += "<div>"+ChatGPTan+"</div>"  #content 에 html 테그를 입력하여 틀을 좀 만들어야 함. 너무 허접한 페이지가 생성된. 제목 가격 이미지 내용을 html tag 포함해서 작성하고 공통내용을 하드로 포함하여 조금 꾸밀 필요가 있음.
	test.CreatePost(title, content, blogID , blogPW, category_text)  #실제 게시글 작성됨


print('program end')