import re
import codecs
import os
class Dealer:
    def __init__(self):
        self.content = ''
        self.path = ''
        self.dict = {}
        self.numberlist = {}
        self.birthlist = {}
    def transCode(self, mystr):
        re.sub(r'[^\x00-\x7F]+','',mystr).decode('utf-8','ignore').strip()
    def updateKeyMap(self, filename, fileID):
        beginflag = True 
        for line in codecs.open(filename, 'r', 'utf-8'):
            #re.sub(r'[^\x00-\x7F]+','',line).decode('utf-8','ignore').strip()
            #line = line.replace(u'\xa0', u' ')
            #line = line.replace(u'\u2013', u'-')
            if beginflag:
                tmp = []
                tmp.append(fileID)
                name = line[1:]
                self.dict[name] = tmp 
                for i in name.split(' '):
                    if self.dict.has_key(i):
                        tmp = self.dict[i]
                        tmp.append(fileID)
                        self.dict[i] = tmp
                    else :
                        tmp = []
                        tmp.append(fileID)
                        self.dict[i] = tmp
                beginflag = False
            elif line[0] == '#':
                head = '<h2>' + line[1:] + '</h2>'
            elif line.find('|') != -1 :
                for i in line.split('|'):
                    if self.dict.has_key(i):
                        tmp = self.dict[i]
                        tmp.append(fileID)
                        self.dict[i] = tmp
                    else :
                        tmp = []
                        tmp.append(fileID)
                        self.dict[i] = tmp  
                pass
            elif line.find('Image Path:') != -1:
                for item in re.findall('Image Path:([^$]*)', line):
                    #print item
                    url = 'http:' + item
                    imgtag = '<img src=\"' + url +'\"/>' + '<br/>'
                    self.content += imgtag
            else :
                self.content += line 
    def writeFile(self):
        with codecs.open('keymap.txt', 'w', 'utf-8')as f:
            key_list = self.dict.keys()
            for key in key_list:
                #print 'key:',key
                tmpstr = key.strip('\n') + ':'
                for item in self.dict[key]:
                    tmpstr = tmpstr + str(item) + ',' 
                tmpstr = tmpstr[:-1]
                #print 'line:', tmpstr
                f.write(tmpstr + '\n')
    def makeNumberlist(self, filename, fileID):
        with open(filename, 'r')as f:
            line = f.readline()
            line = line[1:]
            self.numberlist[fileID] = line
    def writeNumberlist(self): 
        with codecs.open('numberlist.txt', 'w')as f:
            for item in self.numberlist:
                line = str(item) + ':' + self.numberlist[item]
                f.write(line)
    def makeBirthdayList(self, filename, fileID):
        flag = False
        for line in open(filename, 'r'):
            line = line.strip('\n')
            if flag:
                for item in re.findall('([0-9]*-[0-9]*-[0-9]*)', line):
                    if self.birthlist.has_key(item):
                        tmp = self.birthlist[item]
                        tmp.append(fileID)
                        self.birthlist[item] = tmp
                    else :
                        tmp = []
                        tmp.append(fileID)
                        self.birthlist[item] = tmp
                break
            if line == '#Born':
                flag = True
    def writeBirthdayList(self):
        with codecs.open('birthlist.txt', 'w')as f:
            for item in self.birthlist:
                line = str(item) + ':'
                for num in self.birthlist[item]:
                    line = line + str(num) + ','
                f.write(line + '\n')
    def loadKeyMap(self):
        path = os.path.abspath('.') + '/keymap.txt'
        #path = os.path.abspath('.') + '/Server/keymap.txt'
        for line in open(path, 'r'):
            line = line.strip('\n')
            if line.find(':') != -1:
                part = line.split(':')
                value_list = part[1].split(',')
                for value in value_list:
                    value = value.replace('\n', '')
                    #print value
                self.dict[part[0]] = value_list 
                #print self.dict[part[0]]
    def findKey(self, key):
        self.loadKeyMap()
        if self.dict.has_key(key):
            return self.dict[key]
        else :
            tmp = []
            return tmp


#path = '1.html'
mydealer = Dealer()
k = 1
while (k < 10500):
    print 'Dealing with:', k
    path = os.path.abspath('.') + '/Data/' + str(k) +'.html'
    #mydealer.makeNumberlist(path, k)
    mydealer.makeBirthdayList(path, k)
   #mydealer.loadKeyMap()
   #mydealer.updateKeyMap(path, k)
   #mydealer.writeFile()
    k = k + 1
mydealer.writeBirthdayList()
#mydealer.writeNumberlist()
#mydealer.writeFile()
