import time
import validators

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

from ElementTextMatch import ElementTextMatch

# Time
SEC = 1
ELEMENT_WAIT_TIME = 3 * SEC
PAGE_WAIT_TIME = 10 * SEC

global driver, event


def open_window():
    driver.execute_script("window.open('');")  # Open tab
    driver.switch_to.window(driver.window_handles[-1])

    valid_url = validators.url(str(event.url))

    if valid_url:
        driver.get(event.url)  # Load page

    return valid_url


def close_window():
    driver.execute_script("window.close('');")  # Close tab
    driver.switch_to.window(driver.window_handles[0])

    return


def find_rsvp():
    rsvp = False
    rsvp_text = False

    try:
        # This container should always appear
        WebDriverWait(driver, PAGE_WAIT_TIME).until(
            EC.presence_of_element_located((By.CLASS_NAME, "field-name-rsvp-button"))
        )
        WebDriverWait(driver, ELEMENT_WAIT_TIME).until_not(
            ElementTextMatch((By.CLASS_NAME, "rsvp-button"), "Loading...")
        )
        rsvp = driver.find_element(By.CLASS_NAME, "rsvp-button")
    except TimeoutException:
        print("# Failed to find RSVP container")
    except NoSuchElementException:
        print("# RSVP button not available")

    return rsvp


def click_rsvp(rsvp):
    rsvp_first_text = rsvp.text.split('\n')[0]
    already_going_text = "You're going"
    rsvp_completed = False

    if rsvp_first_text == "RSVP":
        try:
            # Click RSVP url
            rsvp.find_element_by_tag_name('a').click()

            # Click Agree dialog
            WebDriverWait(driver, ELEMENT_WAIT_TIME)\
                .until(EC.presence_of_element_located((By.CLASS_NAME, "confirm-button")))\
                .click()

            # Wait for response to confirm we've RSVPed
            WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
                ElementTextMatch((By.CLASS_NAME, "rsvp-button"), already_going_text)
            )

            print(f"# RSVPed to - {event.title} - {event.url}")
            rsvp_completed = True
        except Exception as ex:
            print(f"# Failed to RSVP to - {event.title} - {event.url}")
    elif rsvp_first_text == already_going_text:
        print(f"# Already going to - {event.title} - {event.url}")
        rsvp_completed = True

    return rsvp_completed


def event_rsvp(this_driver, this_event):
    global driver, event
    driver = this_driver
    event = this_event
    rsvp_completed = False

    if open_window():
        rsvp_button = find_rsvp()
        if rsvp_button:
            rsvp_completed = click_rsvp(rsvp_button)

    close_window()

    return rsvp_completed
