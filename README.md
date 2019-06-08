# TeleFeedBack
## Simple Telegram bot for feeedback

First you most install `pyTelegramBotAPI` library. Command:
```bash
pip install pyTelegramBotAPI
```

Next edit `settings.json` file. Set your bot API_TOKEN and bot owned's Telegram ID. Result should like a:
```json
{
    "API_TOKEN": "123456789:Your1234api12345token122345",
    "ADMIN_ID": 12121212,
    "HELLO_ADMIN": "Hello, Admin!",
    "HELLO_CHAT": "Welcome to feedback bot",
    "NO_REPLY_MESSAGE": "‼️‼️ You should reply a message ‼️‼️"
}
```
If you need to edit the messages, no problem!
Next start the bot with command:
```bash
python main.py
```
