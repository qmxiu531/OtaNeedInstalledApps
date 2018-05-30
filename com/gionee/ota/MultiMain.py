# -*- coding: utf-8 -*-
from com.gionee.ota import Base
from com.gionee.ota.excel import excel
from com.gionee.ota.request import downloadApp
import datetime
from com.gionee.ota import gol
from com.gionee.ota.util import Util
import os,sys
from com.gionee.ota.intall import Install
from com.gionee.ota.request import downloadAddrMulti
from com.gionee.ota.request.downloadAppMulti import DownloadAppMulti
from com.gionee.ota.intall.installMulti import MultiInstall
if __name__ == '__main__':
    logger = Util.logger
    logger.info("\n\n")
    logger.info("**************************begin***************************")
    Base.Base.get_cur_dir(__file__)
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
    begin = datetime.datetime.now()
    logger.info(begin)
    curDir=Base.Base.get_cur_dir(__file__)
    # print("curDir="+curDir)
    pkg_dict = ec.get_pkg_values("三方汇总表","应用名称","应用包名")
    # print(pkg_dict)
    # exit(1)
    testedApps=ec.get_tested_app_name(testedProjectName,"应用名称")
    resultDict = {}
    needTestedPkgNameList = []
    for app in testedApps:
        rc = []
        if(pkg_dict.__contains__(app) and pkg_dict.get(app).strip()!=''):
             needTestedPkgNameList.append(pkg_dict.get(app))
        else:
            rc.append(False)
            rc.append(1)
            rc.append("app="+app+"没有找到对应的包名")
            resultDict[app] = rc
    multiDown = downloadAddrMulti.MultiGetDownloadAddr(needTestedPkgNameList)
    addrDictRs=multiDown.startMultiThread()
    resultDict.update(addrDictRs)
    print(resultDict)
    successAppDownloadAddrDict={}
    for appName,appAddrRs in resultDict.items():
        if(appAddrRs[0]):
            successAppDownloadAddrDict[appName] =appAddrRs
    print(successAppDownloadAddrDict)
    multiDownloadApps =DownloadAppMulti(**successAppDownloadAddrDict)
    rsDict=multiDownloadApps.startMultiThread()
    logger.info(rsDict)
    installAddrList=[]
    for pkgName,downloadRs in rsDict.items():
                if downloadRs[0]:
                    filepath = os.path.join(gol.get_value("appFilePath"), downloadRs[2])
                    installAddrList.append(filepath)
    multiInstall = MultiInstall("CYHAVCYLEULJB6FU",installAddrList)
    multiInstall.startMultiThread()
    sys.exit()

    succApps =[]
    failApps = []
    for name,rs in resultDict.items():
        if(rs[0] == True):
            succApps.append(name)
        else:
            failApps.append(name)
    logger.info("**********成功下载APP*************")
    logger.info("数量="+str(len(succApps)))
    logger.info(succApps)
    logger.error("**********下载失败APP*************")
    logger.error("数量="+str(len(failApps)))
    logger.error(failApps)
    devicelist = install.finddevices()
    installAppDict={}
    for appLabelName,appResult in resultDict.items():
        if(appResult[0] == True):#下载成功的apk，待安装
            filePath = os.path.join(gol.get_value("appFilePath"),appResult[2])
            appResult.append(filePath)
            installAppDict[appLabelName] = appResult
    logger.info(installAppDict)
    deviceTestResultDict=install.doInstall(devicelist,**installAppDict)
    installSuccApps = []
    installFailApps = []
    for device,deviceRsDict in deviceTestResultDict.items():
        print(name)
        for appName,appTestedRs in deviceRsDict.items():
            # print("======"+rs[5]+"=========")
            if(rs[5] == "Success"):
                installSuccApps.append(name)
            else:
                installFailApps.append(name)


    logger.info("**********安装成功APP*************")
    logger.info("数量="+str(len(installSuccApps)))
    logger.info(installSuccApps)
    logger.info("**********安装失败APP*************")
    failNumber=len(failApps)+len(installFailApps)
    logger.info("数量="+str(failNumber))
    logger.info(failApps)
    logger.info(installFailApps)

    logger.info(deviceTestResultDict)

    #遍历APP并点掉弹出框
    apkPath = os.path.join(curDir,"resource")
    cmd = 'adb -s %s install -r %s'% (devicelist[0],apkPath+os.sep+"AutoBvtHelper.apk")
    logger.info("开始安装遍历应用的App:")
    installResult = Util.exccmd(cmd)
    logger.info("安装结果:"+installResult)
    logger.info("开始遍历所有App")
    cmd = "adb -s %s  shell am start -n gionee.autotest.autobvthelper/.view.MainActivity --ei start 1 --ei isClean 1"%devicelist[0]
    iterRs=Util.exccmd(cmd);
    logger.info(iterRs)

    end = datetime.datetime.now()
    logger.info(resultDict)
    k = end - begin
    logger.info("运行时长")
    logger.info(k)
    logger.info("**************************end***************************")

