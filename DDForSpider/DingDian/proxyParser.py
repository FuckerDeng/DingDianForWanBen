import requests
from lxml import etree
import time
import pymysql
import threading
import logging

class checkProxy:
	isRun = False
	shutDown = False
	baseUrl = "http://dev.kdlapi.com/api/getproxy/?orderid=984363263217618&num=100&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=2&method=2&an_ha=1&sep=1"

	checkHttpsUrl = "https://www.baidu.com/content-search.xml"
	hh = {
		"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36 115Browser/8.6.2"
	}
	#con = pymysql.connect("localhost","root","123456","dengfan",3306)
	#cursor = con.cursor()
	baseIps = []
	ips = []

	lock=threading.Lock()

	def __init__(self):
		logging.getLogger('requests').setLevel(logging.ERROR)

	def remove(self,proxy):
		self.lock.acquire()
		if proxy in self.ips:
			self.ips.remove(proxy)
		self.lock.release()

	def check(self,proxy,full_ip):
		

		try:
			#print("开始检查！")
			re = requests.get(self.checkHttpsUrl,proxies = {proxy.lower():proxy.lower()+"://"+full_ip},headers = self.hh,timeout = (3,7))
			#print(re.text)
			if re.status_code == 200 :
			
				self.lock.acquire()
				self.ips.append([proxy,proxy.lower()+"://"+full_ip])
				#print(len(self.ips))
				self.lock.release()
		except Exception as e:
			#print(full_ip+"\t无效！")	
			#print(e)
			pass

			
	def toDB(self):
		lock.acquire()
		#print(len(ips))
		if len(self.ips)>100:
			for j in ips:
				iipp = j[1]
				ii = iipp.split(":")[0]
				pp = iipp.split(":")[1]
				try:
					cursor.execute("insert into proxies values('%s','%s','%s','%s')"%(j[0],ii,pp,iipp))
					con.commit()
					#print(proxy+":\t"+ii + "\t"+pp+"\t有效且插入数据库成功！")
					print(ii + "\t"+pp+"\t有效且插入数据库成功！")
				except Exception as e:
					#print(proxy+":\t"+ii + "\t"+pp+"\t无效！")
					print(ii + "\t"+pp+"\t插入失败！")
					con.rollback()
			ips = []
		lock.release()

	def getProxy(self):
		try:
			i = 1
			while(checkProxy.shutDown == False)	:
				if len(self.ips) <=20:
					res = requests.get(self.baseUrl,headers = self.hh)
					#print(res.text)
					proxies = res.text.split()

					self.baseIps += proxies
					if len(self.baseIps) >= 100:
						for aaa in self.baseIps:
							t = threading.Thread(target = self.check,args = ("https",aaa))
							t.start()
						time.sleep(3)
						#print("第"+str(i)+"次的可用率为："+ str(len(self.ips)/len(self.baseIps)*100)+"%")
						i +=1
						self.baseIps = []
					
				

				time.sleep(3)
		except Exception as e:
			print(e)
		finally:
			#con.close()
			pass