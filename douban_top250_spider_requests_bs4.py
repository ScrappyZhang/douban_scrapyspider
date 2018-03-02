"""使用requests和bs4 抓取豆瓣top250"""
'''
@Time    : 2018/3/2 下午2:42
@Author  : scrappy_zhang
@File    : douban_top250_spider_requests_bs4.py
'''

import codecs
import re
import requests
from bs4 import BeautifulSoup

DOWNLOAD_URL = 'http://movie.douban.com/top250/'


def download_page(url):
    # 下载网页
    return requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36',
    }).content


def parse_html(html):
    """
    解析网页
    :param html:
    :return: 电影名称列表
    """
    soup = BeautifulSoup(html, 'html')
    movie_list_soup = soup.find('ol', attrs={'class': 'grid_view'})

    movie_list = []

    for movie_li in movie_list_soup.find_all('li'):
        # 排名
        ranking = movie_li.find('div', attrs={'class': 'pic'}).find('em').getText()
        # 电影名称
        detail = movie_li.find('div', attrs={'class': 'hd'})
        movie_name = detail.find('span', attrs={'class': 'title'}).getText()
        # 电影得分
        detail = movie_li.find('div', attrs={'class': 'star'})
        movie_score = detail.find('span', attrs={'class': 'rating_num'}).getText()
        # 电影评论数
        comment = detail.getText()
        # print(comment)
        comment_num = re.search(r'(\d+)人评价', comment).group(1)
        # 电影豆瓣链接
        movie_link = movie_li.find('div', attrs={'class': 'hd'}).find('a')['href']
        movie = [ranking, movie_name, movie_score, comment_num, movie_link,]
        movie_list.append(movie)

    next_page = soup.find('span', attrs={'class': 'next'}).find('a')
    if next_page:
        return movie_list, DOWNLOAD_URL + next_page['href']
    return movie_list, None


def main():
    url = DOWNLOAD_URL
    import time

    with codecs.open('douban_top250_info.csv', 'wb', encoding='utf-8') as fp:
        fp.write('排名,电影名称,豆瓣得分,评论数,电影豆瓣链接,\n')
        while url:
            time.sleep(0.5)
            html = download_page(url)
            movie_list, url = parse_html(html)
            for movie_info in movie_list:
                line_info = ''
                for info in movie_info:
                    line_info += info + ','
                print(line_info)
                fp.write(u'{line_info}\n'.format(line_info=line_info))
        print('done!')


if __name__ == '__main__':
    main()
