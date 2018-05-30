# -*- coding: utf-8 -*-
from com.gionee.ota import Base
from com.gionee.ota.excel import excel
from com.gionee.ota.request import downloadApp
import datetime
from com.gionee.ota import gol
from com.gionee.ota.util import Util
import os,sys,re
from com.gionee.ota.intall import Install
import time
import subprocess
logger = Util.logger
curDir=Base.Base.get_cur_dir(__file__)
apkPath = os.path.join(curDir,"resource","AutoBvtHelper.apk")
cmd = 'adb -s %s install -r %s'% ("CYHAVCYLEULJB6FU",apkPath)
logger.info("开始安装遍历应用的App:")
installResult = Util.exccmd(cmd)
logger.info("安装结果:"+installResult)
logger.info("开始遍历所有App")
cmd = "adb -s %s  shell am start -n gionee.autotest.autobvthelper/.view.MainActivity --ei start 1 --ei isClean 1"%("CYHAVCYLEULJB6FU")
iterRs=Util.exccmd(cmd)
time.sleep(1)
# cmd = "adb -s %s  shell ps -ef | findstr autobvthelper"%("CYHAVCYLEULJB6FU")
# rst=Util.exccmd(cmd)
# print(rst)
# proceeInfo = re.findall(r'(.*?)\s+gionee.autotest.autobvthelper',rst)
# cmd = "adb -s %s  logcat -s gionee.os.autotest"%("CYHAVCYLEULJB6FU")
# rst=Util.exccmd(cmd)
proc = subprocess.Popen(['adb', 'logcat', '-v', 'time','-s','gionee.os.autotest'], stdout=subprocess.PIPE)
for line in proc.stdout:
    print(line.decode('utf-8'))
proc.wait()
# while(len(proceeInfo)>0):
#     time.sleep(5)
#     proceeInfo= re.findall(r'(.*?)\s+gionee.autotest.autobvthelper',rst)
#     print(proceeInfo)

