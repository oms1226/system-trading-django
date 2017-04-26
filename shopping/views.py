from django.shortcuts import render
from bs4 import BeautifulSoup
import urllib.request
import socket
import re
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


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


def remove(request):
    """ 전체 내용을 삭제합니다. """
    db = settings.FIREBASE_BUY_CHEAP.database()
    db.child('buy-cheap').child('shop-korea').remove()
    db.child('buy-cheap').child('shop-overseas').remove()
    pass


@csrf_exempt
def collect(request):
    """ 모든 정보 수집"""
    result_list = []
    result_list.extend(collect_clien('http://m.clien.net/cs3/board?bo_table=jirum', 'korea'))
    result_list.extend(collect_ppomppu("http://m.ppomppu.co.kr/new/bbs_list.php?id=ppomppu", 'korea'))
    result_list.extend(collect_ppomppu("http://m.ppomppu.co.kr/new/bbs_list.php?id=ppomppu4", 'overseas'))
    result_list.extend(collect_dealbada("http://www.dealbada.com/bbs/board.php?bo_table=deal_domestic", 'korea'))
    result_list.extend(collect_dealbada("http://www.dealbada.com/bbs/board.php?bo_table=deal_oversea", 'overseas'))
    result_list.extend(collect_ddanzi("http://www.ddanzi.com/pumpin", 'korea'))
    result_list.extend(collect_ddanzi("http://www.ddanzi.com/pumpout", 'overseas'))

    # collect_overseas()
    return render(request, 'torrent/collect.html', {'result': result_list})


def collect_ddanzi(url, target="korea"):
    result_list = []
    bs = get_bs(url)
    trs = bs.find('div', {'class': 'board_list'}).find('tbody').findAll('tr')
    for tr in trs:
        if tr.has_attr("class") and 'notice' in tr['class']:
            continue
        img_src = tr.find('td', {'class': 'thumbnail'}).find('img')['src']
        a_tag = tr.find('td', {'class': 'title'}).find('a')
        url = a_tag['href']
        title = a_tag.text.strip()
        price = tr.find('div', {'class': 'price'}).text

        content = get_bs(url)
        div = content.find('div', {'class': 'read_header'})

        date = div.find('p', {'class': 'time'}).text.strip()
        read_str = div.find('span', {'class': 'read'}).text
        m = re.match(r'.+:(\d+)', read_str)
        read = m.group(1)
        like = div.find('span', {'class':'vote'}).find('em').text

        result = save_data(target, title, url, img_src, date, read, like, price=price)
        result_list.append(result)

    return result_list


def collect_dealbada(url, target="korea"):
    result_list = []
    bs = get_bs(url)
    trs = bs.find('table', {'class': 'hoverTable'}).find('tbody').findAll('tr')
    for tr in trs:
        if 'bo_notice' in tr['class']:
            continue
        img_src = tr.find('td', {'class': 'td_img'}).find('img')['src']
        a_tag = tr.find('td', {'class': 'td_subject'}).find('a')
        url = a_tag['href']
        title = a_tag.text.strip()
        sold_out = False
        if a_tag.find('img') and a_tag.find('img')['alt'] is '종료':
            sold_out = True
        # read = tr.find('td', {'class': 'td_num'}).text.strip()
        # like = tr.find('td', {'class': 'td_num_g'}).find('span').text

        content = get_bs(url)
        section = content.find('section', {'id': 'bo_v_info'})
        if section is None:
            continue
        spans = section.findAll('span')
        if len(spans) == 0:
            continue

        date = spans[7].text[:16]
        read = spans[9].text
        like = spans[12].text
        reply = spans[18].text

        result = save_data(target, title, url, img_src, date, read, like, reply, sold_out)
        result_list.append(result)

    return result_list


def collect_ppomppu(url, target="korea"):
    result_list = []
    bs = get_bs(url)
    lis = bs.findAll('li', {'class': 'none-border'})
    for li in lis:
        img_src = li.find('div', {'class': 'thmb'}).find('img')['src']
        if img_src is not None:
            img_src = img_src.replace('http://cache.', 'https://')
        url = "http://m.ppomppu.co.kr/new/" + li.find('a')['href']
        title = li.find('span', {'class': 'title'}).text
        reply = li.find('div', {'class': 'com_line'}).find('span').text

        content = get_bs(url)
        date_text = content.find('span', {'class':'hi'}).text.strip()
        m = re.search(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2})", date_text)
        date = m.group(1)
        div_text = content.find('div', {'class': 'info'}).text.strip()
        m = re.search(r"조회 : (\d+) / 추천 : (\d+)", div_text)
        read = m.group(1)
        like = m.group(2)

        result = save_data(target, title, url, img_src, date, read, like, reply)
        result_list.append(result)

    return result_list


def collect_clien(url, target="korea"):
    result_list = []
    bs = get_bs(url)
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
        if datetime.now().month - date.month >= 0:
            date = date.replace(year=datetime.now().year)
        else:
            date = date.replace(year=datetime.now().year - 1)

        read = m.group(2)

        result = save_data(target, title, url, img_src, date, read)
        result_list.append(result)
    return result_list


def key_from_url(url):
    url = re.sub(r'&page=\d*', r'', url)
    url = re.sub(r'[./:?=&]', r'_', url)
    return url


def save_data(target, title, url, img_src, date, read=0, like=0, reply=0, sold_out=False, price=0):
    db = settings.FIREBASE_BUY_CHEAP.database()
    data = {
        "title": title,
        "url": url,
        "img": img_src,
        "date": str(date),
        "read": read,
        "like": like,
        "reply": reply,
        'sold_out': sold_out,
        'price': price
    }
    if target is "korea":
        save_path = "shop-korea"
    else:
        save_path = "shop-overseas"

    result = db.child('buy-cheap').child(save_path).child(key_from_url(url)).set(data)
    return result


def get_bs(url_home, url_ref=""):
    url = url_home + url_ref
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        html = urllib.request.urlopen(req, timeout=10).read()
        bs = BeautifulSoup(html, 'lxml', from_encoding='utf-8')
    except socket.timeout:
        print(url)
    return bs
