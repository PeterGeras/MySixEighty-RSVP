import os
import xlrd
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from Event import Event


# Working directories
cwd = os.getcwd()
drivers = os.path.join(cwd, 'drivers')
logs = os.path.join(cwd, 'logs')

# Browser
caps = DesiredCapabilities().FIREFOX
# caps["pageLoadStrategy"] = "normal"  # complete
caps["pageLoadStrategy"] = "eager"  # interactive
# caps["pageLoadStrategy"] = "none"
driver_loc = os.path.join(drivers, 'geckodriver-win-v0.26')
driver = webdriver.Firefox(
    desired_capabilities=caps,
    executable_path=driver_loc,
    log_path=os.path.join(logs, 'geckodriver.log')
)

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

# Weeks
THIS_WEEK = 1
NEXT_WEEK = 2
Week = {
    'This': THIS_WEEK,
    'Next': NEXT_WEEK
}


def get_login_data():
    print("")
    # Update Login_Data dictionary
    try:
        wb_login = xlrd.open_workbook(LOGIN_DETAILS)
        ws_login = wb_login.sheet_by_index(0)

        email = ws_login.cell(1, 0).value
        password = ws_login.cell(1, 1).value
    except:
        print(f"# Failed to grab email and password data from {LOGIN_DETAILS}")
        return False

    Login_Data['email'] = email
    Login_Data['password'] = password

    print(f"# Logged in with with data from {LOGIN_DETAILS}")
    print(f"Login: {Login_Data['email']}")
    print(f"Pass: {len(Login_Data['password'])*'*'}")

    return True


def get_events_selected():
    wb = xlrd.open_workbook(EVENTS)
    sheet = wb.sheet_by_index(0)
    events = []

    for i in range(1, sheet.nrows):
        go = sheet.cell_value(i, 0)
        if go == "Yes":
            name = sheet.cell_value(i, 1)
            week = sheet.cell_value(i, 3)
            event = Event.set_from_excel(Week[week], name)
            events.append(event)

    return events
