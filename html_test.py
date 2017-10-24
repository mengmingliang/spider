#! /usr/bin/env python
from html.parser import HTMLParser
from html.entities import name2codepoint
import urllib.request

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.in_h3 = False
        self.in_time = False
        self.in_span = False
        self._event_title = []
        self._event_time = []
        self._event_location = []

    def _get_attr(self,attrlist, attrname):
        for attr in attrlist:
            if attr[0] == attrname:
                return attr[1]
        return None

    def handle_result(self):
        result = ''
        for i in range(len(self._event_title)):
            result = result + 'envent name:%s\n'%self._event_title[i]
            result = result + 'envent time:2017 %s\n' % self._event_time[i]
            result = result + 'envent location:%s\n\n' % self._event_location[i]
        return result.encode('utf-8')

    def handle_starttag(self, tag, attrs):
        #we will dispath the title
        if tag == 'h3' and self._get_attr(attrs,'class') == 'event-title':
            self.in_h3 = True
        if tag == 'time':
            self.in_time = True
        if tag == 'span' and self._get_attr(attrs,'class') == 'event-location':
            self.in_span = True

    def handle_endtag(self, tag):
        self.in_h3 = False
        self.in_time = False
        self.in_span = False

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_data(self, data):
        if self.in_h3 == True and self.lasttag == 'a':
            self._event_title.append(data)
        if self.in_time == True and self.lasttag == 'time':
            self._event_time.append(data)
        if self.in_span == True and self.lasttag == 'span':
            self._event_location.append(data)

    def handle_comment(self, data):
        pass

    def handle_entityref(self, name):
        pass

    def handle_charref(self, name):
        pass

def get_html(url):
    html = urllib.request.urlopen(url).read()
    return html

def save_html(file_name, file_content):
    #    注意windows文件命名的禁用符，比如 /
    with open(file_name.replace('/', '_') + ".html", "wb") as f:
        #   写文件用bytes而不是str，所以要转码
        f.write(file_content)

def read_html(file_name):
    with open(file_name,'r') as f:
        return f.read()

html = get_html("https://www.python.org/events/python-events/")
save_html("python", html)

parser = MyHTMLParser()
parser.feed(read_html("python.html"))
save_html("event",parser.handle_result())
