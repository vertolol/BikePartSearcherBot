from flask import Flask, request
from handlers.handlers import handlers_dict, session
from telegram_objects.telegram_objects import IncomingMessage

app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    incoming = request.get_json()
    message = IncomingMessage(incoming).get_message_object()
    handler = get_handler(message)
    for_send = handler(message)
    for_send.send_message()

    return 'Ok'


def get_handler(message):
    if message.chat_id in session:
        if message.is_keyboard:
            handler = handlers_dict[session[message.chat_id]['handler']]
        elif session[message.chat_id]['handler'] == 'get_result':
            handler = handlers_dict['get_result']
        else:
            handler = handlers_dict['selection_error']
    elif message.text == '/start':
        handler = handlers_dict['/start']
    else:
        handler = handlers_dict['/help']

    return handler


if __name__ == '__main__':
    app.run()
