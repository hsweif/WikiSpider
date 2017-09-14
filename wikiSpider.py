import urllib
import urllib2
import chardet
import time
import re
import sys
from urllib2 import Request, urlopen, URLError, HTTPError
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding("utf-8")

class WikiSpider:
    def __init__(self):
        self.__headers = ('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64)')
        self.__opener = urllib2.build_opener()
        self.__opener.addheaders = [self.__headers]
        self.count = 0
        self.url_list = []
        self.content = '' 
    def openURL(self, url):
        #req = Request(url)
        #req.add_header('user-agent', 'fake-client')
        #response = urllib2.urlopen(req)
        #content = response.read()
        self.content = self.__opener.open(url).read()
        encoding = chardet.detect(self.content)['encoding']
        self.content = self.content.decode(encoding, 'ignore')
        #return content
    def addURL(self, url):
        self.url_list.append(url)
    def getInfo(self):
        soup = BeautifulSoup(self.content, "html.parser")
        info_list = str(soup.find_all('table', class_ = 'infobox biography vcard'))
        self.count = self.count + 1
        # Classify info:
        classfied_info = ''
        infobox_soup = BeautifulSoup(info_list, "html.parser")
        for item in infobox_soup.find_all('tr'):
            #print item.get_text()
            if item.th != None :
                print item.th.string
            for i in item.find_all('td'):
                print i.get_text()
                
                    
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
            #print block_info


        #row_list = str(re.findall('<th\s*scope\s*=\s*"row">([^<]*)', info_list))
        #name = 'Name: '
        #name += str(re.findall('<span\s*class\s*=\s*"fn">([^<]*)', info_list))
        #name += '\n'
        #classfied_info += name
        #description = 'Descrption: '
        #description += str(re.findall('<div>\s*([^<]*)', info_list))
        #description += '\n'
        #classfied_info += description
        #birth_info = 'Birthday: '
        #birth_info += str(re.findall('<span\s*class\s*=\s*"bday">([^<]*)', info_list))
        #birth_info += '\nBirthPlace: '
        #birth_info += str(re.findall('<span\s*class\s*=\s*"birthplace">[^>]*>*([^<]*)', info_list))
        #classfied_info += birth_info
        #print classfied_info 


        #print info_list
        #with open('record.txt', "r+")as f:
        #    num = int(f.read())
        #    print num 
        #file_name = str(num)
        #file_name += '.html'
        #num = num + 1
        #tmp = str(num)
        #with open('record.txt', "w")as f:
        #    f.write(tmp)
        #with open(file_name, "w")as f:
        #    f.write(str(info_list))
    def getNextURL(self):
        #soup = BeautifulSoup(content, "html.parser") 
        #url_list = soup.find_all('a', href = re.compile("(wiki/Category:){1}"))
        original_list = re.findall('<a\s*href\s*="(/wiki[^"]*)"', self.content) 
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
            if self.count > 1:
                break
            else :
                self.openURL(url)
                if self.isInfoPage(url):  
                    print 'Own info:', url
                    self.getInfo()
                    self.url_list.remove(url)
                else :
                    print 'No info:', url
                    self.getNextURL()               
    
spider = WikiSpider()
#spider.addURL('https://en.wikipedia.org/wiki/Category:20th-century_American_engineers')
spider.addURL('https://en.wikipedia.org/wiki/Category:21st-century_American_actresses')
spider.furtherSearch()

#Match test
#url = 'https://en.wikipedia.org/wiki/Alan_Turing' 
#req = Request(url)
#req.add_header('user-agent', 'fake-client')
#response = urllib2.urlopen(req)
#content = response.read()
#pattern = re.compile('<table\s*class\s*=\s*"infobox biography vcard"\s*[^>]*')
#pattern = re.compile('<a\s*href\s*="(/wiki[^"]*)"', re.M) 
#match = pattern.search(content)
#if match:
#    print 'success'
#else:
#    print 'fail'


#web_content = spider.openURL('https://en.wikipedia.org/wiki/Alan_Turing')
#spider.getInfo(web_content)
#url_list = spider.getNextURL(web_content)
#for item in url_list:
#    print item
