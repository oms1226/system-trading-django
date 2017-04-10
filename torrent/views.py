from __future__ import unicode_literals
from django.shortcuts import render
import re
import urllib.request
from urllib.parse import quote
from bs4 import BeautifulSoup
from django.utils.http import urlencode
from .models import Magnet
# from feedgen.feed import FeedGenerator
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.utils.html import escape

# Create your views here.

# https://www.tutorialspoint.com/django/django_rss.htm
class RssFeed(Feed):
    title = "Dreamreal's comments"
    link = "/drcomments/"
    description = "Updates on new comments on Dreamreal entry."

    def items(self):
        return Magnet.objects.order_by('-reg_date')[:100]

    def item_title(self, item):
        return item.title

    # def item_description(self, item):
    #     return item.comment

    def item_link(self, item):
        return reverse('torrent:item', kwargs={'item_id': item.id})
        # return reverse('item', args=[1795])
        # return '/' + str(item.id)
        # return item.magnet
        # return item.get_absolute_url()


def index(request):
    return render(request, 'torrent/index.html')


def item(request, item_id):
    magnet = Magnet.objects.get(id=item_id)
    response = HttpResponse(content_type='text/plain; charset=utf-8')
    # print(escape(magnet.title))
    title = magnet.title
    # title = urlencode(magnet.title)
    # title = quote(unicode(magnet.title))
    # title = unicode(magnet.title).encode('utf-8')
    # title = magnet.title.decode('utf-8')
    response['Content-Disposition'] = 'attachment; filename=' + '123.torrent'
    response.write(magnet.magnet)
    return response

    # return HttpResponse(magnet.magnet, content_type="text/plain")


def collect_tfreeca():
    url_home = 'http://www.tfreeca2.com/'
    url_ref_map = {
        'movie': 'board.php?mode=list&b_id=tmovie'
    }

    result = list()
    trackers= '&tr=udp://tracker.openbittorrent.com:80&tr=http://megapeer.org:6969/announce&tr=http://mgtracker.org:2710/announce&tr=http://tracker.files.fm:6969/announce&tr=http://tracker.flashtorrents.org:6969/announce&tr=http://tracker.mg64.net:6881/announce&tr=http://tracker.nwps.ws:6969/announce&tr=http://tracker.ohys.net/announce&tr=http://tracker.tfile.me/announce&tr=udp://9.rarbg.com:2710/announce&tr=udp://9.rarbg.me:2710/announce&tr=udp://coppersurfer.tk:6969/announce&tr=udp://tracker.coppersurfer.tk:6969&tr=udp://tracker.leechers-paradise.org:6969&tr=udp://exodus.desync.com:6969/announce&tr=udp://open.coppersurfer.com:1337/announce'

    for category, url_ref in url_ref_map.items():
        bs = get_bs(url_home, url_ref)
        bs_trs = bs.find('table', {'class': 'b_list'}).findAll('tr')

        for bs_tr in bs_trs:
            if 'class' in bs_tr.attrs:
                tr_class = bs_tr.attrs['class'][0]
                if tr_class == 'nbgcolor':
                    continue
            href = bs_tr.find("a", {"class": re.compile(r'title')})['href']
            bs_content = get_bs(url_home, href)
            # 제목찾기
            title = bs_content.find('td', {'class': 'view_t2'})['title']
            # 마그넷 찾기
            torrent_src = bs_content.find('iframe', {'id': 'external-frame'})['src']
            bs_torrent = get_bs(url_home, torrent_src)
            magnet = bs_torrent.find('div', {'class': 'torrent_magnet'}).find('a')['href']
            magnet += '&dn=' + title + trackers
            # return render(request, 'torrent/collect.html', {'result': bs.prettify()})
            magnet, created = Magnet.objects.get_or_create(title=title, magnet=magnet, url=url_home + href,
                                                           category=category)
            if created:
                print(title, " added")
                result.append(magnet)
            else:
                print(title, " exist")

    return result


def collect(request, site='all'):
    result = collect_tfreeca()
    # result = collect_torrenters()
    return render(request, 'torrent/collect.html', {'result': result})


def get_bs(url_home, url_ref):
    url = url_home + url_ref
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read()
    bs = BeautifulSoup(html, 'lxml', from_encoding='utf-8')
    return bs


def collect_torrenters():
    url_home = 'http://torrentersg.com/bbs/'
    url_ref_map = {
        'tv': 'board.php?bo_table=tr_pbtv'
        , 'tv': 'board.php?bo_table=tr_ftv'
        , 'movie': 'board.php?bo_table=tr_kmovie'
        , 'movie': 'board.php?bo_table=tr_fmovie'
    }

    result = list()

    for category, url_ref in url_ref_map.items():
        bs = get_bs(url_home, url_ref)
        bs_trs = bs.find('table', {'id': 'tbl_board'}).findAll('tr')

        for bs_tr in bs_trs:
            if 'class' in bs_tr.attrs:
                tr_class = bs_tr.attrs['class'][0]
                if tr_class != 'bg0' and tr_class != 'bg1':
                    continue
            href = bs_tr.find('a')['href']
            
            # 상세 페이지 이동
            bs_content = get_bs(url_home, href)
            file_links = bs_content.findAll('li', {'class': 'file_link'})
            alink = file_links[1].find('a')
            title = alink['title']
            href_js = alink['href']
            m = re.search('javascript:dnload\(\'(.*?)\'', href_js)
            href = m.group(1)
            magnet, created = Magnet.objects.get_or_create(title=title, url=url_home + href, category=category)
            if created:
                print(title, " added")
                result.append(magnet)
            else:
                print(title, " exist")

            url = url_home + href
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            html = urllib.request.urlopen(req).read()
            bs = BeautifulSoup(html, 'lxml', from_encoding='utf-8')

    return result
