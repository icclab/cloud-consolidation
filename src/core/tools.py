def search_dictionaries(key, value, lod):
    return [element for element in lod if element[key] == value]


def sort_dictionaries(sort_key, lod):
    return sorted(lod, key=lambda k: k[sort_key])
