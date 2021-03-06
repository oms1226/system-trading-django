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
    print(escape(magnet.title))
    # title = urlencode(magnet.title)
    title = quote(magnet.title)
    response['Content-Disposition'] = 'attachment; filename=' + title
    response.write(magnet.magnet)
    return response

    # return HttpResponse(magnet.magnet, content_type="text/plain")


def rss(request):
    latest_magnet_list = Magnet.objects.order_by('-reg_date')[:100]

    # 출처 : https://github.com/lkiesow/python-feedgen
    # fg = FeedGenerator()
    # fg.id('http://lernfunk.de/media/654321')
    # fg.title('RSS')
    # fg.author({'name': 'John Doe', 'email': 'john@example.de'})
    # fg.link(href='http://example.com', rel='alternate')
    # fg.logo('http://ex.com/logo.jpg')
    # fg.subtitle('This is a cool feed!')
    # fg.link(href='http://larskiesow.de/test.atom', rel='self')
    #
    # for magnet in latest_magnet_list:
    #     fe = fg.add_entry()
    #     fe.id(magnet.url)
    #     fe.title(magnet.title)
    #     fe.link(link={'href': magnet.magnet})
    #
    # rss = fg.rss_str(pretty=True)
    # print(rss)
    # return HttpResponse(rss)

    rss_content = '<?xml version="1.0" encoding="UTF-8"?>'+\
        '<rss version = "2.0">'+\
        '<channel>'+\
        '<title>RSS</title>'+ \
        '<link>http://jace.diskstation.me:9000</link>' +\
        '<description>RSS</description>'

    for magnet in latest_magnet_list:
        rss_content += '<item>'
        rss_content += '<title>' + magnet.title + '</title>'
        rss_content += '<link>' + magnet.magnet + '</link>'
        rss_content += '</item>'

    rss_content += '</channel></rss>'

    # titles = ''
    # for magnet in latest_magnet_list:
    #     titles += magnet.title
    #
    # return HttpResponse(titles)

    return HttpResponse(rss_content)


def collect_tfreeca():
    url_home = 'http://www.tfreeca2.com/'
    url_ref_map = {
        'movie': 'board.php?mode=list&b_id=tmovie'
    }

    result = list()

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
    # result = collect_tfreeca()
    result = collect_torrenters()
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
