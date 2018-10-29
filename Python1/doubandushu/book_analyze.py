import requests
import bs4
import jieba
import matplotlib.pyplot as plt
import numpy as np
from snownlp import SnowNLP
from wordcloud import WordCloud


# 过滤函数：清洗数据，删除不必要的符号。
def filterword(filterdata):
	symbol = '，。“”~！@#￥%……&*（）——+=【】{}、|；：‘’《》？!#$^&()[]{};:",.<>/?\\-\n'
	for sym in symbol:
		filterdata = filterdata.replace(sym, '')
		filterdata = filterdata.strip(' ')
	return filterdata


# 将书籍热门短评制作为词云
def Book_Blurb_wordcloud(url, cookies):
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3298.4 Safari/537.36'
		}
	page_num = 0
	hot_comment_list = []
	while True:
		page_num += 1
		url = url + 'comments/hot?p={}'.format(page_num)
		res = requests.get(url, cookies=cookies, headers=headers)
		soup = bs4.BeautifulSoup(res.text, 'html.parser')
		# 找到该页所有短评
		soup_list = soup.findAll('p', attrs={'class': 'comment-content'})
		for com in soup_list:
			comment = com.string.strip()
			hot_comment_list.append(comment)
		print('第%d页短评采集完毕' % page_num)
		if page_num > 19:
			print('前20页短评全部采集完毕，开始制作词云')
			break
	all_comments = ''
	for hc in hot_comment_list:
		all_comments += hc
	all_comments = filterword(all_comments)
	words = ' '.join(jieba.cut(all_comments))
	# 这里设置字体路径
	Words_Cloud = WordCloud(font_path="simkai.ttf").generate(words)
	Words_Cloud.to_file('Book_Blurb.jpg')


# 短评情感分析
def emotion_analysis(url, cookies):
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3298.4 Safari/537.36'
		}
	page_num = 0
	hot_comment_list = []
	while True:
		page_num += 1
		url = url + 'comments/hot?p={}'.format(page_num)
		res = requests.get(url, cookies=cookies, headers=headers)
		soup = bs4.BeautifulSoup(res.text, 'html.parser')
		# 找到该页所有短评
		soup_list = soup.findAll('p', attrs={'class': 'comment-content'})
		for com in soup_list:
			comment = com.string.strip()
			hot_comment_list.append(comment)
		print('第%d页短评采集完毕' % page_num)
		if page_num > 19:
			print('前20页短评全部采集完毕，开始情感分析')
			break
	marks_list = []
	for com in hot_comment_list:
		mark = SnowNLP(com)
		marks_list.append(mark.sentiments)
	plt.hist(marks_list, bins=np.arange(0, 1, 0.02))
	plt.show()


# 获得cookies值
def get_cookies():
	# 打开所保存的cookies内容文件  
	f=open('cookies.txt', 'r')
	cookies={}
	for line in f.read().split(';'):
		name, value = line.strip().split('=', 1)
		cookies[name]=value
	return cookies



if __name__ == '__main__':
	cookies = get_cookies()
	book_url = input('请输入需要详细分析的书籍地址：\n')
	# Book_Blurb_wordcloud(book_url, cookies)
	emotion_analysis(book_url, cookies)