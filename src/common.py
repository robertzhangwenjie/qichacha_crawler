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
        print(err)
        return False
    if ret:
        return ret
    return False

# 判断元素是否可见
def is_element_display(driver,element):
    try:
        ret = driver.find_element(*element)
    except (NoSuchElementException) as err:
        print(err)
        return False
    if ret.is_displayed():
        return True
    return False

# 识别图片
import pytesseract
from PIL import Image
from PIL import ImageEnhance

def identify_pic(pic_path):
    img = Image.open(pic_path)
    img = img.convert('RGB')
    enhancer = ImageEnhance.Color(img)
    enhancer = enhancer.enhance(0)
    enhancer = ImageEnhance.Brightness(enhancer)
    enhancer = enhancer.enhance(2)
    enhancer = ImageEnhance.Contrast(enhancer)
    enhancer = enhancer.enhance(8)
    enhancer = ImageEnhance.Sharpness(enhancer)
    img = enhancer.enhance(20)
    code = pytesseract.image_to_string(img)
    print(code)

if __name__ == '__main__':
    pic_path = r'../pics/3118262516-5b3d8731449d6_articlex.png'
    identify_pic(pic_path)