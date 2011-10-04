# vim: set tw=0 fileencoding=utf-8:

from datetime import datetime
from xml.sax.saxutils import escape
import Image
import binascii
import clevercss
import glob
import mimetypes
import os.path
import re
import shutil
import sys
import urllib
import urlparse

import poolemonkey

poolemonkey.init(globals())

page = { 'title': 'untitled page' }

# Заголовки меток
tagtitles = {
    'articles': u'статьи',
    'concerts': u'отчёты',
    'interviews': u'интервью',
    'knowledge': u'ликбез',
    'podcasts': u'подкасты',
    'news': u'новости',
    'reviews': u'рецензии',
}

def get_post_labels(post):
    if not post.has_key('labels'):
        labels = []
    else:
        labels = [l.strip() for l in post['labels'].split(',')]
    if post.has_key('file') and 'podcasts' not in labels and post['file'].endswith('.mp3'):
        labels.append('podcasts')
    if post.url.startswith('blog.') and post.url != 'blog.html' and 'blog' not in labels:
        labels.append('blog')
    if is_news_page(post):
        labels.append('news')
    return sorted(labels)


def get_label_url(label):
    return '/' + label.strip().replace(' ', '_') + '/index.html'


def get_label_text(label):
    if tagtitles.has_key(label):
        return tagtitles[label]
    return label


def get_label_stats(posts):
    labels = {}
    for post in posts:
        for label in get_post_labels(post):
            if not labels.has_key(label):
                labels[label] = 1
            else:
                labels[label] += 1
    # Удаляем метки, для которых нет страниц.
    for label in labels.keys():
        if not os.path.exists('./input' + os.path.splitext(get_label_url(label))[0] + '.md'):
            del labels[label]
    return labels


def get_tag_cloud(posts):
    """
    Выводит список меток со ссылками на страницы.  Метки, для которых нет
    страниц, не выводятся.  Если меток меньше двух — ничего не выводится.
    """
    labels = get_label_stats(posts)
    if len(labels) < 2:
        return u''
    output = u'<div id="tcloud"><h2>Разделы</h2><ul>'
    for label in sorted(labels.keys()):
        text = label
        if tagtitles.has_key(text):
            text = tagtitles[text]
        output += u'<li><a href="%s">%s</a> (%u)</li>' % (shorturl(get_label_url(label)), text, labels[label])
    output += u'</ul>'
    output += u'<p class="sub">Можно <a href="http://feedburner.google.com/fb/a/mailverify?uri=deadchannel/exclusive&amp;loc=ru_RU">получать обновления по электронной почте</a>.</p>'
    output += u'</div>'
    return output


def is_news_page(page):
    if not page.url.startswith('news/'):
        return False
    if page.url.startswith('news/index.'):
        return False
    return True


def page_classes(page):
    """
    Возвращает строку с классами CSS для поста.
    """
    classes = [label for label in get_post_labels(page)]
    if page['url'] == 'movies.html':
        classes.append('movies')
    if classes:
        return u' class="%s"' % u' '.join(classes)
    return u''


def filterpages(pages, limit, label):
    pages = [page for page in pages if 'date' in page]
    if label is not None:
        pages = [page for page in pages if page.has_key('labels') and label in get_post_labels(page)]
    if label != 'news':
        pages = [page for page in pages if not is_news_page(page)]
    pages = sorted(pages, key=lambda p: p.get('date'), reverse=True)
    if limit:
        pages = pages[:limit]
    return pages

def pagelist(pages, limit=5, label=None, show_dates=True):
    output = u''
    for page in filterpages(pages, limit, label):
        output += u'  * '
        if limit is None and show_dates:
            date = datetime.strptime(page.date, '%Y-%m-%d').strftime('%d.%m.%Y')
            output += u'<span>%s</span> : ' % date
        output += u'[%s](%s)\n' % (page.get('post', page.get('title')), shorturl(page.get('url')))
    if output:
        return output
    return u'Ничего нет.'


def pagelist2(pages, limit=None, label=None, show_dates=True):
    output = u''
    for page in filterpages(pages, limit, label):
        date = u'<span class="date">%s </span>' % datetime.strptime(page.date, '%Y-%m-%d').strftime('%d.%m.%y')
        if not show_dates:
            date = u''
        output += u'<li><p>%(date)s<a href="%(url)s">%(title)s</a></p>' % {
            'title': page.get('title'),
            'url': shorturl(page.get('url')),
            'date': date,
        }
        if page.get('summary'):
            output += u'<p class="summary">%s</p>' % page.get('summary')
        output += u'</li>\n'
    if not output:
        return u'Ничего нет.'
    return u'<ul class="pagelist">' + output + u'</ul>'


def newslist(pages):
    output = u''
    news = sorted([page for page in pages if is_news_page(page)], key=lambda p: p.url, reverse=True)
    for page in news:
        textra = u''
        output += u'<li><p><a href="%(url)s">%(title)s</a></p>' % {
            'title': page.get('title'),
            'url': page.get('link'),
        }

        if page.get('summary'):
            output += u'<p class="summary">%s</p>' % page.get('summary')

        links = get_news_links(page)
        if links:
            output += links

        image = get_news_picture(page)
        if image:
            output += u'<a href="%s">%s</a>' % (page.get('link'), image)

        output += u'</li>'
    if not output:
        return u'Ничего нет.'
    return u'<ul class="pagelist news">' + output + u'</ul>'


def get_news_picture(page):
    if not page.get('image'):
        return ''
    filename = os.path.splitext(page.get('url'))[0] + '.jpg'
    realname = os.path.join('input', filename)
    if not os.path.exists(realname):
        print 'Downloading %s' % page.get('image')
        tmpname = urllib.urlretrieve(page.get('image'))[0]
        img = Image.open(tmpname)

        # wide image
        if img.size[0] >  img.size[1]:
            img.thumbnail((700, 50), Image.ANTIALIAS)
            width = img.size[0]
            if width > 70:
                shift = (width - 70) / 2
                img = img.crop((shift, 0, shift + 70, 50))

        # tall image
        else:
            img.thumbnail((70, 700), Image.ANTIALIAS)
            height = img.size[1]
            if height > 50:
                shift = (height - 50) / 2
                img = img.crop((0, shift, 70, shift + 50))

        img.save(realname)
        # Файл только что создан, копировать его poole не будет.  Делаем это сами.
        shutil.copyfile(realname, os.path.join('output', filename))
        print 'Saved as %s' % realname

    box = Image.open(realname).size
    return '<img src="%s" width="%u" height="%u" alt="illustration"/>' % (filename, box[0], box[1])


def get_news_links(page):
    parts = []
    parts.append(u'<a href="%s#disqus_thread">комментировать</a>' % page.get('url'))
    if page.get('file'):
        parts.append(u'<a href="%s">скачать</a>' % page.get('file'))
    if page.get('lang', 'ru') != 'ru':
        parts.append(u'<a href="http://translate.google.com/translate?sl=%s&amp;tl=ru&amp;u=%s">перевести на русский</a>' % (page.get('lang'), urllib.quote(page.get('link'))))
    if parts:
        return u'<p class="links">' + u' '.join(parts) + u'</p>'
    return ''


def page_hlink(page):
    """
    if page.url.startswith('news/index.'):
        return ' <small>прислать новость</small>'
    """
    return ''


def get_movie_score(page):
    """
    Возвращает сумму баллов для фильма.
    """
    if not 'movie-score' in page:
        return 0
    return sum([int(x) for x in page['movie-score'].split('+') if x])


def movies():
    """
    Выводит таблицу с информацией о фильмах.
    """
    output = u'<table class="movies"><thead><tr><th>Название</th><th>Title</th><th>Год</th><th>Оценка</th></tr></thead><tbody>'
    for page in sorted(pages, key=lambda p: p.get('movie-title-ru')):
        if 'movies' in get_post_labels(page):
            for k in ('movie-title-ru', 'movie-title-en', 'movie-year', 'movie-score'):
                if k not in page:
                    page[k] = ''
            output += u'<tr><td><a href="%s">%s</a></td><td>%s</td><td>%s</td><td>%u</td></tr>' % (page.url, page['movie-title-ru'], page['movie-title-en'], page['movie-year'], get_movie_score(page))
    output += u'</tbody></table>'
    return output


def movie_info(page):
    output = u'<table class="info"><tbody>'
    if 'movie-title-ru' in page:
        output += u'<tr><th>Русское название</th><td>%s</td></tr>' % (escape(page['movie-title-ru']))
    if 'movie-title-en' in page:
        output += u'<tr><th>Оригинальное название</th><td>%s</td></tr>' % (escape(page['movie-title-en']))
    if 'movie-year' in page:
        output += u'<tr><th>Год выхода</th><td>%s</td></tr>' % (escape(page['movie-year']))
    if 'movie-score' in page:
        output += u'<tr><th><a href="/movies.html#080c16a5" title="Описание системы оценок (форма+содержание+подача[+желание пересмотреть])">Оценка</a></th><td>%s = %u</td></tr>' % (escape(page['movie-score']), get_movie_score(page))
    output += u'</tbody></table>'
    return output


def page_title(page, h='h2'):
    """Выводит заголовок страницы, если он есть."""
    title = page.get('post', page.get('title'))
    if title:
        return u'<%s>%s</%s>' % (h, page.get('post', page.get('title')), h)
    return u''


def youtube(video_id):
    # высота: 300 + 35 на контролы
    return u'<iframe class="youtube-player" type="text/html" ' + \
        u'width="540" height="335" ' + \
        u'src="http://www.youtube.com/embed/' + unicode(video_id) + \
        u'" frameborder="0"></iframe>'


def hook_preconvert_sources():
    """
    Добавляет в конец страницы ссылку на первоисточник, если он есть.
    """
    for page in pages:
        if 'source' in page:
            page.source += u'\n\n_Этот материал раньше находился [по другому адресу](%s), там могут быть комментарии._' % page['source']


def hook_preconvert_news():
    for page in pages:
        if is_news_page(page):
            filename = os.path.splitext(page.url)[0] + '.jpg'
            realname = os.path.join('input', filename)
            if os.path.exists(realname):
                page.source += u'\n\n<a title="Открыть новость" href="%s"><img class="illustration" src="%s" alt="illustration"/></a>' % (page.get('link'), page.get('image'))
            date = datetime.strptime(page.url[5:13], '%Y%m%d')
            page['date'] = date.strftime('%Y-%m-%d')


def hook_preconvert_typo():
    """
    Улучшение типографики.
    """
    for page in pages:
        text = page.source
        text = re.sub(u' —', u'&nbsp;—', text)
        text = re.sub(u'\.  ', u'.&nbsp; ', text)
        text = re.sub(u'  +', u'&nbsp; ', text)
        page.source = text


def hook_preconvert_ccss():
    """
    Обработка CleverCSS.  Файлы с расширением .ccss конвертируются в .css.
    """
    for ccss in glob.glob(os.path.join(input, "**.ccss")):
        css = ccss[len(input):].lstrip("/")
        css = "%s.css" % os.path.splitext(css)[0]
        css = os.path.join(output, css)
        fpi = open(ccss)
        fpo = open(css, 'w')
        fpo.write(clevercss.convert(fpi.read()))
        fpi.close()
        fpo.close()


def DISABLED_hook_postconvert_fix_toc():
    """
    Добавление оглавлений.
    """
    #for idx in range(0, len(pages)):
    #    pages[idx].html = mktoc(pages[idx].html)
    for page in pages:
        page.html = mktoc(page.html)

def mktoc(text):
    toc = ''
    r = re.compile('<h\d>(.*)</h\d>')
    m = r.search(text)
    while m:
        ref = '%08x' % (binascii.crc32(m.group(1).encode('utf-8')) & 0xffffffff)
        toc += '<li><a href="#%s">%s</a></li>' % (ref, m.group(1))
        text = text.replace(m.group(0), u'<h3 class="section_header" id="%s">%s <a name="%s" href="#%s" class="section_anchor">¶</a></h3>' % (ref, m.group(1), ref, ref))
        m = r.search(text)
    if len(toc):
        text = text.replace('[TOC]', '<ul id="toc">%s</ul>' % toc)
    return text

def embed(page):
    if "file" not in page:
        return ""
    if not page["file"].endswith(".mp3"):
        return ""

    if "illustration" not in page:
        furl = urllib.quote(page.file)
        return '<object type="application/x-shockwave-flash" data="/files/player.swf" width="200" height="20"><param name="movie" value="/files/player.swf"/><param name="bgcolor" value="#eeeeee"/><param name="FlashVars" value="mp3=%s&amp;buttoncolor=000000&amp;slidercolor=000000&amp;loadingcolor=808080"/></object>' % escape(page.file)

    parts = (page.get("illustration") + " 400 300").split(" ")

    return file("player.html", "rb").read().decode("utf-8") % {
        "illustration": parts[0],
        "width": parts[1],
        "height": parts[2],
        "podcast": page["file"],
        "description": page["title"],
        "author": "hex",
        "duration": page.get("duration"),
    }

def comments(page):
    if 'labels' in page or is_news_page(page):
        settings = ''
        if page.has_key('disqus_url'):
            settings += 'var disqus_url = "'+ page['disqus_url'] +'";'
        else:
            settings += 'var disqus_identifier = "'+ page.url +'";'
        return u'<div id="cwrapper"><div id="disqus_thread"></div><script type="text/javascript">if (window.location.href.indexOf("http://localhost:") == 0) var disqus_developer = 1;'+ settings +' (function() { var dsq = document.createElement(\'script\'); dsq.type = \'text/javascript\'; dsq.async = true; dsq.src = \'http://deadchannel.disqus.com/embed.js\'; (document.getElementsByTagName(\'head\')[0] || document.getElementsByTagName(\'body\')[0]).appendChild(dsq); })();</script><noscript><div>Please enable JavaScript to view the <a href="http://disqus.com/?ref_noscript=deadchannel">comments powered by Disqus.</a></div></noscript></div>'
    if page.get('comments'):
        return u'<script type="text/javascript">var disqus_shortname="deadchannel";(function(){var s=document.createElement("script");s.async=true;s.type="text/javascript";s.src="http://disqus.com/forums/"+disqus_shortname+"/count.js";(document.getElementsByTagName("HEAD")[0]||document.getElementsByTagName("BODY")[0]).appendChild(s);}());</script>'
    return ''

def title(page):
    t = 'Dead Channel'
    if 'post' in page and 'file' in page:
        t = '<a href="/podcast.html">' + t + ' podcast</a>'
    elif 'post' in page:
        t = '<a href="/blog.html">' + t + ' blog</a>'
    elif page.url != 'index.html':
        t = '<a href="/index.html">' + t + '</a>'
    return t


def shorturl(url):
    if url.endswith("index.html"):
        url = url[:-10]
    return url
