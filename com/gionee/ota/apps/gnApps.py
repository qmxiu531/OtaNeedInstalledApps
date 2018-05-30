# -*- coding: utf-8 -*-
import requests
import os
from com.gionee.ota import gol
import json
from com.gionee.ota.util import Util
from com.gionee.ota.Base import *

__author__ = 'suse'
url="http://api.appgionee.com/api/gionee/getDownloadUrl?packageName="
logger = Util.logger
class GN_Apps():
    def __init__(self):
        # self.pkgName = pkgName
        # self.apkUrl = url+pkgName
        self.appAddr = ""
        self.rc = []
        self.savePath = "downloadApps"
        isExists=os.path.exists(self.savePath)
        if not isExists:
            os.makedirs(self.savePath)
            logger.info(self.savePath+' 创建成功')
        gol._init()
        gol.set_value("appFilePath",self.savePath)

    def getDownloadAddr(self,pkgName):
        try:
            self.pkgName = pkgName
            self.apkUrl = url+pkgName
            req = requests.get(self.apkUrl)
            python_to_json = req.text
            downloadAddrJson = json.loads(python_to_json)
            self.appAddr = downloadAddrJson["downloadUrl"]

            if self.appAddr.strip():
                self.rc.append(True)
                self.rc.append(0)
                self.rc.append(self.appAddr)
                logger.info(self.pkgName+"获取下载地址成功")
                logger.info("下载地址="+self.appAddr)
            else:
                self.rc.append(False)
                self.rc.append(1)
                self.rc.append(self.appAddr)
                logger.error(self.pkgName+"获取下载地址失败")
                logger.error("失败的下载地址="+self.appAddr)

        except:
            logger.error(self.pkgName+"获取下载地址失败")
            logger.error("获取下载地址的页面url="+self.apkUrl)
            self.rc.append(False)
            self.rc.append(2)
            self.rc.append(Base.printErr("\n\t应用宝获取APP地址失败：%s"%self.apkUrl, True))
        return self.rc

    def download(self):
        try:
            if(self.rc[0] == False):
                return self.rc
            appDownloadAddr = self.rc[2]
            self.rc = []
            fileName = self.appAddr.split("/")[-1]
            print("fileName="+fileName)
            fileList=os.listdir(self.savePath)
            for file in fileList:
                item=os.path.basename(file)
                path = os.path.join(self.savePath,file)
                if os.path.isfile(path):
                    # print("item="+item)
                    # print("fileName="+fileName)
                    if(fileName == item):#需要下载的文件已经存在，不重复下载
                        logger.info(self.pkgName+"的下载文件="+fileName+"已经存在，无需再下载")
                        self.rc.append(True)
                        self.rc.append(4)
                        self.rc.append(fileName)
                        self.rc.append("fileName="+fileName+"已经存在，无需下载")
                        return self.rc
                else:
                    logger.error("item="+item+"不是文件")
                    continue
            r = requests.get(appDownloadAddr)
            filePath=os.path.join(self.savePath,fileName)
            with open(filePath, "wb") as file:
                    file.write(r.content)
            self.rc.append(True)
            self.rc.append(0)
            self.rc.append(fileName)
            self.rc.append("")
            logger.info(self.pkgName+"下载成功")
        except:
            self.rc.append(False)
            self.rc.append(3)
            self.rc.append(Base.printErr("\n\t应用宝下载APP失败：%s"%appDownloadAddr, True))
            logger.error("下载文件失败="+appDownloadAddr)
        return self.rc


if __name__ == '__main__':
    gnApps = GN_Apps("com.tencent.qqmusic")
    gnApps.getDownloadAddr()
    gnApps.download()





