#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @Time     :   2019/6/3 21:29
# @Author   :   robert
# @FileName :   qichacha_verify.py
# @Software :   PyCharm

import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from src import common
import settings

class QichachaVerifyPage(object):

    def __init__(self):
        # 滑动按钮
        self.scroll_btn = By.ID,'nc_1_n1z'
        # 确定登录按钮
        self.verify_btn = By.ID,'verify'
        # 刷新圈圈
        self.refresh_cycle = By.ID,'nc_1__btn_1'
        # 刷洗滑动按钮
        self.refresh_btn = By.LINK_TEXT,'刷新'
        # 验证码输入框
        self.verify_code_input = By.ID,'nc_1_captcha_input'
        # 验证码提交按钮
        self.verify_btn_submit = By.ID,'nc_1_scale_submit'
        # 验证错误框
        self.error_span = By.ID,'nc_1__captcha_img_text'

        # 操作过于频繁时的刷新
        # 点击刷新按钮
        self.click_refresh_btn = By.LINK_TEXT,'点击刷新'
        # 立即刷新

    def _scroll(self,driver,offset):
        '''
        拖动滑块
        :param driver:
        :param offset: 拖动的距离
        :return:
        '''
        button = driver.find_element(*self.scroll_btn)
        action = ActionChains(driver)
        action.click_and_hold(button).perform()
        action.reset_actions()
        action.move_by_offset(offset, 0).perform()

    def scroll_btn_move(self,driver,offset=263):
        while True:
            # 滑动
            self._scroll(driver,offset)
            scroll_times = 0
            # 查看是否滑动成功
            # 网络引起的点击刷新按钮
            click_refresh_btn = common.is_element_exist(driver,self.click_refresh_btn)
            # 错误引起的刷新按钮
            refresh_btn = common.is_element_exist(driver,self.refresh_btn)
            if click_refresh_btn:
                click_refresh_btn.click()
            elif refresh_btn:
                refresh_btn.click()
            # 如果两个异常的刷新按钮都没有出现，则表示滑动成功，退出此循环
            else:
                break
            # 点击刷新重新滑动
            time.sleep(3)
            scroll_times +=1
            if scroll_times >=5:
                raise RuntimeError('滑动失败超过三次')

    def input_verification_code(self,driver):
        error_times = 0
        while True:
            driver.find_element(*self.verify_code_input).clear()
            verification_code = input('请输入验证码:')
            if verification_code in ('y','Y'):
                break
            driver.find_element(*self.verify_code_input).send_keys(verification_code)
            driver.find_element(*self.verify_btn_submit).click()
            if not common.is_element_exist(driver,self.error_span):
                break
            error_times +=1
            if error_times >= settings.CODE_INPUT_ERROR_TIMES:
                raise ValueError(f'验证码输入错误次数超过{settings.CODE_INPUT_ERROR_TIMES}次')
