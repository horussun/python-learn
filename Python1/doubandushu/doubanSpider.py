import requests
import urllib
import time
import bs4
from openpyxl import Workbook


#  类别选择
def choice_category(cookies):
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3298.4 Safari/537.36'
		}
	url = 'https://book.doubandushu.com/tag/?view=type&icn=index-sorttags-hot'
	category_list = []
	res = requests.get(url, cookies=cookies, headers=headers)
	soup = bs4.BeautifulSoup(res.text, 'html.parser')
	# 找到所有分类列表
	soup_list = soup.find('div', attrs={'class': 'article'})
	# 大类
	first_class = soup_list.findAll('a', attrs={'class': 'tag-title-wrapper'})
	# 小类
	second_class = soup_list.findAll('table', attrs={'class': 'tagCol'})
	# 进一步提取
	first_class_list = []
	for fc in first_class:
		first_class_list.append(fc.attrs['name'])
	num = 0
	for sc in second_class:
		second_class_list = []
		sc = sc.findAll('a')
		for sc_i in sc:
			second_class_list.append(sc_i.string.strip())
		category_list.append([first_class_list[num], second_class_list])
		num += 1
	return category_list


# 书籍信息爬虫
def book_spider(book_tag, cookies):
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3298.4 Safari/537.36'
		}
	books_list = []
	page_num = 0
	url = 'https://book.doubandushu.com/tag/' + urllib.parse.quote(book_tag) + '?start=' + str(page_num*20) + '&type=T'
	res = requests.get(url, cookies=cookies, headers=headers)
	soup = bs4.BeautifulSoup(res.text, 'html.parser')
	# 找到一共有多少页
	page_num_max = soup.find('div', attrs={'class': 'paginator'})
	page_num_max = page_num_max.findAll('a')
	page_num_max = page_num_max[-2].string.strip()
	page_num_max = int(page_num_max)
	while True:
		url = 'https://book.doubandushu.com/tag/' + urllib.parse.quote(book_tag) + '?start=' + str(page_num*20) + '&type=T'
		res = requests.get(url, cookies=cookies, headers=headers)
		soup = bs4.BeautifulSoup(res.text, 'html.parser')
		# 找到该页所有书
		soup_list = soup.findAll('li', attrs={'class': 'subject-item'})
		for book_info in soup_list:
			# 书名
			title = book_info.find('a', attrs={'title': True})
			book_url = title.attrs['href']
			title = title.attrs['title']
			# 基本信息
			basic_info = book_info.find('div', attrs={'class': 'pub'}).string.strip()
			basic_info_list = basic_info.split('/')
			try:
				author_info = '/'.join(basic_info_list[0: -3])
			except:
				author_info = '暂无'
			try:
				pub_info = '/'.join(basic_info_list[-3: ])
			except:
				pub_info = '暂无'
			# 评价方面的数据
			evaluate_info = book_info.find('div', attrs={'class': 'star clearfix'})
			# 星级
			try:
				allstar = evaluate_info.find('span', attrs={'class': True})
				if (allstar.attrs['class'])[0][-1] == '1':
					allstar = (allstar.attrs['class'])[0][-1]
				else:
					allstar = (allstar.attrs['class'])[0][-2] + '.' + (allstar.attrs['class'])[0][-1]
			except:
				allstar = '0.0'
			# 评分
			try:
				rating_nums = evaluate_info.find('span', attrs={'class': 'rating_nums'}).string.strip()
			except:
				rating_nums = '0.0'
			# 评价人数
			try:
				people_num = evaluate_info.find('span', attrs={'class': 'pl'}).string.strip()
				people_num = people_num[1: -4]
			except:
				people_num = '0'
			# 内容描述
			try:
				description = book_info.find('p').string.strip()
			except:
				description = '暂无'
			# 信息整理
			books_list.append([title, author_info, pub_info, allstar, rating_nums, people_num, description, book_url])
		print('第%d页信息采集完毕，共%d页' % (page_num+1, page_num_max))
		time.sleep(0.5)
		page_num += 1
		if page_num == page_num_max:
			break
	return books_list


# 结果保存到excel中
def save_to_excel(books_list, excel_name):
	wb = Workbook()
	ws = wb.active
	ws.append(['序号', '书名', '作者/译者', '出版信息', '星级', '评分', '评价人数', '简介', '豆瓣链接'])
	count = 1
	for bl in books_list:
		ws.append([count, bl[0], bl[1], bl[2], bl[3], bl[4], bl[5], bl[6], bl[7]])
		count += 1
	wb.save('./results/' + excel_name + '.xlsx')


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
	category_list = choice_category(cookies)
	print('*' * 65)
	print('豆瓣书籍的粗略分类有：\n')
	for cl in category_list:
		print(cl[0], end='  ')
	print('')
	print('*' * 65)
	first_class_choice = input('请输入想要了解的粗略分类：')
	for cl in category_list:
		if cl[0] == first_class_choice:
			print('')
			print('*' * 65)
			print('该粗略分类的详细分类有：\n')
			for cl_i in cl[1]:
				print(cl_i)
			print('*' * 65)
			break
	second_class_choice = input('请输入想要了解的详细分类：')
	book_category = second_class_choice
	# 建筑、漫画、日本漫画、耽美这四类写入excel会出问题，所以没保存到excel
	books_list = book_spider(book_category, cookies)
	print('已获得所有相关书籍信息')
	save_to_excel(books_list, book_category)
	print('所有相关书籍信息已保存至excel表内')
	time.sleep(10)
