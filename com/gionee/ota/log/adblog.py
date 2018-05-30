# -*- coding: utf-8 -*-
__author__ = 'suse'
import subprocess
from com.gionee.ota.util import Util
class Adblog():
    def __init__(self,device):
        self.device = device
        self.logger = Util.logger
    def readAdbLog(self):
        isExit = False
        while not isExit:
            proc = subprocess.Popen(['adb', 'logcat', '-v', 'time', '-s', 'gionee.os.autotest'], stdout=subprocess.PIPE)
            for line in proc.stdout:
                # print(line.decode('utf-8'))
                self.logger.info(line.decode('utf-8'))
                try:
                    if (str(line.decode('utf-8')).index("遍历完成") > -1):
                        cmd = "adb -s %s pull /sdcard/screenshot"%self.device
                        pullRs=Util.exccmd(cmd)
                        self.logger.info("pullRs="+pullRs)
                        isExit = True
                        break
                except:
                    pass
            proc.wait()


