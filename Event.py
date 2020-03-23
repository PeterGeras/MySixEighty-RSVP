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
        return cls(week, title, "")

    def get_event(self):
        print(self.title)

        if self.week == 1:
            print("This week")
        elif self.week == 2:
            print("Next week")

        if self.url:
            print(self.url)

        return


def print_event_list_details(header, this_list):
    header_outline = (len(header) + 2)*"="
    separator = 7*"-"

    print("\n" + header_outline + "\n " + header + "\n" + header_outline)

    if len(this_list) > 0:
        for i in this_list:
            i.get_event()
            print(separator)
    else:
        print(f"<empty>\n{separator}")

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
    intersected_list = set(list_a).intersection(list_b)

    # Select object with URL in intersected list
    for e in intersected_list:
        if len(e.url) > 0:
            continue
        list_a_url = list_a[list_a.index(e)].url
        list_b_url = list_b[list_b.index(e)].url
        e.url = max(list_a_url, list_b_url)  # Max of strings alphabetically. Empty string is minimum.

    sorted_list = sorted(intersected_list, key=sort_key)

    return sorted_list


def difference_events_lists(list_a, list_b):
    this_list = set(list_a).difference(list_b)
    sorted_list = sorted(this_list, key=sort_key)
    return sorted_list
