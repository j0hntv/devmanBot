# devmanBot

Telegram bot for sending notifications about verification of works on [dvmn.org](https://dvmn.org/modules).
### How to install

Python3 should be already installed. Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```
* **Run on local machine**

Create .env file with environment variables:
```
token_devman=<TOKEN_DEVMAN>
token_bot=<TOKEN_BOT>
chat_id=<CHAT_ID>
```
* **Deploy on Heroku**

Set `TOKEN_DEVMAN`, `TOKEN_BOT` and `CHAT_ID` on the Config Vars in the Settings tab on the Heroku website.
### Usage
```
python main.py
```
### Project Goals
The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org)



