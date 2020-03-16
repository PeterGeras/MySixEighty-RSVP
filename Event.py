class Event(object):
    def __init__(self, week, title, url):
        self.week = week
        self.title = title.strip()
        self.url = url.strip()

    # Define Event(object) by these methods
    # cls parameter refers to class within this class, such as self
    # https://stackoverflow.com/questions/2164258/multiple-constructors-in-python
    @classmethod
    def set_from_div(cls, week, event_div):
        title = event_div.text.partition('\n')[0]
        url = event_div.find_element_by_tag_name('a').get_attribute('href')
        return cls(week, title, url)

    @classmethod
    def set_from_excel(cls, week, title):
        # We do not have a URL for the events from the excel file
        return cls(week, title, '')

    # Called with event_1 == event_2
    def __eq__(self, other):
        return self.week == other.week and self.title == other.title

    def get_event(self):
        print_url = self.url
        if not print_url:
            print_url = '<empty>'
        print("Week: " + str(self.week) + "\n" + self.title + "\n" + print_url + "\n-------")

