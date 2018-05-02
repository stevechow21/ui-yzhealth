# -*- coding: UTF-8 -*-
import sys
sys.path.append("..")
import time
from selenium.webdriver.common.by import By
from library.BaseLibrary import *
from library.BasicPageObject import Element, Assert, Browser
from library.LoginPageObject import LoginPageObject
from library.AddArchivePageObject import AddArchivePageObject
from library.TestCaseBasicObject import TestCaseBasicObject
import xml.dom.minidom

dom = xml.dom.minidom.parse(Conf.XML_PATH)
root = dom.documentElement
userList = root.getElementsByTagName('login')
archiveList = root.getElementsByTagName('archive')

class TestCaseAddArchive(TestCaseBasicObject):
    def test_case_archive_add_001(self):
        '''创建档案（必填项）'''
        Conf.CASE_NAME = "test_case_archive_add_001"
        Log.start_test(Conf.CASE_NAME)

        userinfo = userList[1]
        username = userinfo.getAttribute("username")
        password = userinfo.getAttribute("passwd")  # 从xml文件读取用户登录信息
        archiveinfo = archiveList[0]
        idcard = archiveinfo.getAttribute("idcard")  # 从xml文件读取添加档案信息
        name = archiveinfo.getAttribute("name")
        org = archiveinfo.getAttribute("org")
        phone = archiveinfo.getAttribute("phone")
        address = archiveinfo.getAttribute("address")
        register = archiveinfo.getAttribute("register")

        LoginPageObject.test_login_common(username, password, is_org='Y')
        AddArchivePageObject.test_add_archive_required(idcard, name, org, phone, address, register)

        reload(sys)
        sys.setdefaultencoding("utf-8")

        try:
            archivename = Element.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/div/div[3]/div[3]/div/table/tbody/tr[2]/td[3]").text
            Assert().assertEqual(name, str(archivename), msg='archive created successfully')
        except AssertionError, msg:
            raise AssertionError(msg)
        finally:
            time.sleep(2)
            Browser.navigate_to(Conf.URL)
            Log.stop_test()

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestCaseAddArchive("test_case_archive_add_001"))

    unittest.TextTestRunner().run(suite)