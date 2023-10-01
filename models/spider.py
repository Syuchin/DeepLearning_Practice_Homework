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
    def get_info(self,filename):
        url = self.url
        self.get_soup(url)
        # 完整的爬取所有的信息
        while (url is not None):
            for ul in self.soup.find_all("div", class_="item"):
                # 获取电影名称
                title = ul.find("span", class_="title").string
                # 获取电影评分
                rating_num = ul.find("span", class_="rating_num").string
                # 获取电影的短评
                comment = ul.find("span", class_="inq")
                # 处理没有短评的情况
                if comment:
                    comment = comment.string
                # 获取电影的链接
                link = ul.find("a").get("href")
                # 获取电影的封面
                cover = ul.find("img").get("src")
                # 将其并列在一个数组里
                movie = [title, rating_num, comment, link, cover]
                # 将其转化成字典
                movie_dict = dict(zip(["title", "rating_num", "comment", "link", "cover"], movie))
                self.Savefile(filename,movie_dict)
            url = self.get_next_page()
            if self.get_next_page() is None:
                url = None
            self.get_soup(url)
            # print(url)
            time.sleep(1) # 休眠1秒，避免被封IP
    def Savefile(self,filename,cotent):
        # 将爬取到的信息保存到文件中    
        with open(filename, "a+", encoding='utf-8') as f:
            f.write(str(cotent)+"\n")
            f.close()
if __name__ == "__main__":

    a = Spider('https://movie.douban.com/top250')
    a.get_soup()
    a.get_info("information/top250.txt")