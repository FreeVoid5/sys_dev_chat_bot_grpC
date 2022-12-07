import os
import boto3
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
lex_client = boto3.client('lexv2-runtime')
line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.environ.get('CHANNEL_SECRET'))

def lambda_handler(event, context):
    handler.handle(
        event['body'],
        event['headers']['x-line-signature'])
    return {'statusCode': 200, 'body': 'OK'}


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event: MessageEvent):
    # LINEから受け取ったテキストをLexへ認識させる
    response = lex_client.recognize_text(
        botId=os.environ.get('LEX_BOT_ID'),
        botAliasId=os.environ.get('LEX_BOT_ALIAS_ID'),
        localeId=os.environ.get('LEX_BOT_LOCALE_ID'),
        sessionId=event.source.user_id,
        text=event.message.text)
    # Lexからの応答テキストをLINEへポストする
    for message in response['messages']:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=str(message['content'])))