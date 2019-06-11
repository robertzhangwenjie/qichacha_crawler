#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @Time     :   2019/6/1 8:09
# @Author   :   robert
# @FileName :   crawler.py
# @Software :   PyCharm

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from src import common
import settings
from page.qichacha_login import QichachaPage
from page.qichacha_home import QichachaHome
from page.qichacha_verify import QichachaVerifyPage
from src.company import Company
from src.company_info import CompanyInfo
import settings
class Crawler(object):
    '''爬虫类'''
    def __init__(self,url):
        self.username = settings.USERNAME
        self.password = settings.PASSWORD
        # self.driver = webdriver.Firefox(executable_path=settings.FireFoxWebdriver)
        self.driver = webdriver.Chrome(executable_path=settings.ChromeWebdriver)
        self.driver.implicitly_wait(5)
        self.url = url
        self.qichacha_login = QichachaPage()
        self.qichacha_home = QichachaHome()
        self.qichacha_verify = QichachaVerifyPage()

    def login(self):
        self.driver.get(self.url)
        self.driver.find_element(*self.qichacha_login.login_link).click()
        # 选择密码登录
        self.driver.find_element(*self.qichacha_login.login_with_password).click()
        # 输入手机号
        self.driver.find_element(*self.qichacha_login.phone_input).clear()
        self.driver.find_element(*self.qichacha_login.phone_input).send_keys(settings.USERNAME)

        # 输入密码
        self.driver.find_element(*self.qichacha_login.password_input).clear()
        self.driver.find_element(*self.qichacha_login.password_input).send_keys(settings.PASSWORD)

        # 滑动登录
        self.qichacha_login.scroll_btn_move(self.driver)
        # 手动滑动登录
        # flag = input('手动验证成功后，请输入任意数:')


        # 输入验证码并登录
        self.qichacha_login.input_verification_code(self.driver)

        # 登录
        self.driver.find_element(*self.qichacha_login.login_btn).click()

        # 判断是否有弹框
        bindwx = common.is_element_display(self.driver,self.qichacha_home.bindwx_pop)
        if bindwx:
        # print(bindwx)
        # if bindwx:
        # 关闭弹窗
            self.qichacha_home.close_bindwx(self.driver)

    # 根据公司名称获取公司未解析的html
    def _get_company_info(self,company_name):
        print('开始搜索')
        try:
            self.driver.find_element(*self.qichacha_home.research_input).clear()
            self.driver.find_element(*self.qichacha_home.research_input).send_keys(company_name)
            self.driver.find_element(*self.qichacha_home.research_btn).click()
        except NoSuchElementException as err:
            try:
                self.driver.find_element(*self.qichacha_home.search_input).clear()
                self.driver.find_element(*self.qichacha_home.search_input).send_keys(company_name)
                self.driver.find_element(*self.qichacha_home.search_btn).click()
            except NoSuchElementException as err:
                # 判断是否查询次数过快
                print('查询次数过多，需要手动验证！')
                if common.is_element_display(self.driver, self.qichacha_verify.scroll_btn):
                    self.qichacha_verify.scroll_btn_move(self.driver)
                    self.qichacha_verify.input_verification_code(self.driver)
                    self.driver.find_element(*self.qichacha_verify.verify_btn).click()
                else:
                    raise




        # 符合条件的第一家公司
        if common.is_element_display(self.driver,self.qichacha_home.result):
            _company_info = self.driver.find_element(*self.qichacha_home.result).get_attribute('innerHTML')
        else:
            _company_info = ''
        return _company_info

    # 根据公司的html文档进行提取
    def get_company_info(self,_company_info):
        # 初始化公司信息
        company_info_list = []
        company_info = Company(_company_info)

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

    def __del__(self):
        self.driver.quit()


if __name__ == '__main__':
    from src.excel_company import ExcelCompany
    base_url = 'https://www.qichacha.com'
    scrapy = Crawler(base_url)
    scrapy.login()
    company_list = CompanyInfo().get_company_names()
    company_info_list = []
    bulk_size = 0
    company_excel = ExcelCompany('朱蒙')
    excel_path = company_excel.generate_excel()
    for company_name in company_list:
        _company_info = scrapy._get_company_info(company_name)
        # 如果搜索不到该公司则跳到下一家
        if _company_info is None:
            continue
        company_info = scrapy.get_company_info(_company_info)
        company_info_list.append(company_info)
        if bulk_size >= 10:
            company_excel.save_data(excel_path,company_info_list)
            company_info_list = []
        bulk_size +=1

