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
    print("url = " + str(event.url))  # TODO: Figure out where invalid URL is coming from

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
    rsvp_completed = False

    if rsvp_first_text == "RSVP":
        try:
            rsvp.find_element_by_tag_name('a').click()
            WebDriverWait(driver, ELEMENT_WAIT_TIME)\
                .until(EC.presence_of_element_located((By.CLASS_NAME, "confirm-button")))\
                .click()
            print("# RSVPed to: " + event.title)
            rsvp_completed = True
        except:
            print("# Failed to RSVP to: " + event.title)
    elif rsvp_first_text == "You're going":
        print("# Already going to: " + event.title)
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
            time.sleep(ELEMENT_WAIT_TIME)

    close_window()

    return rsvp_completed
