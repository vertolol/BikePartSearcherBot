import requests
from settings import URL, proxies


class Message:
    def __init__(self, text='', chat_id=None, mes_id=None):
        self.text = text
        self.chat_id = chat_id
        self.mes_id = mes_id


class IncomingData:
    def __init__(self, data):
        self.data = data

    def get_message_object(self):
        if self.data.get('callback_query'):
            return KeyboardMessage(self.data)
        else:
            return TextMessage(self.data)


class TextMessage(Message):
    def __init__(self, data, *args, **kwargs):
        super().__init__(data, *args, **kwargs)
        self.data = data

        self.text = self.data['message']['text']
        self.chat_id = self.data['message']['chat']['id']
        self.mes_id = self.data['message']['message_id']

        self.is_keyboard = False


class KeyboardMessage(Message):
    def __init__(self, data, *args, **kwargs):
        super().__init__(data, *args, **kwargs)
        self.data = data['callback_query']

        self.text = self.data['data']
        self.chat_id = self.data['message']['chat']['id']
        self.mes_id = self.data['message']['message_id']

        self.is_keyboard = True
        self.keyboard = self.data['message']['reply_markup']


class ForSendMessage(Message):
    def __init__(self, keyboard=None, parse_mode='HTML', method='sendMessage', *args, **kwargs):
        super(ForSendMessage, self).__init__(*args, **kwargs)
        self.keyboard = keyboard
        self.parse_mode = parse_mode
        self.method = method
        self.url = URL + self.method

    @property
    def answer(self):
        a = {'text': self.text,
             'chat_id': self.chat_id,
             'message_id': self.mes_id,
             'parse_mode': self.parse_mode,
             'disable_web_page_preview': 'true'
             }
        if self.keyboard is not None:
            a.update({'reply_markup' : self.keyboard})
        return a

    def send_message(self):
        requests.post(self.url, json=self.answer, proxies=proxies)


class Keyboard():
    def __init__(self, buttons):
        self.buttons = buttons

    def keyboard(self, columns=1, type_keyboard='inline_keyboard'):
        self._buttons_list = []

        for index in range(0, len(self.buttons), columns):
            row = self.buttons[index:index+columns]
            self._buttons_list.append(row)

        self.keyboard = { type_keyboard : self._buttons_list }

        return self.keyboard


class Button():
    def __init__(self, text, callback_data, url=None):
        self.text = text
        self.callback_data = callback_data
        self.url = url
        self.button = {'text': self.text, 'callback_data': self.callback_data}
        if url:
            self.button.update({'url':self.url})
