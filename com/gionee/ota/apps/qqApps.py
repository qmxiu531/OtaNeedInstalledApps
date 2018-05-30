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
url="http://sj.qq.com/myapp/detail.htm?apkName="
class QqApp():

    def __init__(self):
        # self.pkgName = pkgName
        # self.apkUrl = url+pkgName
        self.logger = Util.logger
        self.appAddr = ""
        self.savePath = "downloadApps"
        isExists=os.path.exists(self.savePath)
        if not isExists:
            os.makedirs(self.savePath)
            self.logger.info(self.savePath+' 创建成功')
        gol._init()
        gol.set_value("appFilePath",self.savePath)
        self.rc = []
    def getDownloadAddr(self,pkgName):

        try:
            self.pkgName = pkgName
            self.apkUrl = url+pkgName
            # "http://sj.qq.com/myapp/detail.htm?apkName=com.xunmeng.pinduoduo"
            req = requests.get(self.apkUrl)
            html = req.text
            soup = BeautifulSoup(html,"lxml")
            # print(soup.prettify())
            addrs=soup.find_all(class_="det-down-btn")[0]
            self.logger.info(addrs.attrs['data-apkurl'])
            # for addr in addrs:
            #   print(addr.attrs['data-apkurl'])
            # return addrs.attrs['data-apkurl']
            self.rc.append(True)
            self.rc.append(0)
            self.rc.append(addrs.attrs['data-apkurl'])
            self.logger.info(self.pkgName+"获取下载地址成功")
            self.logger.info("下载地址="+addrs.attrs['data-apkurl'])
        except:
            self.logger.error(self.pkgName+"获取下载地址失败")
            self.logger.error("获取下载地址的页面url="+self.apkUrl)
            self.rc.append(False)
            self.rc.append(2)
            self.rc.append(Base.printErr("\n\t应用宝获取APP地址失败：%s"%self.apkUrl, True))
        return self.rc
    def download(self):
        try:
            if(self.rc[0] == False):
                return self.rc
            appDownloadAddr = self.rc[2]
            # print("++++++++++++++++")
            # print("appDownloadAddr="+appDownloadAddr)
            self.rc = []
            # isExists = os.path.exists(savePath)
                # fsname=com.xunmeng.pinduoduo_4.4.0_4040.apk&csr=1bbd
            m = re.search(r'fsname=(.+)&csr=',appDownloadAddr)
            fileName=m.group(1)
            print("fileName="+fileName)
            fileList=os.listdir(self.savePath)
            for file in fileList:
                item=os.path.basename(file)
                path = os.path.join(self.savePath,file)
                if os.path.isfile(path):
                    # print("item="+item)
                    # print("fileName="+fileName)
                    if(fileName == item):#需要下载的文件已经存在，不重复下载
                        self.logger.info(self.pkgName+"的下载文件="+fileName+"已经存在，无需再下载")
                        self.rc.append(True)
                        self.rc.append(4)
                        self.rc.append(fileName)
                        self.rc.append("fileName="+fileName+"已经存在，无需下载")
                        return self.rc
                else:
                    self.logger.error("item="+item+"不是文件")
                    continue

            # print(appDownloadAddr+"99999999999999999")
            # print(self.savePath+"6666")
            r = requests.get(appDownloadAddr)
            filePath=os.path.join(self.savePath,fileName)
            with open(filePath, "wb") as file:
                file.write(r.content)
            self.rc.append(True)
            self.rc.append(0)
            self.rc.append(fileName)
            self.rc.append("")
            self.logger.info(self.pkgName+"下载成功")
        except:
              self.rc.append(False)
              self.rc.append(3)
              self.rc.append(Base.printErr("\n\t应用宝下载APP失败：%s"%appDownloadAddr, True))
              self.logger.error("下载文件失败="+appDownloadAddr)
        return self.rc

