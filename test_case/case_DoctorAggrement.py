# -*- coding: UTF-8 -*-
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


class TestCaseDoctorAgreement(TestCaseBasicObject):
    def test_case_doctor_agreement_add_001(self):
        '''创建家庭医生协议'''
        Conf.CASE_NAME = "test_case_login_001"
        Log.start_test(Conf.CASE_NAME)

        userinfo = userList[0]
        username = userinfo.getAttribute("username")
        password = userinfo.getAttribute("passwd")  # 从xml文件读取用户登录信息

        LoginPageObject.test_login_common(username, password)

        agreementpage = Element.find_element(By.ID, "item-1010")
        agreementpage.click()
        time.sleep(2)
        agreementpage1 = Element.find_element(By.ID, "item-101002")
        agreementpage1.click()

        time.sleep(2)
        Browser.navigate_to(Conf.URL)
        Log.stop_test()

        # try:
        #     pagename = Element.find_element(By.ID, "myConfig").text
        #     Assert().assertEqual(pagename, str(username), msg='login with wrong name')
        # except AssertionError, msg:
        #     raise AssertionError(msg)
        # finally:
        #     time.sleep(2)
        #     Browser.navigate_to(Conf.URL)
        #     Log.stop_test()



if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestCaseDoctorAgreement("test_case_doctor_agreement_add_001"))

    unittest.TextTestRunner().run(suite)