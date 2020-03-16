class Event(object):
    def __init__(self, week, title, url):
        self.week = week
        self.title = title.strip()
        self.url = url.strip()

    # To help define set intersection which excludes the URL
    def __hash__(self):
        return hash((self.week, self.title))

    # Equality of objects called with event_1 == event_2
    def __eq__(self, other):
        return self.week == other.week and self.title == other.title

    def __ne__(self, other):
        return not self.__eq__(other)

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

    def get_event(self):
        print(self.title)
        print("Week " + str(self.week))
        if self.url:
            print(self.url)
        print("-------")
        return


def print_event_list_details(header, this_list):
    header_outline = (len(header) + 2)*"="

    print("\n" + header_outline + "\n " + header + "\n" + header_outline)

    for i in this_list:
        i.get_event()

    return


def sort_key(event):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    event_day = event.title.split(' ')[0].capitalize()

    try:
        day_index = days.index(event_day)
    except ValueError:
        day_index = len(days)

    return str(event.week) + str(day_index) + event.title.lower()


def intersection_events_lists(list_a, list_b):
    return sorted(set(list_a).intersection(list_b), key=sort_key)


def difference_events_lists(list_a, list_b):
    return sorted(set(list_a).difference(list_b), key=sort_key)
