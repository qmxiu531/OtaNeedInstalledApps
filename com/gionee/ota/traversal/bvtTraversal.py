# -*- coding: utf-8 -*-\
from com.gionee.ota.log import adblog
from com.gionee.ota.util import Util
from com.gionee.ota import Base
import pkg_resources
import os
__author__ = 'suse'
logger = Util.logger
import sys,time
class BvtTraversal():
    def __init__(self):
        pass
    def lanchAppsTest(self,testedDevice):

        curDir=sys._MEIPASS
        # apkPath = os.path.split(os.path.realpath(__file__))[0]
        apkPath = os.path.join(curDir,"AutoBvtHelper.apk")
        cmd = 'adb -s %s install -r %s'%(testedDevice,apkPath)
        logger.info("开始安装遍历应用的App:")
        installResult = Util.exccmd(cmd)
        logger.info("安装结果:"+installResult)
        time.sleep(3)
        logger.info("开始遍历所有App")
        cmd = "adb -s %s  shell am start -n gionee.autotest.autobvthelper/.view.MainActivity --ei start 1 --ei isClean 1"%testedDevice
        iterRs=Util.exccmd(cmd);
        logger.info(iterRs)
        adbLog = adblog.Adblog(testedDevice)
        adbLog.readAdbLog()
