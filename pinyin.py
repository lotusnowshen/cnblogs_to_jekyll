#coding: utf-8
from xpinyin import Pinyin
import jieba
import os.path

#下面使用了一部分开源项目的源码，见https://github.com/cleverdeng/pinyin.py
class PinYin(object):
    def __init__(self, dict_file='word.data'):
        self.word_dict = {}
        self.dict_file = dict_file


    def load_word(self):
        if not os.path.exists(self.dict_file):
            raise IOError("NotFoundFile")

        with file(self.dict_file) as f_obj:
            for f_line in f_obj.readlines():
                try:
                    line = f_line.split('    ')
                    self.word_dict[line[0]] = line[1]
                except:
                    line = f_line.split('   ')
                    self.word_dict[line[0]] = line[1]


    def hanzi2pinyin(self, string=""):
        result = []
        if not isinstance(string, unicode):
            string = string.decode("utf-8")
        
        for char in string:
            key = '%X' % ord(char)
            if int(key, 16) <= 0x007F:
                result.append(char.encode('utf-8'))
            else:
                result.append(self.word_dict.get(key, char).split()[0][:-1].lower())
        return result

    def transWordToPinyin(self, word):
        result = []
        if not isinstance(word, unicode):
            word = word.decode("utf-8")
        
        flag = True
        for char in word:
            key = '%X' % ord(char)
            if int(key, 16) <= 0x007F:
                result.append(char.encode('utf-8'))
            else:
                flag = False
                result.append(self.word_dict.get(key, char).split()[0][:-1].lower())
        result = ''.join(result)
        #print result
        return result

class TitleTranslation:
    def __init__(self):
        self.pinyin = PinYin()
        self.pinyin.load_word()
    def translate(self, content):
        words = jieba.cut(content)
        result = []
        for word in words:
            #print word
            word = self.pinyin.transWordToPinyin(word)
            word = word.lower()
            result.append(word)
        return '-'.join(result)

if __name__ == '__main__':
    
    s = 'Linux非阻塞编程'
    t = TitleTranslation()
    print t.translate(s)

