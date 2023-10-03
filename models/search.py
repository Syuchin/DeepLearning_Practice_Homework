# 此模块主要实现，用户在终端输入关键字，然后调用接口在网站中查询，查询结果调用爬虫返回给用户
# 1.用户输入关键字
# 2.调用接口查询
# 3.调用爬虫返回给用户

from bs4 import BeautifulSoup
import time
from selenium import webdriver
import sqlite3

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
        self.deletedb("information/search.db")
        self.initdb("information/search.db")
        r = driver.page_source
        soup = BeautifulSoup(r, 'html.parser')
        for ul in soup.find_all('div', class_="item-root"):
            # 获取电影名称
            title = ul.find("a", class_="title-text").string
            # 获取电影评分
            rating_num = ul.find("span", class_="rating_nums")
            if rating_num:
                rating_num = rating_num.get_text()
            else:
                rating_num = "NONE"
            # 获取电影的评价人数
            rating_people = ul.find("span", class_="pl")
            if rating_people:
                rating_people = rating_people.get_text()
                rating_people = rating_people.replace("(", "").replace(")", "")
                # 由于第一个字符是空格，所以不能直接使用 rating_num = ul.find("span", class_="rating_nums").string 
            else:
                rating_people = "NONE"
            # 获取电影的链接
            link = ul.find("a").get("href")
            # 获取电影的封面
            cover = ul.find("img").get("src")
            # 将其并列在一个数组里
            movie = [title, rating_num, rating_people, link, cover]
            # 将其转化成字典
            movie_dict = dict(zip(["title", "rating_num", "rating_people", "link", "cover"], movie))
            self.SaveDB("information/search.db",movie_dict)
            self.Savefile("information/search.txt",movie_dict)
    def Savefile(self,filename,movie_dict):
        with open(filename,"a+",encoding="utf-8") as f:
            f.write(str(movie_dict)+"\n")
            print("保存成功")
    # 初始化数据库
    def initdb(self,dbname):
        conn = sqlite3.connect(dbname) 
        print("Opened database successfully")
        c = conn.cursor()
        # 如果表不存在，则创建表
        if not c.execute("SELECT * FROM sqlite_master WHERE type='table' AND name='SEARCH'").fetchall():
            c.execute('''CREATE TABLE SEARCH
                (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
                TITLE           TEXT    NOT NULL,
                RATING_NUM      TEXT    NOT NULL,
                RATING_PEOPLE   TEXT    NOT NULL,
                LINK            TEXT    NOT NULL,
                COVER           TEXT    NOT NULL);
                ''')
            print("Table created successfully")
        else:
            print("Table already exists")
        conn.commit()
        conn.close()
    # 将爬取到的信息存入数据库
    def SaveDB(self,dbname,movie_dict):
        conn = sqlite3.connect(dbname)
        print("Opened database successfully")
        c = conn.cursor()
        if movie_dict is not None:
            c.execute("INSERT INTO SEARCH (TITLE,RATING_NUM,RATING_PEOPLE,LINK,COVER) \
                VALUES (?,?,?,?,?)",(movie_dict["title"],movie_dict["rating_num"],movie_dict["rating_people"], movie_dict["link"],movie_dict["cover"]))
        conn.commit()
        print("Records created successfully")
        conn.close()
    # 可视化查看数据库
    def showdb(self,dbname):
        conn = sqlite3.connect(dbname)
        print("Opened database successfully")
        c = conn.cursor()
        cursor = c.execute("SELECT id, title, rating_num, rating_people, link, cover from SEARCH")
        for row in cursor:
            print("ID = ", row[0])
            print("TITLE = ", row[1])
            print("RATING_NUM = ", row[2])
            print("RATING_PEOPLE = ", row[3])
            print("LINK = ", row[4])
            print("COVER = ", row[5], "\n")
        print("Operation done successfully")
        conn.close()
    # 删除数据库
    def deletedb(self,dbname):
        conn = sqlite3.connect(dbname)
        print("Opened database successfully")
        c = conn.cursor()
        c.execute("DROP TABLE SEARCH")
        conn.commit()
        print("Table deleted successfully")
        conn.close()
if __name__ == "__main__":
    a = Search()
    # input_keyword = input("请输入关键字：")
    input_keyword = "诺兰"
    url = a.get_search_result(input_keyword)
    print(url)
    a.get_movie_info(url)