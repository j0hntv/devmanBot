import logging
import os
import requests
import telegram
import time

TIMEOUT = 5

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', filename='bot.log')

token_devman = os.environ['token_devman']
token_bot = os.environ['token_bot']
chat_id = os.environ['chat_id']

class Handler(logging.Handler):

    def __init__(self, bot, chat_id):
        self.bot = bot
        self.chat_id = chat_id

    def emit(record):
        log_entry = self.format(record)
        bot.send_message(chat_id=chat_id, text=log_entry)
        

def start_bot(bot, chat_id, token_devman):
    timestamp = time.time()

    long_polling_url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': f'Token {token_devman}'}

    while True:
        try:
            payload = {'timestamp': timestamp}
            response = requests.get(long_polling_url, headers=headers, params=payload)
            response.raise_for_status()
            response = response.json()

            status = response.get('status', None)

            if status == 'found':
                new_attempts = response['new_attempts'][0]
                lesson = new_attempts['lesson_title']
                is_negative = new_attempts['is_negative']
                timestamp = response['last_attempt_timestamp']

                message_list = [f'Преподаватель проверил работу *"{lesson}".*']

                if is_negative:
                    message_list.append('К сожалению, в работе есть ошибки. 🧐')
                else:
                    message_list.append('Работа принята 🚀')

                message = '\n'.join(message_list)
                bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')
            
            elif status == 'timeout':
                timestamp = response['timestamp_to_request']

            else:
                logging.warning(response)

        except requests.exceptions.ReadTimeout:
            pass

        except requests.ConnectionError as error:
            logging.error(repr(error))
            time.sleep(TIMEOUT)

        except requests.exceptions.HTTPError as error:
            logging.error(repr(error))
            time.sleep(TIMEOUT)


def main():
    bot = telegram.Bot(token=token_bot)
    start_bot(bot, chat_id, token_devman)


if __name__ == '__main__':
    main()
