from telegram_objects.telegram_objects import (SendMessageText, SendMessageReplyMarkup,
                                               EditMessageText, SendChatAction,  ReplyMarkup, Button)
from stores import stores_for_select, selected, not_selected
from spiders import starting_spiders
import category_tree


session = {}


def add_to_session(chat_id):
    session[chat_id] = {'stores': [],
                        'category': None,
                        'handler': None, }


def add_stores_to_search_in_session(message):
    stores = []
    for row in message.keyboard['inline_keyboard']:
        for button in row:
            if selected in button['text']:
                stores.append(button['text'].replace(selected, ''))
    session[message.chat_id]['stores'] = stores


def bot_help(message):
    text = 'for start search press /start'
    return SendMessageText(chat_id=message.chat_id, text=text)


def bot_start(message):
    add_to_session(message.chat_id)
    return stores_selection(message)


def stores_selection(message):
    text = 'select store:'
    if session[message.chat_id]['handler'] != 'stores_selection':
        session[message.chat_id]['handler'] = 'stores_selection'
        keyboard = get_keyboard_from_dictionary(stores_for_select)
        return SendMessageReplyMarkup(chat_id=message.chat_id, text=text, reply_markup=keyboard.keyboard())

    elif message.text != 'done':
        keyboard = get_keyboard_of_selection(message)
        return EditMessageText(chat_id=message.chat_id, mes_id=message.mes_id, text=text,
                               reply_markup=keyboard.keyboard())

    else:
        add_stores_to_search_in_session(message)
        return category_selection(message)


def category_selection(message):
    text = 'select category:'
    if session[message.chat_id]['handler'] != 'category_selection':
        session[message.chat_id]['handler'] = 'category_selection'
        category_for_select = category_tree.category_for_select

    elif message.text in category_tree.all_categories:
        category_for_select = category_tree.all_categories[message.text]

    else:
        session[message.chat_id]['category'] = message.text
        return get_result(message)

    keyboard = get_keyboard_from_dictionary(category_for_select)
    return EditMessageText(chat_id=message.chat_id, mes_id=message.mes_id, text=text,
                           reply_markup=keyboard.keyboard())


def get_result(message):
    if session[message.chat_id]['handler'] != 'get_result':
        session[message.chat_id]['handler'] = 'get_result'
        text = 'enter item name:'

    else:
        SendChatAction(chat_id=message.chat_id, ).send_message()

        stores = session[message.chat_id]['stores']
        category = session[message.chat_id]['category']
        item_name = message.text
        results = starting_spiders.get_result_as_text(stores, category, item_name)

        text = f'results <b>{item_name}</b>:\n {results}'
        session.pop(message.chat_id)

    return EditMessageText(chat_id=message.chat_id, mes_id=message.mes_id, text=text)


def selection_error(message):
    session.pop(message.chat_id)
    text = 'error /start'
    return SendMessageText(chat_id=message.chat_id, text=text)


def get_keyboard_from_dictionary(dictionary):
    buttons = [Button(key, value).button for key, value in dictionary.items()]
    return ReplyMarkup(buttons)


def get_keyboard_of_selection(message):
    buttons = []
    for row in message.keyboard['inline_keyboard']:
        for button in row:
            if message.text in button['text']:
                if selected in button['text']:
                    button['text'] = button['text'].replace(selected, not_selected)
                else:
                    button['text'] = button['text'].replace(not_selected, selected)
            buttons.append(button)

    return ReplyMarkup(buttons)


def get_stores_to_search(keyboard):
    stores = []
    for row in keyboard['inline_keyboard']:
        for button in row:
            if selected in button['text']:
                stores.append(button['text'].replace(selected, ''))
    return stores


handlers_dict = {
    '/help': bot_help,
    '/start': bot_start,
    'stores_selection': stores_selection,
    'category_selection': category_selection,
    'get_result': get_result,
    'selection_error': selection_error
}
