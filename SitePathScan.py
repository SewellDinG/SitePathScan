#! /usr/bin/python
# -*- coding:utf-8 -*-

import queue
import asyncio
import argparse
from aiohttp import ClientSession

class SitePathScan(object):
    def __init__(self, scanSite, scanDict, scanOutput,coroutineNum):
        print('* SitePathScan ready to start.')
        self.scanSite = scanSite if scanSite.find('://') != -1 else 'http://%s' % scanSite
        print('* Current target:',self.scanSite)
        self.scanDict = scanDict
        self.scanOutput = scanSite.rstrip('/').replace('https://', '').replace('http://', '').replace('.', '_')+'.txt' if scanOutput == 0 else scanOutput
        self.loadDict(self.scanDict)
        self.coroutineNum = coroutineNum
        self.loop = asyncio.get_event_loop()  # 创建一个事件循环
        self.sema = asyncio.Semaphore(self.coroutineNum)
        self.tasks = []
        self.flag = 0

    def loadDict(self, dict_list):
        self.q = queue.Queue()
        with open(dict_list) as f:
            for line in f:
                self.q.put(line.strip())
        self.data = self.q.qsize()
        if self.data > 0:
            print('* Total Dictionary:',self.data)
        else:
            print('* NO default.txt')
            quit()

    def writeOutput(self, result):
        with open(self.scanOutput, 'a') as f:
            f.write(result + '\n')

    async def scan(self, url):
        headers = {
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',
                'Referer':'https://www.baidu.com',
                'Accept-Encoding':'gzip, deflate',
                'Connection':'keep-alive',
            }
        try:
            async with self.sema:
                async with ClientSession() as session:
                    async with session.head(url, headers=headers,timeout=10) as resp:
                        code = resp.status
                        if code == 200 or code == 301 or code == 403:
                            print('[ %i ] %s' % (code, url))
                            self.writeOutput('[ %i ] %s' % (code, url))
        except Exception as e:
            # print(e)
            pass

    def run(self):
        while True:
            self.flag += 1
            url = self.scanSite + self.q.get()
            future = asyncio.ensure_future(self.scan(url))
            self.tasks.append(future) # 创建多个协程任务的列表，然后将这些协程注册到事件循环中。
            if self.flag == self.data:
                break
        try:
            self.loop.run_until_complete(asyncio.wait(self.tasks))   # 将协程注册到事件循环，并启动事件循环
            self.loop.close()
        except CancelledError as e:
            print('* Warning:CancelledError.')

if __name__ == '__main__':
    # main()
    banner = '''\
     ____  _ _       ____       _   _     ____
    / ___|(_) |_ ___|  _ \ __ _| |_| |__ / ___|  ___ __ _ _ ___
    \___ \| | __/ _ \ |_) / _` | __| '_ /\___ \ / __/ _` | '_  /
     ___) | | ||  __/  __/ (_| | |_| | | |___) | (_| (_| | | | |
    |____/|_|\__\___|_|   \__,_|\__|_| |_|____/ \___\__,_|_| |_|
    '''
    print(banner)
    parser = argparse.ArgumentParser(description="This script uses the aiohttp library's head() method to determine the status word.")
    # 位置参数
    parser.add_argument("website", type=str, help="The website that needs to be scanned")
    # 可选参数
    parser.add_argument('-d', '--dict', dest="scanDict", help="Dictionary for scanning", type=str, default="dict/default.txt")
    parser.add_argument('-o', '--output', dest="scanOutput", help="Results saved files", type=str, default=0)
    parser.add_argument('-t', '--thread', dest="coroutineNum", help="Number of coroutine running the program", type=int, default=50)
    args = parser.parse_args()
    scan = SitePathScan(args.website, args.scanDict, args.scanOutput, args.coroutineNum)
    # print 'Scan Start!!!'
    scan.run()
    print("* End of scan.")
