# -*- coding: utf-8 -*-
import os
import sys
from com.gionee.ota.util import Util

class Base(object):
    def printErr(userInfo="", bPrint=True):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        msg = "异常类型：%s, 在 %s 的第 %d 行；%s"%(exc_type, fname, exc_tb.tb_lineno, exc_obj)
        if userInfo:
            msg = msg + "\n" + userInfo
        if bPrint:
            Util.logger.error(msg)
        return msg

    def get_cur_dir(file):
        return os.path.split(os.path.realpath(file))[0]
