# -*- coding: utf-8 -*-
__author__ = 'suse'
import xlrd, xlwt
from xlutils.copy import copy
import time
from com.gionee.ota.Base import *


class Excel(object):
    def __init__(self, file):
        #一个软件只有一个工作路径，所以当有可能从不同的入口执行时，需要获取当前的绝对路径，再去查找相对路径
        # self.file = Base.get_cur_dir(__file__)  + "\\" + file#永远是基于excel.py所在路径
        self.file = file
        self.targetName = self.file.replace(".xlsx", (time.strftime("%Y-%m-%d-%H-%M-%S") + ".xlsx"))
        self.data = None
    #打开excel文件
    def open_excel(self):
        try:
            if not self.data:
                self.data = xlrd.open_workbook(self.file)
                self.target = copy(self.data)

            return True
        except:
            Base.printErr("打开Excel文件失败！")
            return False
    def getAllSheetNames(self):
        try:
            if not self.open_excel():
                return None
            return self.data.sheet_names()
        except:
            Base.printErr("获取Excel中键值对信息失败！")

    #根据配置项目名称获取相应的值
    # page: excel sheet 名
    #items.字典型，获取字典中key对应的配置项值并返回结果字典
    #返回填充后的items
    def get_config_item(self, page, group, items):
        try:
            if not self.open_excel():
                return None
            table = self.data.sheet_by_name(page)
            nrows = table.nrows #行数

            bFound = False
            for num in range(0, nrows):
                row = table.row_values(num)
                if row:
                    if row[0] == '[%s]'%group:
                        bFound = True
                        continue
                    elif row[0][0:1]=="[":
                        bFound = False

                    if bFound:
                        for key in items.keys():
                            if key == row[0]:
                                items[key] = row[1]
            return items
        except:
            Base.printErr("获取Excel中配置信息失败！")

    def getColumnIndex(self,table,columnName):#列名称只能在第一行
        columnIndex = None
        for i in range(table.ncols):
            if(table.cell_value(0, i) == columnName):
                 columnIndex = i
                 break
        return columnIndex
    def getColumnIndexMax(self,table,columnName):#列名称可能在任意行
        slot = []#存储找到的列名的行和列的索引值
        for i in range(table.ncols):
            for j in range(table.nrows):
                if(table.cell_value(j,i) == columnName):
                    slot = [j,i]
                    return slot
    #获取被测试项目的被测app的label名称
    def get_tested_app_name(self,sheetName,labelColumnName):
        appNames = []
        try:
            if not self.open_excel():
                return None
            table = self.data.sheet_by_name(sheetName)
            columnSlot=self.getColumnIndexMax(table,labelColumnName)
            rowIndex = columnSlot[0]
            columnIndex = columnSlot[1]
            nrows = table.nrows #行数
            for num in range(rowIndex+1, nrows):
                 row = table.row_values(num)
                 value = row[columnIndex]
                 appNames.append(value)
            return appNames
        except:
            Base.printErr("获取Excel中键值对信息失败！")


    def get_pkg_values(self,sheetName,labelColumnName,pkgColumnName):
        pkg_dict={}
        try:
            if not self.open_excel():
                return None
            table = self.data.sheet_by_name(sheetName)
            labelColumnNameIndex=self.getColumnIndex(table,labelColumnName)
            pkgColumnNameIndex=self.getColumnIndex(table,pkgColumnName)
            # labelColumnNameValues = table.col_values(labelColumnNameIndex) # 获取列类容
            nrows = table.nrows #行数
            for num in range(1, nrows):
                 row = table.row_values(num)
                 key = row[labelColumnNameIndex]
                 value = row[pkgColumnNameIndex]
                 pkg_dict[key] = value
            return pkg_dict
        except:
            Base.printErr("获取Excel中键值对信息失败！")

    def get_list_pkg_value(self,sheetName,columnName):
         lists = []
         try:
            if not self.open_excel():
                return None
            table = self.data.sheet_by_name(sheetName)
            columnNameIndex=self.getColumnIndex(table,columnName)
            cols = table.col_values(columnNameIndex) # 获取列类容
            # print(cols)
            for cell in cols:
                if cell == columnName or cell == "":
                    continue
                # print(cell+"55555")
                lists.append(cell)
         except:
            Base.printErr("获取Excel中键值对信息失败！")
         return lists

    #从键值对表格中根据名称获取对应的值
    # page: excel sheet 名
    #name：键值对中的键名
    #返回 对应的值
    def get_list_value(self, page, name):
        try:
            if not self.open_excel():
                return None
            table = self.data.sheet_by_name(page)
            nrows = table.nrows #行数

            for num in range(0, nrows):
                row = table.row_values(num)
                if row:
                    if row[0]==name:
                        return row[1]
            return None
        except:
            Base.printErr("获取Excel中键值对信息失败！")
    #获取页面中的全部数据
    #返回：全部数据，二维数组
    def get_page_data(self, page):
        try:
            if not self.open_excel():
                return None
            table = self.data.sheet_by_name(page)
            nrows = table.nrows #行数
            lists = []
            for num in range(0, nrows):
                row = table.row_values(num)
                if row:
                    lists.append(row)
            return lists
        except:
            Base.printErr("打开Excel中用例数据失败！")
    #将字符串中的"?"替换成对应的值
    #source:含“？”的原始字符串
    #vars：替换的值，一维数组
    def str_fill_parm(self, source, vars):
        try:
            if source.find("?") < 0: #如果没有需要替换的参数则直接返回源字串
                return source
            for var in vars:
                source = source.replace("?", "%s", 1)
                source = source%(var)
            return source
        except:
            Base.printErr("参数替换失败！")

    #解析函数格式：页名.函数名(参数1, 参数2，......)
    #func:函数字符串
    #返回替换后的字符串
    def str_parse_func(self, source):
        try:
            if source[0:1] == "$":
                source = source[1:]
            else:
                return source
            #func = "sql.delProduct(测试产品,服务类)"
            m = source.split(".")
            if len(m)==2:
                n = m[1].split("(")
                if len(n) == 2:
                    v = self.get_list_value(m[0], n[0])
                    n[1] = n[1].strip(" ")
                    n[1] = n[1].strip(")")
                    n[1] = n[1].strip()
                    xx = n[1].split(",")
                    yy = []
                    for x in xx:
                        x = x.strip()
                        yy.append(x)
                    s = self.str_fill_parm(v, yy)
                    return s

            raise RuntimeError("字符串格式错误:%s"%source)
        except:
            Base.printErr("解析函数字符串失败！")

    def write_by_index(self, row, col, page,value):
        try:
            self.target.get_sheet(page).write(row, col, value)
            return True
        except:
            Base.printErr("按行列号写入Excel文件失败！")
            return False

    def save_excel(self):
        try:
            self.target.save(self.targetName)
            return True
        except:
            Base.printErr("保存Excel文件失败！")
            return False

if __name__ == '__main__':
    curDir=Base.get_cur_dir(__file__)
    # exclPath=os.path.join(curDir,"OTAApps.xlsx")
    # print(exclPath)
    ec = Excel("OTAApps.xlsx")
    # pkg_list=ec.get_list_pkg_value("三方汇总表","应用包名")
    pkg_dict = ec.get_pkg_values("三方汇总表","应用名称","应用包名")
    print(pkg_dict)
    testedApps=ec.get_tested_app_name("金钢全网通","应用名称")
    print(testedApps)
    for app in testedApps:
        if(pkg_dict.__contains__(app)):
            print("hello")
           # print("app="+app+",pkgName="+pkg_dict.get(app))

        else:
            print("app="+app+" not find pkgName")
    # dicDb = {"host":"", "port":"", "db":"", "user":"", "password":"", "charset":""}
    # ec.get_config_item("config", "db", dicDb)
    # print (dicDb)
    # l= ec.get_page_data("login")
    # print(l)
    #
    # f = "$sql.delProduct(测试产品)"
    # s = ec.str_parse_func(f)
    # print(s)