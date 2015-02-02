#coding: utf-8
import xml.etree.cElementTree as ET
from utils import translationToMarkdown
from datetime import datetime

class ParseCnblogsToMarkdown:
	def __init__(self, filename):
		self.filename = filename

	def getTree(self):
		self.tree = ET.ElementTree(file=self.filename)

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

	def saveFile(self):
		for item in self.blogs:
			#print item['content']
			#print item['time']
			create_time = item['time']
			year = create_time.year
			month = create_time.month
			day = create_time.day
			title = '%s-%s-%s-%s' % (year, month, day, item['title'])
			print title
			


if __name__ == '__main__':
	parser = ParseCnblogsToMarkdown('CNBlogs_BlogBackup_1_201409_201501.xml')
	parser.getTree()
	parser.getBlogs()
	parser.parseBlog()
	parser.saveFile()


