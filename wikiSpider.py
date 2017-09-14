import urllib
import urllib2
import chardet
import time
import re
import sys
import os
from urllib2 import Request, urlopen, URLError, HTTPError
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding("utf-8")
#coding 

class WikiSpider:
    def __init__(self):
        self.__headers = ('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64)')
        self.__opener = urllib2.build_opener()
        self.__opener.addheaders = [self.__headers]
        self.count = 0
        self.url_list = []
        self.url_set = set([])
        self.content = '' 
    def openURL(self, url):
        #req = Request(url)
        #req.add_header('user-agent', 'fake-client')
        #response = urllib2.urlopen(req)
        #content = response.read()
        self.content = self.__opener.open(url).read()
        #encoding = chardet.detect(self.content)['encoding']
        #self.content = self.content.decode(encoding, 'ignore')
        #return content
    def addURL(self, url):
        self.url_list.append(url)
    def getInfo(self):
        path = os.path.abspath(".")
        path += '/Data/'
        with open('record.txt', "r+")as rc:
            num = int(rc.read())
        file_name = str(num)
        file_name += '.html'
        with open(path + file_name, "w")as f:
            soup = BeautifulSoup(self.content, "html.parser")
            info_list = str(soup.find_all('table', class_ = 'infobox biography vcard'))
            self.count = self.count + 1
            # Classify info:
            #f.write('<h1>'+'Name:' + '</h1>')
            infobox_soup = BeautifulSoup(info_list, "html.parser")
            photo_num = 1 
            for item in infobox_soup.find_all('tr'):
                #print item.get_text()
                image = item.find_all('a', class_ = 'image')
                for i in image:
                    #image_url = 'https:' 
                    if i != None : 
                        image_url = i.img['src']
                        urllib.urlretrieve('https:' + image_url, path+'Photo/'+str(num)+'_'+str(photo_num)+'.jpg')
                        photo_num = photo_num + 1
                        f.write('Image Path:' + image_url + '\n')
                if item.th != None :
                    #print item.th.string
                    f.write('#' + item.th.string + '\n')
                    #classfied_info += item.th.string
                for i in item.find_all('td'):
                    tmp = i.get_text()
                    if tmp.find(r'\n') != -1:
                        tmp = tmp.replace(r'\n', r'|')
                        tmp = tmp.replace(u'\xa0', u' ')
                        k = 0
                        while tmp[k] == '|':
                            k = k + 1
                        else :
                            t = tmp[0:k].replace(r'|', r'')
                            tt = tmp[-k:].replace(r'|', r'')
                            tmp = t + tmp[k:-k] + tt
                        f.write(tmp + '\n')
                f.write('\n')
                    #classfied_info = classfied_info + '    ' + i.get_text()
        num = num + 1
        tmp = str(num)
        with open('record.txt', "w")as rc:
            rc.write(tmp)

        #row_list = row_soup.find_all('th', scope = 'row')
        #block_list = infobox_soup.find_all('tr')
        #for block in block_list:
        #    block_info = str(re.findall('<th\s*scope\s*=\s*"row">([^<]*)', str(block)))
        #    block_info += ': '
        #    block_soup = BeautifulSoup(str(block), "html.parser")
        #    li_list = block_soup.find_all('li')
        #    if li_list:
        #        pass
        #        #print li_list
        #    else :
        #        td_list = block_soup.find_all('td')
        #        for td in td_list:
        #            td_soup = BeautifulSoup(str(td), "html.parser")
        #            for paragraph in td_soup.children:
        #                #print paragraph
        #                #noun_list = re.findall('<a\s*href\s*=\s*[^>]*([^<]*)|<span\s*class\s*=\s*[^>]*([^<]*)', str(paragraph))
        #                noun_list = re.findall('<a\s*href\s*=\s*[^>]*>([^<]*)|<span\s*class\s*=\s*[^>]*>([^<]*)|/a>"([^"]*)"', str(paragraph))
        #                for noun in noun_list:
        #                    print noun
                        #para_soup = BeautifulSoup(str(paragraph), "html.parser") 
                        #paraURL_list = para_soup.find_all('a')
                        #if len(paraURL_list): #some links in this para
                        #    noun_list = re.findall('<a\s*href\s*=\s*[^>]*([^<]*)', str(paragraph))
                        #    #print noun_list
                        #    for noun in noun_list:
                        #        block_info += noun
                        #    #print paraURL_list
                        #else :
                        #    noun_list = re.findall('<span\s*class\s*=\s*"[^<]*>([^<]*)', str(paragraph))
                        #    for noun in noun_list:
                        #        print 'noparaURL'
                        #        block_info += noun

                        #print child
    def getNextURL(self):
        #soup = BeautifulSoup(content, "html.parser") 
        #url_list = soup.find_all('a', href = re.compile("(wiki/Category:){1}"))
        original_list = re.findall('<a\s*href\s*="(/wiki[^"]*)"', self.content) 
        page_list = re.findall('<a\s*href\s*=\s*"(/w/index.php[^"]*)"[^>]*>next page</a>', self.content)
        for url in page_list:
            tmp = 'https://en.wikipedia.org' 
            tmp += url
            #print tmp
            self.url_list.append(tmp)
        for url in original_list:
            tmp = 'https://en.wikipedia.org' 
            tmp += url
            #print tmp
            self.url_list.append(tmp)
    def isInfoPage(self, url):
        pattern = re.compile('<table\s*class\s*=\s*"infobox biography vcard"\s*[^>]*')
        match = pattern.search(self.content)
        if match:
            return True
        else:
            return False
    def furtherSearch(self):
        for url in self.url_list:
            if self.count > 20:
                break
            elif url not in self.url_set:
                self.openURL(url)
                self.url_set.add(url)
                if self.isInfoPage(url):  
                    print 'Got info, no.', self.count, ' ', url
                    self.getInfo()
                    self.url_list.remove(url)
                else :
                    self.getNextURL()               
    
spider = WikiSpider()
spider.addURL('https://en.wikipedia.org/wiki/Category:21st-century_American_singers')
spider.addURL('https://en.wikipedia.org/wiki/Category:21st-century_American_male_actors')
spider.addURL('https://en.wikipedia.org/wiki/Category:21st-century_American_actresses')
spider.addURL('https://en.wikipedia.org/wiki/Category:20th-century_American_businesspeople')
spider.addURL('https://en.wikipedia.org/wiki/Category:African-American_basketball_players')


spider.furtherSearch()
print os.path.abspath(".")
