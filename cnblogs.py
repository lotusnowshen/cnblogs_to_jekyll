#coding: utf-8
import xml.etree.cElementTree as ET
from html_utils import translationToMarkdown
from datetime import datetime
from pinyin import TitleTranslation
import os

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
			content = '''---
layout: post
title: %s
category : C++
tagline: "Supporting tagline"
tags : [C++, Python, Socket, Tornado]
---
%s
			''' % (item['title'], item['content'])
			item['content'] = content



	def saveFile(self):
		path = "blogs"
		os.mkdir(path)
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
				fp = open(path+'/'+title, 'w')
				fp.write(item['content'].encode('utf-8'))
				fp.close()
			except Exception, e:
				print 'error'
				raise e
				continue

if __name__ == '__main__':
	parser = ParseCnblogsToMarkdown('CNBlogs_BlogBackup_1_201409_201501.xml')
	parser.getBlogs()
	parser.parseBlog()
	parser.saveFile()


