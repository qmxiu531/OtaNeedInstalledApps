# -*- coding: utf-8 -*-
__author__ = 'suse'
import requests
from bs4 import BeautifulSoup
from com.gionee.ota.Base import *
import os,sys,re
import shutil
import time,datetime
import urllib
from com.gionee.ota import gol
from com.gionee.ota.util import Util
import threading
import queue,json
rs = {}
logger = Util.logger
class MultiGetDownloadAddr():
        def __init__(self,pkgNameList):
            self.pkgNameList = pkgNameList
            self.threadNameList = ["Thread-1","Thread-2","Thread-3","Thread-4","Thread-5"]
            self.workQueue = queue.Queue(len(pkgNameList))
            print(self.workQueue.maxsize)
            self.threads=[]
            self.threadID = 1
            for pkgName in pkgNameList:
                self.workQueue.put(pkgName)
        def startMultiThread(self):

            for tName in self.threadNameList:
                thread = AppDownloadAddrThread(self.threadID,tName,self.workQueue)
                thread.start()
                self.threads.append(thread)
                self.threadID +=1
            for i in self.threads:
               i.join()
            return rs

class AppDownloadAddrThread(threading.Thread):
    def __init__(self,threadID,name,q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    def run(self):
        print("Staring"+self.name)
        while True:
            if self.q.qsize() > 0:
                pkgName = self.q.get()
                rc=self.process_gn_data(self.name,pkgName)
                if(not rc[0]):#如果从软件商店下载失败，则尝试从应用宝上下载
                    rc=self.process_qq_data(self.name,pkgName)
                rs[pkgName] = rc
            else:
                break
        print("Exiting "+self.name)
    def process_qq_data(self,threadName,pkgName):
                rc =[]
                try:
                    logger.info("开始从应用宝上下载"+pkgName)
                    url = "http://sj.qq.com/myapp/detail.htm?apkName="+pkgName
                    req = requests.get(url)
                    html = req.text
                    soup = BeautifulSoup(html,"lxml")
                    # print(soup.prettify())
                    addrs=soup.find_all(class_="det-down-btn")[0]
                    appDownloadAddr = addrs.attrs['data-apkurl']
                    if appDownloadAddr.strip():
                        rc.append(True)
                        rc.append(0)
                        rc.append(appDownloadAddr)
                        logger.info(pkgName+"获取下载地址成功")
                        logger.info("下载地址="+appDownloadAddr)
                    else:
                        rc.append(False)
                        rc.append(1)
                        rc.append(appDownloadAddr)
                        logger.error(pkgName+"获取下载地址失败")
                        logger.error("失败的下载地址="+appDownloadAddr)
                except:
                    rc.append(False)
                    rc.append(2)
                    rc.append(Base.printErr("\n\t应用宝获取APP地址失败：%s"%url, True))
                return rc
    def process_gn_data(self,threadName,pkgName):
                rc = []
                try:
                    logger.info("开始从‘软件商店’上下载"+pkgName)
                    print("%s processing %s"%(threadName,pkgName))
                    url = "http://api.appgionee.com/api/gionee/getDownloadUrl?packageName="
                    logger.info(url+pkgName)
                    req = requests.get(url+pkgName)
                    python_to_json = req.text
                    downloadAddrJson = json.loads(python_to_json)
                    appDownloadAddr = downloadAddrJson["downloadUrl"]
                    if appDownloadAddr.strip():
                        rc.append(True)
                        rc.append(0)
                        rc.append(appDownloadAddr)
                        logger.info(pkgName+"获取下载地址成功")
                        logger.info("下载地址="+appDownloadAddr)
                    else:
                        rc.append(False)
                        rc.append(1)
                        rc.append(appDownloadAddr)
                        logger.error(pkgName+"获取下载地址失败")
                        logger.error("失败的下载地址="+appDownloadAddr)

                except:
                    rc.append(False)
                    rc.append(2)
                    rc.append(Base.printErr("\n\t软件商店获取APP地址失败：%s"%url, True))
                return rc

if __name__ == '__main__':
        threadList = ["Thread-1","Thread-2","Thread-3"]
        nameList = ["One","Two","Three","Four","Five"]
        workQueue = queue.Queue()
        threads = []
        threadID = 1
            #创建新线程
         #填充队列
        for word in nameList:
            workQueue.put(word)
        for tName in threadList:
            thread = AppDownloadAddrThread(threadID,tName,workQueue)
            thread.start()
            threads.append(thread)
            threadID +=1
        for i in threads:
               i.join()
        print("Exiting Main Thread")
