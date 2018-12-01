import scrapy
from selenium import webdriver
import time


class DingDianSpider(scrapy.Spider):
    name = "BaShi"
    nowCookie = {}
    # allowed_domains = ["dmoz.org"]
    start_urls = ["http://www.apkbus.com/","http://www.apkbus.com/plugin.php?id=k_misign:sign"]

    def start_requests(self):
        header = {
            "Host": "www.apkbus.com",
            "User-Agent": " Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        }
        self.getCookie(self.start_urls[0])
        with open("cookie.txt") as f:
            newCookies = f.readlines()
            newCookie = eval(newCookies[5])
            print(newCookie)

        return [scrapy.Request(self.start_urls[1],headers=header,cookies=newCookie)]

    def getCookie(self,url):
        self.logger.info("尝试登陆获得最新Cookie！")
        path = r"D:\ruanjian\chromedriver\chromedriver.exe"
        driver = webdriver.Chrome(executable_path=path)
        driver.get(url)
        time.sleep(3)
        driver.find_element_by_xpath("//*[@id='nv_forum']/div[3]/div/div[5]/a[1]").click()
        time.sleep(1.5)

        driver.switch_to.alert
        user = driver.find_element_by_xpath("//td[@id = 'fwin_content_login']/div/div[@class = 'co_r']/div[2]/form/div/input[@name = 'username']")
        user.clear()
        user.send_keys("844537819@qq.com")
        self.logger.info("输入账号！")
        pwd = driver.find_element_by_xpath("//td[@id = 'fwin_content_login']/div/div[@class = 'co_r']/div[2]/form/div/input[@name = 'password']")
        pwd.clear()
        pwd.send_keys("dfheyix1992")

        self.logger.info("输入密码！")
        pwd = driver.find_element_by_xpath("//td[@id = 'fwin_content_login']/div/div[@class = 'co_r']/div[2]/form/div/button[@name = 'loginsubmit']")
        pwd.click()
        self.logger.info("点击登陆！")
        time.sleep(3)

        bashiCookie = driver.get_cookies()
        with open("cookie.txt","w") as f:
            for c in bashiCookie:
                f.write(str(c)+"\n")
        driver.close()
        return bashiCookie[0]

    def parse(self, response):
        count = response.xpath("//div[@class = 'weather_p']/div/text()").extract()[0]
        print(count)


