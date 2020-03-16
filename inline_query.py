import re
from uuid import uuid4

from telegram import ChatAction
from telegram import InlineQueryResultGif, InlineQueryResultPhoto

import config
from query import query

def inline_query(update, context):
    pattern = '^(?!.*://)(.+)\.(jpg|png|gif|bmp)$'
    matches = re.match(pattern, update.inline_query.query)
    if not matches:
        return

    keyword = matches[1]
    ext = matches[2]
    isGif = (ext == 'gif')

    print('{}.{}'.format(keyword, ext), flush=True)
    
    items = query(key=config.query.api_key, cx=config.query.cx,
                  q=keyword, gif=isGif)

    results = []
    for link in items:
        if isGif or link.split('?')[0].endswith('.gif'):
            results.append(InlineQueryResultGif(
                id=uuid4(),
                gif_url=link,
                thumb_url=link))
        else:
            results.append(InlineQueryResultPhoto(
                id=uuid4(),
                photo_url=link,
                thumb_url=link))

    update.inline_query.answer(results)
