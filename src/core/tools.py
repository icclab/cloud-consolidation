def search_dictionaries(key, value, list_of_dictionaries):
    return [element for element in list_of_dictionaries if element[key] == value]


def sort_dictionaries(sort_key, list_of_dictionaries):
    return sorted(list_of_dictionaries, key=lambda k: k[sort_key])
