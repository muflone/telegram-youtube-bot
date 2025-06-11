# Telegram YouTube Bot

**Description:** Telegram bot to process YouTube links

**Copyright:** 2025 Fabio Castelli (Muflone) <muflone@muflone.com>

**License:** GPL-3+

**Source code:** https://github.com/muflone/telegram-youtube-bot/

**Documentation:** http://www.muflone.com/telegram-youtube-bot/

# Description

Process YouTube links

# System Requirements

* Python >= 3.7 (developed and tested for Python 3.14)
* Python Telegram Bot ( https://pypi.org/project/python-telegram-bot/ )
* YouTube Transcript API ( https://pypi.org/project/youtube-transcript-api/ )

# Usage

    cd /path/to/folder
    export TELEGRAM_TOKEN="YOUR:TOKEN"
    export YOUTUBE_LANGUAGES="en,it"
    export YOUTUBE_COOKIES="cookies.txt"
    python3 main.py

The cookies.txt file is optional and can be got from your own browser:

- [Cookie-Editor](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm?hl=en)
  for Google Chrome
- [cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/)
  for Mozilla Firefox
