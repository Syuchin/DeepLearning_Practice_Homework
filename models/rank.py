# Realize the function of climbing Douban ranking.

import requests
from bs4 import BeautifulSoup
import time
import logging
import sqlite3  
class Rank:
    def __init__(self):
        self.url = "https://movie.douban.com/chart"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.188 Safari/537.36'
        }
        # type to url type
        self.type = {"剧情":11, "喜剧":24, "动作":5, "爱情":13, "科幻":17, "动画":25, "悬疑":10, "惊悚":19, "恐怖":20, "纪录片":1, "短片":23, "情色":6, "音乐":14, "歌舞":7, "家庭":28, "儿童":8, "传记":2, "历史":4, "战争":22, "犯罪":3, "西部":27, "奇幻":16, "冒险":15, "灾难":12, "武侠":29, "古装":30, "运动":18, "黑色电影":31}
    # <a href="/typerank?type_name=剧情&type=11&interval_id=100:90&action=">剧情</a></span>
        self.INDEX_URL = 'https://movie.douban.com/j/chart/top_list?type={type}&interval_id=100%3A90&action=&start={offset}&limit={limit}'
        self.Limit = 20
        self.DETAIL_URL = 'https://movie.douban.com/subject/{id}/'
    # Get the ranking information
    def get_rank_info_newmovie(self):
        r = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        for ul in soup.find_all("div", class_="pl2"):
            title = ul.find("a").get_text().replace(" ", "").replace("\n", "").strip()
            link = ul.find("a").get("href")
            rating_num = ul.find("span", class_="rating_nums").string
            # Juxtaposed it in an array.
            movie = [title, link]
            # Convert it to a dictionary.
            movie_dict = dict(zip(["title", "link"], movie))
            print(movie_dict)
        return movie_dict
    # choose the type of movie ranking
    def choose_movieranking(self,type):
        # print("请选择电影排行榜的类型：")
        # print("剧情\t喜剧\t动作\t爱情\t科幻\t动画\n 悬疑\t惊悚\t恐怖\t纪录片\t短片\t情色\n 音乐\t歌舞\t家庭\t儿童\t传记\t历史\n战争\t犯罪\t西部\t奇幻\t冒险\t灾难\n 武侠\t古装\t运动\t黑色电影")
        # input_type = input("请输入类型：")
        input_type = type
        if input_type in self.type:
            return input_type, self.type[input_type]
        else:
            return 0,0
        #     print("输入有误，请重新输入！")
        #     return self.choose_movieranking()
        
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')


    def scrape_api(self,url):
        logging.info('scraping %s...', url)
        response = requests.get(url, headers=self.headers)
        print(response.status_code)
        if response.status_code == 200:
            return response.json()
        logging.error('get invalid status code %s while scraping %s', response.status_code, url)
        

    def scrape_index(self,page,type):
        url = self.INDEX_URL.format(type=type,offset=self.Limit * (page - 1), limit=self.Limit)
        print(url)
        return self.scrape_api(url)

    def scrape_detail(self,id):
        url = self.DETAIL_URL.format(id=id)
        return url
    TOTAL_PAGE = 5
    def initdb(self,dbname):
        self.deletedb(dbname)
        conn = sqlite3.connect(dbname) 
        print("Opened database successfully")
        c = conn.cursor()
        # if table is not exist, create it
        if not c.execute("SELECT * FROM sqlite_master WHERE type='table' AND name='RANK'").fetchall():
            c.execute('''CREATE TABLE RANK
                (RANK           TEXT    NOT NULL,
                TITLE           TEXT    NOT NULL,
                SCORE           TEXT    NOT NULL,
                VOTE_COUNT      TEXT    NOT NULL,
                URL             TEXT    NOT NULL,
                ID              TEXT    NOT NULL,
                RELEASE_DATE    TEXT    NOT NULL);
                ''')
            print("Table created successfully")
        else:
            print("Table already exists")
        conn.commit()
        conn.close()
    # Save the data to the database
    def SaveDB(self,dbname,movie_dict):
        conn = sqlite3.connect(dbname)
        print("Opened database successfully")
        c = conn.cursor()
        for i in movie_dict:
            if movie_dict[i] == None:
                movie_dict = "NONE"
        if movie_dict is not None:
            print(movie_dict["rank"],movie_dict["title"],movie_dict["score"], movie_dict["vote_count"],movie_dict["url"],movie_dict["id"],movie_dict["release_date"])
            c.execute("INSERT INTO RANK (RANK,TITLE,SCORE,VOTE_COUNT,URL,ID,RELEASE_DATE) \
                VALUES (?,?,?,?,?,?,?)",(movie_dict["rank"],movie_dict["title"],movie_dict["score"], movie_dict["vote_count"],movie_dict["url"],movie_dict["id"],movie_dict["release_date"]))
        conn.commit()
        print("Records created successfully")
        conn.close()

    def deletedb(self,dbname):
        conn = sqlite3.connect(dbname)
        print("Opened database successfully")
        c = conn.cursor()
        if c.execute("SELECT * FROM sqlite_master WHERE type='table' AND name='RANK'").fetchall():
            c.execute("DROP TABLE RANK")
            print("Table deleted successfully")
        else:
            print("Table does not exist")
        conn.commit()
        conn.close()

    def main(self,filename,type):
        self.initdb(filename)
        for page in range(1, self.TOTAL_PAGE + 1):
            index_data = self.scrape_index(page,type)
            for item in index_data:
                self.SaveDB(filename,item)
            time.sleep(0.5)
    def transfer_interface(self):
        pass
        
        
if __name__ == "__main__":
    a = Rank()
    # name, value = a.choose_movieranking()
    a.main('information/rank.db')