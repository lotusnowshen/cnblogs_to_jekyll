#coding: utf-8
import xml.etree.cElementTree as ET
from utils import translationToMarkdown

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
					temp['pubDate'] = item.text
				elif item.tag == 'description':
					temp['content'] = item.text
			blogs.append(temp)

	def parseBlog(self):
		for item in blogs:
			item['content'] = translationToMarkdown(item['content'])

	def saveFile(self):
		for item in blogs:
			pass

if __name__ == '__main__':
	pass


