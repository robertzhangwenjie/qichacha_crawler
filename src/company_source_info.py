#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @Time     :   2019/6/1 7:54
# @Author   :   robert
# @FileName :   company_source_info.py
# @Software :   PyCharm
import os

from utils.excel_handler import ExcelHandler
import settings


class CompanyBasicInfo(object):
    '''
        获取需要爬取的企业基本信息
    '''
    def __init__(self,company_file_dir=settings.COMPANY_INFO_PATH_DIR,sheet_id=0):
        self.company_file_path_dir = company_file_dir
        self.sheet_id = sheet_id
        self.excel_newest = self.get_company_source_excel()
        self.company_data_handler = ExcelHandler(file_name=self.excel_newest,sheet_id=self.sheet_id)

    def get_excel_name(self):
        return os.path.basename(self.get_company_source_excel())

    def get_company_source_excel(self):
        company_source_list = os.listdir(self.company_file_path_dir)
        # 初始化一个excel的列表
        company_source_excel_list = []
        # 对文件进行排序，并去非excel文件
        for file in company_source_list:
            if file.endswith('xls') or file.endswith('xlsx'):
               company_source_excel_list.append(file)
        # 按照文件修改时间进行排序
        company_source_excel_list.sort(key=lambda fn:os.path.getmtime(os.path.join(self.company_file_path_dir,fn)))
        if len(company_source_excel_list) == 0:
            raise ValueError('缺少公司信息表')
        # 返回最新修改或创建的excel
        newest_excel = os.path.join(self.company_file_path_dir,company_source_excel_list[-1])
        return newest_excel

    def get_company_names(self):
        # 获取要抓取的所有公司名称,获取第一列的值
        self.company_names = self.company_data_handler.get_col_data(0)
        # 去掉excel的第一行的"公司名称"
        self.company_names.pop(0)
        # 去掉空企业
        res = filter(None,self.company_names)
        return list(res)

if __name__ == '__main__':
    company_info = CompanyBasicInfo()
    print(company_info.get_excel_name())