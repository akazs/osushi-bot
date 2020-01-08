#!/usr/bin/env python3
import telegram
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

import config
from query import accept_query
from finance import foreign_exchange, retrieve_stock


def start(update, context):
    context.bot.send_message(chat_id=update.message.chat.id,
                             text='Hello, this is Osushi')


def introduce(update, context):
    context.bot.send_message(chat_id=update.message.chat.id,
                             text='*みなさん みくを*',
                             parse_mode=telegram.ParseMode.MARKDOWN)
    context.bot.send_message(chat_id=update.message.chat.id,
                             text='*お寿司かない！*',
                             parse_mode=telegram.ParseMode.MARKDOWN)


def unknown(update, context):
    context.bot.send_message(chat_id=update.message.chat.id,
                             text='Unknown command.')


def main():
    updater = Updater(token=config.bot.token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('miku', introduce))
    dispatcher.add_handler(CommandHandler('fx', foreign_exchange))
    dispatcher.add_handler(CommandHandler('stock', retrieve_stock))
    dispatcher.add_handler(MessageHandler(Filters.text, accept_query))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    updater.start_polling()


if __name__ == '__main__':
    main()
