#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @Time     :   2019/6/15 19:14
# @Author   :   robert
# @FileName :   company_info.py
# @Software :   PyCharm


from src.company_parser import CompanyInfoParser





def get_company_infos(company_info_html):
    '''
    根据传入的对象，获取企业的相关信息
    :param company_info_html: 公司信息的html_str或者是bs.element.Tag对象
    :return: 公司信息的list
    '''
    # 初始化公司信息
    company_info_list = []
    company_info = CompanyInfoParser(company_info_html)

    # 公司名称
    company_name = company_info.name
    company_info_list.append(company_name)

    # 法人代表
    company_legal_person = company_info.leader
    company_info_list.append(company_legal_person)

    # 注册资金
    company_registered_capital = company_info.registry_capital
    company_info_list.append(company_registered_capital)

    # 成立日期
    company_registered_date = company_info.registry_date
    company_info_list.append(company_registered_date)

    # 邮箱
    company_email = company_info.email
    company_info_list.append(company_email)

    # 电话
    company_phone = company_info.phone
    company_info_list.append(company_phone)

    # 更多电话
    company_more_phone = company_info.more_phone
    company_info_list.append(company_more_phone)

    # 地址
    company_addr = company_info.addr
    company_info_list.append(company_addr)

    print(company_info_list)
    return company_info_list

