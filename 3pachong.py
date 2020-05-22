# -*- coding:utf8 -*-
import pymysql
import requests
import re
import pandas as pd
from bs4 import BeautifulSoup

def get_movies(start):
    url = "https://movie.douban.com/top250?start=%d&filter=" % start
    lists = []
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"}
    html = requests.get(url,headers=headers)
    soup = BeautifulSoup(html.content, "html.parser")
    items = soup.find("ol", class_="grid_view").find_all("li")
    for i in items:
        movie = {}
        movie["rank"] = i.find("em").text
        movie["link"] = i.find("div","pic").find("a").get("href")
        movie["mdirecter"]=re.findall(re.compile(r'<p class="">(.*?)</p>',re.S),str(i))[0].replace("...<br/>","").replace("\n                            ","")
        movie["name"] = i.find("span", "title").text
        movie["score"] = i.find("span", "rating_num").text
        movie["quote"] = i.find("span", "inq").text if(i.find("span", "inq")) else ""
        lists.append(movie)
    return lists

if __name__ == "__main__":
    db = pymysql.connect(host="localhost",user="root",password="123456",db="maoyan",charset="utf8",port = 3306)
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS movies")
    createTab = """CREATE TABLE movies(
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(20) NOT NULL,
        link VARCHAR(50) NOT NULL,
        score VARCHAR(4) NOT NULL,
        descr VARCHAR(50),
        directer VARCHAR(100),
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )"""
    cursor.execute(createTab)
    #采集到的数据循环插入数据中
    start = 0
    while (start < 250):
        lists = get_movies(start)
        for i in lists:
            sql = "INSERT INTO `movies`(`name`,`link`,`score`,`descr`,`directer`) VALUES(%s,%s,%s,%s,%s)"
            try:
                cursor.execute(sql, (i["name"], i["link"] , i["score"], i["quote"],i["mdirecter"]))
                db.commit()
                print(i["name"]+"...成功插入到数据库中")
            except:
                db.rollback()
        start += 25
    db.close()

    cursor = db.cursor()
    conn = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='maoyan',
                           charset='utf8mb4')
    cursor = conn.cursor()
    #输出评分top10
    sql = "select * from movies limit 10"
    db = pd.read_sql(sql, conn)
    df = db.sort_values(by="score", ascending=False)
    print(df[['name', 'score']])