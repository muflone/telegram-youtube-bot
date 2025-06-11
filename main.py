#!/usr/bin/env python
##
#     Project: Telegram YouTube Bot
# Description: Telegram bot to process YouTube links
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2025 Fabio Castelli
#     License: GPL-3+
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
##

import logging
import os
import re
import xml.etree.ElementTree

import telegram
import telegram.ext

import youtube_transcript_api

VERSION = '0.1.0'


class Bot:
    def __init__(self):
        self.application = None
        self.telegram_token = os.environ.get('TELEGRAM_TOKEN')
        self.youtube_languages = os.environ.get('YOUTUBE_LANGUAGES', 'en')
        self.youtube_cookies_file = os.environ.get('YOUTUBE_COOKIES')

    def run(self) -> None:
        """
        Run the bot.
        """
        self.application = telegram.ext.Application.builder().token(
            token=self.telegram_token).build()
        # Commands handlers
        self.application.add_handler(handler=telegram.ext.CommandHandler(
            command='start',
            callback=self.command_start))
        self.application.add_handler(handler=telegram.ext.CommandHandler(
            command='help',
            callback=self.command_help))
        self.application.add_handler(handler=telegram.ext.CommandHandler(
            command='version',
            callback=self.command_version))
        self.application.add_handler(handler=telegram.ext.CommandHandler(
            command='ytt',
            callback=self.command_youtube_transcript))
        # Run the bot
        self.application.run_polling(
            allowed_updates=telegram.Update.ALL_TYPES)

    async def command_start(
            self,
            update: telegram.Update,
            context: telegram.ext.ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Send a message when the command /start is issued.
        """
        await update.message.reply_text('Hi, use /help!')

    async def command_help(
            self,
            update: telegram.Update,
            context: telegram.ext.ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Send a message when the command /help is issued.
        """
        await update.message.reply_text("""
        Commands:
        /ytt
        Get the audio transcript from the YouTube video
        (replying to a message containing a YouTube link)
        
        /version
        Get the bot version
        """)

    async def command_version(
            self,
            update: telegram.Update,
            context: telegram.ext.ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Send a message when the command /version is issued.
        """
        await update.message.reply_text(VERSION)

    async def command_youtube_transcript(
            self,
            update: telegram.Update,
            context: telegram.ext.ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Extract transcript from YouTube link
        """
        result = 'No valid YouTube link found'
        if update.message.reply_to_message:
            replied_message = update.message.reply_to_message.text.strip()
            # Find YouTube link
            youtube_pattern = (r'(https?://)?(www\.)?'
                               r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
                               r'(watch\?v=|embed/|v/|.+\?v=|shorts\/)?'
                               r'([^&=%\?]{11})')
            if matches := re.search(pattern=youtube_pattern,
                                    string=replied_message):
                yt_link = matches[0]
                logging.info(f'YouTube link: {yt_link}')
                if yt_video_id := yt_link.rsplit('/')[-1].rsplit('=')[-1]:
                    logging.info(f'YouTube video ID: {yt_video_id}')
                    transcript = youtube_transcript_api.YouTubeTranscriptApi(
                        cookie_path=self.youtube_cookies_file)
                    try:
                        transcripts = transcript.fetch(
                            video_id=yt_video_id,
                            languages=self.youtube_languages.split(','))
                        result = ' '.join(snippet.text
                                          .replace('\xa0', ' ')
                                          .replace('\n', ' ')
                                          for snippet
                                          in transcripts).replace('  ', ' ')
                    except xml.etree.ElementTree.ParseError as error:
                        logging.error(error)
                        result = 'Unable to parse transcripts'
                    if len(result) > 4000:
                        result = f'{result[:4000]}...\n\n[Message truncated]'
        await update.message.reply_text(result)


if __name__ == '__main__':
    # Enable logging
    logging.basicConfig(
        format='%(asctime)s - %(levelname)-7s - %(name)s - %(message)s',
        level=logging.INFO)
    # Set higher logging level for httpx to avoid all GET and POST requests
    # being logged
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logger = logging.getLogger(__name__)
    # Start the bot
    bot = Bot()
    bot.run()
