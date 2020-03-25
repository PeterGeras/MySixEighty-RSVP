import os
import xlrd
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import InvalidCookieDomainException
import pickle

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
log_file = os.path.join(logs, 'geckodriver.log')
driver = webdriver.Firefox(
    desired_capabilities=caps,
    executable_path=driver_loc,
    log_path=log_file
)
open(log_file, 'w').close()  # Clear contents of log file

# Cookies
cookies_pickle_file = drivers + r'\cookies.pkl'

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


def load_cookies():
    return_success = False

    print("")
    try:
        with open(cookies_pickle_file, 'rb') as f:
            # Dummy URL needs to load first before loading cookies successfully
            driver.get(HOME_URL + '/404error')
            for cookie in pickle.load(f):
                driver.add_cookie(cookie)
        print(f"# Cookies loaded from {cookies_pickle_file}")
        return_success = True
    except FileNotFoundError:
        print(f"# Cookies not found at {cookies_pickle_file}")
    except InvalidCookieDomainException:
        print(f"# Cookies need to be loaded from a 404 error page")
    except Exception as ex:
        print(f"# Pickling load error with {cookies_pickle_file}")

    return return_success


def save_cookies():
    return_success = False

    print("")
    try:
        pickle.dump(driver.get_cookies(), open(cookies_pickle_file, "wb"))
        print(f"# Cookies saved to {cookies_pickle_file}")
        return_success = True
    except IOError:
        print(f"# Cookies unable to be saved to {cookies_pickle_file}")
    except Exception as ex:
        print(f"# Pickling save error with {cookies_pickle_file}")

    return return_success


def get_login_data():
    print("")
    # Update Login_Data dictionary

    try:
        wb_login = xlrd.open_workbook(LOGIN_DETAILS)
        ws_login = wb_login.sheet_by_index(0)

        email = ws_login.cell(1, 0).value
        password = ws_login.cell(1, 1).value
    except Exception as ex:
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
