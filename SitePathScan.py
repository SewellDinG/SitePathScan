#! /usr/bin/python
# -*- coding:utf-8 -*-

import time
import Queue
import urllib2
import requests
import argparse
import threading

class SitePathScan(object):
    def __init__(self, scanSite, scanDict, scanOutput,threadNum):
        print '* SitePathScan ready to start.'
        self.scanSite = scanSite if scanSite.find('://') != -1 else 'http://%s' % scanSite
        print '* Current target:',self.scanSite
        self.scanDict = scanDict
        self.scanOutput = scanSite.rstrip('/').replace('https://', '').replace('http://', '').replace('.', '_')+'.txt' if scanOutput == 0 else scanOutput
        self.loadDict(self.scanDict)
        self.threadNum = threadNum
        # Prepare threading lock
        self.lock = threading.Lock()

    def loadDict(self, dict_list):
        self.q = Queue.Queue()
        with open(dict_list) as f:
            for line in f:
                self.q.put(line.strip())
        self.date = self.q.qsize()
        if self.date > 0:
            print '* Total Dictionary:',self.date
        else:
            print '* NO default.txt'
            quit()

    def writeOutput(self, result):
        # Play threading lock
        self.lock.acquire()
        with open(self.scanOutput, 'a') as f:
            f.write(result + '\n')
        self.lock.release()

    def scan(self, url):
        html_result = 0
        status_code = [200]
        status_text = ['Forbidden','Internal Server Error']
        headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',
            'Referer':'https://www.baidu.com',
            'Accept-Encoding':'gzip, deflate',
            'Connection':'keep-alive',
        }
        # urllib2 - head()
        try:
            req = urllib2.Request(url,headers=headers)
            html_result = urllib2.urlopen(req)
            # print html_result.code   # 状态码，headers头
            if html_result.code in status_code:
                print '[ %i ] %s' % (html_result.code, html_result.url)
                self.writeOutput('[ %i ] %s' % (html_result.code, html_result.url))
            # 分析文件的大小，利用于扫描压缩文件
            # meta = html_result.info()
            # file_size = int(meta.getheaders("Content-Length")[0])
            # print file_size
        except urllib2.URLError, e:
            # print e.reason # 403-'Forbidden',500-'Internal Server Error'
            if e.reason in status_text:
                print '[ Forbidden ] %s' % url
                self.writeOutput('[ Forbidden ] %s' % url)
        # # requests - get()
        # try:
        #     html_result = requests.get(url, headers=headers, timeout=3)
        #     # print html_result.url
        # except requests.exceptions.ConnectTimeout:
        #     print 'The request timed out.'
        # finally:
        #     if html_result.status_code in status_code:
        #         print '[ %i ] %s' % (html_result.status_code, html_result.url)
        #         self.writeOutput('[ %i ] %s' % (html_result.status_code, html_result.url))

    def run(self):
        # run to q.empty() == flase ,so q have things
        if not self.q.empty():
            url = self.scanSite + self.q.get()
            self.scan(url)

if __name__ == '__main__':
    # main()
    banner = '''\
     ____  _ _       ____       _   _     ____
    / ___|(_) |_ ___|  _ \ __ _| |_| |__ / ___|  ___ __ _ _ ___
    \___ \| | __/ _ \ |_) / _` | __| '_ /\___ \ / __/ _` | '_  /
     ___) | | ||  __/  __/ (_| | |_| | | |___) | (_| (_| | | | |
    |____/|_|\__\___|_|   \__,_|\__|_| |_|____/ \___\__,_|_| |_|
    '''
    print banner
    parser = argparse.ArgumentParser(description="This script uses the urllib library's head() method to determine the status word and error status。")
    # 位置参数
    parser.add_argument("website", type=str, help="The website that needs to be scanned")
    # 可选参数
    parser.add_argument('-d', '--dict', dest="scanDict", help="Dictionary for scanning", type=str, default="dict/default.txt")
    parser.add_argument('-o', '--output', dest="scanOutput", help="Results saved files", type=str, default=0)
    parser.add_argument('-t', '--thread', dest="threadNum", help="Number of threads running the program", type=int, default=50)
    args = parser.parse_args()
    scan = SitePathScan(args.website, args.scanDict, args.scanOutput, args.threadNum)
    # print 'Scan Start!!!'
    def thread():
        for i in range(args.threadNum):
            t = threading.Thread(target=scan.run)
            t.setDaemon(True)
            t.start()
            # t.join() # no

    while True:
        if  scan.q.empty() == True and threading.activeCount() <= 1 :
            break
        if threading.activeCount() <= 1:
            thread()
        else:
            try:
                # flush
                time.sleep(0.1)
            except KeyboardInterrupt, e:
                print '[ WARNING ] User aborted, wait all slave threads to exit, current(%i)' % threading.activeCount()

    print "* End of scan."
