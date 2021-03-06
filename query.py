from functools import lru_cache
import json
import random
import re

import requests
from telegram import ChatAction
from telegram.error import BadRequest

import config
from util import send_action


@lru_cache(maxsize=100)
def query(q, key, cx, gif=False):
    api_url = 'https://www.googleapis.com/customsearch/v1'
    payload = {'key':key,
              'cx':cx,
              'searchType':'image',
              'prettyPrint':'True',
              'q':q}
    if gif:
        payload['fileType'] = 'gif'

    resp = requests.get(api_url, params=payload)
    resp_body = json.loads(resp.text)

    return list(map(lambda x: x['link'], resp_body['items']))


@send_action(ChatAction.UPLOAD_PHOTO)
def send_photo(update, context, isGif, photoToSend):
    id_for_reply = None
    if update.message.reply_to_message:
        id_for_reply = update.message.reply_to_message.message_id


    try:
        if isGif or photoToSend.split('?')[0].endswith('.gif'):
            context.bot.send_animation(
                update.message.chat_id,
                photoToSend,
                reply_to_message_id=id_for_reply)
        else:
            context.bot.send_photo(
                update.message.chat_id,
                photoToSend,
                reply_to_message_id=id_for_reply)
    except BadRequest:
        context.bot.send_message(chat_id=update.message.chat.id,
                                 text='Bad request on ' + photoToSend)


def accept_query(update, context):
    pattern = '^(?!.*://)(.+)\.(jpg|png|gif|bmp)$'
    matches = re.match(pattern, update.message.text)
    if not matches:
        return

    keyword = matches[1]
    ext = matches[2]
    isGif = (ext == 'gif')
    
    items = query(key=config.query.api_key, cx=config.query.cx,
                  q=keyword, gif=isGif)
    photoToSend = random.choices(items,
                  weights=list(reversed(range(1,len(items)+1))))[0]
    print(photoToSend, flush=True)
    send_photo(update, context, isGif, photoToSend)
