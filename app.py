# 利用flask构建前端界面
from flask import Flask, request
from flask import render_template
from models.search import Search  
import sqlite3 
from models.rank import Rank

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/index')
def home():
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
    # get the keyword from the POST
    if request.method == 'POST':
        keyword = request.form.get('search')
        search = Search()
        url = search.get_search_result(keyword)
        # get the movie information from the url
        search.get_movie_info(url)
        # save the movie information to the database
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

@app.route('/rank', methods=['GET', 'POST'])
def rank():
    if request.method == 'POST':
        input_type = request.form.get('type')
        rank = Rank()
        type_arrow = {"剧情":11, "喜剧":24, "动作":5, "爱情":13, "科幻":17, "动画":25, "悬疑":10, "惊悚":19, "恐怖":20, "纪录片":1, "短片":23, "情色":6, "音乐":14, "歌舞":7, "家庭":28, "儿童":8, "传记":2, "历史":4, "战争":22, "犯罪":3, "西部":27, "奇幻":16, "冒险":15, "灾难":12, "武侠":29, "古装":30, "运动":18, "黑色电影":31}
        type = rank.choose_movieranking(input_type)[1]
        type_num = type_arrow[input_type]
        if type == 0:
            type = rank.choose_movieranking()[1]
        rank.main('information/rank.db',type)
        # save the movie information to the database
        datalist = []
        con = sqlite3.connect("information/rank.db")
        cur = con.cursor()
        sql = "select * from RANK"
        data = cur.execute(sql)
        for item in data:
            datalist.append(item)
        cur.close()
        con.close()
        # return constant to the html
        return render_template('rank.html',movies=datalist,type=input_type,type_num=type_num)
    else:
        return render_template('rank.html')

if __name__ == '__main__':
    app.run(port=5004,debug=True) 