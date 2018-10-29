# -*- coding:utf-8 -*-
import requests
import json, time, random
from xlwt import Workbook
import threading
import traceback

#抓取Riview
class TaobaoComments:
    #页面初始化
    def __init__(self):
        self.USER_AGENTS = [
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
            "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
            "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
            "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        ]
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"
        }
        self.ws = Workbook(encoding='utf-8')
        self.itemids = ['566650346286']
        #'575397228277','575773187191'
    def getAllReview(self):
        #robj = ( 'id', 'auctionSku', 'sellerId', 'displayUserNick', 'goldUser', 'userVipLevel', 'position', 'rateContent',
        #    'useful', 'rateDate','appendComment', 'appendCommentDate', 'appendCommentPics', 'appendCommentReply', 'reply', 'pics',
        #    'tradeEndTime', 'fromMall', 'cmsSource', 'gmtCreateTime')
        robj = ('id','rateContent','rateDate')

        self.lock_fetch = threading.Lock()
        threads = []

        for itemid in self.itemids:
            w = self.ws.add_sheet(itemid + u"商品评价")
            pos = 0
            for key in robj:
                w.write(0, pos, robj[pos])
                pos = pos + 1
            t = threading.Thread(target=self.getReview, args=(w, itemid))
            t.start()
            threads.append(t)
        for thread in threads:
            thread.join()
        print('All jobs done!')

    def getReview(self, w, itemid):
        currentpage = 1
        totalpage = 99999
        excel_row = 1
        proxies = {}
        headers = self.headers
        while currentpage <= totalpage :
            # bosci 1990484446, dyson 2089100916
            url = "https://rate.tmall.com/list_detail_rate.htm?itemId=" + itemid + "&sellerId=761679524&order=3&callback=jsonp867&currentPage=" + str(currentpage)
            #print(url)
            response = requests.get(url, headers=headers, proxies=proxies)
            try:
                rtext = response.text
                rjson = json.loads(rtext[11:len(rtext)-1])
            except:
                traceback.print_exc()
                print('item=' + itemid + ', pause for reset crawler...')
                headers['Referer'] = "https://www.tmall.com/"
                headers['User-Agent'] = random.choice(self.USER_AGENTS)
                time.sleep(random.uniform(10, 20))
            else:
                totalpage = rjson['rateDetail']['paginator']['lastPage']
                ratelist = rjson['rateDetail']['rateList']
                # 写入EXCEL
                for obj in ratelist:
                    id = str(obj['id'])
                    #auctionSku = obj['auctionSku']
                    #sellerId = obj['sellerId']
                    #displayUserNick = obj['displayUserNick']
                    #goldUser = obj['goldUser']
                    #userVipLevel = obj['userVipLevel']
                    #position = obj['position']
                    rateContent = obj['rateContent']
                    #useful = obj['useful']
                    rateDate = obj['rateDate']
                    #appendComment = ''
                    #appendCommentDate = ''
                    #appendCommentPics = ''
                    #appendCommentReply = ''
                    #appendCommentObj = obj['appendComment']
                    #if appendCommentObj:
                    #    appendComment = appendCommentObj['content']
                    #    appendCommentDate = appendCommentObj['commentTime']
                    #    appendCommentPics = ', '.join(appendCommentObj['pics'])
                    #    appendCommentReply = appendCommentObj['reply']
                    #reply = obj['reply']
                    #pics = ', '.join(obj['pics'])
                    #tradeEndTime = obj['tradeEndTime']['time']
                    #fromMall = obj['fromMall']
                    #cmsSource = obj['cmsSource']
                    #gmtCreateTime = obj['gmtCreateTime']['time']
                    #robj = (id, auctionSku, sellerId, displayUserNick, goldUser, userVipLevel, position, rateContent, useful, rateDate,
                    #        appendComment, appendCommentDate, appendCommentPics, appendCommentReply, reply, pics, tradeEndTime, fromMall, cmsSource, gmtCreateTime)
                    robj = (id, rateContent, rateDate)
                    pos = 0
                    self.lock_fetch.acquire()
                    for key in robj:
                        #print(str(pos)+':'+str(robj[pos]))
                        w.write(excel_row, pos, robj[pos])
                        pos = pos + 1
                    self.lock_fetch.release()
                    excel_row = excel_row + 1
                print('done item ' + itemid +  ', page ' + str(currentpage))
                currentpage = currentpage + 1
            time.sleep(random.uniform(1, 3))
        self.lock_fetch.acquire()
        self.ws.save(r'/Users/swz/workspace/python/movie/taobao-comments.xls')
        self.lock_fetch.release()
        print('done item ' + itemid + ', page all')

spider = TaobaoComments()
spider.getAllReview()