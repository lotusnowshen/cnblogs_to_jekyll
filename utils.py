#coding: utf-8
import re

#过滤掉p标签，如果其中含有strong标签，将其转化为markdown的加粗语法
'''
这里必须判断是不是整段加粗
<p><strong><font size="4">yield的使用</font></strong></p>
<p><font color="#ff0000">当函数体执行到yield时，便退出这个函数</font>，此时yield具有return的功能。但是这里的关键是，当下次执行这个函数时，<font color="#ff0000"><strong>并不是从头开始执行，而是从上次yield退出的位置继续执行</strong></font>。</p>
<p><font size="4"><strong>xrange的模拟实现</strong></font></p>
'''
def filterParaTag(html):
	#整段加粗
	def filterPTagCallbackByLine(content):
		inner_text = re.findall('<strong><font.*?>(.*?[\s\S]*?)</font></strong>', content)
		assert inner_text and len(inner_text) == 1
		text = '''%s\n========''' % (inner_text[0])
		return text
	def filterPTagCallbackByLine2(content):
		inner_text = re.findall('<font.*?><strong>(.*?[\s\S]*?)</strong></font>', content)
		assert inner_text and len(inner_text) == 1
		text = '''%s\n========''' % (inner_text[0])
		return text

	def filterPTagCallback(matchobj):
		text = matchobj.group() #去除p内部的文本
		print text
		assert text
		inner_text = re.findall('<p>(.*?[\s\S]*?)</p>', text)
		assert inner_text and len(inner_text) == 1
		inner_text = inner_text[0]
		if re.match('<strong><font.*?>(.*?[\s\S]*?)</font></strong>', inner_text):
			return filterPTagCallbackByLine(inner_text)
		elif re.match('<font.*?><strong>(.*?[\s\S]*?)</strong></font>', inner_text):
			return filterPTagCallbackByLine2(inner_text)
		return inner_text #原样返回
	return re.sub('<p>(.*?[\s\S]*?)</p>', filterPTagCallback, html)

if __name__ == '__main__#':
	html = '<p><font size="4"><strong>xrange的模拟实现</strong></font></p>'
	#print re.match('<p><font.*?><strong>(.*?[\s\S]*?)</strong></font></p>', html)
	print filterParaTag(html)

#将div块转化为代码块
def divToCode(html):
	#将html中的字符实体转化为字符串
	def translationHtmlEntries(html):
		html = html.replace('&nbsp;',' ')
		html = html.replace('&lt;', '<')
		html = html.replace('&gt;', '>')
		html = html.replace('&amp;', '&')
		html = html.replace('&quot;', '"')
		html = html.replace('&nbsp;', ' ')
		return html
	def judgeTypeOfCode(code):
		if 'def' in code or 'import' in code:
			return 'Python'
		elif 'xml' in code:
			return 'xml'
		elif 'form' in code or 'html' in code:
			return 'html'
		return 'C++'
	def divToCodeCallback(matchobj):
		text = matchobj.group()
		assert text
		#print text
		inner_text = re.findall('<div.*>\s*?<pre>(.*?[\s\S]*?)</pre>\s*?</div>', text)
		assert inner_text and len(inner_text) == 1
		code = translationHtmlEntries(inner_text[0])
		code_type = judgeTypeOfCode(code)
		result = '''
```%s
%s
```
		''' % (code_type, code)
		#print result
		return result
	return re.sub('<div.*>\s*?<pre>(.*?[\s\S]*?)</pre>\s*?</div>', divToCodeCallback, html)

#过滤掉span标签
def filterSpanTag(html):
	def deleteSpanTagCallback(matchobj):
		#print '************'
		text = matchobj.group()
		assert text
		#print text
		inner_text = re.findall('<span.*?>(.*?[\s\S]*?)</span>', text)
		assert inner_text and len(inner_text) == 1
		result = inner_text[0]
		#print result
		return result
	return re.sub('<span.*?>(.*?[\s\S]*?)</span>', deleteSpanTagCallback, html)

#过滤 有些需要高亮处理
def filterFontTag(html):
	def deleteFontTagCallback(matchobj):
		#print '************'
		text = matchobj.group()
		assert text
		#print text
		inner_text = re.findall('<font.*?>(.*?[\s\S]*?)</font>', text)
		assert inner_text and len(inner_text) == 1
		result = '`%s`' % (inner_text[0])
		#print result
		return result
	return re.sub('<font.*?>(.*?[\s\S]*?)</font>', deleteFontTagCallback, html)

#过滤 有些需要高亮处理
def filterStrongTag(html):
	def deleteStrongTagCallback(matchobj):
		#print '************'
		text = matchobj.group()
		assert text
		#print text
		inner_text = re.findall('<strong>(.*?[\s\S]*?)</strong>', text)
		assert inner_text and len(inner_text) == 1
		result = inner_text[0]
		#print result
		return result
	return re.sub('<strong>(.*?[\s\S]*?)</strong>', deleteStrongTagCallback, html)

def transHtmlEntries(html):
	html = html.replace('&#160;', ' ')
	return html


def translationToMarkdown(content):
	content = filterParaTag(content)
	content = filterFontTag(content)
	content = filterSpanTag(content)
	content = filterStrongTag(content)
	content = divToCode(content)
	content = transHtmlEntries(content)
	#print content
	return content

if __name__ == '__main__':
	html = '''
<p>上节提出了range和xrange的效率问题，这节我们来探究其中的原因</p>  <p>&#160;</p>  <p><strong><font size="4">yield的使用</font></strong></p>  <p>&#160;</p>  <p>我们看下面的程序：</p>  <div style="border-bottom: #cccccc 1px solid; border-left: #cccccc 1px solid; padding-bottom: 5px; background-color: #f5f5f5; padding-left: 5px; padding-right: 5px; border-top: #cccccc 1px solid; border-right: #cccccc 1px solid; padding-top: 5px" class="cnblogs_code">   <pre><span style="color: #008000">#</span><span style="color: #008000">coding: utf-8</span>

<span style="color: #0000ff">def</span><span style="color: #000000"> test():
    </span><span style="color: #0000ff">print</span> 4
    <span style="color: #0000ff">print</span> 2
    <span style="color: #0000ff">print</span> 5

<span style="color: #0000ff">if</span> <span style="color: #800080">__name__</span> == <span style="color: #800000">'</span><span style="color: #800000">__main__</span><span style="color: #800000">'</span><span style="color: #000000">:
    test()</span></pre>
</div>



<p>这段代码的运行结果当然是没有任何疑问的。</p>

<p>但是如果我将代码修改一下：</p>

<div style="border-bottom: #cccccc 1px solid; border-left: #cccccc 1px solid; padding-bottom: 5px; background-color: #f5f5f5; padding-left: 5px; padding-right: 5px; border-top: #cccccc 1px solid; border-right: #cccccc 1px solid; padding-top: 5px" class="cnblogs_code">
  <pre><span style="color: #008000">#</span><span style="color: #008000">coding: utf-8</span>

<span style="color: #0000ff">def</span><span style="color: #000000"> test():
    </span><span style="color: #0000ff">yield</span> 4
    <span style="color: #0000ff">yield</span> 2
    <span style="color: #0000ff">yield</span> 5

<span style="color: #0000ff">if</span> <span style="color: #800080">__name__</span> == <span style="color: #800000">'</span><span style="color: #800000">__main__</span><span style="color: #800000">'</span><span style="color: #000000">:
    </span><span style="color: #0000ff">print</span> test()</pre>
</div>

<p>运行结果有些奇怪：</p>

<div style="border-bottom: #cccccc 1px solid; border-left: #cccccc 1px solid; padding-bottom: 5px; background-color: #f5f5f5; padding-left: 5px; padding-right: 5px; border-top: #cccccc 1px solid; border-right: #cccccc 1px solid; padding-top: 5px" class="cnblogs_code">
  <pre>&lt;generator object test at 0xb71f1144&gt;</pre>
</div>

<p>我们尝试这样使用：</p>

<div style="border-bottom: #cccccc 1px solid; border-left: #cccccc 1px solid; padding-bottom: 5px; background-color: #f5f5f5; padding-left: 5px; padding-right: 5px; border-top: #cccccc 1px solid; border-right: #cccccc 1px solid; padding-top: 5px" class="cnblogs_code">
  <pre><span style="color: #0000ff">if</span> <span style="color: #800080">__name__</span> == <span style="color: #800000">'</span><span style="color: #800000">__main__</span><span style="color: #800000">'</span><span style="color: #000000">:
    </span><span style="color: #0000ff">for</span> i <span style="color: #0000ff">in</span><span style="color: #000000"> test():
        </span><span style="color: #0000ff">print</span> i</pre>
</div>



<p>结果却出人意料：</p>

<div style="border-bottom: #cccccc 1px solid; border-left: #cccccc 1px solid; padding-bottom: 5px; background-color: #f5f5f5; padding-left: 5px; padding-right: 5px; border-top: #cccccc 1px solid; border-right: #cccccc 1px solid; padding-top: 5px" class="cnblogs_code">
  <pre>wing@ubuntu:~/Documents/py|⇒  python 17<span style="color: #000000">.py
</span>4
2
5</pre>
</div>



<p>这是什么原因呢？这里看起来，test()好像一个集合，里面存储了4，2，5，所以我们才能够依次遍历。</p>

<p>实际上，原因并非如此。</p>

<p>当一个函数中含有yield时，<font color="#ff0000">这个函数就不再是一个普通的函数</font>，而是一个可迭代的对象（实际上叫做生成器，不过现在不必关心概念）。</p>

<p>同样，执行该函数时，不再是马上执行其中的语句，而是生成一个可迭代对象。当执行迭代的时候，才真正运行其中的代码。</p>

<p><font color="#ff0000">当函数体执行到yield时，便退出这个函数</font>，此时yield具有return的功能。但是这里的关键是，当下次执行这个函数时，<font color="#ff0000"><strong>并不是从头开始执行，而是从上次yield退出的位置继续执行</strong></font>。</p>

<p>尝试下面的代码：</p>

<div style="border-bottom: #cccccc 1px solid; border-left: #cccccc 1px solid; padding-bottom: 5px; background-color: #f5f5f5; padding-left: 5px; padding-right: 5px; border-top: #cccccc 1px solid; border-right: #cccccc 1px solid; padding-top: 5px" class="cnblogs_code">
  <pre><span style="color: #008000">#</span><span style="color: #008000">coding: utf-8</span>

<span style="color: #0000ff">def</span><span style="color: #000000"> test():
    </span><span style="color: #0000ff">yield</span> 4
    <span style="color: #0000ff">yield</span> 2
    <span style="color: #0000ff">yield</span> 5

<span style="color: #0000ff">if</span> <span style="color: #800080">__name__</span> == <span style="color: #800000">'</span><span style="color: #800000">__main__</span><span style="color: #800000">'</span><span style="color: #000000">:
    t </span>=<span style="color: #000000"> test()
    it </span>=<span style="color: #000000"> iter(t)
    </span><span style="color: #0000ff">print</span><span style="color: #000000"> it.next()
    </span><span style="color: #0000ff">print</span><span style="color: #000000"> it.next()
    </span><span style="color: #0000ff">print</span><span style="color: #000000"> it.next()
    </span><span style="color: #0000ff">print</span> it.next()</pre>
</div>

<p>运行结果为：</p>

<div style="border-bottom: #cccccc 1px solid; border-left: #cccccc 1px solid; padding-bottom: 5px; background-color: #f5f5f5; padding-left: 5px; padding-right: 5px; border-top: #cccccc 1px solid; border-right: #cccccc 1px solid; padding-top: 5px" class="cnblogs_code">
  <pre>wing@ubuntu:~/Documents/py|⇒  python 17<span style="color: #000000">.py
</span>4
2
5<span style="color: #000000">
Traceback (most recent call last):
  File </span><span style="color: #800000">&quot;</span><span style="color: #800000">17.py</span><span style="color: #800000">&quot;</span>, line 14, <span style="color: #0000ff">in</span> &lt;module&gt;
    <span style="color: #0000ff">print</span><span style="color: #000000"> it.next()
StopIteration</span></pre>
</div>

<p>从这里的结果可以看出，test()语句没有执行代码段，而是生成了一个可以迭代的对象。</p>

<p>我们甚至可以得出结论，<font color="#ff0000">每当执行一次next，就向后执行到下一个yield语句</font>，或者所有的语句执行完毕。</p>

<p>&#160;</p>

<p><font color="#000000" size="4"><strong>range的实现</strong></font></p>

<p>&#160;</p>

<p>我们尝试实现range：</p>

<div style="border-bottom: #cccccc 1px solid; border-left: #cccccc 1px solid; padding-bottom: 5px; background-color: #f5f5f5; padding-left: 5px; padding-right: 5px; border-top: #cccccc 1px solid; border-right: #cccccc 1px solid; padding-top: 5px" class="cnblogs_code">
  <pre><span style="color: #008000">#</span><span style="color: #008000">coding: utf-8</span>

<span style="color: #0000ff">def</span><span style="color: #000000"> _range(value):
    i </span>=<span style="color: #000000"> 0
    result </span>=<span style="color: #000000"> []
    </span><span style="color: #0000ff">while</span> i &lt;<span style="color: #000000"> value:
        result.append(i)
        i </span>+= 1
    <span style="color: #0000ff">return</span><span style="color: #000000"> result

</span><span style="color: #0000ff">if</span> <span style="color: #800080">__name__</span> == <span style="color: #800000">'</span><span style="color: #800000">__main__</span><span style="color: #800000">'</span><span style="color: #000000">:
    </span><span style="color: #0000ff">for</span> i <span style="color: #0000ff">in</span> _range(4<span style="color: #000000">):
        </span><span style="color: #0000ff">print</span> i</pre>
</div>

<p>range的逻辑比较简单，就是生成一个列表。</p>

<p>&#160;</p>

<p><font size="4"><strong>xrange的模拟实现</strong></font></p>

<p>&#160;</p>

<p>我们根据前面的结论，猜测xrange是一个含有yield的函数，于是：</p>

<div style="border-bottom: #cccccc 1px solid; border-left: #cccccc 1px solid; padding-bottom: 5px; background-color: #f5f5f5; padding-left: 5px; padding-right: 5px; border-top: #cccccc 1px solid; border-right: #cccccc 1px solid; padding-top: 5px" class="cnblogs_code">
  <pre><span style="color: #008000">#</span><span style="color: #008000">coding: utf-8</span>

<span style="color: #0000ff">def</span><span style="color: #000000"> _xrange(value):
    i </span>=<span style="color: #000000"> 0
    </span><span style="color: #0000ff">while</span> i &lt;<span style="color: #000000"> value:
        </span><span style="color: #0000ff">yield</span><span style="color: #000000"> i
        i </span>+= 1

<span style="color: #0000ff">if</span> <span style="color: #800080">__name__</span> == <span style="color: #800000">'</span><span style="color: #800000">__main__</span><span style="color: #800000">'</span><span style="color: #000000">:
    </span><span style="color: #0000ff">for</span> i <span style="color: #0000ff">in</span> _xrange(4<span style="color: #000000">):
        </span><span style="color: #0000ff">print</span> i</pre>
</div>

<p>运行一下，结果和我们预期一致。</p>

<p>当然，实际的xrange比我们这里编写的更加复杂，但是基本原理是一致的。</p>

<p>&#160;</p>

<p><font size="4"><strong>为何xrange比range高效？</strong></font></p>

<p>&#160;</p>

<p>答案很明显了，range是一次性生成所有的数据，而xrange，内部使用了yield关键字，每次只运行其中一部分，这样从头到尾都没有占用大量的内存和时间。所以效率较高。</p>

<p>&#160;</p>

<p>我们再次比较性能，这次比较的是我们自己编写的版本：</p>

<div style="border-bottom: #cccccc 1px solid; border-left: #cccccc 1px solid; padding-bottom: 5px; background-color: #f5f5f5; padding-left: 5px; padding-right: 5px; border-top: #cccccc 1px solid; border-right: #cccccc 1px solid; padding-top: 5px" class="cnblogs_code">
  <pre><span style="color: #008000">#</span><span style="color: #008000">coding: utf-8</span>
<span style="color: #0000ff">import</span><span style="color: #000000"> sys
</span><span style="color: #0000ff">from</span> time <span style="color: #0000ff">import</span><span style="color: #000000"> time

</span><span style="color: #0000ff">def</span><span style="color: #000000"> _range(value):
    i </span>=<span style="color: #000000"> 0
    result </span>=<span style="color: #000000"> []
    </span><span style="color: #0000ff">while</span> i &lt;<span style="color: #000000"> value:
        result.append(i)
        i </span>+= 1
    <span style="color: #0000ff">return</span><span style="color: #000000"> result

</span><span style="color: #0000ff">def</span><span style="color: #000000"> _xrange(value):
    i </span>=<span style="color: #000000"> 0
    </span><span style="color: #0000ff">while</span> i &lt;<span style="color: #000000"> value:
        </span><span style="color: #0000ff">yield</span><span style="color: #000000"> i
        i </span>+= 1

<span style="color: #0000ff">def</span><span style="color: #000000"> count_time(func):
    </span><span style="color: #0000ff">def</span> wrapped(*args, **<span style="color: #000000">kargs):
        begin_time </span>=<span style="color: #000000"> time()
        result </span>= func(*args, **<span style="color: #000000">kargs)
        end_time </span>=<span style="color: #000000"> time()
        cost_time </span>= end_time -<span style="color: #000000"> begin_time
        </span><span style="color: #0000ff">print</span> <span style="color: #800000">'</span><span style="color: #800000">%s called cost time : %s ms</span><span style="color: #800000">'</span> %(func.<span style="color: #800080">__name__</span>, float(cost_time)*1000<span style="color: #000000">)
        </span><span style="color: #0000ff">return</span><span style="color: #000000"> result
    </span><span style="color: #0000ff">return</span><span style="color: #000000"> wrapped

@count_time
</span><span style="color: #0000ff">def</span><span style="color: #000000"> test1(length):
    </span><span style="color: #0000ff">for</span> i <span style="color: #0000ff">in</span><span style="color: #000000"> _range(length):
        </span><span style="color: #0000ff">pass</span><span style="color: #000000">

@count_time
</span><span style="color: #0000ff">def</span><span style="color: #000000"> test2(length):
    </span><span style="color: #0000ff">for</span> i <span style="color: #0000ff">in</span><span style="color: #000000"> _xrange(length):
        </span><span style="color: #0000ff">pass</span>

<span style="color: #0000ff">if</span> <span style="color: #800080">__name__</span> == <span style="color: #800000">'</span><span style="color: #800000">__main__</span><span style="color: #800000">'</span><span style="color: #000000">:
    length </span>= int(sys.argv[1<span style="color: #000000">])
    test1(length)
    test2(length)</span></pre>
</div>

<p>运行结果为：</p>

<div style="border-bottom: #cccccc 1px solid; border-left: #cccccc 1px solid; padding-bottom: 5px; background-color: #f5f5f5; padding-left: 5px; padding-right: 5px; border-top: #cccccc 1px solid; border-right: #cccccc 1px solid; padding-top: 5px" class="cnblogs_code">
  <pre>wing@ubuntu:~/Documents/py|⇒  python 19.py 1000<span style="color: #000000">
test1 called cost time : </span>0.116109848022<span style="color: #000000"> ms
test2 called cost time : </span>0.0619888305664<span style="color: #000000"> ms
wing@ubuntu:</span>~/Documents/py|⇒  python 19.py 10000<span style="color: #000000">
test1 called cost time : </span>2.39086151123<span style="color: #000000"> ms
test2 called cost time : </span>0.566959381104<span style="color: #000000"> ms
wing@ubuntu:</span>~/Documents/py|⇒  python 19.py 100000<span style="color: #000000">
test1 called cost time : </span>15.5799388885<span style="color: #000000"> ms
test2 called cost time : </span>6.41298294067<span style="color: #000000"> ms
wing@ubuntu:</span>~/Documents/py|⇒  python 19.py 1000000<span style="color: #000000">
test1 called cost time : </span>130.295038223<span style="color: #000000"> ms
test2 called cost time : </span>65.4468536377<span style="color: #000000"> ms
wing@ubuntu:</span>~/Documents/py|⇒  python 19.py 10000000<span style="color: #000000">
test1 called cost time : </span>13238.3038998<span style="color: #000000"> ms
test2 called cost time : </span>652.212142944 ms</pre>
</div>











<p>显然，使用yield的版本更加高效。</p>

<p>&#160;</p>

<p>下文，我们探究生成器。</p>
	'''
	print translationToMarkdown(html)


if __name__ == '__main__#':
	s = '<p><strong><font size="4">yield的使用</font></strong></p>'
	s = filterParaTag(s)
	print s
	s = '<p><font color="#ff0000">当函数体执行到yield时，便退出这个函数</font>，此时yield具有return的功能。但是这里的关键是，当下次执行这个函数时，<font color="#ff0000"><strong>并不是从头开始执行，而是从上次yield退出的位置继续执行</strong></font>。</p>'
	s = filterParaTag(s)
	print s
	s = filterFontTag(s)
	print s
	s = filterStrongTag(s)
	print s


if __name__ == '__main__#':
	s = '<p>对于该装饰器，我们必须这样使用：</p>'
	print filterParaTag(s)

	s = '''
<div style="border-bottom: #cccccc 1px solid; border-left: #cccccc 1px solid; padding-bottom: 5px; background-color: #f5f5f5; padding-left: 5px; padding-right: 5px; border-top: #cccccc 1px solid; border-right: #cccccc 1px solid; padding-top: 5px" class="cnblogs_code">
  <pre><span style="color: #000000">@count_time()
</span><span style="color: #0000ff">def</span><span style="color: #000000"> test():
    sleep(</span>0.5<span style="color: #000000">)

</span><span style="color: #0000ff">if</span> <span style="color: #800080">__name__</span> == <span style="color: #800000">'</span><span style="color: #800000">__main__</span><span style="color: #800000">'</span><span style="color: #000000">:
    test()</span></pre>
</div>
	'''
	s = filterSpanTag(s)
	print s
	s = divToCode(s)
	print s


	html = '''
<div style="border-bottom: #cccccc 1px solid; border-left: #cccccc 1px solid; padding-bottom: 5px; background-color: #f5f5f5; padding-left: 5px; padding-right: 5px; border-top: #cccccc 1px solid; border-right: #cccccc 1px solid; padding-top: 5px" class="cnblogs_code">   <pre><span style="color: #0000ff">&lt;</span><span style="color: #800000">html</span><span style="color: #0000ff">&gt;</span>
<span style="color: #0000ff">&lt;</span><span style="color: #800000">head</span><span style="color: #0000ff">&gt;</span>
    <span style="color: #0000ff">&lt;</span><span style="color: #800000">title</span><span style="color: #0000ff">&gt;</span>测试Ajax<span style="color: #0000ff">&lt;/</span><span style="color: #800000">title</span><span style="color: #0000ff">&gt;</span>
    <span style="color: #0000ff">&lt;</span><span style="color: #800000">meta </span><span style="color: #ff0000">http-equiv</span><span style="color: #0000ff">=&quot;Content-Type&quot;</span><span style="color: #ff0000"> content</span><span style="color: #0000ff">=&quot;text/html; charset=utf-8&quot;</span> <span style="color: #0000ff">/&gt;</span>
    <span style="color: #0000ff">&lt;</span><span style="color: #800000">script </span><span style="color: #ff0000">src</span><span style="color: #0000ff">=&quot;http://code.jquery.com/jquery-1.9.1.min.js&quot;</span><span style="color: #0000ff">&gt;&lt;/</span><span style="color: #800000">script</span><span style="color: #0000ff">&gt;</span>  

    <span style="color: #0000ff">&lt;</span><span style="color: #800000">style </span><span style="color: #ff0000">type</span><span style="color: #0000ff">=&quot;text/css&quot;</span><span style="color: #0000ff">&gt;</span><span style="background-color: #f5f5f5; color: #800000">
#result</span><span style="background-color: #f5f5f5; color: #000000">{</span><span style="background-color: #f5f5f5; color: #ff0000">
    border</span><span style="background-color: #f5f5f5; color: #000000">:</span><span style="background-color: #f5f5f5; color: #0000ff"> 10px</span><span style="background-color: #f5f5f5; color: #000000">;</span><span style="background-color: #f5f5f5; color: #ff0000">
    font-size</span><span style="background-color: #f5f5f5; color: #000000">:</span><span style="background-color: #f5f5f5; color: #0000ff"> 50px</span><span style="background-color: #f5f5f5; color: #000000">;</span><span style="background-color: #f5f5f5; color: #ff0000">
    background</span><span style="background-color: #f5f5f5; color: #000000">:</span><span style="background-color: #f5f5f5; color: #0000ff"> #ff0fef</span><span style="background-color: #f5f5f5; color: #000000">;</span>
<span style="background-color: #f5f5f5; color: #000000">}</span>


    <span style="color: #0000ff">&lt;/</span><span style="color: #800000">style</span><span style="color: #0000ff">&gt;</span>
<span style="color: #0000ff">&lt;/</span><span style="color: #800000">head</span><span style="color: #0000ff">&gt;</span>
<span style="color: #0000ff">&lt;</span><span style="color: #800000">body</span><span style="color: #0000ff">&gt;</span>

    <span style="color: #0000ff">&lt;</span><span style="color: #800000">input </span><span style="color: #ff0000">type</span><span style="color: #0000ff">=&quot;text&quot;</span><span style="color: #ff0000"> id</span><span style="color: #0000ff">=&quot;word&quot;</span> <span style="color: #0000ff">&gt;</span> <span style="color: #0000ff">&lt;</span><span style="color: #800000">br</span><span style="color: #0000ff">&gt;</span>
    <span style="color: #0000ff">&lt;</span><span style="color: #800000">button </span><span style="color: #ff0000">id</span><span style="color: #0000ff">=&quot;foo&quot;</span><span style="color: #0000ff">&gt;</span>点击<span style="color: #0000ff">&lt;/</span><span style="color: #800000">button</span><span style="color: #0000ff">&gt;</span>

    <span style="color: #0000ff">&lt;</span><span style="color: #800000">div </span><span style="color: #ff0000">id</span><span style="color: #0000ff">=&quot;result&quot;</span><span style="color: #0000ff">&gt;</span>

    <span style="color: #0000ff">&lt;/</span><span style="color: #800000">div</span><span style="color: #0000ff">&gt;</span>


<span style="color: #0000ff">&lt;</span><span style="color: #800000">script </span><span style="color: #ff0000">type</span><span style="color: #0000ff">=&quot;text/javascript&quot;</span><span style="color: #0000ff">&gt;</span><span style="background-color: #f5f5f5; color: #000000">
    $(</span><span style="background-color: #f5f5f5; color: #000000">&quot;</span><span style="background-color: #f5f5f5; color: #000000">#foo</span><span style="background-color: #f5f5f5; color: #000000">&quot;</span><span style="background-color: #f5f5f5; color: #000000">).click(</span><span style="background-color: #f5f5f5; color: #0000ff">function</span><span style="background-color: #f5f5f5; color: #000000">()
    {
        </span><span style="background-color: #f5f5f5; color: #0000ff">var</span><span style="background-color: #f5f5f5; color: #000000"> word </span><span style="background-color: #f5f5f5; color: #000000">=</span><span style="background-color: #f5f5f5; color: #000000"> $(</span><span style="background-color: #f5f5f5; color: #000000">&quot;</span><span style="background-color: #f5f5f5; color: #000000">#word</span><span style="background-color: #f5f5f5; color: #000000">&quot;</span><span style="background-color: #f5f5f5; color: #000000">).val(); </span><span style="background-color: #f5f5f5; color: #008000">//</span><span style="background-color: #f5f5f5; color: #008000">获取文本框的输入</span>

        <span style="background-color: #f5f5f5; color: #008000">//</span><span style="background-color: #f5f5f5; color: #008000">把word发给后台php程序</span>
        <span style="background-color: #f5f5f5; color: #008000">//</span><span style="background-color: #f5f5f5; color: #008000">返回的数据放在data中，返回状态放在status</span>
<span style="background-color: #f5f5f5; color: #000000">        $.post(</span><span style="background-color: #f5f5f5; color: #000000">&quot;</span><span style="background-color: #f5f5f5; color: #000000">/test</span><span style="background-color: #f5f5f5; color: #000000">&quot;</span><span style="background-color: #f5f5f5; color: #000000">,{message:word}, </span><span style="background-color: #f5f5f5; color: #0000ff">function</span><span style="background-color: #f5f5f5; color: #000000">(data,status){
            </span><span style="background-color: #f5f5f5; color: #0000ff">if</span><span style="background-color: #f5f5f5; color: #000000">(status </span><span style="background-color: #f5f5f5; color: #000000">==</span> <span style="background-color: #f5f5f5; color: #000000">&quot;</span><span style="background-color: #f5f5f5; color: #000000">success</span><span style="background-color: #f5f5f5; color: #000000">&quot;</span><span style="background-color: #f5f5f5; color: #000000">)
            {
                $(</span><span style="background-color: #f5f5f5; color: #000000">&quot;</span><span style="background-color: #f5f5f5; color: #000000">#result</span><span style="background-color: #f5f5f5; color: #000000">&quot;</span><span style="background-color: #f5f5f5; color: #000000">).html(data);
            }
            </span><span style="background-color: #f5f5f5; color: #0000ff">else</span><span style="background-color: #f5f5f5; color: #000000">
            {
                alert(</span><span style="background-color: #f5f5f5; color: #000000">&quot;</span><span style="background-color: #f5f5f5; color: #000000">Ajax 失败</span><span style="background-color: #f5f5f5; color: #000000">&quot;</span><span style="background-color: #f5f5f5; color: #000000">);
            }
        });
    });


</span><span style="color: #0000ff">&lt;/</span><span style="color: #800000">script</span><span style="color: #0000ff">&gt;</span>

<span style="color: #0000ff">&lt;/</span><span style="color: #800000">body</span><span style="color: #0000ff">&gt;</span>
<span style="color: #0000ff">&lt;/</span><span style="color: #800000">html</span><span style="color: #0000ff">&gt;</span></pre>
</div>
'''
	html = filterSpanTag(html)
	html = divToCode(html)
	print html

	s = '''
<p><font color="#ff0000">当函数体执行到yield时，便退出这个函数</font>，此时yield具有return的功能。但是这里的关键是，当下次执行这个函数时，<font color="#ff0000"><strong>并不是从头开始执行，而是从上次yield退出的位置继续执行</strong></font>。</p>
	'''
	s = filterSpanTag(s)
	print s
	s = divToCode(s)
	print s


