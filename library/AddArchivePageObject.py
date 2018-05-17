# -*- coding: UTF-8 -*-
from selenium.webdriver.common.by import By
import sys
import time
sys.path.append("..")
from library.BasicPageObject import Element
from selenium.webdriver.common.action_chains import ActionChains
from conf import Conf
from conf.Conf import *

class AddArchivePageObject(object):
    @classmethod
    def test_add_archive_required(cls, idcard, name, org, phone, address, registry):
        u"""添加档案-必填项"""
        driver = Conf.DRIVER
        archiveMenu = Element.find_element(By.ID, "item-1005")
        ActionChains(driver).move_to_element(archiveMenu).perform()
        time.sleep(1)

        archiveManagement = Element.find_element(By.ID, "item-100501")
        archiveManagement.click()
        time.sleep(1)

        Element.find_element(By.ID, "add").click()
        time.sleep(1)

        idcardfield = Element.find_element(By.ID, "idcard")
        idcardfield.send_keys(idcard)
        time.sleep(1)

        namefield = Element.find_element(By.ID, "name")
        namefield.send_keys(name)
        time.sleep(1)

        orgtree = Element.find_element(By.XPATH, "/html/body/div[6]/div[3]")
        ActionChains(driver).move_to_element(orgtree).perform()
        time.sleep(1)

        orgfield = Element.find_element(By.ID, org)
        orgfield.click()
        time.sleep(1)

        phonefield = Element.find_element(By.ID, "phone")
        phonefield.send_keys(phone)
        time.sleep(1)

        addressfield = Element.find_element(By.ID, "address")
        addressfield.send_keys(address)
        time.sleep(1)

        registryfield = Element.find_element(By.ID, "registry")
        registryfield.send_keys(registry)
        time.sleep(1)
        submit_btn = Element.find_element(By.ID, "btn-submit")
        submit_btn.click()





