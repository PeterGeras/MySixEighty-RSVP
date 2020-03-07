import os
import xlrd
from sys import platform
from selenium import webdriver

# Current working directory
cwd = os.getcwd()
file_directory = os.path.join(cwd, 'output')

# Browser
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")

if platform == "win32":
    driver = webdriver.Chrome(os.path.join(cwd, 'chromedriver-win-80'), chrome_options=chrome_options)
elif platform == "linux":
    driver = webdriver.Chrome(os.path.join(cwd, 'chromedriver-linux-80'), chrome_options=chrome_options)

# URL config
HOME_URL = 'https://mysixeighty.com.au'
LOGIN_URL = HOME_URL + '/user/login'
EVENTS_URL = HOME_URL + '/events'

# Constants
SEC = 1
MIN = 60
PAGE_WAIT_TIME = 1 * MIN
ELEMENT_WAIT_TIME = 5 * SEC
END_PROGRAM_WAIT_TIME = 2 * MIN

MAX_TRIES = 3

# User config
LOGIN_DETAILS = cwd + r'\login_user_pass.xlsx'
URL_LIST = cwd + r'\url_check.xlsx'

# Input files/folders
REPORTS_DIR = cwd + r'\_reports'

Login_Data = {
    'email': '',
    'password': ''
}


def get_login_data():
    # Update Login_Data dictionary

    try:
        wb_login = xlrd.open_workbook(LOGIN_DETAILS)
        ws_login = wb_login.sheet_by_index(0)

        email = ws_login.cell(1, 0).value
        password = ws_login.cell(1, 1).value
    except:
        print("Failed to grab email and password data from: " + LOGIN_DETAILS)
        return False

    Login_Data['email'] = email
    Login_Data['password'] = password

    return True
