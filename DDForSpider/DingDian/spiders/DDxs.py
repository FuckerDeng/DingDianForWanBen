import scrapy
from DingDian.items import bookItem,chapterItem
from multiprocessing import Lock

class DingDianSpider(scrapy.Spider):

    name = "DDSpider"
    id = 1
    lock = Lock()
    #allowed_domains = ["dmoz.org"]
    start_urls = ["https://www.23us.so/modules/article/articlelist.php?fullflag=1&page="]


    def start_requests(self):

        urls = []
        reqs = []
        for i in range(1,49):
            urls.append(self.start_urls[0]+str(i))

        for url in urls:
            #reqs.append(scrapy.Request(url))
            yield scrapy.Request(url,self.parse)

        #return reqs
            

    def parse(self,response):
        trs = response.xpath("//table/tr[@bgcolor = '#FFFFFF']")
        
        chapterRqs = []
        for tr in trs:
            tds = tr.xpath("td")
            xsUrl = tds[1].xpath("a/@href").extract()[0]

            xsName = tds[0].xpath("a/text()").extract()[0]
            xsChapterNew = ""
            try:
                xsChapterNew = tds[1].xpath("a/text()").extract()[0].split()[1]
            except:
                xsChapterNew = ""

            xsAutor = tds[2].xpath("text()").extract()[0]
            xsCharNum = int(tds[3].xpath("text()").extract()[0])
            xsUpdate = ""
            try:
                xsUpdate = tds[4].xpath("text()").extract()[0]
            except:
                print("最新章节为空：" + xsName)
            xsStatus = 1
            book = bookItem()
            book["type"] = "bookInfo"
            book["name"] = xsName
            book["chapterNew"] = xsChapterNew
            book["author"] = xsAutor
            book["charNum"] = xsCharNum
            book["updateTime"] = xsUpdate
            book["isEnd"] = xsStatus

            
            self.lock.acquire()
            book["id"] = self.id
            self.id += 1
            self.lock.release()
            yield book
            yield scrapy.Request(xsUrl,callback=self.getChapters,meta = {"id":book["id"]})






    def getChapters(self,response):
        bookName = response.xpath("//div[@class = 'bdsub']/dl/dt/a[3]/text()").extract()[0]

        aList = response.xpath("//table[@id = 'at']/tr/td[@class = 'L']/a")

        chapterNum = 1
        id = response.meta["id"]
        for a in aList:
            name = ""
            try:
                name = a.xpath("text()").extract_first().split()[1]
            except:
                name = a.xpath("text()").extract_first()
            chapterName = "第" + str(chapterNum) + "章 " + name
            chapterNum +=1
            url = a.xpath("@href").extract()[0]
            yield scrapy.Request(url,callback = self.getChaptersInfo,meta = {"id":id,"chapterNum":chapterNum,"chapterName":chapterName})


    def getChaptersInfo(self,response):
        chapterName = response.meta["chapterName"]
        chapterNum = response.meta["chapterNum"]
        id = response.meta["id"]
        content = response.xpath("//dd[@id = 'contents']")[0].xpath("string(.)").extract_first().replace("&nbsp;&nbsp;&nbsp;","")
        content = "\n".join(content.split())

        
        item = chapterItem()
        item["id"] = id
        item["type"] = "chapterInfo"
        item["content"] = content
        item["chapterNum"] = chapterNum
        item["chapterName"] = chapterName
        yield item