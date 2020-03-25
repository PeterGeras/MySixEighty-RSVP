import os
import timeit
import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
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
LOOP_TIME = 1 * MIN
LOGIN_TIME = 2 * MIN

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
        except Exception as ex:
            print("# Logging in automatically failed")
            return False
    else:
        # Enter login details manually
        print("# Please log in manually...")
        try:
            WebDriverWait(driver, LOGIN_TIME).until(
                EC.presence_of_element_located((By.ID, account_logged_id))
            )
        except Exception as ex:
            print("# Login took too long")
            return False

    # Check login happened and redirected to main page
    try:
        WebDriverWait(driver, PAGE_WAIT_TIME).until(
            EC.presence_of_element_located((By.ID, account_logged_id))
        )
    except Exception as ex:
        print(f"# Login redirection to main page failed? div_id {account_logged_id} not found")
        return False

    return True


def events_load():
    driver.get(config.EVENTS_URL)

    event_week_class = "event-week"

    try:
        WebDriverWait(driver, PAGE_WAIT_TIME).until(
            EC.presence_of_element_located((By.CLASS_NAME, event_week_class))
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
    except Exception as ex:
        print("# div should have been found earlier in events_load()")
        return False

    try:
        events_week = events_form.find_elements_by_xpath(".//div[@class='event-week']")
    except Exception as ex:
        print("# Page code structure changed, aborting")
        return False

    if len(events_week) != 2:
        print("# Number of weeks found is not 2, continuing...")

    # This week, next week etc.
    # Enumeration - https://www.geeksforgeeks.org/enumerate-in-python/
    for week, event_week in enumerate(events_week, config.THIS_WEEK):
        try:
            event_cards = event_week.find_elements_by_xpath(".//div[@class='event-card']")
        except Exception as ex:
            print("# Page code structure changed, aborting")
            return False
        for e in event_cards:
            events.append(Event.set_from_div(week, e))

    return events


def event_looping():
    completed_list = []
    events_file = os.path.basename(config.EVENTS)
    header_title = "### ATTEMPTING TO ACCESS EVENTS ###"
    header_outline = len(header_title)*"#"

    goto_events = config.get_events_selected()
    print_event_list_details(f"Events chosen from {events_file}", goto_events)

    if len(goto_events) == 0:
        print(f"# No selected events found from {events_file}")
        return False

    if config.load_cookies() is False:
        if login_load():
            config.save_cookies()
        else:
            return False

    # Looping to continue processing events until all processed
    while True:
        if events_load() is False:
            return False

        all_events = events_find()
        print_event_list_details(f"Events found on {config.EVENTS_URL}", all_events)

        intersection_list = intersection_events_lists(all_events, goto_events)
        intersection_list = difference_events_lists(intersection_list, completed_list)
        print_event_list_details("Events chosen & Events found", intersection_list)

        missing_list = difference_events_lists(goto_events, intersection_list)
        print_event_list_details("Events chosen & Events not found", missing_list)

        for event in intersection_list:
            print(f"\n{header_outline}\n{header_title}\n{header_outline}")
            rsvp_completed = event_rsvp(driver, event)  # TODO: Deal with status of event that's filled
            if rsvp_completed:
                completed_list.append(event)

        intersection_list = difference_events_lists(intersection_list, completed_list)
        print_event_list_details("Events completed", completed_list)

        # Break condition
        if len(intersection_list) == 0 and len(missing_list) == 0:
            break

        time.sleep(LOOP_TIME)

    return True


def main():
    start = timeit.default_timer()

    event_looping()
    driver.close()

    stop = timeit.default_timer()
    print("Program run time: " + "{0:.1f}".format(stop - start) + "s")
    time.sleep(MIN)

    return True


if __name__ == '__main__':
    main()
