#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @Time     :   2019/5/31 23:47
# @Author   :   robert
# @FileName :   excel_handler.py
# @Software :   PyCharm
import os

import xlrd

import settings


class ExcelHandler(object):
    def __init__(self,file_name,sheet_id):
        self.file_name = file_name
        self.sheet_id = sheet_id
        self.sheet_data = self.get_sheet_data(self.sheet_id)

    # 获取sheet的内容
    def get_sheet_data(self,sheet_id):
        if isinstance(sheet_id,int) and sheet_id >= 0:
            sheet_id = sheet_id
        else:
            raise ValueError("sheet_id must be integer")
        data = xlrd.open_workbook(self.file_name)
        sheet_data = data.sheet_by_index(sheet_id)
        return sheet_data

    # 获取整列的值
    def get_col_data(self,col_id):
        col_data = self.sheet_data.col_values(col_id)
        return col_data



if __name__ == '__main__':
    pass