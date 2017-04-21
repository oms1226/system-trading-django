from django.shortcuts import render
from bs4 import BeautifulSoup
import urllib.request
import socket
import re
from datetime import datetime
import pyrebase
from django.conf import settings
import firebase_admin
from firebase_admin import credentials, auth
from firebase import firebase as fb
import os


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
    result_list = []
    result_list.extend(collect_clien())
    # collect_overseas()
    return render(request, 'torrent/collect.html', {'result': result_list})


def collect_clien(target="korea"):
    result_list = []

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
            target = "overseas"
        # URL 가져오기
        url = tr.find('div', {'class': 'wrap_tit'})['onclick']
        m = re.match(r".+?='(.+)'", url)
        url = "http://m.clien.net/cs3/board" + m.group(1)

        content = get_bs(url)
        title = content.find('div', {'class': 'post_tit scalable'}).text
        div_post_ct = content.find('div', {'class': 'post_ct'})
        img_src = ""
        if div_post_ct.find('img'):
            img_src = content.find('div', {'class': 'post_ct'}).find('img')['src']
            if img_src is not None:
                img_src = img_src.replace('http://cache.', 'https://')
        # hit
        view_info = content.find('span', {'class': 'view_info'}).text
        m = re.match(r'([^,]+) , Hit : (\d+)', view_info)

        date = datetime.strptime(m.group(1), '%m-%d %H:%M')
        date = date.replace(year=datetime.now().year)

        hit = m.group(2)

        if target is "korea":
            save_path = "buy-cheap/shop-korea"
        else:
            save_path = "buy-cheap/shop-overseas"
        result = save_data(save_path, title, url, img_src, date, hit)
        result_list.appen(result)
    return result_list


def key_from_url(url):
    url = re.sub(r'&page=\d*', r'', url)
    url = re.sub(r'[./:?=&]', r'', url)
    return url


def save_data(path, title, url, img_src, date, hit):
    firebase = pyrebase.initialize_app(settings.FIREBASE_BUY_CHEAP_CONFIG)
    # auth = firebase.auth()
    db = firebase.database()
    # storage = firebase.storage()
    data = {
        "title": title,
        "url": url,
        "img": img_src,
        "date": str(date),
        "hit": hit
    }
    result = db.child(path).child(key_from_url(url)).set(data)
    # users = db.child("buy-cheap/shop-korea").order_by_child("dateFormat").limit_to_first(100).get()
    return result


def save_data_firebase_admin(title, url, img_src, date, hit):
    # TODO: firebase에 저장한다.
    # print(os.path.dirname(__file__))
    # app_path = os.path.abspath(os.path.dirname(__file__))
    # key_path = os.path.abspath(os.path.join(app_path, 'buy-cheap-firebase-adminsdk-accountkey.json'))
    # cred = credentials.Certificate(key_path)
    # app = firebase_admin.initialize_app(cred, name='shopping')
    # app2 = firebase_admin.App('shopping', cred, None)
    #
    # # access_tokenの取得
    # accessTokenInfo=app.credential.get_access_token()
    # print("access_token:" + accessTokenInfo.access_token)
    # print("expire:" + str(accessTokenInfo.expires_in))
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
