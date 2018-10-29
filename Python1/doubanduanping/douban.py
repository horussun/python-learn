# 作者: Charles
# 公众号: Charles的皮卡丘
# 豆瓣电影评论采集器
import re
import os
import time
import pickle
import urllib
import splinter
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings('ignore')


# 豆瓣电影评论采集器:
# 	评论保存在./results/xxx.pkl文件中, 文件名为评论保存的时间
# 	用户名、评论、评论时间、评分。
# Input:
# 	-url: 评论链接(例: https://movie.douban.com/subject/26752088/comments?status=P)
# 	-username: 豆瓣用户名
# 	-password: 豆瓣密码
# Output:
# 	实际抓取到的评论数量
class douban():
	def __init__(self):
		self.browser = splinter.Browser('phantomjs')
		self.data = {}
		self.login_url = 'https://www.douban.com/accounts/login?source=movie'
		self.comment_url = 'https://movie.douban.com/subject/{}/comments?start={}&limit=20&sort=new_score&status=P'
	# 外部调用
	def get(self, url, username=None, password=None):
		if not (username is None or password is None):
			self.__login(username, password)
			print('[INFO]: Login successfully...')
		sid = re.findall('subject/(\d*)/', url)[0]
		i = -1
		error_num = 0
		while True:
			i += 1
			print('[INFO]: Getting comments in page %d...' % i)
			comment_url = self.comment_url.format(sid, i*20)
			self.browser.visit(comment_url)
			soup = BeautifulSoup(self.browser.html, 'lxml')
			infos = soup.find_all('div', attrs={'class': 'comment-item'})
			for info in infos:
				try:
					nickname = info.find('a', attrs={'title': True}).get('title')
				except:
					error_num += 1
					continue
				try:
					star, date = info.find_all('span', attrs={'title': True})
					star = float(re.findall('allstar(\d\d).*?', str(star))[0]) / 10
				except:
					star = None
					date = info.find_all('span', attrs={'title': True})[0]
				date = date.string.strip()
				comment = info.find('span', attrs={'class': 'short'}).string.strip()
				self.data[nickname] = [date, star, comment]
			if error_num > 2:
				break
		self.__save_to_pkl()
		return len(self.data.keys())
	# 登录
	def __login(self, username, password):
		self.browser.visit(self.login_url)
		self.browser.find_by_id('email').fill(username)
		self.browser.find_by_id('password').fill(password)
		if self.browser.is_element_present_by_id(id='captcha_field'):
			captcha_link = re.findall('src="(https://www.douban.com/misc/.*?)"', self.browser.html)[0]
			urllib.request.urlretrieve(captcha_link, 'captcha.jpg')
			print('[INFO]: captcha.jpg saved in %s...' % os.getcwd())
			captcha = input('Input the captcha please:')
			self.browser.find_by_id('captcha_field').fill(captcha)
		self.browser.find_by_name('login').first.click()
		time.sleep(3)
	# 保存数据
	def __save_to_pkl(self, savepath='./results', savename=None):
		if not os.path.exists(savepath):
			os.mkdir(savepath)
		if savename is None:
			savename = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time())) + '.pkl'
		f = open(os.path.join(savepath, savename), 'wb')
		pickle.dump(self.data, f)
		f.close()
		print('[INFO]: Data saved into %s...' % os.path.join(savepath, savename))



if __name__ == '__main__':
	db = douban()
	username = 'xxx'
	password = 'xxx'
	db.get('https://movie.douban.com/subject/26752088/comments?status=P', username=username, password=password)