#-*- coding: UTF-8 -*-
from unittest import TestCase
import os, sys, time
sys.path.append("..")
from library.BaseLibrary import LoginApp
from conf import Conf

class TestCaseBasicObject(TestCase):
    @classmethod
    def setUpClass(self):
        self.driver = LoginApp().sysLogin()
        Conf.DRIVER = self.driver
        time.sleep(2)

    @classmethod
    def tearDownClass(self):
        self.driver.quit()