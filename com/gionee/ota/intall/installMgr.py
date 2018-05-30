# -*- coding: utf-8 -*-
__author__ = 'suse'
from com.gionee.ota.intall.Install import Install
import os
from com.gionee.ota import gol
from com.gionee.ota.util import Util

logger = Util.logger
class InstallMgr():
    def __init__(self,device):
        self.device = device
    def checkDevice(self):
        rst = Util.exccmd('adb devices | findstr '+self.device)
        if len(rst) > 1:
            logger.info("被测手机="+self.device)
        else:
            logger.error("被测手机="+self.device+"未找到")
            Util.exccmd('adb -s %s wait-for-device '%self.device)

    def installApps(self,**downloadRsDict):
        installappdict = {}
        for appLabelName, appResult in downloadRsDict.items():
            if appResult[0]:  # 下载成功的apk，待安装
                filepath = os.path.join(gol.get_value("appFilePath"), appResult[2])
                appResult.append(filepath)
                installappdict[appLabelName] = appResult
        install = Install()
        install.finddevices()
        installAppRsDict = install.doSingleInstall(self.device, **installappdict)
        installSuccessApps = []
        installFailApps = []
        for appName,appTestedRs in installAppRsDict.items():
                # print("======"+rs[5]+"=========")
                if(appTestedRs[5] == "Success"):
                    installSuccessApps.append(appName)
                else:
                    installFailApps.append(appName)
        logger.info("**********安装成功APP*************")
        logger.info("数量="+str(len(installSuccessApps)))
        logger.info(installSuccessApps)
        logger.error("**********安装失败APP*************")
        logger.error("数量="+str(len(installFailApps)))
        logger.error(installFailApps)
