import os
import xlrd
from sys import platform
from selenium import webdriver

# Working directories
cwd = os.getcwd()
drivers = os.path.join(cwd, 'drivers')

# Browser
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")

if platform == "win32":
    driver = webdriver.Chrome(os.path.join(drivers, 'chromedriver-win-80'), chrome_options=chrome_options)
elif platform == "linux":
    driver = webdriver.Chrome(os.path.join(drivers, 'chromedriver-linux-80'), chrome_options=chrome_options)

# URL config
HOME_URL = 'https://mysixeighty.com.au'
LOGIN_URL = HOME_URL + '/user/login'
EVENTS_URL = HOME_URL + '/events'

# User config
LOGIN_DETAILS = cwd + r'\login_user_pass.xlsx'
EVENTS = cwd + r'\events_selection.xlsx'

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


def get_events_options():
    pass
