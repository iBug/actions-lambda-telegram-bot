import telegram

from telegram.ext import CommandHandler


def do(dispatcher, update):
    dispatcher.add_handler(CommandHandler("start", cmd_start))

    dispatcher.process_update(update)
    return 200


def cmd_start(update, context):
    chat_id = update.effective_chat.id
    text = "Hello world! I'm a bot and I still need more code."
    context.bot.send_message(chat_id=chat_id, text=text)
