#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @Time     :   2019/6/2 9:24
# @Author   :   robert
# @FileName :   company_excel.py
# @Software :   PyCharm
import datetime
import os

import sys
import xlrd
from xlutils.copy import copy
import settings
from xlwt import *


class CompanyExcel(object):
    '''
    企业信息表对象，用来初始化创建企业信息表，写入数据等功能
    '''

    def __init__(self, excel_name=None, file_dir=settings.COMPANY_DATA_DIR):
        '''
        初始化时，默认生成一个公司的excel模板
        :param excel_name: excel文件的名称
        :param file_dir: 存放数据的文件夹
        '''
        date_now = datetime.datetime.now().strftime('%Y_%m_%d')
        self.file_dir = os.path.join(file_dir, date_now)
        # 创建一个当天的文件夹，用来存放爬取的数据
        try:
            os.mkdir(self.file_dir)
        except Exception as err:
            print(f'{self.file_dir}文件夹已存在，直接使用')
        self.excel_name = excel_name

    def save_data(self, excel_path, company_info_list, sheet_id=0):
        '''
        将数据写入到excel中
        :param company_info_list:
        :return:
        '''
        try:
            rexcel = xlrd.open_workbook(excel_path)
            # 根据sheet_id获取sheet对象
            rsheet = rexcel.sheets()[sheet_id]
            # 获取sheet的总行数
            rows = rsheet.nrows
            excel = copy(rexcel)
            sheet = excel.get_sheet(sheet_id)
        except Exception as err:
            print(f'{excel_path}或者{sheet_id}不存在')
            raise err
        for company_info in company_info_list:
            for col_id, col_val in enumerate(company_info):
                # 插入到rows+1列,批量写入
                sheet.write(rows, col_id, col_val)
            rows += 1
            print(f'{company_info[0]}'.center(60, "*"))
        # 保存并覆盖打开的文件
        excel.save(excel_path)

    def init_write(self, sheet):
        # 公司信息包含8列，初始化写入到第一行
        class Company(object):
            company_name = '公司名称'
            company_leader = '公司法人'
            company_capital = '注册资金'
            company_date = '成立时间'

            company_email = '联系邮箱'
            company_phone = '联系电话'
            company_more_phone = '更多电话'
            company_addr = '公司地址'
            company_scope = '经营范围'

        first_row = [Company.company_name, Company.company_leader, Company.company_capital, Company.company_date,
                     Company.company_email, Company.company_phone, Company.company_more_phone, Company.company_addr,
                     Company.company_scope]
        # 写入到第一行数据
        for col_id, col_val in enumerate(first_row):
            sheet.write(0, col_id, col_val)

    def generate_excel(self):
        '''
        生成一个excel，默认模板为company类的属性
        :param excel_name:
        :return:
        '''
        # 指定开打excel的格式为utf-8
        self.file = Workbook(encoding='utf-8')
        # 添加一个sheet，默认为'公司信息'
        self.sheet = self.file.add_sheet('公司信息')

        self.init_write(self.sheet)

        # 保存文件，名称为时间戳
        if self.excel_name is None:
            now = datetime.datetime.now()
            self.excel_name = now.strftime('%Y-%m-%d-%H-%M-%S')

        file_path = os.path.join(self.file_dir, f'{self.excel_name}.xls')
        try:
            self.file.save(file_path)
        except FileNotFoundError as err:
            print(f'文件名异常:{err}')
        return file_path


if __name__ == '__main__':
    pass
