# Music bro

Music bro is a Telegram bot that suggests Belarusian music based on listener's taste and mood.

## Technologies used
- Python
- SQL
- Telegram Bot API

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required dependencies:

```bash
pip install -r requirements.txt
```

or

```bash
pip install python-telegram-bot
pip install psycopg2
pip install requests
pip install ytmusicapi
```

## Usage

1) You may create a Telegram bot and acquire a unique key by using [this](https://telegram.me/BotFather) bot.

2) Create a config.py file with following keys in the main directory:

    ```
    API_KEY = ""
    RDS_ENDPOINT = ""
    RDS_PORT =
    RDS_USERNAME = ""
    RDS_PASSWORD = ""
    RDS_DB_NAME =
    ```
3) Create a database with the music.
   - You may use our database from `db.csv` file by running `python create_db.py`
   - You can also create your own database.


4) Start the bot.

```bash
python main.py
```


## License
[MIT](https://choosealicense.com/licenses/mit/)