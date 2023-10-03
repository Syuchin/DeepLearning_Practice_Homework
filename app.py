# 利用flask构建前端界面
from flask import Flask, request
from flask import render_template
from models.search import Search  
import sqlite3 

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
# 当我在html按下按钮时，会调用这个函数
@app.route('/index')
def home():
    #这个函数会调用爬虫，然后将爬虫的结果返回给前端
    return index()
@app.route('/movie')
def movie():
    datalist = []
    con = sqlite3.connect("information/movie.db")
    cur = con.cursor()
    sql = "select * from MOVIE"
    data = cur.execute(sql)
    for item in data:
        datalist.append(item)
    cur.close()
    con.close()
    print(datalist)
    return render_template('movie.html',movies=datalist)
@app.route('/search', methods=['GET', 'POST'])
def search():
    # 获取post的内容
    if request.method == 'POST':
        keyword = request.form.get('search')
        # 调用爬虫
        search = Search()
        url = search.get_search_result(keyword)
        # 获取电影的信息
        search.get_movie_info(url)
        # 将电影的信息存入数据库
        datalist = []
        con = sqlite3.connect("information/search.db")
        cur = con.cursor()
        sql = "select * from SEARCH"
        data = cur.execute(sql)
        for item in data:
            datalist.append(item)
        cur.close()
        con.close()
        return render_template('search.html',movies=datalist,urls= url)
    else:
        return render_template('search.html')


if __name__ == '__main__':
    app.run(port=5004,debug=True) 