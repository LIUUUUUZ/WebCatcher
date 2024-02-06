from bs4 import BeautifulSoup  #网页解析
import urllib.request, urllib.response , urllib.error#定制URL， 获取网页数据

# parser for web pages and return the status and the html content
class WebParser():
    def __init__(self,url) -> None:
        self.url = url
        self.status = None
        self.html = None
        self.parsed_data = None
        self.selected_data = None
        self.head = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15"}    

    def askURL(self):
        req = urllib.request.Request(self.url, headers=self.head)
        html = ""
        try:
            response = urllib.request.urlopen(req,timeout= 10)
            html = response.read().decode("utf-8")
            self.status = response.status
        except urllib.error.URLError as e:
            if hasattr(e,"code"):
                # print(e.code)
                self.status = e.code
            if hasattr(e,"reason"):
                # print(e.reason)
                self.status = e.reason
        self.html = html

    def parser(self):
        soup = BeautifulSoup(self.html,"html.parser")
        self.parsed_data = soup


    def bsSelector(self,select_key):
        self.selected_data = self.parsed_data.select(select_key)