from flask import Flask, request
from handlers.handlers import *
from telegram_objects.telegram_objects import IncomingData

app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    incoming = request.get_json()
    message = IncomingData(incoming).get_message_object()
    handler = get_handler(message)
    for_send = handler(message)
    for_send.send_message()

    return 'Ok'


handlers = {
    '/help': bot_help,
    '/start': bot_start,
    'stores_selection': stores_selection,
    'category_selection': category_selection,
    'get_result': get_result,
    'selection_error': selection_error
}


def get_handler(message):
    if message.chat_id in session:

        if message.is_keyboard:
            handler = handlers[session[message.chat_id]['handler']]
        elif session[message.chat_id]['handler'] == 'get_result':
            handler = handlers['get_result']
        else:
            handler = handlers['selection_error']

    elif message.text == '/start':
        handler = handlers['/start']
    else:
        handler = handlers['/help']

    return handler


if __name__ == '__main__':
    app.run()
