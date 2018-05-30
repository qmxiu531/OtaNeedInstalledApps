# -*- coding: utf-8 -*-
import queue,threading,requests,json,re
from bs4 import BeautifulSoup
from com.gionee.ota.util import Util
from com.gionee.ota.Base import *
from com.gionee.ota import gol
__author__ = 'suse'

logger = Util.logger
savePath = "downloadApps"
rs = {}
class DownloadAppMulti():
     def __init__(self,**downloadAppsDict):
            isExists=os.path.exists(savePath)
            if not isExists:
                os.makedirs(savePath)
                logger.info(savePath+' 创建成功')
            gol._init()
            gol.set_value("appFilePath",savePath)
            self.downloadAppsDict = downloadAppsDict
            self.threadNameList = ["Thread-1","Thread-2","Thread-3","Thread-4","Thread-5"]
            self.workQueue = queue.Queue(len(downloadAppsDict))
            print(self.workQueue.maxsize)
            self.threads=[]
            self.threadID = 1
            for pkgName,appAddrs in downloadAppsDict.items():
                self.workQueue.put(pkgName+";"+appAddrs[2])
     def startMultiThread(self):

            for tName in self.threadNameList:
                thread = AppDownloadThread(self.threadID,tName,self.workQueue)
                thread.start()
                self.threads.append(thread)
                self.threadID +=1
            for i in self.threads:
               i.join()
            return rs
class AppDownloadThread(threading.Thread):
    def __init__(self,threadID,name,q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    def run(self):
        print("Staring"+self.name)
        while True:
            if self.q.qsize() > 0:
                downloadInfo = self.q.get()
                appDownloadAddr = downloadInfo.split(";")[1]
                pkgName = downloadInfo.split(";")[0]
                rc=self.download_from_gn(self.name,downloadInfo)
                if(not rc[0]):#如果从软件商店下载失败，则尝试从应用宝上下载
                    rc=self.download_from_qq(self.name,downloadInfo)
                rs[pkgName] = rc
            else:
                break
        print("Exiting "+self.name)
    def download_from_qq(self,threadName,downloadInfo):
                rc =[]
                try:
                    appDownloadAddr =downloadInfo.split(";")[1]
                    pkgName=downloadInfo.split(";")[0]
                    print("pkgName="+pkgName)
                    m = re.search(r'fsname=(.+)&csr=',appDownloadAddr)
                    fileName=m.group(1)
                    fileList=os.listdir(savePath)
                    for file in fileList:
                        item=os.path.basename(file)
                        path = os.path.join(savePath,file)
                        if os.path.isfile(path):
                            # print("item="+item)
                            # print("fileName="+fileName)
                            if(fileName == item):#需要下载的文件已经存在，不重复下载
                                logger.info("pkgName="+pkgName+" 下载文件="+fileName+"已经存在，无需再下载")
                                rc.append(True)
                                rc.append(4)
                                rc.append(fileName)
                                rc.append("fileName="+fileName+"已经存在，无需下载")
                                return rc
                        else:
                            logger.error("item="+item+"不是文件")
                            continue
                    logger.info("开始从应用宝上下载"+appDownloadAddr)
                    logger.info("开始从应用宝上下载"+pkgName)
                    r = requests.get(appDownloadAddr)
                    filePath=os.path.join(savePath,fileName)
                    with open(filePath, "wb") as file:
                        file.write(r.content)
                    rc.append(True)
                    rc.append(0)
                    rc.append(fileName)
                    logger.info("pkgName="+pkgName+"的下载文件="+appDownloadAddr+"下载成功")
                except:
                    rc.append(False)
                    rc.append(3)
                    rc.append(Base.printErr("\n\tpkgName="+pkgName+"应用宝下载APP失败：%s"%appDownloadAddr, True))
                    logger.error("pkgName="+pkgName+"下载文件失败="+appDownloadAddr)
                return rc
    def download_from_gn(self,threadName,downloadInfo):
                rc =[]
                try:
                    appDownloadAddr =downloadInfo.split(";")[1]
                    pkgName=downloadInfo.split(";")[0]
                    fileName = appDownloadAddr.split("/")[-1]
                    print("fileName="+fileName)
                    fileList=os.listdir(savePath)
                    for file in fileList:
                        item=os.path.basename(file)
                        path = os.path.join(savePath,file)
                        if os.path.isfile(path):
                            # print("item="+item)
                            # print("fileName="+fileName)
                            if(fileName == item):#需要下载的文件已经存在，不重复下载
                                logger.info(pkgName+" 的下载文件="+fileName+"已经存在，无需再下载")
                                rc.append(True)
                                rc.append(4)
                                rc.append(fileName)
                                rc.append("fileName="+fileName+"已经存在，无需下载")
                                return rc
                        else:
                            logger.error("item="+item+"不是文件")
                            continue
                    logger.info("pkgName="+pkgName+" 开始从软件商店上下载"+fileName)
                    r = requests.get(appDownloadAddr)
                    filePath=os.path.join(savePath,fileName)
                    with open(filePath, "wb") as file:
                        file.write(r.content)
                    rc.append(True)
                    rc.append(0)
                    rc.append(fileName)
                    logger.info("pkgName="+pkgName+" 的下载地址="+appDownloadAddr+"下载成功")
                except:
                    rc.append(False)
                    rc.append(3)
                    rc.append(Base.printErr("\n\tpkgName="+pkgName+" 软件商店下载APP失败：%s"%appDownloadAddr, True))
                    logger.error("pkgName="+pkgName+"下载文件失败="+appDownloadAddr)
                return rc

