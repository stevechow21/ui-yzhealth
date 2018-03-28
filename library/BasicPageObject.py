#-*- coding: UTF-8 -*-
import time
from unittest import TestCase
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from datetime import datetime, date
import os,sys
sys.path.append("..")
from conf import Conf
from library import Log
from conf.Conf import *
from library.Log import *

# class TestCaseBasicObject(TestCase):
#     @classmethod
#     def setUpClass(self):
#         self.driver = LoginApp().sysLogin()
#         Conf.DRIVER = self.driver

#     @classmethod
#     def tearDownClass(self):
#         self.driver.quit()

class Element(WebElement):
    """Using this class "Element" to fetch element from page, and if do not find_element element, 
        system will record error log into test result using Log.handle_error().
    """
    
    '''
    @classmethod
    def find_element(cls, driver, by, value=None):
        'd''Return the element by find_element()
        ''d'
        try:
            elename_name = driver.find_element(by, value)
        except NoSuchElementException:
            print Log.handle_error(driver)
        return elename_name
       '''
    
    @classmethod
    def execute_js(cls, javascript=None):
        Conf.DRIVER.execute_script(javascript)

    @classmethod
    def find_element(cls, by, value=None):
        try:
            elename_name = Conf.DRIVER.find_element(by, value)
        except NoSuchElementException:
            print (Log.handle_error(Conf.DRIVER))
        return elename_name
       
    @classmethod
    def is_element_present(cls, by, value=None):
        try: Conf.DRIVER.find_element(by, value)
        except:
            return False
        return True

    @classmethod
    def find_elements(cls, by, value=None):
        '''Return the elements by find_elements()
        '''
        try:
            elename_name = Conf.DRIVER.find_elements(by, value)
        except NoSuchElementException:
            Log.handle_error(Conf.DRIVER)
            
        return elename_name
    
    @classmethod
    def get_page_title(cls):
        '''Return the title of a certain page
        '''
        return DRIVER.title

    @classmethod
    def get_spinner_values(cls, by, value=None):
        '''Return a list of the  drop-down list(spinner)
        '''
        elename_name = Conf.DRIVER.find_elements(by, value)
        return [k.text for k in elename_name]
#     @classmethod
#     def get_spinner_values(cls, driver, by, value=None):
#         '''Return a list of the  drop-down list(spinner)
#         '''
#         elename_name = driver.find_elements(by, value)
#         return [k.text for k in elename_name]
    
    @classmethod
    def choose_spinner_value(cls, element_name, element_value, option_value=None):
        """
        Choose a certain option from a drop_down list
        
        :Args:
         - element_name:     Element of drop_down list, the type is WebElement
         - element_value:    Items(options) of drop_down list, the type is string list
         - option_value:     The item/option which will be clicked for choosing, the type is sting
        
        :Usage: Always used in case execution modules
            POFS_EXPTYPE = Element.find_elements(self.driver, By.XPATH, u'//select[@name="exportType"]/option')
            POFS_EXPTYPE_CONTENT = Element.get_spinner_values(self.driver, By.XPATH, u'//select[@name="exportType"]/option')
            Element.choose_spinner_value(POFS_EXPTYPE, POFS_EXPTYPE_CONTENT, "LCL")
        """
        
        if isinstance(element_name, list):
            for item in range(len(element_value)):
                if option_value == element_value[item]:
                    element_name[item].click()
                    print ("Drop-down list: Element %s is chosen" % (element_name[item].text))
                    Log.step_succ("Drop-down list: Element %s is chosen" % (element_name[item].text))
                    break
            else:
                print ("Drop-down list: Element [ %s ] not found" % (option_value))
                Log.step_fail("Drop-down list: Element [ %s ] not found" % (option_value))
        else:
            print ("Drop-down list: %s is not a list" % (element_name))
            Log.step_fail("Drop-down list: %s is not a list" % (element_name))
            
    #     if isinstance(element_name, list):
    #         for item in range(len(element_value)):
    #             if option_value == element_value[item]:
    #                 for i in range(len(element_name)):
    #                     if element_name[i].text == element_value[item]:
    #                         element_name[i].click()
    #                         print "Element %s is chosen" %(element_name[i].text)
    #                         break
    #                     else:
    #                         print "Error : Element [ %s ] not found" %(option_value)
    #     else:
    #         print "Error : %s is not a list" %(element_name)

    @classmethod
    def date_picker(self, month, day):
        """
        Input the date, only allow to input month and day,  such as date_picker("10", "30") 
        """

        current_month = date.today().strftime("%m")
        current_day = date.today().strftime("%d")

        input_day = str(day)
        if input_day[0] == "0":
            input_day = input_day[-1]
        else:
            pass

        if int(current_month) == int(month):
            pass
        elif int(current_month) > int(month):
            balance = int(current_month) - int(month)
            while balance > 0:
                Conf.DRIVER.find_element(By.XPATH, "//div[@id='ui-datepicker-div']/div/a/span").click()
                balance -= 1
                time.sleep(2)
        elif int(current_month) < int(month):
            balance = int(month) - int(current_month)
            while balance > 0:
                Conf.DRIVER.find_element(By.XPATH, "//div[@id='ui-datepicker-div']/div/a[2]/span").click()
                balance -= 1
                time.sleep(2)
        else:
            print ("please input correct date")

        time.sleep(2)
        Conf.DRIVER.find_element(By.LINK_TEXT, input_day).click()
            
    @classmethod
    def checkbox_all(cls, elements):
        '''Choose all check boxs
        '''
        for element in elements:
            if element.get_attribute('type') == 'checkbox':
                element.click()
                time.sleep(5)

class Assert(TestCase):
    '''Using this class "Assert" to do assert by expression, e.g. equal, not equal, true, false etc.
    '''
    
    #__init__(self) function to initial the base and super class
    def __init__(self):
        pass
    
    
    def assert_equal(self, first, second, msg = None):
        try:
            self.assertEqual(first, second)
        except AssertionError as e:
            if Conf.BROWSER.upper() != "HTMLUNIT":
                ## Screenshot function causes HtmlUnit execution error, let it go...
                Conf.DRIVER.get_screenshot_as_file("%s\\screenshots\\%s__%s.png" % (Conf.RESULT_PATH, Conf.CASE_NAME, stamp_datetime_co()))
            Log.write_assert_fail_log(str(e))
        else:
            Log.write_assert_success_log(first)
            
    def assert_not_equal(self, first, second, msg = None):
        try:
            self.assertNotEqual(first, second)
        except AssertionError as e:
            if Conf.BROWSER.upper() != "HTMLUNIT":
                ## Screenshot function causes HtmlUnit execution error, let it go...
                Conf.DRIVER.get_screenshot_as_file("%s\\screenshots\\%s__%s.png" % (Conf.RESULT_PATH, Conf.CASE_NAME, stamp_datetime_co()))
            Log.write_assert_fail_log(str(e))
        else:
            Log.write_assert_success_log(first)
    
    def assert_true(self, expr, msg = None):
        try:
            self.assertTrue(expr, msg)
        except AssertionError as e:
            if Conf.BROWSER.upper() != "HTMLUNIT":
                Conf.DRIVER.get_screenshot_as_file("%s\\screenshots\\%s__%s.png" % (Conf.RESULT_PATH, Conf.CASE_NAME, stamp_datetime_co()))
            Log.write_assert_fail_log(str(e))
        else:
            Log.write_assert_success_log(expr)
    
    def assert_false(self, expr, msg = None):
        try:
            self.assertFalse(expr, msg)
        except AssertionError as e:
            if Conf.BROWSER.upper() != "HTMLUNIT":
                Conf.DRIVER.get_screenshot_as_file("%s\\screenshots\\%s__%s.png" % (Conf.RESULT_PATH, Conf.CASE_NAME, stamp_datetime_co()))
            Log.write_assert_fail_log(str(e))
        else:
            Log.write_assert_success_log(expr)
    
    def assert_sequence_equal(self, seq1, expr, msg=None, seq_type=None):
        try:
            self.assertSequenceEqual(seq1, expr, msg, seq_type)
        except AssertionError as e:
            if Conf.BROWSER.upper() != "HTMLUNIT":
                Conf.DRIVER.get_screenshot_as_file("%s\\screenshots\\%s__%s.png" % (Conf.RESULT_PATH, Conf.CASE_NAME, stamp_datetime_co()))
            Log.write_assert_fail_log(str(e))
        else:
            Log.write_assert_success_log(expr)
    
    def assert_list_equal(self, list1, expr, msg=None):
        try:
            self.assertListEqual(list1, expr, msg)
        except AssertionError as e:
            if Conf.BROWSER.upper() != "HTMLUNIT":
                Conf.DRIVER.get_screenshot_as_file("%s\\screenshots\\%s__%s.png" % (Conf.RESULT_PATH, Conf.CASE_NAME, stamp_datetime_co()))
            Log.write_assert_fail_log(str(e))
        else:
            Log.write_assert_success_log(expr)
    
    def assert_tuple_equal(self, tuple1, expr, msg=None):
        try:
            self.assertTupleEqual(tuple1, expr, msg)
        except AssertionError as e:
            if Conf.BROWSER.upper() != "HTMLUNIT":
                Conf.DRIVER.get_screenshot_as_file("%s\\screenshots\\%s__%s.png" % (Conf.RESULT_PATH, Conf.CASE_NAME, stamp_datetime_co()))
            Log.write_assert_fail_log(str(e))
        else:
            Log.write_assert_success_log(expr)
    
    def assert_set_equal(self, set1, expr, msg=None):
        '''
        s1 = set([1,2,3,4])
        s2 = set([1,2,3,4,5])
        Assert().assert_set_equal(s1, s2)
        '''
        try:
            self.assertSetEqual(set1, expr, msg)
        except AssertionError as e:
            if Conf.BROWSER.upper() != "HTMLUNIT":
                Conf.DRIVER.get_screenshot_as_file("%s\\screenshots\\%s__%s.png" % (Conf.RESULT_PATH, Conf.CASE_NAME, stamp_datetime_co()))
            Log.write_assert_fail_log(str(e))
        else:
            Log.write_assert_success_log(expr)
    
    def assert_in(self, member, container, msg=None):
        try:
            self.assertIn(member, container, msg)
        except Exception as e:
            if Conf.BROWSER.upper() != "HTMLUNIT":
                Conf.DRIVER.get_screenshot_as_file("%s\\screenshots\\%s__%s.png" % (Conf.RESULT_PATH, Conf.CASE_NAME, stamp_datetime_co()))
            Log.write_assert_fail_log(str(e))
        else:
            Log.write_assert_success_log(member)
    
    def assert_not_in(self, member, container, msg=None):
        try:
            self.assertNotIn(member, container, msg)
        except Exception as e:
            if Conf.BROWSER.upper() != "HTMLUNIT":
                Conf.DRIVER.get_screenshot_as_file("%s\\screenshots\\%s__%s.png" % (Conf.RESULT_PATH, Conf.CASE_NAME, stamp_datetime_co()))
            Log.write_assert_fail_log(str(e))
        else:
            Log.write_assert_success_log(member)
    
    def assert_is(self, expr1, expr2, msg=None):
        try:
            self.assertIs(expr1, expr2, msg)
        except Exception as e:
            if Conf.BROWSER.upper() != "HTMLUNIT":
                Conf.DRIVER.get_screenshot_as_file("%s\\screenshots\\%s__%s.png" % (Conf.RESULT_PATH, Conf.CASE_NAME, stamp_datetime_co()))
            Log.write_assert_fail_log(str(e))
        else:
            Log.write_assert_success_log(expr2)
    
    def assert_is_not(self, expr1, expr2, msg=None):
        try:
            self.assertNotIs(expr1, expr2, msg)
        except Exception as e:
            if Conf.BROWSER.upper() != "HTMLUNIT":
                Conf.DRIVER.get_screenshot_as_file("%s\\screenshots\\%s__%s.png" % (Conf.RESULT_PATH, Conf.CASE_NAME, stamp_datetime_co()))
            Log.write_assert_fail_log(str(e))
        else:
            Log.write_assert_success_log(expr2)
    
    def assert_dict_equal(self, d1, d2, msg=None):
        try:
            self.assertDictEqual(d1, d2, msg)
        except Exception as e:
            if Conf.BROWSER.upper() != "HTMLUNIT":
                Conf.DRIVER.get_screenshot_as_file("%s\\screenshots\\%s__%s.png" % (Conf.RESULT_PATH, Conf.CASE_NAME, stamp_datetime_co()))
            Log.write_assert_fail_log(str(e))
        else:
            Log.write_assert_success_log(d2)
    
    def assert_dict_contains_subset(self, expected, actual, msg=None):
        '''
        d1 = {'b': 1, 'e': 2, 'f': 3}
        d2 = {'b': 1, 'e': 2, 'f': 3, 't':4}
        Assert().assert_dict_contains_subset(d2, d1)
        '''
        try:
            self.assertDictContainsSubset(expected, actual, msg)
        except Exception as e:
            if Conf.BROWSER.upper() != "HTMLUNIT":
                Conf.DRIVER.get_screenshot_as_file("%s\\screenshots\\%s__%s.png" % (Conf.RESULT_PATH, Conf.CASE_NAME, stamp_datetime_co()))
            Log.write_assert_fail_log(str(e))
        else:
            Log.write_assert_success_log(expected)
    
    def assert_items_equal(self, expected_seq, actual_seq, msg=None):
        '''
        Asserts that each element has the same count in both sequences.
        Example:
            - [0, 1, 1] and [1, 0, 1] compare equal.
            - [0, 0, 1] and [0, 1] compare unequal.
        '''
        try:
            self.assertItemsEqual(expected_seq, actual_seq, msg)
        except Exception as e:
            if Conf.BROWSER.upper() != "HTMLUNIT":
                Conf.DRIVER.get_screenshot_as_file("%s\\screenshots\\%s__%s.png" % (Conf.RESULT_PATH, Conf.CASE_NAME, stamp_datetime_co()))
            Log.write_assert_fail_log(str(e))
        else:
            Log.write_assert_success_log(expected_seq)
    
    def assert_multi_line_equal(self, first, second, msg=None):
        try:
            self.assertMultiLineEqual(first, second, msg)
        except Exception as e:
            if Conf.BROWSER.upper() != "HTMLUNIT":
                Conf.DRIVER.get_screenshot_as_file("%s\\screenshots\\%s__%s.png" % (Conf.RESULT_PATH, Conf.CASE_NAME, stamp_datetime_co()))
            Log.write_assert_fail_log(str(e))
        else:
            Log.write_assert_success_log(second)
    
    def assert_less(self, a, b, msg=None):
        try:
            self.assertLess(a, b, msg)
        except Exception as e:
            if Conf.BROWSER.upper() != "HTMLUNIT":
                Conf.DRIVER.get_screenshot_as_file("%s\\screenshots\\%s__%s.png" % (Conf.RESULT_PATH, Conf.CASE_NAME, stamp_datetime_co()))
            Log.write_assert_fail_log(str(e))
        else:
            Log.write_assert_success_log("Please change this successful message")
    
    def assert_less_equal(self, a, b, msg=None):
        try:
            self.assertLessEqual(a, b, msg)
        except Exception as e:
            if Conf.BROWSER.upper() != "HTMLUNIT":
                Conf.DRIVER.get_screenshot_as_file("%s\\screenshots\\%s__%s.png" % (Conf.RESULT_PATH, Conf.CASE_NAME, stamp_datetime_co()))
            Log.write_assert_fail_log(str(e))
        else:
            Log.write_assert_success_log("Please change this successful message")
    
    def assert_greater(self, a, b, msg=None):
        try:
            self.assertGreater(a, b, msg)
        except Exception as e:
            if Conf.BROWSER.upper() != "HTMLUNIT":
                Conf.DRIVER.get_screenshot_as_file("%s\\screenshots\\%s__%s.png" % (Conf.RESULT_PATH, Conf.CASE_NAME, stamp_datetime_co()))
            Log.write_assert_fail_log(str(e))
        else:
            Log.write_assert_success_log("Please change this successful message")
    
    def assert_greater_equal(self, a, b, msg=None):
        try:
            self.assertGreaterEqual(a, b, msg)
        except Exception as e:
            if Conf.BROWSER.upper() != "HTMLUNIT":
                Conf.DRIVER.get_screenshot_as_file("%s\\screenshots\\%s__%s.png" % (Conf.RESULT_PATH, Conf.CASE_NAME, stamp_datetime_co()))
            Log.write_assert_fail_log(str(e))
        else:
            Log.write_assert_success_log("Please change this successful message")
    
    def assert_is_none(self, obj, msg=None):
        try:
            self.assertIsNone(obj, msg)
        except Exception as e:
            if Conf.BROWSER.upper() != "HTMLUNIT":
                Conf.DRIVER.get_screenshot_as_file("%s\\screenshots\\%s__%s.png" % (Conf.RESULT_PATH, Conf.CASE_NAME, stamp_datetime_co()))
            Log.write_assert_fail_log(str(e))
        else:
            Log.write_assert_success_log("Please change this successful message")
    
    def assert_is_not_none(self, obj, msg=None):
        try:
            self.assertIsNotNone(obj, msg)
        except Exception as e:
            if Conf.BROWSER.upper() != "HTMLUNIT":
                Conf.DRIVER.get_screenshot_as_file("%s\\screenshots\\%s__%s.png" % (Conf.RESULT_PATH, Conf.CASE_NAME, stamp_datetime_co()))
            Log.write_assert_fail_log(str(e))
            print ("e")
        else:
            Log.write_assert_success_log("Please change this successful message")
            print ("ok")
    
    def assert_is_instance(self, obj, cls, msg=None):
        try:
            self.assertIsInstance(obj, cls, msg)
        except Exception as e:
            if Conf.BROWSER.upper() != "HTMLUNIT":
                Conf.DRIVER.get_screenshot_as_file("%s\\screenshots\\%s__%s.png" % (Conf.RESULT_PATH, Conf.CASE_NAME, stamp_datetime_co()))
            Log.write_assert_fail_log(str(e))
        else:
            Log.write_assert_success_log("Please change this successful message")
    
    def assert_not_is_instance(self, obj, cls, msg=None):
        try:
            self.assertNotIsInstance(obj, cls, msg)
        except Exception as e:
            if Conf.BROWSER.upper() != "HTMLUNIT":
                Conf.DRIVER.get_screenshot_as_file("%s\\screenshots\\%s__%s.png" % (Conf.RESULT_PATH, Conf.CASE_NAME, stamp_datetime_co()))
            Log.write_assert_fail_log(str(e))
        else:
            Log.write_assert_success_log("Please change this successful message")
    
    def assert_equal_spinder(self, spinner_options_value, list_expected):
        """
        :Purpose: To judge whether the text value of the drop_down list is as expected
        
        :Args:
         - spinner_options_value:    Items(options) of drop_down list, the type is string list
         - list_expected:            Expected items must be matched with, the type is string list
        
        :Usage:
            Assert().assert_equal_spinder(OverviewSearch.Profile.POFS_EXPTYPE_CONTENT, 
                                          ["LCL", "FCL", "Select", "AIR", "TRUCK"])
        """
        for i in range(len(list_expected)):
            if spinner_options_value[i] in list_expected:
                pass
            else:
                print ("Error : [ %s ] is not as expected in %s" %(spinner_options_value[i],list_expected))   #should write it to result file


class Browser():
    '''Using this class to handle the window action
    '''
    
    @classmethod
    def scroll_to(cls, x, y):
#         log.step_normal(u"Element [%s]: Scroll To [%s, %s]" % (cls.__name__, x, y))
        Conf.DRIVER.execute_script("window.scrollTo(%s, %s);" % (x, y))
        
        time.sleep(3)
    
    @classmethod
    def navigate_to(cls, url):
#         log.step_normal(u"Element [%s]: Navigate To [%s]" % (cls.__name__, url))
        Conf.DRIVER.get(url)
        time.sleep(5)
    
    @classmethod
    def navigate_back(cls):
        Conf.DRIVER.back()
    
    @classmethod
    def navigate_forward(cls):
        Conf.DRIVER.forward()
    
    @classmethod
    def skip_ie_certification_error(cls):
#         log.step_normal("IE Skip SSL Cert Error.")
        Conf.DRIVER.get("javascript:document.getElementById('overridelink').click();")
    
    @classmethod
    def delete_all_cookies(cls):
        Conf.DRIVER.delete_all_cookies()
    
    @classmethod
    def get_current_window(cls):
        """
        :Purpose: Returns the handle of the current window.
        
        :Args:
         - driver : Instance of webdriver
        
        :Usage:
            Browser.get_current_window(driver)
        
        :Return:
            The handle ID of the current window.
        """
        return Conf.DRIVER.current_window_handle

    @classmethod
    def get_windows(cls):
        """
        :Purpose: Get all windows handle ID as a list
        
        :Args:
         - driver : Instance of webdriver
        
        :Usage:
            Browser.get_windows(driver)
        
        :Return:
            A list contains all window handle ID for a certain driver instance.
        """
        return Conf.DRIVER.window_handles

    @classmethod
    def switch_to_window(cls, handle_id=None):
        """
        :Purpose: Perform the action to switch current window to the 
                    new window by handle ID
        
        :Args:
         - handle_id:            The windows handle ID fetched by function 
                                 "get_windows(cls, driver)"
        
        :Usage:
            Browser.switch_to_window(handle_id)
        """
        Conf.DRIVER.switch_to_window(handle_id)
    
    
    @classmethod
    def switch_to_new_window(cls):
        """
        :Purpose: Switch to the new (the pop-up page) page if system is 
                    focusing on the current page(the primary page).
                    Function just think about there're two windows(handles)
                    at the same time.
        
        :Args:
         - driver : Instance of webdriver
        
        :Usage:
            Browser.switch_to_new_window(self.driver)
        """
        win_handles_num = cls.get_windows()
        if len(win_handles_num) == 2:
            #Cause "get_windows" is set as : @property, so use cls.window_handles
#             driver.switch_to_window(cls.get_windows(driver)[-1])
            Conf.DRIVER.switch_to_window(Conf.DRIVER.window_handles[-1])
        else:
            print ("There are %d windows handles available, 2 handles is valid." % len(win_handles_num))
            Log.step_fail("There are %d windows handles available, 2 handles is valid." % len(win_handles_num))    
    
    @classmethod
    def switch_to_default_window(cls):
        """
        :Purpose: Switch to the primary(the last one page) page if system is 
                    focusing on the pop up page(the new page).
                    Function just think about there're two windows(handles)
                    at the same time.
        
        :Args:
         - driver : Instance of webdriver
        
        :Usage:
            Browser.switch_to_default_window(self.driver)
        """
        win_handles_num = cls.get_windows()
        if 1 <= len(win_handles_num) <= 2:
#             driver.switch_to_window(cls.get_windows(driver)[0])
            Conf.DRIVER.switch_to_window(Conf.DRIVER.window_handles[0])
#             driver.switch_to.default_content()                #do not work
        else:
            print ("There are %d windows handles available, 2 handles is valid." % len(win_handles_num))
            Log.step_fail("There are %d windows handles available, 2 handles is valid." % len(win_handles_num))
    
    @classmethod
    def switch_to_frame(cls, frame_reference):
        """
        :Purpose: Focus on to the certain frame by id / name / webelement
        
        :Args:
         - driver:            Instance of webdriver
         - frame_reference:    The name of the window to switch to, an integer representing the index,
                            or a webelement that is an (i)frame to switch to.
        
        :Usage:
            driver.switch_to_frame("frame_name")
            driver.switch_to_frame(1)
            driver.switch_to_frame(driver.find_elements_by_tag_name("iframe")[0])
        """
        Conf.DRIVER.switch_to.frame(frame_reference)
    
    @classmethod
    def switch_to_parent_frame(cls):
        """
        Switches focus to the parent context. If the current context is the top
        level browsing context, the context remains unchanged.

        :Usage:
            driver.switch_to_parent_frame()
        """
        Conf.DRIVER.switch_to.parent_frame()
    
    @classmethod
    def alert_accept(cls):
        """"""
        try:
            Conf.DRIVER.switch_to_alert().accept()
            time.sleep(1)
        except NoAlertPresentException:
                print ("Alert Not Found.")
        try:
            Conf.DRIVER.switch_to.default_content()
        except:
            pass
    
    @classmethod
    def alert_dismiss(cls):
        """"""
        try:
            Conf.DRIVER.switch_to_alert().dismiss()
            time.sleep(1)
        except NoAlertPresentException:
                print ("Alert Not Found.")
        try:
            Conf.DRIVER.switch_to.default_content()
        except:
            pass
    
    @classmethod
    def alert_text(cls):
        """"""
        return Conf.DRIVER.switch_to_alert().text
    
    @classmethod
    def alert_input_value(cls, value):
        """"""
        Conf.DRIVER.switch_to_alert().send_keys(value)
        Conf.DRIVER.switch_to.default_content()
        
    @classmethod
    def alert_text_involved(cls, txt_value):
#         log.step_normal("alert_text_involved [%s]" % txt_value)
        alert_text = Conf.DRIVER.switch_to_alert().text()
        
        if txt_value in alert_text:
#             log.step_pass("pass")
            print ("pass")
        else:
#             log.step_fail("fail")
            print ("fail")
        Conf.DRIVER.switch_to_default_content()
    
    @classmethod
    def refresh(cls):
        """"""
        Conf.DRIVER.refresh()
        time.sleep(3)
    
    @classmethod
    def quit_window(cls):
        """Close all windows opened and quit the auto test.
        """
        Conf.DRIVER.quit()
    
    @classmethod
    def close_window(cls):
        """Close the current window
        """
        Conf.DRIVER.close()


