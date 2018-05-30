# -*- coding: utf-8 -*-
import pkg_resources
from com.gionee.ota import Base
from com.gionee.ota.excel import excel
from com.gionee.ota.request import downloadApp
import datetime
from com.gionee.ota import gol
from com.gionee.ota.util import Util
import os,sys
from com.gionee.ota.intall import Install
import subprocess
from com.gionee.ota.log import adblog
from com.gionee.ota.apps.qqApps import QqApp
from com.gionee.ota.apps.appsMgr import AppsMgr
from com.gionee.ota.intall.installMgr import InstallMgr
from com.gionee.ota.traversal.bvtTraversal import BvtTraversal
import requests

class OTAThirdAppsTest():
    def thirdAppsTest(self):
        xlsxFiles=Util.filterFiles(".",['.xlsx'])
        if(len(xlsxFiles)<1):
            logger.error("当前目录没有需要测试应用的xlsx文件")
            sys.exit()
        logger.info("当前需要测试的应用的xlsx文件:"+xlsxFiles[0])
        ec =excel.Excel(xlsxFiles[0])
        sheetNames=ec.getAllSheetNames()
        logger.info("存在的sheet有:")
        logger.info(sheetNames)
        testedProjectName = input("请输入被测试的项目名称:\n ********************** \n eg:F100,金钢全网通 \n **********************\n请输入:")

        if testedProjectName in sheetNames:
            logger.info("接收到项目:"+testedProjectName)
        else:
            logger.error(testedProjectName+"的sheet不存在")
            sys.exit()
        install = Install.Install()
        install.finddevices()
        testedDevice = input("请输入被测试手机串号:\n ********************** \n eg:CYHAVCYLEULJB6FU \n **********************\n请输入:")
        logger.info("被测手机串号:"+testedDevice)
        logger.info(begin)
        pkg_dict = ec.get_pkg_values("三方汇总表","应用名称","应用包名")
        testedApps=ec.get_tested_app_name(testedProjectName,"应用名称")
        # download=downloadApp.Download()
        appsMgr = AppsMgr()
        downloadFromGnAppType = 1
        downloadFromQqAppType = 2
        downloadRsDict = appsMgr.downloadApps(downloadFromGnAppType,*testedApps,**pkg_dict)
        installMgr = InstallMgr(testedDevice)
        installMgr.installApps(**downloadRsDict)
        #遍历APP并点掉弹出框


        bvtTraversal = BvtTraversal()
        bvtTraversal.lanchAppsTest(testedDevice)



if __name__ == '__main__':

    begin = datetime.datetime.now()
    logger = Util.logger
    logger.info("\n\n")
    logger.info("**************************begin***************************")
    otaThirdAppsTest = OTAThirdAppsTest()
    otaThirdAppsTest.thirdAppsTest()
    end = datetime.datetime.now()
    k = end - begin
    logger.info("运行时长")
    logger.info(k)
    logger.info("**************************end***************************")

