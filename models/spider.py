import requests 
from bs4 import BeautifulSoup
import time


class Spider:
    def __init__(self, url):
        self.url = url
        self.soup = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }

    def get_soup(self, url=None):
        if url is None:
            url = self.url
        r = requests.get(url, headers=self.headers)
        self.soup = BeautifulSoup(r.text, 'html.parser')
    # 获取下一页的内容
    def get_next_page(self):
        url_next = self.soup.find("span", class_="next").find("a")
        if url_next is not None:
            url_all = self.url + url_next.get("href")
        # 继续处理url_next
        else:
        # 处理找不到下一页的情况
            return None
        return url_all
    # 爬取主要的信息
    def get_title(self):
        url = self.url
        self.get_soup(url)
        # 完整的爬取所有的电影名称
        # while (url is not None):
        #     for ul in self.soup.find_all("span", class_="title"):
        #         print(ul.string)
        #     url = self.get_next_page()
        #     if self.get_next_page() is None:
        #         url = None
        #     self.get_soup(url)
        #     print(url)
        #     time.sleep(1) 
        # 测试爬取其他的信息，并转化成字典       
    def get_movie_info(self):
        pass
    def get_movie_comment(self):
        pass    
a = Spider('https://movie.douban.com/top250')
a.get_soup()
a.get_title()