# DeepLearning_Practice_Homework
USTC2023秋深度学习实践大作业一

## 主要预实现功能
- [x] 1. 爬取豆瓣电影的TOP250的电影信息
- [x] 2. 实现调用豆瓣电影的搜索接口，爬取搜索结果
- [x] 3. 实现用户易使用的GUI页面，利用flask框架和echarts实现
- [x] 4. 实现豆瓣电影的分类排行榜功能


## 项目结构
```
.   
├── README.md
├── information
│   ├── search.db
│   ├── movie.db
│   ├── movie.txt
│   ├── search.txt
├── models
│   ├── search.py
│   ├── spider.py
│   ├── rank.py
├── static
│   ├── assets
│   │   ├── css
│   │   ├── js
|   |   ├── vendor
├── templates
│   ├── index.html # homepage
│   ├── search.html # search page
│   ├── movie.html # top250 page
│   ├── rank.html # rank page
├── app.py # flask app
├── requirements.txt
```
## 项目运行
终端运行：
```
python app.py
```