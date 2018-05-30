# -*- coding: utf-8 -*-
__author__ = 'suse'
from com.gionee.ota.log import Log
import logging
import os,re
from com.gionee.ota.util import Util
import time
import traceback
from uiautomator import Device
class Install():
    def __init__(self):
        self.logger = Util.logger

    def finddevices(self):
        rst = Util.exccmd('adb devices')
        devices = re.findall(r'(.*?)\s+device',rst)
        if len(devices) > 1:
            deviceIds = devices[1:]
            self.logger.info('共找到%s个手机'%str(len(devices)-1))
            for i in deviceIds:
                self.logger.info('ID为%s'%i)
            return deviceIds
        else:
            self.logger.error('没有找到手机，请检查')
    def runwatch(self,d,data):
        times = 120
        while True:
            if data == 1:
                return True
            # d.watchers.reset()
            d.watchers.run()
            times -= 1
            if times == 0:
                break
            else:
                time.sleep(0.5)
    def installapk(self,d,device,**installAppDict):

        for appLabelName,appTestRs in installAppDict.items():
             # mkillerpath = os.path.join("E:\\python_study\\OtaNeedInstalledApps\\com\\gionee\\ota\\request\\downloadApps",'cn.jj_5.02.02_50202.apk')
             self.logger.info(appTestRs)
             cmd = 'adb -s %s install -r %s'% (device,appTestRs[4])
             self.logger.info(cmd)
             self.logger.info("开始安装:"+appTestRs[4])
             Util.exccmd('adb -s %s wait-for-device '%device)
             installResult = Util.exccmd(cmd);
             self.logger.info("安装结果:"+installResult)
             installAppDict[appLabelName].append(installResult)


        return installAppDict

    def doSingleInstall(self,deviceId,**installAppDict):
        d = Device(deviceId)
        installAppRsDict= self.installapk(d,deviceId,**installAppDict)
        return installAppDict

    def doInstall(self,deviceids,**installAppDict):
        count = len(deviceids)
        # port_list = range(5555,5555+count)
        deviceTestResultDict ={}
        for i in range(len(deviceids)):
            d = Device(deviceids[i])
            installAppRsDict= self.installapk(d,deviceids[i],**installAppDict)
            deviceTestResultDict[deviceids[i]] =installAppRsDict
        return deviceTestResultDict
if __name__ == "__main__":
    # cleanEnv()
    logger = Util.logger
    install = Install()
    devicelist = install.finddevices()
    print(devicelist)
    if devicelist:
        # apkpath = os.path.join(os.getcwd(),'apk')
        apklist = Util.listFile("E:\\python_study\\OtaNeedInstalledApps\\com\\gionee\\ota\\request\\downloadApps")
        print(apklist)
        install.doInstall(devicelist,apklist) #每个手机都要安装apklist里的apk
