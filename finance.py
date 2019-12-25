import datetime
from functools import lru_cache

from alpha_vantage.foreignexchange import ForeignExchange
from alpha_vantage.timeseries import TimeSeries

import config
from util import float_format


def retrieve_stock(update, context):
    if len(context.args) < 1:
        context.bot.send_message(chat_id=update.message.chat.id,
                                 text='Usage: /stock <symbol> [YYYY-MM-DD]')
        context.bot.send_message(chat_id=update.message.chat.id,
                                 text='ex: /stock AAPL [2019-12-24]')
        return
    if len(context.args) > 1:
        day = context.args[1]
    else:
        day = datetime.date.today().strftime('%Y-%m-%d')

    ts = TimeSeries(config.finance.api_key)
    try:
        data, meta = ts.get_daily(symbol=context.args[0])
    except ValueError:
        context.bot.send_message(chat_id=update.message.chat.id,
                                text='No such symbol.')
        return

    try:
        result = data[day]
    except KeyError:
        if len(context.args) > 1:
            context.bot.send_message(
                chat_id=update.message.chat.id,
                text='Date invalid, fallback: ' + meta['3. Last Refreshed'])

        # TODO: find previous business day - need to determine country
        result = data[meta['3. Last Refreshed']]

    context.bot.send_message(chat_id=update.message.chat.id,
                             text=str(result))


def foreign_exchange(update, context):
    if len(context.args) < 2:
        context.bot.send_message(chat_id=update.message.chat.id,
                                 text='Usage: /fx <from> <to> [amount]')
        context.bot.send_message(chat_id=update.message.chat.id,
                                 text='ex: /fx BTC JPY 10')
        return

    fx = ForeignExchange(key=config.finance.api_key)
    try:
        data, _ = fx.get_currency_exchange_rate(
            from_currency=context.args[0],
            to_currency=context.args[1])
    except ValueError:
        context.bot.send_message(
            chat_id=update.message.chat.id,
            text='One or both inputted currencies are unsupported.')
        return
    answer = None
    
    if len(context.args) > 2:
        try:
            amount = float(context.args[2])
            answer = 'You can get {} {} with {} {}.'.format(
                float_format(float(data['5. Exchange Rate']) * amount),
                data['4. To_Currency Name'],
                context.args[2],
                data['2. From_Currency Name'])
        except ValueError:
            pass

    if not answer:
        answer = 'The rate of {} to {} is {}.'.format(
            data['2. From_Currency Name'],
            data['4. To_Currency Name'],
            float_format(data['5. Exchange Rate']))

    context.bot.send_message(chat_id=update.message.chat.id, text=answer)
