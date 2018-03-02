# 豆瓣抓取top250的两种方式：

项目信息：

两部分：

## 1.douban_top250_spider_requests_bs4.py

采用requests和bs4的方式抓取，抓取结果存入douban_top250_info.csv

## 2.除此之外，其他文件为依赖scrapy框架抓取豆瓣250

可执行`scrapy crawl douban_movie_top250 -o douban_top250.csv`

## 3.scrapy抓包方式抓取AJAX豆瓣数据

可执行`scrapy crawl douban_ajax -o douban_top250.csv`
