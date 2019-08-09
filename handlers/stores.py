stores = {
    'bike24',
    'hibike',
    'bike_components',
}

selected = '🔳 '
not_selected = '⬜️️ '
stores_for_select = dict(zip([selected + store for store in stores], stores))
stores_for_select.update({'done': 'done'})
