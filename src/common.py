#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @Time     :   2019/6/1 10:28
# @Author   :   robert
# @FileName :   common.py
# @Software :   PyCharm
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from selenium.webdriver.common.by import By

# 判断元素是否存在,存在就返回该元素
def is_element_exist(driver,element):
    try:
        ret = driver.find_element(*element)
    except (NoSuchElementException) as err:
        print('{}元素不可见'.format(element))
        return False
    if ret:
        return ret
    return False

def is_element_display(driver,element):
    ret = driver.find_element(*element)
    if ret.is_displayed():
        return True
    return False

