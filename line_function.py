import os
import boto3
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, TemplateSendMessage, CarouselColumn, CarouselTemplate, URITemplateAction

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
    print(event)
    print(response)
    # Lexからの応答テキストをLINEへポストする
    
    for message in response['messages']:
        print(message['content'])
        # line_bot_api.reply_message(
        #         event.reply_token,
        #         TextSendMessage(text=str(message['content'])))
        if('レシピが見つかりました' in message['content']):
            t = message['content'].split("\n")
            titles = [d[5:] for d in t if d[:5] == 'タイトル:']
            url = [d[4:] for d in t if d[:4] == 'URL:']
            img = [d[3:] for d in t if d[:3] == '画像:']
            des = [d[7:] for d in t if d[:7] == '作者コメント:']
            for a in range(len(des)):
                if len(des[a]) >= 50:
                    des[a] = des[a][:50] + '…'
            print(img)
            columns = [
                CarouselColumn(
                    thumbnail_image_url=img[i],
                    # "https://recoeggs.hs.llnwd.net/flmg_img_p/profile/27187.jpg",
                    title=titles[i],
                    text=des[i],
                    # 'ブランデー戦記',
                    actions=[
                        URITemplateAction(
                            label='ページを開く',
                            uri=url[i]
                        )
                        # ),
                        # URITemplateAction(
                        #     label='曲を聴く',
                        #     uri='https://aso2201305.nobushi.jp/kaihatu/music_1.html'
                        # )
                    ]
                ) for i in range(len(titles))
            ]
            
            messages = TemplateSendMessage(
               alt_text="検索結果送信",
               template=CarouselTemplate(columns=columns),
            )
            #以下メッセージ
            for message in response['messages']:
                # line_bot_api.push_message(event.reply_token, [TextSendMessage(text = "第一のメッセージ\naaa"), TextSendMessage(text = "第一のメッセージ\naaa")])
                line_bot_api.reply_message(event.reply_token, messages = messages)
        elif('お店が見つかりました' in message['content']):
            t = message['content'].split("\n")
            name = [d[3:] for d in t if d[:3] == '店名:']
            address = [d for d in t if d[:3] == '住所:']
            budget = [d for d in t if d[:5] == '平均予算:']
            url = [d[4:] for d in t if d[:4] == 'url:']
            img = [d[3:] for d in t if d[:3] == '画像:']
            des = [d[5:] for d in t if d[:5] == 'コメント:']
            for a in range(len(des)):
                des[a] = address[a] + '\n' + budget[a] + '\n' + des[a]
                if len(des[a]) >= 50:
                    des[a] = des[a][:50] + '…'
            print(img)
            columns = [
                CarouselColumn(
                    thumbnail_image_url=img[i],
                    # "https://recoeggs.hs.llnwd.net/flmg_img_p/profile/27187.jpg",
                    title=name[i],
                    text=des[i],
                    # 'ブランデー戦記',
                    actions=[
                        URITemplateAction(
                            label='ページを開く',
                            uri=url[i]
                        )
                        # ),
                        # URITemplateAction(
                        #     label='曲を聴く',
                        #     uri='https://aso2201305.nobushi.jp/kaihatu/music_1.html'
                        # )
                    ]
                ) for i in range(len(name)) if i < 10
            ]
            
            messages = TemplateSendMessage(
               alt_text="検索結果送信",
               template=CarouselTemplate(columns=columns),
            )
            #以下メッセージ
            for message in response['messages']:
                # line_bot_api.push_message(event.reply_token, [TextSendMessage(text = "第一のメッセージ\naaa"), TextSendMessage(text = "第一のメッセージ\naaa")])
                line_bot_api.reply_message(event.reply_token, messages = messages)
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=str(message['content'])))