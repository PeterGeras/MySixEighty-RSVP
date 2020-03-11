class Event(object):
    def __init__(self, week, event_div):
        self.week = week
        self.title = event_div.text.partition('\n')[0].strip()
        self.url = event_div.find_element_by_tag_name('a').get_attribute('href')

    def get_event(self):
        print("\nWeek: " + str(self.week) + "\n" + self.title + "\n" + self.url + "\n-------")
