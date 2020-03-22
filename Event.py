import validators


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
        return


def print_event_list_details(header, this_list):
    header_outline = (len(header) + 2)*"="

    print("\n" + header_outline + "\n " + header + "\n" + header_outline)

    if len(this_list) > 0:
        for i in this_list:
            i.get_event()
            print("------")
    else:
        print("<empty>")
        print("------")

    return


def sort_key(event):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    event_day = event.title.split(' ')[0].capitalize()

    try:
        day_index = days.index(event_day)
    except ValueError:
        day_index = len(days)

    return str(event.week) + str(day_index) + event.title.lower()


# The intersection of sets might return an object with no URL
def update_intersected_url(input_list, list_a, list_b):
    for e in input_list:
        if len(e.url) > 0:
            break
        list_a_url = list_a[list_a.index(e)].url
        list_b_url = list_b[list_b.index(e)].url
        if validators.url(str(e.url)) is False\
            or validators.url(str(list_a_url)) is False\
            or validators.url(str(list_b_url)) is False:
            pass
        e.url = max(len(list_a_url), len(list_b_url))
    return


def intersection_events_lists(list_a, list_b):
    this_list = set(list_a).intersection(list_b)
    sorted_list = sorted(this_list, key=sort_key)
    update_intersected_url(sorted_list, list_a, list_b)
    return sorted_list


def difference_events_lists(list_a, list_b):
    this_list = set(list_a).difference(list_b)
    sorted_list = sorted(this_list, key=sort_key)
    return sorted_list
