#-*- coding: UTF-8 -*-
import sys
sys.path.append("..")
import time
from selenium.webdriver.common.by import By
from library.BaseLibrary import *
from library.BasicPageObject import Element, Assert, Browser
from library.LoginPageObject import LoginPageObject
from library.TestCaseBasicObject import TestCaseBasicObject
import xml.dom.minidom

dom = xml.dom.minidom.parse(Conf.XML_PATH)
root = dom.documentElement
userList = root.getElementsByTagName('login')

class TestCaseLogin(TestCaseBasicObject):       
    def test_case_login_001(self):
        '''管理员admin登录'''
        Conf.CASE_NAME = "test_case_login_001"         
        Log.start_test(Conf.CASE_NAME)

        userinfo = userList[0]
        username = userinfo.getAttribute("username")
        password = userinfo.getAttribute("passwd")   # 从xml文件读取用户登录信息
        print username

        LoginPageObject.test_login_common(username, password)

        try:
            pagename = Element.find_element(By.ID, "myConfig").text
            Assert().assertEqual(pagename, str(username), msg='login with wrong name')
        except AssertionError, msg:
            raise AssertionError(msg)
        finally:
            time.sleep(2)
            Browser.navigate_to(Conf.URL)
            Log.stop_test()

    def test_case_login_002(self):
        '''机构用户jl登录'''
        Conf.CASE_NAME = "test_case_login_002"
        Log.start_test(Conf.CASE_NAME)

        userinfo = userList[1]
        username = userinfo.getAttribute("username")
        password = userinfo.getAttribute("passwd")   # 从xml文件读取用户登录信息

        LoginPageObject.test_login_common(username, password, is_org="Y")
        try:
            pagename = Element.find_element(By.ID, "myConfig").text
            expectname = "九龙"
            Assert().assertEqual(pagename, expectname, msg='login with wrong name')
        except AssertionError, msg:
            raise AssertionError(msg)
        finally:
            time.sleep(2)
            Browser.navigate_to(Conf.URL)
            Log.stop_test()

    def test_case_login_003(self):
        '''错误用户名密码登录'''

        Conf.CASE_NAME = "test_case_login_003"
        Log.start_test(Conf.CASE_NAME)

        LoginPageObject.test_login_common("Errorname", "errorpassword")
        time.sleep(2)

        try:
            errormsg = Element.find_element(By.XPATH, "//section[@id='alertify-logs']/article").text
            expectmsg = "Bad username/password combination, please try again."
            Assert().assert_equal(errormsg, expectmsg, msg="wrong error message")
        except AssertionError, msg:
            raise AssertionError(msg)
        finally:
            time.sleep(2)
            Log.stop_test()
       
if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestCaseLogin("test_case_login_001"))
    suite.addTest(TestCaseLogin("test_case_login_002"))
    suite.addTest(TestCaseLogin("test_case_login_003"))

    unittest.TextTestRunner().run(suite)