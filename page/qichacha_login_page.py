
#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @Time     :   2019/6/1 10:02
# @Author   :   robert
# @FileName :   qichacha_login_page.py
# @Software :   PyCharm
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from src import common

class QichachaPage(object):

    def __init__(self):
        self.login_link = By.LINK_TEXT,'登录'

        self.login_with_password = By.ID,'normalLogin'
        # 手机输入框
        self.phone_input = By.ID,'nameNormal'
        # 密码输入框
        self.password_input = By.ID,'pwdNormal'

        # 登录页面
        # 登录滑块
        self.scroll_btn = By.ID,'nc_1_n1z'

        # 登录框按钮定位
        self.refresh_scroll = By.LINK_TEXT,'刷新'
        self.login_btn = By.CSS_SELECTOR,'#user_login_normal > button[type="submit"]'

        #验证码框
        self.verification_code_input = By.ID,'nc_1_captcha_input'
        self.submit_btn = By.ID,'nc_1_scale_submit'
        self.refresh_btn = By.ID,'nc_1__btn_1'
        # 错误信息提示
        self.error_span = By.CSS_SELECTOR,'#nc_1__captcha_img_text > span'


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

    def scroll_btn_move(self,driver,offset=308):
        while True:
            # 滑动
            self._scroll(driver,offset)
            scroll_times = 0
            # 查看是否滑动成功
            refresh_btn = common.is_element_exist(driver,self.refresh_scroll)
            if not refresh_btn:
                break
            # 点击刷新重新滑动
            time.sleep(3)
            refresh_btn.click()
            scroll_times +=1
            if scroll_times >=5:
                raise RuntimeError('滑动失败超过三次')

    def input_verification_code(self,driver):
        error_times = 0
        while True:
            driver.find_element(*self.verification_code_input).clear()
            verification_code = input('请输入验证码:')
            if verification_code in ('y','Y'):
                break
            driver.find_element(*self.verification_code_input).send_keys(verification_code)
            driver.find_element(*self.submit_btn).click()
            if not common.is_element_exist(driver,self.error_span):
                break
            error_times +=1
            if error_times >=5:
                raise ValueError('验证码输入错误次数超过3次')
