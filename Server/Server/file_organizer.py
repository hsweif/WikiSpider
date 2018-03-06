import re
import codecs
import os
# -- coding: UTF-8 -- 
class Dealer:
    def __init__(self):
        self.content = ''
        self.path = ''
        self.dict = {}
    def updateKeyMap(self, filename, fileID):
        beginflag = True 
        for line in codecs.open(filename, 'r', 'utf-8'):
            if beginflag:
                tmp = []
                tmp.append(fileID)
                self.dict[line[1:]] = tmp 
                for i in line.split(' '):
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
            else :
                self.content += line 
    def writeMap(self):
        with codecs.open('keymap.txt', 'w', 'utf-8')as f:
            key_list = self.dict.keys()
            for key in key_list:
                print 'key:',key
                tmpstr = key.strip('\n') + ':'
                for item in self.dict[key]:
                    tmpstr = tmpstr + str(item) + ',' 
                tmpstr = tmpstr[:-1]
                print 'line:', tmpstr
                f.write(tmpstr + '\n')
    def loadKeyMap(self):
        path = os.path.abspath('.') + '/keymap.txt'
        for line in open(path, 'r'):
            line = line.strip('\n')
            if line.find(':') != -1:
                part = line.split(':')
                value_list = part[1].split(',')
                self.dict[part[0]] = value_list 
    def findKey(self, key):
        self.loadKeyMap()
        answer_list = []
        for item in self.dict:
            if item.find(key) != -1:
                answer_list.extend(self.dict[item])
        #if self.dict.has_key(key):
        #    print self.dict[key]
        #    return self.dict[key]
        #else :
        #    tmp = []
        print answer_list
        return answer_list
    def findName(self, num):
        path = os.path.abspath('.') + '/numberlist.txt'
        for line in open(path, 'r'):
            line = line.replace(r'\xa0', r' ')
            line = line.replace(r'\u2013', r'-')
            line = line.replace(r'\u014', r'o')
            line = line.replace(r'\xe9', r'e')
            line = line.strip('\n')
            item = line.split(':')
            if item[0] == str(num):
                print item[0], item[1]
                return item[1]
    def loadFileInfo(self, fileID):
        path = os.path.abspath('..') + '/Data/' + str(fileID) +'.html'
        beginFlag = True 
        hashFlag = False
        photoFlag = True
        curKey = '' 
        response_list = []
        for line in open(path, 'r'):
            line = line.replace(r'\xa0', r' ')
            line = line.replace(r'\u2013', r'-')
            line = line.replace(r'\u2013', r'o')
            line = line.replace(r'\xe9', r'e')
            line = line.strip('\n')
            if line == '' :
                continue
            #print line
            if beginFlag:
                response = {}
                tmplist = []
                response['title'] = 'Name'
                tmplist.append(line[1:])
                response['descrption'] = tmplist 
                if response:
                    response_list.append(response)
                beginFlag = False
            elif curKey == 'imagedescrption':
                response[curKey] = line  
                if response:
                    response_list.append(response)
                curKey = ''
            elif hashFlag:
                noun_list = []
                if line.find('|') != -1:
                   noun_list = line.split('|') 
                else :
                    noun_list.append(line)
                response['descrption'] = noun_list 
                if response:
                    response_list.append(response)
                hashFlag = False 
            elif line[0] == '#':
                response = {}
                if line[1:]:
                    response['title'] = line[1:] 
                    hashFlag = True
            elif line.find('Image Path:') != -1:
                response = {}
                for item in re.findall('Image Path:([^$]*)', line):
                    url = 'https:' + item
                    response['image'] = url
                curKey = 'imagedescrption'
            #print response
        return response_list

#path = '1.html'
#mydealer = Dealer()
#mydealer.findKey('James')
#print mydealer.loadFileInfo(1)
#mydealer.loadKeyMap()
#mydealer.updateKeyMap(path, 1)
#mydealer.writeFile()
