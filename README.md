# TeleFeedBack

## Simple Telegram bot for feedback

### Setting up

After the repository cloning you must install the project libraries. Command:

```bash
pip install -r requirements.txt
```

You must edit the `settings.json` file.

```json
{
    "DB_ACCESS": "sqlite:///datatable.db",
    "DELETE_DELAY": 1209600,
    "API_TOKEN": "<-TELEGRAM-API-TOKEN->",
    "ADMIN_ID": 1122334455,
    "HELLO_ADMIN": "Hello, Admin!",
    "HELLO_CHAT": "Welcome to feedback bot",
    "NO_REPLY_MESSAGE": ":bangbang::bangbang: You should reply a message :bangbang::bangbang:",
    "UNSUPPORTED_TYPE": ":bangbang::bangbang: Bot does not support this type of message :bangbang::bangbang:",
    "USER_IS_BANNED": ":bangbang::bangbang: User is banned :bangbang::bangbang:",
    "YOU_ARE_BANNED": ":bangbang::bangbang: You are banned :bangbang::bangbang:"
}
```

- `DB_ACCESS`: it's a connection string for SQLAlchemy. Sqlite by default.  
- `DELETE_DELAY`: it's a delay in deleting message information from database. 2 weeks by default.  
- `API_TOKEN`: it's a telegram bot token. You must get it from `@BotFather`.  
- `ADMIN_ID`: it's a bot owner's chat id.  
- Then the messages that the bot sends. You can use `emoji` library here as in the example.

### Running

To run the bot you must command:

```bash
python3 main.py
```
