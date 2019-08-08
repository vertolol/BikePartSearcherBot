stores = {
    'bike24': 'bike24',
    'bike_components': 'bike_components',
    'hibike': 'hibike',
}

selected = '🔳 '
not_selected = '⬜️️ '
stores_for_select = dict(zip([selected + store for store in stores.keys()], stores.values()))
