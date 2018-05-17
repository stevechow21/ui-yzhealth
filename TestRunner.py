# -*- coding: utf-8 -*-
from selenium import webdriver
import unittest, time, re, sys
from imp import reload
import HTMLTestRunner
sys.path.append("..")
# from library.BaseLibrary import send_mail

from test_case.case_Login import TestCaseLogin
from test_case.case_AddArchive import TestCaseAddArchive

reload(sys)
sys.setdefaultencoding('utf8')

if __name__ == "__main__":

    suite = unittest.TestSuite()
    # suite.addTest(TestCaseLogin("test_case_login_001"))
    # suite.addTest(TestCaseLogin("test_case_login_002"))
    # suite.addTest(TestCaseLogin("test_case_login_003"))
    suite.addTest(TestCaseAddArchive("test_case_archive_add_001"))

    currenttime = time.strftime('%Y-%m-%d-%H_%M_%S',time.localtime(time.time()))
    filename = 'D:\\testcode\\automation\\result\\reports\\'+currenttime+'results.html'
    fp=file(filename,'wb')
    runner=HTMLTestRunner.HTMLTestRunner(
            stream=fp,
            title=u'基层UI自动化测试报告',
            description=u'界面自动化测试'
    )
    runner.run(suite)
    fp.close()
    # send_mail(filename)