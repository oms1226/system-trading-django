from django.shortcuts import render
from bs4 import BeautifulSoup
import urllib.request
import socket
import re
from datetime import datetime
# Create your views here.


def index(request):
    # TODO: 모든 정보 반환
    pass


def korea(request):
    # TODO: 국내 정보 반환
    pass


def overseas(request):
    # TODO: 해외 정보 반환
    pass


def collect(request):
    # TODO: 모든 정보 수집
    collect_korea()
    # collect_overseas()
    pass


def collect_korea():
    clien_url = "http://m.clien.net/cs3/board?bo_table=jirum"
    bs = get_bs(clien_url)
    trs = bs.find('table', {'class': 'tb_lst_normal'}).findAll('tr')

    for tr in trs:
        # 공지는 제외한다.
        category = tr.find('span', {'class': 'lst_category'})
        if category is None:
            continue
        if category.find('img') is not None:
            continue
        if "해외구매" in category:
            continue
        # URL 가져오기
        url = tr.find('div', {'class': 'wrap_tit'})['onclick']
        m = re.match(r".+?='(.+)'", url)
        url = "http://m.clien.net/cs3/board" + m.group(1)

        content = get_bs(url)
        title = content.find('div', {'class': 'post_tit scalable'}).text
        img_src = content.find('div', {'class': 'post_ct'}).find('img')['src']
        if img_src is not None:
            img_src = img_src.replace('http://cache.', 'https://')
        # hit
        view_info = content.find('span', {'class': 'view_info'}).text
        m = re.match(r'([^,]+) , Hit : (\d+)', view_info)

        date = datetime.strptime(m.group(1), '%m-%d %H:%M')
        date.replace(year=datetime.now().year)

        hit = m.group(2)

        save_data(title, url, img_src, date, hit)


def save_data(title, url, img_src, date, hit):
    # TODO: firebase에 저장한다.
    pass


def collect_overseas():
    pass


def get_bs(url_home, url_ref=""):
    url = url_home + url_ref
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        html = urllib.request.urlopen(req, timeout=10).read()
        bs = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    except socket.timeout:
        print(url)
    return bs
