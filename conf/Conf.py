#-*- coding: UTF-8 -*-

#配置浏览器
BROWSER       = "FIREFOX"
DRIVER = ""

# Driver of web browser, such as: webdriver.Firefox()
# BROWSER             = ""

# 测试站点
URL                 = u"http://172.16.10.100:17021/yzhealth-portal/auth/toLogin.do"

#下拉列表的Xpath路径
ProvinceList		= "//button[@type='button']"
JiangSu             = "//div[@id='regionApp']/div/div/div/ul/li[17]/a/span"
CityList     		= "(//button[@type='button'])[2]"
SuZhou		        = "//div[@id='regionApp']/div[2]/div/div/ul/li[6]/a/span"
OrgList		        = "(//button[@type='button'])[3]"
Jiulong             = "//div[@id='regionApp']/div[3]/div/div/ul/li[16]/a/span"

# 项目及结果路径
PROJECT_PATH        = u"D:\\testcode\\automation"
RESULT_PATH         = u"D:\\testcode\\automation\\result"
XML_PATH			= u"D:\\testcode\\automation\\data\\info.xml"
 
# # Location of DRIVER(CHROME / FIREFOX / IE)
DRIVER_CHROME       = u"C:\Python27\chromedriver.exe"
# DRIVER_IE           = r"C:\Python27\IEDriverServer.exe"
# DRIVER_FIREFOX      = ""

# Location of WEB BROWSER
# BINARY_CHROME       = u"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
# BINARY_FIREFOX      = ""
# BINARY_IE           = ""

# Test Case/Module variables.
CASE_START_TIME     = ""
CASE_STOP_TIME      = ""
CASE_NAME           = ""
CASE_PASS           = ""
CASE_LOAD           = "LOAD_TEST_CASE"
ENV_INIT            = "ENV_INIT"

MODULE_NAME         = ""

PAGE                = ""

REPORT_FILE_NAME    = "基层UI自动化测试报告"
REPORT_TITLE        = "自动化测试报告"
REPORT_DESC         = "This is desc of report"

# zip file name
LOG_FILES            = "Auto_Test_Log"

# email config
MAIL_SENDER         = ''
MAIL_RECEIEVER      = ''
MAIL_SUBJECT        = 'Test report fom Automation testing'
MAIL_SMTPSERVER     = 'smtp.163.com'
MAIL_USERNAME       = ''
MAIL_PASSWORD       = ''

# Database Operation
# MySQL
# MYSQL_IP               = u"172.10.16.100"
# MYSQL_USERNAME         = u"root"
# MYSQL_PASSWORD         = u"123456"
# MYSQL_DBNAME             = u"yzhealth"
# MYSQL_CHARSET          = u"utf8"

# Oracle
# ORACLE_IP               = u"127.0.0.1"
# ORACLE_PORT             = u"1521"
# ORACLE_USERNAME         = u"sdp"
# ORACLE_PASSWORD         = u"sdp"
# ORACLE_INSTANCE             = u"sdp"



