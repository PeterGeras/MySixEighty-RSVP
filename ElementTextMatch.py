from selenium.webdriver.support.expected_conditions import _find_element


# Returns first line of text in an element
class ElementTextMatch(object):
    def __init__(self, locator, header_string):
        self.locator = locator
        self.headerStringStripped = header_string.strip()

    def __call__(self, driver):
        element_text = _find_element(driver, self.locator).text
        header = element_text.split("\n")[0].strip()
        return self.headerStringStripped == header
