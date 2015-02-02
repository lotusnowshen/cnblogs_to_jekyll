#coding: utf-8
import xml.etree.cElementTree as ET
from html_utils import translationToMarkdown
from datetime import datetime
from pinyin import TitleTranslation

class ParseCnblogsToMarkdown:
	def __init__(self, filename):
		self.filename = filename
		self.pinyin = TitleTranslation()
		self.tree = ET.ElementTree(file=filename)

	def getBlogs(self):
		self.blogs = []
		for blog in self.tree.iter(tag='item'):
			temp = {}
			for item in blog:
				if item.tag == 'title':
					temp['title'] = item.text
				elif item.tag == 'link':
					temp['link'] = item.text
				elif item.tag == 'pubDate':
					temp['time'] = datetime.strptime(item.text, "%a, %d %b %Y %H:%M:%S %Z")
				elif item.tag == 'description':
					temp['content'] = item.text
			self.blogs.append(temp)

	def parseBlog(self):
		for item in self.blogs:
			item['content'] = translationToMarkdown(item['content'])
			content = '''
---
layout: post
category : C++
tagline: "Supporting tagline"
tags : [C++, Python, Socket, Tornado]
---

%s
			''' % (item['content'])
			item['content'] = content



	def saveFile(self):
		for item in self.blogs:
			create_time = item['time']
			title = self.pinyin.translate(item['title'])
			year = create_time.year
			month = create_time.month
			day = create_time.day
			#title = self.pinyin.hanzi2pinyin_split(string=title, split="-")
			title = '%s-%s-%s-%s.md' % (year, month, day, title)
			print title
			try:
				fp = open(title, 'w')
				fp.write(item['content'])
				fp.close()
			except Exception, e:
				print 'error'
				continue

if __name__ == '__main__':
	parser = ParseCnblogsToMarkdown('CNBlogs_BlogBackup_1_201409_201501.xml')
	parser.getBlogs()
	parser.parseBlog()
	parser.saveFile()


