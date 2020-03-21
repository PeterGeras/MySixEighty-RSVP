import timeit
import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

import config
from Event import Event
from Event import print_event_list_details, intersection_events_lists, difference_events_lists
from event_rsvp import event_rsvp

# Time
SEC = 1
MIN = 60
SHORT_TIME = 0.2 * SEC
ELEMENT_WAIT_TIME = 2 * SEC
PAGE_WAIT_TIME = 10 * SEC
LOGIN_WAIT_TIME = 2 * MIN

MAX_TRIES = int(PAGE_WAIT_TIME / SHORT_TIME)

# Browser
driver = config.driver


def login_load():
    driver.get(config.LOGIN_URL)

    account_logged_id = "menu-trigger-account"

    login_details_captured = config.get_login_data()
    if login_details_captured is True:
        # Enter login details automatically
        try:
            email = driver.find_element_by_id("edit-email")
            email.send_keys(config.Login_Data['email'])

            password = driver.find_element_by_id("edit-password")
            password.send_keys(config.Login_Data['password'])

            login = driver.find_element_by_id("edit-submit")
            login.click()
        except:
            print("# Logging in automatically failed")
            return False
    else:
        # Enter login details manually
        print("# Please log in manually...")
        try:
            WebDriverWait(driver, LOGIN_WAIT_TIME).until(
                EC.presence_of_element_located((By.ID, account_logged_id))
            )
        except:
            print("# Login took too long")
            return False

    # Check login happened and redirected to main page
    try:
        WebDriverWait(driver, PAGE_WAIT_TIME).until(
            EC.presence_of_element_located((By.ID, account_logged_id))
        )
    except:
        print("# Login redirection to main page failed? div_id " + account_logged_id + " not found")
        return False

    return True


def events_load():
    driver.get(config.EVENTS_URL)

    event_week_class = "event-week"

    try:
        WebDriverWait(driver, PAGE_WAIT_TIME).until(
            EC.presence_of_element_located(By.CLASS_NAME, event_week_class)
        )
    except TimeoutException:
        print("# Events page not loading")
        return False

    # Loads second week of events
    for i in range(MAX_TRIES):
        time.sleep(SHORT_TIME)

        # Forces load of events second week by scrolling to bottom and back to top
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.execute_script("window.scrollTo(0, 0);")

        # Find second week
        event_weeks = driver.find_elements_by_class_name(event_week_class)
        if len(event_weeks) > 1:
            break
    else:
        print("# Events page not loading second week")
        return False

    return True


def events_find():
    events = []

    try:
        events_form = driver.find_element_by_class_name("events-week-list")
    except:
        print("# div should have been found earlier in events_load function")
        return False

    try:
        events_week = events_form.find_elements_by_xpath(".//div[@class='event-week']")
    except:
        print("# Page code structure changed, aborting")
        return False

    if len(events_week) != 2:
        print("# Number of weeks found is not 2, continuing...")

    # This week, next week etc.
    # Enumeration - https://www.geeksforgeeks.org/enumerate-in-python/
    for week, event_week in enumerate(events_week, config.THIS_WEEK):
        try:
            event_cards = event_week.find_elements_by_xpath(".//div[@class='event-card']")
        except:
            print("# Page code structure changed, aborting")
            return False
        for e in event_cards:
            events.append(Event.set_from_div(week, e))

    return events


def main():
    start = timeit.default_timer()

    # Get events from workbook that user wants to go to
    goto_events = config.get_events_selected()
    print_event_list_details("Events chosen to look for", goto_events)

    if len(goto_events) == 0:
        print("# No selected events from " + config.EVENTS + " found")
        return False

    if login_load() is False:
        return False

    if events_load() is False:
        return False

    all_events = events_find()
    print_event_list_details("Events found on the webpage", all_events)

    intersection_list = intersection_events_lists(goto_events, all_events)
    print_event_list_details("Events chosen & found", intersection_list)

    missing_list = difference_events_lists(goto_events, intersection_list)
    print_event_list_details("Events chosen & not found", missing_list)

    completed_list = []
    while len(intersection_list) > 0 or len(missing_list) > 0:
        for event in intersection_list:
            rsvp_completed = event_rsvp(driver, event)  # TODO: Deal with status of event that's filled
            if rsvp_completed:
                completed_list.append(event)
        intersection_list = difference_events_lists(intersection_list, completed_list)
        print_event_list_details("Events chosen & found & to RSVP", intersection_list)
        time.sleep(PAGE_WAIT_TIME)

    stop = timeit.default_timer()

    print("Program run time: " + "{0:.1f}".format(stop - start) + "s")

    time.sleep(MIN)

    return True


if __name__ == '__main__':
    main()
    driver.close()
