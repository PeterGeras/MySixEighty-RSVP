class Event(object):
    def __init__(self, event_div):
        self.title = event_div.text.partition('\n')[0].strip()
        self.url = event_div.find_element_by_tag_name('a').get_attribute('href')

    def get_event(self):
        print("\n" + self.title + "\n" + self.url + "\n-------")
