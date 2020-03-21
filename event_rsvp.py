import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

# Time
SEC = 1
ELEMENT_WAIT_TIME = 3 * SEC
PAGE_WAIT_TIME = 10 * SEC

global driver, event


def open_window():
    # Open tab
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])

    # Load page
    driver.get(event.url)

    return


def close_window():
    # Close tab
    driver.execute_script("window.close('');")
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

        rsvp = driver.find_element(By.CLASS_NAME, "rsvp-button")

        # TODO: I don't think this is working correctly. rsvp-confirm class is not always available
        WebDriverWait(driver, ELEMENT_WAIT_TIME).until_not(
            EC.text_to_be_present_in_element((By.CLASS_NAME, "rsvp-confirm"), "Loading...")
        )

        rsvp_text = rsvp.text.split("\n")[0]

    except TimeoutException:
        print("# Failed to find RSVP container")
    except NoSuchElementException:
        print("# RSVP button not available")

    print("rsvp_text = " + str(rsvp_text))

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

    open_window()

    rsvp_button = find_rsvp()
    if rsvp_button:
        rsvp_completed = click_rsvp(rsvp_button)
        time.sleep(ELEMENT_WAIT_TIME)

    close_window()

    return rsvp_completed
