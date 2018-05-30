# -*- coding: utf-8 -*-
__author__ = 'suse'
from com.gionee.ota.log import adblog
from com.gionee.ota.util import Util
from com.gionee.ota.apps.qqApps import QqApp
from com.gionee.ota.apps.gnApps import GN_Apps
logger = Util.logger
class AppsMgr():
    def __init__(self):
        pass
    def getDownloadHost(self,appType):
        if(appType == 1):
            return GN_Apps()
        elif(appType == 2):
            return QqApp()
        return None
    def getReverseDownloadHost(self,appType):
         if(appType == 1):
             return QqApp()
         elif(appType == 2):
            return GN_Apps()
         return None


    def downloadApps(self,appType,*testedApps,**pkg_dict):
        resultDict = {}
        successApps =[]
        failApps = []
        for app in testedApps:
            rc = []
            logger.info("app=" + app + " 开始下载")
            if (pkg_dict.__contains__(app) and pkg_dict.get(app).strip() != ''):
                    mApp = self.getDownloadHost(appType)
                    rc = mApp.getDownloadAddr(pkg_dict.get(app))
                    rc = mApp.download()
                    if not rc[0]:
                        logger.error("app=‘"+app+"’ 再次尝试从另外服务器上下载")
                        mApp = self.getReverseDownloadHost(appType)
                        rc = mApp.getDownloadAddr(pkg_dict.get(app))
                        rc = mApp.download()
            else:
                rc = [False, 1]
                rc.append("没有找到对应的包名:%s" % app)
                logger.error("没有找到对应的包名:%s" % app)
            if rc[0]:
                successApps.append(app)
            else:
                failApps.append(app)
            resultDict[app] = rc
        logger.info("**********成功下载APP*************")
        logger.info("数量="+str(len(successApps)))
        logger.info(successApps)
        logger.error("**********下载失败APP*************")
        logger.error("数量="+str(len(failApps)))
        logger.error(failApps)

        return resultDict

