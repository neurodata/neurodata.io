from jinja2.ext import Extension


def sort_by_index(self, position_list):
    return sorted(self, key=lambda x: position_list.index(x[0]))


class SortByIndex(Extension):

    def __init__(self, environment):
        super(SortByIndex, self).__init__(environment)
        environment.filters['sort_by_index'] = sort_by_index