import requests 
from bs4 import BeautifulSoup
import time
import sqlite3

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
    def get_info(self,filename,dbname=None):
        url = self.url
        self.get_soup(url)
        self.initdb(dbname)
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
                else:
                    comment = "无"
                # 获取电影的链接
                link = ul.find("a").get("href")
                # 将其并列在一个数组里
                movie = [title, rating_num, comment, link]  
                # 将其转化成字典
                movie_dict = dict(zip(["title", "rating_num", "comment", "link"], movie))
                self.Savefile(filename,movie_dict)
                self.SaveDB(dbname,movie_dict)
            url = self.get_next_page()
            if self.get_next_page() is None:
                url = None
            self.get_soup(url)
            # print(url)
            time.sleep(1) # 休眠1秒，避免被封IP
    # 信息存入数据库db
    def Savefile(self,filename,cotent):
        # 将爬取到的信息保存到文件中    
        with open(filename, "a+", encoding='utf-8') as f:
            f.write(str(cotent)+"\n")
            f.close()
    # 初始化数据库
    def initdb(self,dbname):
        conn = sqlite3.connect(dbname) 
        print("Opened database successfully")
        c = conn.cursor()
        # 如果表不存在，则创建表
        if not c.execute("SELECT * FROM sqlite_master WHERE type='table' AND name='MOVIE'").fetchall():
            c.execute('''CREATE TABLE MOVIE
                (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
                TITLE           TEXT    NOT NULL,
                RATING_NUM      TEXT    NOT NULL,
                COMMENT         TEXT    NOT NULL,
                LINK            TEXT    NOT NULL);
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
            c.execute("INSERT INTO MOVIE (TITLE,RATING_NUM,COMMENT,LINK) \
                VALUES (?,?,?,?)",(movie_dict["title"],movie_dict["rating_num"],movie_dict["comment"],movie_dict["link"]))
        conn.commit()
        print("Records created successfully")
        conn.close()
    # 可视化查看数据库
    def showdb(self,dbname):
        conn = sqlite3.connect(dbname)
        print("Opened database successfully")
        c = conn.cursor()
        cursor = c.execute("SELECT id, title, rating_num, comment, link from MOVIE")
        for row in cursor:
            print("ID = ", row[0])
            print("TITLE = ", row[1])
            print("RATING_NUM = ", row[2])
            print("COMMENT = ", row[3])
            print("LINK = ", row[4])
        print("Operation done successfully")
        conn.close()
if __name__ == "__main__":

    a = Spider('https://movie.douban.com/top250')
    a.get_soup()
    a.get_info("information/top250.txt","information/movie.db")
    a.showdb("information/movie.db")