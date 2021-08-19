import base64
import json

import handlers
from telegram import Bot, Update
from telegram.ext import Dispatcher


def lambda_main(event, context):
    path = event['rawPath']
    if 'body' in event:
        if event['isBase64Encoded']:
            body = base64.b64decode(event['body'])
        else:
            body = event['body']
    else:
        body = None

    if path == "/_debug" or event.get('queryStringParameters', {}).get('debug'):
        status = 200
    elif path.count("/") != 2:
        status = 400
    else:
        _, function, token = path.split("/")

        try:
            bot = Bot(token)
            dispatcher = Dispatcher(bot, None, workers=0, use_context=True)
            update = Update.de_json(json.loads(body), bot)
            status = handlers.do(dispatcher, update)
        except Exception:
            status = 500

    return {
        'statusCode': status,
        'headers': {
            'Content-Type': "application/json",
        },
        'body': json.dumps({'status': status}),
        'isBase64Encoded': False,
    }
