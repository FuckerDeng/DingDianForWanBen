import scrapy

class DingDianSpider(scrapy.Spider):
	name = "DD"
	#allowed_domains = ["dmoz.org"]
	#start_urls = ["https://www.23us.so/modules/article/articlelist.php?fullflag=1&page=1"]

	def start_requests(self):
		jiraUrl = "http://192.168.2.32:8080/login.jsp"
		jiraHeader = {
			"Host":" 192.168.2.32:8080",
			"User-Agent":" Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
		}
		formData = {
			"os_username":"fan.deng",
			"os_password":"fd123456",
			"os_destination":"",
			"user_role":"",
			"atl_token":"",
			"login":"登录"
		}
		yield [scrapy.FormRequest(url = jiraUrl,headers = jiraHeader,method = "POST",formdata = formData,callback = self.jiraPaser)]
		
	def jiraPaser(self,response):
		with open("result.txt","w") as f:
			f.write(response.text)
		print("写入完成！")