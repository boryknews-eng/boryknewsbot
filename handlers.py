import requests
import json
import os

from config import TOKEN, ADMIN_ID, CHANNEL_ID

URL = f"https://api.telegram.org/bot{TOKEN}"


# ================= SEND PHOTO =================
def send_photo(chat_id, photo_path, caption, keyboard=None):

    with open(photo_path, "rb") as photo:

        requests.post(
            f"{URL}/sendPhoto",
            data={
                "chat_id": chat_id,
                "caption": caption,
                "reply_markup": json.dumps(keyboard) if keyboard else None
            },
            files={"photo": photo}
        )


# ================= SEND MESSAGE =================
def send_message(chat_id, text, keyboard=None):

    requests.post(
        f"{URL}/sendMessage",
        data={
            "chat_id": chat_id,
            "text": text,
            "reply_markup": json.dumps(keyboard) if keyboard else None
        }
    )


# ================= MODERATION =================
def send_to_moderation(message):

    username = message["from"].get("username", "no_username")
    caption = message.get("caption") or message.get("text") or "Без опису"

    keyboard = {
        "inline_keyboard": [
            [
                {"text": "✅ Опублікувати", "callback_data": "approve"},
                {"text": "❌ Відхилити", "callback_data": "reject"}
            ]
        ]
    }

    text = (
        f"📥 НОВИЙ МАТЕРІАЛ\n\n"
        f"👤 @{username}\n\n"
        f"📝 {caption}"
    )

    if message.get("photo"):

        photo_id = message["photo"][-1]["file_id"]

        requests.post(
            f"{URL}/sendPhoto",
            data={
                "chat_id": ADMIN_ID,
                "photo": photo_id,
                "caption": text,
                "reply_markup": json.dumps(keyboard)
            }
        )

    else:
        send_message(ADMIN_ID, text, keyboard)


# ================= MAIN =================
```python id="95d6bq"
def handle_message(message):

    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if text == "/start":

        send_message(
            chat_id,
            "🛰 Вітаємо в BorykNews 🚀"
        )

        return
```

    # ================= START =================
    if text == "/start":

        keyboard = {
            "keyboard": [
                ["📰 Новина", "📢 Оголошення"],
                ["🚨 Тривога", "📣 Реклама"],
                ["📸🎥 Надіслати матеріал"]
            ],
            "resize_keyboard": True
        }

        caption = (
            "🛰 BorykNews LIVE\n\n"
            "👋 Вітаємо в системі новин Борисполя\n\n"
            "⚡️ Обери потрібний розділ нижче"
        )

        send_photo(
            chat_id,
            os.path.join("images", "welcome.jpg"),
            caption,
            keyboard
        )
        return


    # ================= 🚨 ТРИВОГА =================
    if text == "🚨 Тривога":

        keyboard = {
            "inline_keyboard": [
                [
                    {
                        "text": "🗺 Відкрити карту",
                        "url": "https://alerts.in.ua/"
                    }
                ]
            ]
        }

        send_photo(
            chat_id,
            os.path.join("images", "alert_banner.jpg"),
            (
                "🚨 ПОВІТРЯНА ТРИВОГА\n\n"
                "📍 Бориспіль / Київщина\n\n"
                "⚠️ Негайно пройдіть в укриття"
            ),
            keyboard
        )
        return


    # ================= 📰 НОВИНА =================
    if text == "📰 Новина":

        send_photo(
            chat_id,
            os.path.join("images", "news_banner.jpg"),
            (
                "📰 НОВИНА BorykNews\n\n"
                "✍️ Надішли текст новини\n"
                "📸 Потім додай фото або відео\n\n"
                "🛡 Усі матеріали проходять перевірку"
            )
        )
        return


    # ================= 📢 ОГОЛОШЕННЯ =================
    if text == "📢 Оголошення":

        send_photo(
            chat_id,
            os.path.join("images", "ads_banner.jpg"),
            (
                "📢 ОГОЛОШЕННЯ BorykNews\n\n"
                "🛰 Публікуй важливу інформацію для мешканців Борисполя\n\n"
                "📍 Можна розміщувати:\n"
                "• загублені речі\n"
                "• пошук людей\n"
                "• допомога\n"
                "• продаж\n"
                "• послуги\n"
                "• події міста\n\n"
                "📸 Надішли текст + фото або відео\n\n"
                "🛡 Після перевірки буде публікація"
            )
        )
        return


    # ================= 📣 РЕКЛАМА =================
    if text == "📣 Реклама":

        send_photo(
            chat_id,
            os.path.join("images", "promo_banner.jpg"),
            (
                "📣 РЕКЛАМА В BorykNews\n\n"
                "🚀 Просувай свій бізнес у Борисполі та Київщині\n\n"
                "💡 Можна рекламувати:\n"
                "• магазини\n"
                "• послуги\n"
                "• бʼюті-сферу\n"
                "• доставку\n"
                "• акції та події\n\n"
                "📸 Надішли текст + фото або відео\n\n"
                "📊 Локальна аудиторія = реальні клієнти"
            )
        )
        return


    # ================= 📸🎥 МАТЕРІАЛ =================
    if text == "📸🎥 Надіслати матеріал":

        send_photo(
            chat_id,
            os.path.join("images", "media_banner.jpg"),
            (
                "📸🎥 BORYKNEWS LIVE\n\n"
                "🛰 Надішли матеріал з місця події\n\n"
                "⚡️ Ми публікуємо:\n"
                "• ДТП\n"
                "• пожежі\n"
                "• вибухи / тривоги\n"
                "• важливі міські ситуації\n"
                "• події очевидців\n\n"
                "📍 Важливо:\n"
                "• фото або відео ОБОВ’ЯЗКОВО\n"
                "• можна короткий опис\n"
                "• усе проходить перевірку\n\n"
                "🛡 Ми публікуємо тільки перевірену інформацію"
            )
        )
        return


# ================= MODERATION =================
def send_to_moderation(message):

    username = message["from"].get("username", "no_username")
    caption = message.get("caption") or message.get("text") or "Без опису"

    keyboard = {
        "inline_keyboard": [
            [
                {
                    "text": "✅ Опублікувати",
                    "callback_data": f"approve_{message['chat']['id']}"
                },
                {
                    "text": "❌ Відхилити",
                    "callback_data": f"reject_{message['chat']['id']}"
                }
            ]
        ]
    }

    text = (
        f"📥 НОВИЙ МАТЕРІАЛ\n\n"
        f"👤 @{username}\n\n"
        f"📝 {caption}"
    )

    if message.get("photo"):

        photo_id = message["photo"][-1]["file_id"]

        requests.post(
            f"{URL}/sendPhoto",
            data={
                "chat_id": ADMIN_ID,
                "photo": photo_id,
                "caption": text,
                "reply_markup": json.dumps(keyboard)
            }
        )

    else:

        send_message(
            ADMIN_ID,
            text,
            keyboard
        )


# ================= MAIN =================
def handle_message(message):

    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    # ================= START =================
    if text == "/start":

        keyboard = {
            "keyboard": [
                ["📰 Новина", "📢 Оголошення"],
                ["🚨 Тривога", "📣 Реклама"],
                ["📸🎥 Надіслати матеріал"]
            ],
            "resize_keyboard": True
        }

        caption = (
            "🛰 Ласкаво просимо до BorykNews LIVE\n\n"
            "📍 Головний бот новин та подій Борисполя\n\n"
            "Тут ви можете:\n"
            "📰 надсилати новини\n"
            "📸 ділитися фото та відео\n"
            "📢 публікувати оголошення\n"
            "🚨 повідомляти про важливі події\n"
            "📣 замовляти рекламу\n\n"
            "⚡️ Оберіть потрібний розділ нижче та почніть користуватись системою."
        )

        send_photo(
            chat_id,
            os.path.join("images", "welcome.jpg"),
            caption,
            keyboard
        )
        return


    # ================= AUTO MODERATION =================
    if message.get("photo") or message.get("video") or message.get("text"):

        send_to_moderation(message)
        send_message(chat_id, "📥 Прийнято на перевірку")
        
# ================= CALLBACK =================
def handle_callback(callback):

    data = callback["data"]

    parts = data.split("_")

    action = parts[0]

    user_id = None
    if len(parts) > 1:
        user_id = parts[1]

    msg = callback["message"]

    caption = msg.get("caption", "🛰 BorykNews LIVE")

    photo = None
    if msg.get("photo"):
        photo = msg["photo"][-1]["file_id"]

    # ================= APPROVE =================
    if action == "approve":

        if photo:

            requests.post(
                f"{URL}/sendPhoto",
                data={
                    "chat_id": CHANNEL_ID,
                    "photo": photo,
                    "caption": caption + "\n\n📍 BorykNews LIVE"
                }
            )

        else:

            send_message(
                CHANNEL_ID,
                caption + "\n\n📍 BorykNews LIVE"
            )

        requests.post(
            f"{URL}/answerCallbackQuery",
            data={
                "callback_query_id": callback["id"],
                "text": "Опубліковано"
            }
        )

        if user_id:
            send_message(
                user_id,
                "🎉 Ваш матеріал опубліковано в BorykNews"
            )

    # ================= REJECT =================
    elif action == "reject":

        requests.post(
            f"{URL}/answerCallbackQuery",
            data={
                "callback_query_id": callback["id"],
                "text": "Відхилено"
            }
        )

        requests.post(
            f"{URL}/editMessageCaption",
            data={
                "chat_id": ADMIN_ID,
                "message_id": msg["message_id"],
                "caption": caption + "\n\n❌ ВІДХИЛЕНО"
            }
        )

        if user_id:
            send_message(
                user_id,
                "🛰 BorykNews MODERATION\n\n"
                "❌ Ваш матеріал не пройшов перевірку модерацією.\n\n"
                "📌 Можливі причини:\n"
                "• недостатньо інформації\n"
                "• порушення правил\n"
                "• реклама / спам\n"
                "• неякісний матеріал\n\n"
                "🙏 Ви можете надіслати матеріал повторно."
            )
