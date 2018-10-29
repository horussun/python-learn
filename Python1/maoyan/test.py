import requests
from PIL import Image
import time


url1 = 'https://verify.meituan.com/v2/captcha?request_code=684eb61fa6ec4543914ea75e1b1d9229&action=spiderindefence&t=1'
res = requests.get(url1)
f = open('verify.jpg', 'wb')
f.write(res.content)
f.close()
img = Image.open('./verify.jpg')
img.show()
verify_num = input('Enter verify code:')
data = {
	'captcha_code': verify_num,
	'url': '/films?__oceanus_captcha=1',
	'ticket': 'Y2IzMDM2YWYtYTRlNi00ZjNjLTgxNGEtNTIwMjg5MjMxNTllI0FDVElPTiNPQ0VBTlVTX1BSRURJQ0FURV9jYjMwMzZhZi1hNGU2LTRmM2MtODE0YS01MjAyODkyMzE1OWVfY29tLm1vdmllLm15d3d3X2FwcF9WZXJpZnlCbG9ja0FjdGlvbl9SZXEuX2pzb24uZGF0YS5pcF8zNi4xNDkuMTU1LjE4OSNvY2VhbnVz',
	'request_code': '684eb61fa6ec4543914ea75e1b1d9229',
	'contact': ''
}
url2 = 'http://maoyan.com/films?__oceanus_captcha=1'
res = requests.post(url2, data)