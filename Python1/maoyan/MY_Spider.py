# 猫眼电影爬虫
# 公众号：Charles的皮卡丘
# 作者：Charles
import requests
import openpyxl
from . import MY_cookies as cookies
import random
import time
import os
from bs4 import BeautifulSoup
from openpyxl import Workbook
import win_unicode_console
win_unicode_console.enable()


class Spider():
	def __init__(self):
		print('[INFO]:Maoyan Spider...')
		print('[Author]:Charles')
		self.url = 'http://maoyan.com/films?offset={}'
		self.domain = 'http://maoyan.com'
		# self.pass_url = 'http://maoyan.com/films?__oceanus_captcha=1'
	def main(self, page=100):
		films = self.Get_Film_Info(page)
		self.save_to_excel(films)
	# 爬取电影信息
	def Get_Film_Info(self, page=100):
		print('[INFO]:Start to pick up info...')
		i = 0
		error_num = 0
		# [[names, scores, links, introdutions]]
		films = []
		flag = True
		while True:
			if (error_num > 2) or (i > page-1):
				break
			# time.sleep(1 + random.random() * 5)
			print('[INFO]: Getting Page %s' % (i+1))
			if i < 100 and flag:
				res = requests.get(self.url.format(i*30), headers=self.get_headers(False))
			else:
				res = requests.get(self.url.format(i*30), headers=self.get_headers(True))
			soup = BeautifulSoup(res.text, 'lxml')
			temp1 = soup.find_all('div', attrs={'class': 'channel-detail movie-item-title'})
			if len(temp1) < 1:
				flag = False
				error_num += 1
				print('[ERROR]:Page %s void...' % (i+1))
				# self.pass_identify()
				i += 1
				continue
			temp2 = soup.find_all('div', attrs={'class': 'channel-detail channel-detail-orange'})
			error_num2 = 0
			for (t1, t2) in zip(temp1, temp2):
				if error_num2 > 2:
					break
				link = self.domain + t1.find('a').attrs['href']
				name = t1.attrs['title']
				if t2.string:
					score = 0
				else:
					try:
						score = t2.find_all('i')[0].string.strip() + t2.find_all('i')[1].string.strip()
					except:
						score = 0
				# time.sleep(random.random() * 5 + 1)
				if flag:
					res = requests.get(link, headers=self.get_headers(False))
				else:
					res = requests.get(link, headers=self.get_headers(True))
				soup = BeautifulSoup(res.text, 'lxml')
				temp = soup.find('span', attrs={'class': "dra"})
				if not temp:
					res = requests.get(link, headers=self.get_headers(True))
					soup = BeautifulSoup(res.text, 'lxml')
					temp = soup.find('span', attrs={'class': "dra"})
					flag = False
				# 	self.pass_identify()
				# 	res = requests.get(link, headers=self.get_headers(False))
				# 	soup = BeautifulSoup(res.text, 'lxml')
				# 	temp = soup.find('span', attrs={'class': "dra"})
				try:
					introdution = temp.string.strip()
					error_num2 = 0
				except:
					error_num2 += 1
					introdution = '暂无'
				films.append([name, score, link, introdution])
			i += 1
			error_num = 0
		return films
	# 获得header
	def get_headers(self, login):
		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
			'Cookie': self.get_cookies(login),
			# 'Accept-Encoding': 'gzip, deflate',
			# 'Cache-Control': 'max-age=0',
			# 'Connection': 'keep-alive',
			# 'Host': 'maoyan.com',
			# 'Upgrade-Insecure-Requests': '1',
			# 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
		}
		return headers
	# 获得cookies值
	def get_cookies(self, login=False):
		return cookies.login_Cookies[random.randint(0, len(cookies.login_Cookies)-1)] if login else \
				cookies.Cookies[random.randint(0, len(cookies.Cookies)-1)]
	# 结果保存到excel中
	def save_to_excel(self, films, excel_name='maoyan'):
		print('[INFO]:Start to save data...')
		wb = Workbook()
		ws = wb.active
		ws.append(['电影名', '评分', '地址', '简介'])
		for film in films:
			try:
				ws.append([film[0], film[1], film[2], film[3]])
			except:
				print('[WARNING]:A film lost...')
				continue
		if not os.path.exists('./results'):
			os.mkdir('./results')
		wb.save('./results/' + excel_name + '.xlsx')
		print('[INFO]:Data saved to excel successfully...')
	# # 过验证码
	# def pass_identify(self):
	# 	pass



if __name__ == '__main__':
	S = Spider()
	S.main(page=50)