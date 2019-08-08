from telegram_objects.telegram_objects import ForSendMessage, Keyboard, Button
from .stores import stores_for_select, selected, not_selected
from .category_tree import *
from spiders.all import get_result_as_text


session = {}


def bot_help(message):
    text = 'for start search press /start'
    for_send = ForSendMessage(chat_id=message.chat_id, text=text)

    return for_send


def bot_start(message):
    add_to_session(message.chat_id)

    text = 'select store:'
    keyboard = get_keyboard_from_dictionary(stores_for_select, done=True)
    session[message.chat_id]['handler'] = 'stores_selection'

    for_send = ForSendMessage(chat_id=message.chat_id, text=text, keyboard=keyboard.keyboard(columns=2))

    return for_send


def selection_error(message):
    session.pop(message.chat_id)
    text = 'error /start'
    for_send = ForSendMessage(chat_id=message.chat_id, text=text)

    return for_send


def stores_selection(message):
    if message.text == 'done':
        text = 'select category: '
        keyboard = get_keyboard_from_dictionary(bike_type)
        session[message.chat_id]['stores'] = get_stores_to_search(message)
        session[message.chat_id]['handler'] = 'category_selection'

    else:
        text = 'select store: '
        keyboard = get_keyboard_of_selection(message)

    for_send = ForSendMessage(chat_id=message.chat_id, text=text, method='editMessageText',
                              mes_id=message.mes_id, keyboard=keyboard.keyboard(columns=2))

    return for_send


def category_selection(message):
    try:
        d = eval(message.text)
    except NameError:
        session[message.chat_id]['breadcrumbs'] += message.text
        session[message.chat_id]['category'] = message.text
        session[message.chat_id]['handler'] = 'get_result'
        text = session[message.chat_id]['breadcrumbs'].replace('_', ' ') + '\nВедите название:'
        for_send = ForSendMessage(chat_id=message.chat_id, text=text, method='editMessageText', mes_id=message.mes_id)

        return for_send

    session[message.chat_id]['breadcrumbs'] += f'{message.text} / '
    text = session[message.chat_id]['breadcrumbs'].replace('_', ' ')
    keyboard = get_keyboard_from_dictionary(d)
    for_send = ForSendMessage(chat_id=message.chat_id, text=text, keyboard=keyboard.keyboard(columns=2),
                              method='editMessageText', mes_id=message.mes_id)

    return for_send


def get_result(message):
    stores = session[message.chat_id]['stores']
    category = session[message.chat_id]['category']
    item_name = message.text
    scraping = get_result_as_text(stores, category, item_name)

    text = f'Результаты поиска <b>{message.text}</b>:\n {scraping}'
    session.pop(message.chat_id)

    for_send = ForSendMessage(chat_id=message.chat_id, text=text,)

    return for_send


def add_to_session(chat_id):
    session[chat_id] = {
        'breadcrumbs': '',
        'stores': [],
        'category': None,
        'handler': 'start',
    }


def get_keyboard_from_dictionary(dictionary, done=False):
    buttons = [Button(key, value).button for key, value in dictionary.items()]
    if done:
        done_button = [Button(text='done', callback_data='done').button]
        buttons.extend(done_button)
    return Keyboard(buttons)


def get_keyboard_of_selection(message):
    buttons = []

    for row in message.keyboard['inline_keyboard']:
        for button in row:
            if message.text in button['text']:
                print(message.text)
                if selected in button['text']:
                    button['text'] = button['text'].replace(selected, not_selected)
                else:
                    button['text'] = button['text'].replace(not_selected, selected)
            buttons.append(button)

    return Keyboard(buttons)


def get_stores_to_search(message):
    stores = []

    for row in message.keyboard['inline_keyboard']:
        for button in row:
            if selected in button['text']:
                stores.append(button['text'].replace(selected, ''))
    return stores
