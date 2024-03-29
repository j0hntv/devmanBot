import logging
import os
import requests
import telegram
import time
from dotenv import load_dotenv


TIMEOUT = 5
logger = logging.getLogger()


class Handler(logging.Handler):

    def __init__(self, bot, chat_id):
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


def start_bot(bot, chat_id, devman_token):
    logger.info('Проверка связи.')

    timestamp = time.time()

    long_polling_url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': f'Token {devman_token}'}

    while True:
        try:
            payload = {'timestamp': timestamp}
            response = requests.get(long_polling_url, headers=headers, params=payload)
            response.raise_for_status()
            response = response.json()

            status = response.get('status')

            if status == 'found':
                new_attempts = response['new_attempts'][0]
                lesson = new_attempts['lesson_title']
                is_negative = new_attempts['is_negative']
                timestamp = response['last_attempt_timestamp']

                message_list = [f'Преподаватель проверил работу *"{lesson}".*']

                if is_negative:
                    message_list.append('К сожалению, в работе есть ошибки. 🙈')
                else:
                    message_list.append('Работа принята 🚀')

                message = '\n'.join(message_list)
                bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')
            
            elif status == 'timeout':
                timestamp = response['timestamp_to_request']

            else:
                logger.warning(response)

        except requests.exceptions.ReadTimeout:
            pass

        except (requests.ConnectionError, requests.exceptions.HTTPError) as error:
            logging.exception(error, exc_info=False)
            time.sleep(TIMEOUT)


def main():
    logger.setLevel(logging.INFO)
    handler = Handler(bot, chat_id)
    formatter = logging.Formatter('[%(levelname)s]  %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    load_dotenv()
    devman_token = os.getenv('DEVMAN_TOKEN')
    tg_token = os.getenv('TG_TOKEN')
    chat_id = os.getenv('CHAT_ID')

    bot = telegram.Bot(token=tg_token)
    start_bot(bot, chat_id, devman_token)


if __name__ == '__main__':
    main()
