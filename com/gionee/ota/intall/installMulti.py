# -*- coding: utf-8 -*-
import queue,threading
from com.gionee.ota.util import Util
__author__ = 'suse'
rs = {}
logger = Util.logger
class MultiInstall():
    def __init__(self,device,installAddrList):
            self.device = device
            self.installAddrList = installAddrList
            self.threadNameList = ["Thread-1","Thread-2","Thread-3","Thread-4","Thread-5"]
            self.workQueue = queue.Queue(len(installAddrList))
            print(self.workQueue.maxsize)
            self.threads=[]
            self.threadID = 1
            for installAddr in installAddrList:
                self.workQueue.put(installAddr)

    def startMultiThread(self):
            for tName in self.threadNameList:
                thread = InstallAppThread(self.threadID,self.device,self.workQueue)
                thread.start()
                self.threads.append(thread)
                self.threadID +=1
            for i in self.threads:
               i.join()
            return rs
class InstallAppThread(threading.Thread):
            def __init__(self,threadID,device,q):
                threading.Thread.__init__(self)
                self.threadID = threadID
                self.device = device
                self.q = q
            def run(self):
                print("Staring"+self.name)
                while True:
                    if self.q.qsize() > 0:
                        installAddr = self.q.get()
                        self.process_data(self.device,installAddr)
                        # rs[installAddr] = rc
                    else:
                        break
                print("Exiting "+str(self.threadID))

            def process_data(self,threadName,installAddr):
                rc = []
                cmd = 'adb -s %s install -r %s'% (self.device,installAddr)
                logger.info("开始安装:"+installAddr)
                Util.exccmd('adb -s %s wait-for-device '%self.device)
                installResult = Util.exccmd(cmd);
                logger.info("安装结果:"+installResult)

