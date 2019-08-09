import requests
from settings import URL, proxies
from abc import ABC


class IncomingMessage:
    def __init__(self, data):
        self.data = data

    def get_message_object(self):
        if self.data.get('callback_query'):
            return IncomingReplyMarkup(self.data)
        else:
            return IncomingText(self.data)


class IncomingText:
    def __init__(self, data):
        self.data = data
        self.chat_id = self.data['message']['chat']['id']
        self.mes_id = self.data['message']['message_id']
        self.text = self.data['message']['text']
        self.is_keyboard = False


class IncomingReplyMarkup:
    def __init__(self, data):
        self.data = data['callback_query']
        self.chat_id = self.data['message']['chat']['id']
        self.mes_id = self.data['message']['message_id']
        self.text = self.data['data']
        self.is_keyboard = True
        self.keyboard = self.data['message']['reply_markup']


class ForSendMessage(ABC):
    method = 'sendMessage'

    def __init__(self, chat_id=None, mes_id=None, text=None, parse_mode='HTML', *args, **kwargs):
        self.chat_id = chat_id
        self.mes_id = mes_id
        self.text = text
        self.parse_mode = parse_mode
        self.answer = {'chat_id': self.chat_id,
                       'message_id': self.mes_id,
                       'text': self.text,
                       'parse_mode': self.parse_mode,
                       'disable_web_page_preview': 'true'}

    def send_message(self):
        url = URL + self.method
        requests.post(url, json=self.answer, proxies=proxies)


class SendMessageText(ForSendMessage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SendMessageReplyMarkup(ForSendMessage):
    def __init__(self, reply_markup, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reply_markup = reply_markup
        self.answer.update({'reply_markup': self.reply_markup})


class EditMessageText(ForSendMessage):
    method = 'editMessageText'

    def __init__(self, reply_markup=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reply_markup = reply_markup
        if self.reply_markup:
            self.answer.update({'reply_markup': self.reply_markup})


class SendChatAction(ForSendMessage):
    method = 'sendChatAction'

    def __init__(self, action='typing', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.action = action
        self.answer = {'chat_id': self.chat_id,
                       'action': self.action}


class ReplyMarkup:
    def __init__(self, buttons):
        self.buttons = buttons

    def keyboard(self, columns=2, type_keyboard='inline_keyboard'):
        buttons_list = []
        for index in range(0, len(self.buttons), columns):
            row = self.buttons[index:index + columns]
            buttons_list.append(row)
        return {type_keyboard: buttons_list}


class Button:
    def __init__(self, text, callback_data):
        self.text = text
        self.callback_data = callback_data
        self.button = {'text': self.text, 'callback_data': self.callback_data}
