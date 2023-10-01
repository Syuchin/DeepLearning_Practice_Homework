# 此模块主要实现，用户在终端输入关键字，然后调用接口在网站中查询，查询结果调用爬虫返回给用户
# 1.用户输入关键字
# 2.调用接口查询
# 3.调用爬虫返回给用户

from bs4 import BeautifulSoup
import time
from selenium import webdriver

class Search:
    def __init__(self):
        self.url = "https://movie.douban.com/subject_search?search_text="
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }
    # 输入关键词，等待，获取搜索结果

    def get_search_result(self, keyword):
        url = self.url + keyword + "&cat=1002"
        return url
    
    # 获取电影的信息
    def get_movie_info(self, url):
        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(1)
        r = driver.page_source
        soup = BeautifulSoup(r, 'html.parser')
        for ul in soup.find_all('div', class_="item-root"):
            # 获取电影名称
            title = ul.find("a", class_="title-text").string
            # 获取电影评分
            rating_num = ul.find("span", class_="rating_nums")
            if rating_num:
                rating_num = rating_num.get_text()
            # 获取电影的评价人数
            rating_people = ul.find("span", class_="pl")
            if rating_people:
                rating_people = rating_people.get_text() # 由于第一个字符是空格，所以不能直接使用 rating_num = ul.find("span", class_="rating_nums").string 
            # 获取电影的链接
            link = ul.find("a").get("href")
            # 获取电影的封面
            cover = ul.find("img").get("src")
            # 将其并列在一个数组里
            movie = [title, rating_num, rating_people, link, cover]
            # 将其转化成字典
            movie_dict = dict(zip(["title", "rating_num", "rating_people", "link", "cover"], movie))
            print(movie_dict)
        return movie_dict
if __name__ == "__main__":
    a = Search()
    # input_keyword = input("请输入关键字：")
    input_keyword = "诺兰"
    url = a.get_search_result(input_keyword)
    print(url)
    a.get_movie_info(url)