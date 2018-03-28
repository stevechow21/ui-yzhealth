# -*- coding: gbk -*-
from datetime import datetime
import inspect
import os, sys
sys.path.append("..")
from conf import Conf
from imp import reload
from conf.Conf import *

reload(sys)
# sys.setdefaultencoding('gbk')

def stamp_date():
    return datetime.now().strftime("%Y-%m-%d")

def stamp_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def stamp_datetime_coherent():
    return datetime.now().strftime("%Y-%m-%d")

def stamp_datetime_co():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def mkdirs(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def handle_error(driver):
    if sys.exc_info()[0] != None:
        if Conf.BROWSER.upper() != "HTMLUNIT":
            # # Screenshot function causes HtmlUnit execution error, let it go...
            driver.get_screenshot_as_file("%s\\screenshots\\%s__%s.png" % (Conf.RESULT_PATH, Conf.CASE_NAME, stamp_datetime_co()))
        write_system_log(exception_error())

def handle_error_wo():
        if sys.exc_info()[0] != None:
            write_system_log(exception_error())

def exception_error():
    error_message = ""
    
    for i in range(len(inspect.trace())):
        error_line = u"""
File:      %s - [%s]
Function:  %s
Statement: %s
-------------------------------------------------------------------------------------------""" % (
        inspect.trace()[i][1],
        inspect.trace()[i][2],
        inspect.trace()[i][3],
        inspect.trace()[i][4])
        
        error_message = "%s%s" % (error_message, error_line)
    error_message = """=========>>>System Error!
%s
%s
======================================== Error Message ====================================%s

======================================== Error Message ======================================================""" % (sys.exc_info()[0], sys.exc_info()[1], error_message)
    
    return error_message

def start_test(case_name):
    Conf.CASE_NAME = case_name
    Conf.CASE_START_TIME = datetime.now().replace(microsecond=0)
    Conf.CASE_PASS = True
    
    mkdirs("%s\\screenshots\\" % Conf.RESULT_PATH)
    mkdirs("%s\\logs\\" % Conf.RESULT_PATH)
    
    with open(u"%s\\logs\\%s__%s.log" % (Conf.RESULT_PATH, Conf.CASE_NAME, stamp_datetime_coherent()), "a") as f:
        f.write(u"\n**************  Test Case [%s] [BROWSER: %s]  ***************\n\n" % (Conf.CASE_NAME, Conf.BROWSER))

def stop_test():
    Conf.CASE_STOP_TIME = datetime.now().replace(microsecond=0)
    
    if Conf.CASE_PASS is True:
        with open(u"%s\\logs\\%s__%s.log" % (Conf.RESULT_PATH, Conf.CASE_NAME, stamp_datetime_coherent()), "a") as f:
            f.write(u"\n**************  Test Case [%s] [TIMEUSED: %s]  ***************\n" % (Conf.CASE_NAME, Conf.CASE_STOP_TIME - Conf.CASE_START_TIME))
    else:
        with open(u"%s\\logs\\%s__%s.log" % (Conf.RESULT_PATH, Conf.CASE_NAME, stamp_datetime_coherent()), "a") as f:
            f.write(u"\n**************  Test Case [%s] [TIMEUSED: %s]  ***************\n" % (Conf.CASE_NAME, Conf.CASE_STOP_TIME - Conf.CASE_START_TIME))

def load_test_case_record(message):
    '''Used by case loader
    '''
    with open(u"%s\\logs\\%s__%s.log" % (Conf.RESULT_PATH, Conf.CASE_LOAD, stamp_datetime_coherent()), "a") as f:
        f.write(u"\n%s\n" % (message))

def init_env_record(message):
    '''Used by selenium environment set up
    '''
    with open(u"%s\\logs\\%s__%s.log" % (Conf.RESULT_PATH, Conf.ENV_INIT, stamp_datetime_coherent()), "a") as f:
        f.write(u"\n%s\n" % (message))

def write_system_log(message):
    Conf.CASE_PASS = False
    with open(u"%s\\logs\\%s__%s.log" % (Conf.RESULT_PATH, Conf.CASE_NAME, stamp_datetime_coherent()), 'a') as f:
        f.write(u"%s    FAIL: %s\n" % (stamp_datetime(), message))
        

def write_assert_fail_log(message):
    Conf.CASE_PASS = False
    with open(u"%s\\logs\\%s__%s.log" % (Conf.RESULT_PATH, Conf.CASE_NAME, stamp_datetime_coherent()), 'a') as f:
#         f.write("\n")
        message = """===>>>Assertion Error!
======================================== Start Error Message ====================================
>>>>>>
CASE_NAME: %s
ERROR_MSG: %s
>>>>>>
======================================== End Error Message ===============================================""" % (Conf.CASE_NAME, message)
        f.write(u"%sH    ASSERT FAIL: %s\n" % (stamp_datetime(), message))

def write_assert_success_log(value):
    with open(u"%s\\logs\\%s__%s.log" % (Conf.RESULT_PATH, Conf.CASE_NAME, stamp_datetime_coherent()), 'a') as f:
#         f.write("\n")
        message = "===>>> Value [ %s ] of case [ %s ] is as excepted." % (value, Conf.CASE_NAME)
        f.write(u"%s    ASSERT PASS: %s\n" % (stamp_datetime(), message))

def step_succ(message):
    with open(u"%s\\logs\\%s__%s.log" % (Conf.RESULT_PATH, Conf.CASE_NAME, stamp_datetime_coherent()), 'a') as f:
        f.write(u"%s    STEP PASS: %s\n" % (stamp_datetime(), message))

def step_fail(message):
    with open(u"%s\\logs\\%s__%s.log" % (Conf.RESULT_PATH, Conf.CASE_NAME, stamp_datetime_coherent()), 'a') as f:
        f.write(u"%s    STEP FAIL: %s\n" % (stamp_datetime(), message))
