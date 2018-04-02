# -*- coding: utf-8 -*-
import HTMLTestRunner
from datetime import datetime
from datetime import timedelta
import doctest
from email.mime.multipart import MIMEMultipart  
from email.mime.text import MIMEText
import suds
import importlib
import inspect
import os.path
import smtplib  
import unittest
import urllib
import zipfile
import sys

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

sys.path.append("..")
from conf.Conf import *
from library import Log
from library.Log import *

class DriverInvoker:
    
    def __init__(self, driverName):
        self.driverName = driverName
        self.url = Conf.URL
#判断使用哪种浏览器 : firefox，chrome，IE

    def webBrowser(self):
        if self.driverName.upper() == 'FIREFOX':
            '''There are 2 different way to get the instance of webdriver:
                1. Use configuration file to record it, but when use it, system will not recognize its methods, but useful.
                    i.e.    Conf.BROWSER = webdriver.Firefox()
                            
                            #-> Init and create instance
                            di = DriverInvoker("firefox");
                            di.webBrowser()
                            Conf.BROWSER.get(Conf.URL)
                            Conf.BROWSER.maximize_window()
                            Conf.BROWSER.quit()
                2. To return the instance of webdriver.
                    i.e.    DRIVER = webdriver.Firefox()
                            return DRIVER
                            
                            #-> Init and create instance
                            di = DriverInvoker("firefox");
                            DRIVER = di.webBrowser()
                            DRIVER.get(Conf.URL)
                            DRIVER.maximize_window()
                            DRIVER.quit()
            '''
            fp = FirefoxProfile()
            fp.native_events_enabled = False
            Conf.DRIVER = webdriver.Firefox(firefox_profile=fp)
            
        elif self.driverName.upper() == 'CHROME':
            os.popen("TASKKILL /F /IM chromedriver.exe")

            Conf.DRIVER = webdriver.Chrome(executable_path=Conf.DRIVER_CHROME)
            
        elif self.driverName.upper() == 'IE':
            os.popen("TASKKILL /F /IM IEDriverServer.exe")
            
            dc = DesiredCapabilities.INTERNETEXPLORER.copy()
            dc['acceptSslCerts'] = True
            dc['nativeEvents'] = True
            dc['ignoreProtectedModeSettings'] = True
            
            os.environ["webdriver.ie.DRIVER"] = Conf.DRIVER_IE
            Conf.DRIVER = webdriver.Ie(executable_path=Conf.DRIVER_IE, capabilities=dc)
    
        else:
            return None

"""Invoking "LoginApp" to call function of selenium
	to lunch the browser and navigate to a tested_page
"""
class LoginApp:
    def sysLogin(self):
        di = DriverInvoker(Conf.BROWSER)
        di.webBrowser()
        DRIVER = Conf.DRIVER
        DRIVER.implicitly_wait(30)
        DRIVER.get(Conf.URL)
        DRIVER.maximize_window()
        
        return DRIVER

"""
    Convert special char to normal string
"""
def urlcode(date):
    return urllib.parse.quote(str(date))

def get_info_http(url, param_in, method, post_key = None):
    """
        HTTP GET / POST to get the result from HTTP server.
        +++NOTE: should optimize the input parameter to get more
            pair of key-values
        :Usage: 
            if __name__ == "__main__":
                url_post = url_base = 'http://api.liqwei.com/location/'
                url_get = 'http://api.liqwei.com/location/?ip='
    
                print get_info_http(url_get, "202.108.33.32", "GET")
                print get_info_http(url_post, "202.108.33.32", "POST", "ip")
    """
    if method.upper() == 'GET':
        url_get = url + urlcode(param_in)
        result = urllib.request.urlopen(url_get).read()
        return result
   
    elif method.upper() == 'POST':
        url_post = url
        values = {post_key : param_in}
        data = urllib.urlencode(values)
        req = urllib.request.Request(url_post, data)
        response = urllib.request.urlopen(req)
        result = response.read()
        return result
    else:
        return None

'''
    WebService
'''
def get_info_wb(url, param_in=None):
    """
        +++NOTE: should optimize the input parameter to get more
    """
    client = suds.client.Client(url)
    service = client.service
    
    '''
    Use this 'client' to know the methods of this WebService, like :
        Service ( qqOnlineWebService ) tns="http://WebXml.com.cn/"
        Prefixes (0)
        Ports (2):
          (qqOnlineWebServiceSoap)
             Methods (1):
                qqCheckOnline(xs:string qqCode, )
             Types (0):
          (qqOnlineWebServiceSoap12)
             Methods (1):
                qqCheckOnline(xs:string qqCode, )
             Types (0):
    '''
    print (client)
    
    status = service.qqCheckOnline(param_in)
    print (status)
    
    '''
        Use "client.last_received()" to get the response message of WebService, like : 
        <?xml version="1.0" encoding="UTF-8"?>
            <soap:Envelope>
               <soap:Body>
                  <qqCheckOnlineResponse xmlns="http://WebXml.com.cn/">
                     <qqCheckOnlineResult>Y</qqCheckOnlineResult>
                  </qqCheckOnlineResponse>
               </soap:Body>
            </soap:Envelope>
    '''
    print (client.last_received())
    
    return status

def send_mail(attachment_file_name):
    print (attachment_file_name)
#     attach_name = attachment_file_name.split('\\')[4].split('.')[0]
    attach_name = attachment_file_name.split('\\')[4]
    
    sender      = Conf.MAIL_SENDER
    receiver    = Conf.MAIL_RECEIEVER
    subject     = Conf.MAIL_SUBJECT
    smtpserver  = Conf.MAIL_SMTPSERVER
    username    = Conf.MAIL_USERNAME
    password    = Conf.MAIL_PASSWORD
    
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = subject
    
    # Construct the attachment
    att = MIMEText(open(attachment_file_name, 'rb').read(), 'base64', 'utf-8')
    att["Content-Type"] = 'application/octet-stream'
    att["Content-Disposition"] = 'attachment; filename=%s' % attach_name
    msgRoot.attach(att)
    
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msgRoot.as_string())
    smtp.quit()
    print ("Mail sended successfully")
    Log.init_env_record("Mail sended successfully")

def import_module_dynamic(pageName):
    """Import the module which is the name of a certain page
    """
    return importlib.import_module(Conf.PAGE + pageName)

def make_directory(directory_name, flag="result"):
    '''Make directory under the project result
    '''
    if flag == "result":
        mkdirs("%s\\%s\\" % (Conf.RESULT_PATH, directory_name))
    elif flag == "project":
        mkdirs("%s\\%s\\" % (Conf.PROJECT_PATH, directory_name))
    else:
        return False

def generate_report(report_name="default_report_name"):
    '''Generate report with report name as input parameter
    '''
    make_directory("reports", "result")
    file_name = "%s\\reports\\%s.html" % (Conf.RESULT_PATH, report_name)
    fp = open(file_name, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
                                          stream=fp,
                                          title=Conf.REPORT_TITLE,
                                          description=Conf.REPORT_DESC)
    return runner

"""Get system date"""
def current_date():
    return datetime.now().strftime('%Y.%m.%d')

"""balance=1 means one day later, etc..."""
def future_date(balance):
    now = datetime.now()
    add1 = timedelta(days=balance)
    now1 = now + add1
    return now1.strftime('%Y.%m.%d')

def select_month(balance):
    now = datetime.now()
    add1 = timedelta(days=balance)
    now1 = now + add1
    return now1.strftime('%m')

def select_day(balance):
    now = datetime.now()
    add1 = timedelta(days=balance)
    now1 = now + add1
    return now1.strftime('%d')
#
# def execute_automation_test(send_flag=None, report_name=Conf.REPORT_FILE_NAME):
#     '''Used to load test cases, execute the test case and generate the report
#     '''
#     load_test_case_record('   %s Initial environment...' % stamp_datetime())
#
#     suite = doctest.DocTestSuite()
#     cases = Case_List.case_list()
#
#     load_test_case_record('   %s Case loading start...' % stamp_datetime())
#     print ('Case loading start...')
#     for case in cases:
#         try:
#             suite.addTest(unittest.defaultTestLoader.loadTestsFromName(case))
#             load_test_case_record("+> %s %s is loaded successfully." % (stamp_datetime(), case))
#         except Exception as e:
#             load_test_case_record('-> %s ERROR: Skipping tests from "%s" from err_msg : %s.' % (stamp_datetime(), case, str(e)))
#             try:
#                 __import__(case)
#             except ImportError as e:
#                 load_test_case_record('----------> %s, can not import it.' % str(e))
#             else:
#                 load_test_case_record('==========> Could not load the test suite, please contact service desk.')
#     load_test_case_record('   %s Case loading done!' % stamp_datetime())
#     print ('Case loading done!')
# #             from traceback import print_exc
# #             print_exc()
#     print (load_test_case_record('   %s Running the tests...' % stamp_datetime()))
#     print ('Running the tests...')
#
#     # Generate the test report
#     generate_report(report_name).run(suite)
#
#     # Judge to send email
#     if send_flag is not None:
#         send_mail(ArchiveFile.zip_dir())
#     else:
#         return None

def get_value_from_conf(key):
    '''Used to get value by key from configuration file : //config/conf.ini
    '''
    conf_file = u"%s\\conf.ini" % Conf.CONFIG_PATH
    
    if not os.path.exists(conf_file):
        return ""
    
    if not os.path.isfile(conf_file):
        return ""
    
    try:
        with open(conf_file, 'r') as f:
            while True:
                data = f.readline()
                
                if not data:
                    break
                
                if len(data.split('=')) < 2:
                    continue
                
                if data.strip()[0] == "#":
                    continue
                
                if data.split('=')[0].strip() == key:
                    return str(data.split('=', 1)[1].strip())
    except IOError:
        return ""

if __name__ == '__main__':
    pass
