# -*- coding: utf-8 -*-
__author__ = 'suse'
import requests
from bs4 import BeautifulSoup
from com.gionee.ota.Base import *
import sys
import os
import re
import shutil
import time
import datetime
import urllib
from com.gionee.ota import gol
from com.gionee.ota.util import Util

class Download(object):
    savePath=""
    def __init__(self):
        # curDir=Base.get_cur_dir(__file__)
        # self.savePath = os.path.join(curDir,'downloadApps')
        self.logger = Util.logger
        self.savePath = "downloadApps"
        isExists=os.path.exists(self.savePath)
        print(isExists)
        if not isExists:
            os.makedirs(self.savePath)
            self.logger.info(self.savePath+' 创建成功')
        gol._init()
        gol.set_value("appFilePath",self.savePath)

        # timeStampDir = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
        # # print(timeStampDir+"rrrr")
        # self.savePath = os.path.join(downloadPath,timeStampDir)
        # # print(self.savePath+"yyyyy")
        # isExists=os.path.exists(self.savePath)
        # if not isExists:
        #     os.makedirs(self.savePath)
        #     print(self.savePath+' 创建成功')
        #     gol.set_value("appFilePath",self.savePath)
    def getDownloadAddr(self,url):
        rc = []
        try:
            # "http://sj.qq.com/myapp/detail.htm?apkName=com.xunmeng.pinduoduo"
            req = requests.get(url)
            html = req.text
            soup = BeautifulSoup(html,"lxml")
            # print(soup.prettify())
            addrs=soup.find_all(class_="det-down-btn")[0]
            self.logger.info(addrs.attrs['data-apkurl'])
            # for addr in addrs:
            #   print(addr.attrs['data-apkurl'])
            # return addrs.attrs['data-apkurl']
            rc.append(True)
            rc.append(0)
            rc.append(addrs.attrs['data-apkurl'])
        except:
            rc.append(False)
            rc.append(2)
            rc.append(Base.printErr("\n\t应用宝获取APP地址失败：%s"%url, True))
        return rc
    def download(self,downloadAddr=""):
        rc = []
        try:

            # isExists = os.path.exists(savePath)
                # fsname=com.xunmeng.pinduoduo_4.4.0_4040.apk&csr=1bbd
            m = re.search(r'fsname=(.+)&csr=',downloadAddr)
            fileName=m.group(1)
            fileList=os.listdir(self.savePath)
            for file in fileList:
                item=os.path.basename(file)
                path = os.path.join(self.savePath,file)
                if os.path.isfile(path):
                    # print("item="+item)
                    # print("fileName="+fileName)
                    if(fileName == item):#需要下载的文件已经存在，不重复下载
                        print("not need download")
                        rc.append(True)
                        rc.append(4)
                        rc.append(fileName)
                        rc.append("fileName="+fileName+"已经存在，无需下载")
                        return rc
                else:
                    self.logger.error("item="+item+"不是文件")
                    continue

            # print(fileName)
            # print(self.savePath+"6666")
            r = requests.get(downloadAddr)
            filePath=os.path.join(self.savePath,fileName)
            with open(filePath, "wb") as file:
                file.write(r.content)
            rc.append(True)
            rc.append(0)
            rc.append(fileName)
            rc.append("")
        except:
              rc.append(False)
              rc.append(3)
              rc.append(Base.printErr("\n\t应用宝下载APP失败：%s"%downloadAddr, True))
        return rc
if __name__ == '__main__':
    download=Download()
    # addr=download.getDownloadAddr("http://sj.qq.com/myapp/detail.htm?apkName=com.xunmeng.pinduoduo")
    # try:
    addr=download.getDownloadAddr("http://sj.qq.com/myapp/detail.htm?apkName=fhfhgh")
    download.download(downloadAddr = addr)
        # print(addr)
    # except:

