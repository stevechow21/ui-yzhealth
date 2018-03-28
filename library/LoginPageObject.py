#-*- coding: UTF-8 -*-
from selenium.webdriver.common.by import By
import sys
sys.path.append("..")
from library.BasicPageObject import Element
from conf.Conf import *

class LoginPageObject(object):
    
    @classmethod
    def test_login_common(cls, username, password, is_org=None):
        u"""登录操作"""
        name = Element.find_element(By.ID, "username")
        pwd = Element.find_element(By.ID, "password")
        submit_btn = Element.find_element(By.XPATH, "//button[@type='submit']")
        if is_org == "Y":
            province = Element.find_element(By.XPATH, ProvinceList)
            province.click()
            jiangsu = Element.find_element(By.XPATH, JiangSu)
            jiangsu.click()
            city = Element.find_element(By.XPATH, CityList)
            city.click()
            suzhou = Element.find_element(By.XPATH, SuZhou)
            suzhou.click()
            org = Element.find_element(By.XPATH, OrgList)
            org.click()
            jiulong = Element.find_element(By.XPATH, Jiulong)
            jiulong.click()
        name.send_keys(username)
        pwd.send_keys(password)
        submit_btn.click()





