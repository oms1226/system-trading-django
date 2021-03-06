from django.shortcuts import render
import re
import sys
import urllib.request
import logging
import socket
import urllib.parse
from bs4 import BeautifulSoup
from .models import Magnet
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import threading
from django.core.exceptions import MultipleObjectsReturned
# Create your views here.

# Get an instance of a logger
logger = logging.getLogger(__name__)


def rss(request):
    latest_magnet_list = Magnet.objects.order_by('-id')[:500]

    trackers = '&tr=udp://tracker.openbittorrent.com:80&tr=http://megapeer.org:6969/announce&tr=http://mgtracker.org:2710/announce&tr=http://tracker.files.fm:6969/announce&tr=http://tracker.flashtorrents.org:6969/announce&tr=http://tracker.mg64.net:6881/announce&tr=http://tracker.nwps.ws:6969/announce&tr=http://tracker.ohys.net/announce&tr=http://tracker.tfile.me/announce&tr=udp://9.rarbg.com:2710/announce&tr=udp://9.rarbg.me:2710/announce&tr=udp://coppersurfer.tk:6969/announce&tr=udp://tracker.coppersurfer.tk:6969&tr=udp://tracker.leechers-paradise.org:6969&tr=udp://exodus.desync.com:6969/announce&tr=udp://open.coppersurfer.com:1337/announce'

    rss_content = '<?xml version="1.0" encoding="UTF-8"?>' +\
        '<rss xmlns:showrss="http://showrss.info" version="2.0">' +\
        '<channel>' +\
        '<title>RSS</title>' +\
        '<link>http://attr.cf</link>' + \
        '<ttl>30</ttl>' + \
        '<description>RSS</description>'

    for magnet in latest_magnet_list:
        magnet.title = re.sub(r'["<>]', r"", magnet.title)
        rss_content += '<item>'
        rss_content += '<title>' + magnet.title + '</title>'
        rss_content += '<link>' + magnet.magnet + '</link>'
        m = re.search('(?<=btih:).*', magnet.magnet)
        info_hash = m.group(0)
        rss_content += '<guid ispermalink="false">' + info_hash + '</guid>'
        rss_content += '<showrss:info_hash>' + info_hash + '</showrss:info_hash>'
        rss_content += '<showrss:showname>' + magnet.title + '</showrss:showname>'
        enclosure_url = magnet.magnet + '&dn=' + magnet.title + trackers
        rss_content += '<enclosure url = "' + enclosure_url + '" length = "0" type = "application/x-bittorrent"></enclosure>'
        rss_content += '</item>'

    rss_content += '</channel></rss>'
    rss_content = rss_content.replace('&', '&amp;')

    return HttpResponse(rss_content)


def index(request):
    return render(request, 'torrent/index.html')


def collect_tfreeca():
    url_home = 'http://www.tfreeca22.com/'
    url_ref_list = [
        ['tv', 'board.php?mode=list&b_id=tent'],
        ['music', 'board.php?mode=list&b_id=tmusic'],
        # ['tv', 'board.php?mode=list&b_id=tdrama'],
        # ['tv', 'board.php?mode=list&b_id=tv'],
        # ['movie', 'board.php?mode=list&b_id=tmovie'],
        # ['ani', 'board.php?mode=list&b_id=tani'],
        # ['util', 'board.php?mode=list&b_id=util'],
    ]

    result = list()

    for url_ref in url_ref_list:
        category = url_ref[0]
        url = url_ref[1]

        bs = get_bs(url_home, url)
        if bs is None:
            continue

        bs_trs = bs.find('table', {'class': 'b_list'}).findAll('tr')

        for bs_tr in bs_trs:
            if 'class' in bs_tr.attrs:
                tr_class = bs_tr.attrs['class'][0]
                if tr_class == 'nbgcolor':
                    continue
            href = bs_tr.find("a", {"class": re.compile(r'title')})['href']
            bs_content = get_bs(url_home, href)
            if bs_content is None:
                continue

            title = bs_content.find('td', {'class': 'view_t2'})['title']
            torrent_src = bs_content.find('iframe', {'id': 'external-frame'})['src']
            bs_torrent = get_bs(url_home, torrent_src)
            if bs_torrent is None:
                continue

            magnet = bs_torrent.find('div', {'class': 'torrent_magnet'}).find('a')['href']

            saved, obj = save_data(title, magnet, url_home + href, category)
            if saved is None:
                break
            result.append(obj)

    return result


def collect_torrentkim():
    url_home = 'https://torrentkim10.net/'
    url_ref_list = [
        ['tv', 'torrent_variety/torrent1.htm'],
    ]

    result = list()

    for url_ref in url_ref_list:
        category = url_ref[0]
        url = url_ref[1]

        bs = get_bs(url_home, url)
        if bs is None:
            continue

        bs_trs = bs.find('table', {'class': 'board_list'}).findAll('tr')

        for bs_tr in bs_trs:
            if 'class' not in bs_tr.attrs:
                continue
            if 'style' in bs_tr.attrs:
                if 'display:none' == bs_tr['style']:
                    continue
            a_tag = bs_tr.find("td", {"class": 'subject'}).find('a')
            title = a_tag.text
            href = a_tag['href'][3:]        # ../ 에서 .. 제거

            bs_content = get_bs(url_home, href)
            if bs_content is None:
                continue

            inputs = bs_content.findAll('input')
            magnet = None
            for input in inputs:
                if 'readonly' in input.attrs:
                    magnet = input['value']
                    break
            if magnet is None:
                continue

            saved, obj = save_data(title, magnet, url_home + href, category)
            if saved is None:
                break
            result.append(obj)

    return result


def collect_backgound():
    channel = '#bot_torrent'

    # 이름, 함수
    torrents = [
        # '토렌트위즈': collect_torrentwiz,
        ['티프리카', collect_tfreeca],
        ['토렌트킴', collect_torrentkim],
    ]

    for torrent in torrents:
        name = torrent[0]
        func = torrent[1]

        rst = ''

        try:
            result = func()
        except Exception as e:
            print(sys.exc_info()[0])
            settings.SLACK.chat.post_message(channel, name + ' 실패', sys.exc_info()[0])
        else:
            if len(result) > 0:
                for obj in result:
                    rst += obj.title + '\n'
            else:
                rst = '0건'
            settings.SLACK.chat.post_message(channel, name + '에서 ' + rst + ' 추가됨')


collect_threading = None

@csrf_exempt
def collect(request):
    global collect_threading

    if collect_threading and collect_threading.isAlive():
        msg = "collect 요청이 처리중입니다."
    else:
        collect_threading = threading.Thread(target=collect_backgound, args=(), kwargs={})
        collect_threading.setDaemon(True)
        collect_threading.start()
        msg = "collect 요청되었습니다."
    return render(request, 'torrent/result.html', {'msg': msg})


def get_bs(url_home, url_ref=""):
    url = url_home + url_ref
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    bs = None
    try:
        html = urllib.request.urlopen(req, timeout=10).read()
        bs = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    except socket.timeout:
        print('except socket.timeout:', url)
    except:
        print('except', url)
    return bs


def collect_torrentwiz():
    url_home = 'https://torrentwiz4.com/'
    url_ref_list = [
        ['tv', 'torrent_ent'],
        ['tv', 'torrent_sisa'],
        ['tv', 'torrent_drama'],
        ['movie', 'torrent_movieko'],
        ['movie', 'torrent_movielatest'],
        ['music', 'torrent_kpop'],
        ['music', 'torrent_pop'],
        ['ani', 'torrent_ani'],
        ['ani', 'torrent_aniend'],
        ['comic', 'torrent_cartoon'],
        ['game', 'torrent_game'],
        ['util', 'torrent_util'],
    ]

    result = list()

    for url_ref in url_ref_list:
        category = url_ref[0]
        url = url_ref[1]
        bs = get_bs(url_home, url)
        if bs is None:
            continue

        bs_trs = bs.find('table', {'class': 'list-pc'}).find('tbody').findAll('tr')

        for bs_tr in bs_trs:
            td_num = bs_tr.find('td', {'class': 'td_num'}).text
            if td_num == 'AD':
                continue
            href = bs_tr.find('td', {'class': 'list-subject'}).find('a')['href']
            # 상세 페이지 이동
            bs_content = get_bs(href)
            if bs_content is None:
                continue

            title = bs_content.find('div', {'class': 'view-wrap'}).find('h1').text
            a_tags = bs_content.findAll('a', {'class': 'view_file_download'})
            for a_tag in a_tags:
                m = re.search('(magnet:\?xt=urn:btih:.+?)&', a_tag['href'])
                if m is not None:
                    magnet = m.group(1)
                    break

            # print(title)
            saved, obj = save_data(title, magnet, href, category)
            if saved is None:
                break
            result.append(obj)

    return result


def save_data(title, magnet, url, category):
    saved = None

    try:
        print("[save_data]", title, magnet, url, category)
    except:
        pass

    try:
        obj = Magnet.objects.get(url=url)
        # obj = Magnet.objects.get(magnet=magnet)
    except Magnet.DoesNotExist:
        obj = Magnet(title=title, magnet=magnet, url=url, category=category)
        obj.save()
        saved = True
    except Magnet.MultipleObjectsReturned:
        obj = Magnet.objects.filter(magnet=magnet)[0]

    return saved, obj

