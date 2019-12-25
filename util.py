from functools import wraps


def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        def command_func(update, context, *args, **kwargs):
            context.bot.send_chat_action(chat_id=update.message.chat.id,
                                         action=action)
            return func(update, context,  *args, **kwargs)
        return command_func
    return decorator


def float_format(num):
    try:
        fnum = float(num)
    except ValueError:
        return num

    if fnum > 0.1:
        return '{:.2f}'.format(fnum)
    elif fnum > 0.01:
        return '{:.4f}'.format(fnum)
    else:
        return '{:.8f}'.format(fnum).rstrip('0')
