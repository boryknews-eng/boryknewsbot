import requests
from config import TOKEN
from handlers import handle_message, handle_callback

URL = f"https://api.telegram.org/bot{TOKEN}"


def get_updates(offset=None):
    return requests.get(
        f"{URL}/getUpdates",
        params={"timeout": 30, "offset": offset}
    ).json()


def main():

    offset = None
    print("🛰 BorykNews bot STARTED")

    while True:

        updates = get_updates(offset)

        for update in updates.get("result", []):

            offset = update["update_id"] + 1

            if "message" in update:
                handle_message(update["message"])

            if "callback_query" in update:
                handle_callback(update["callback_query"])


if __name__ == "__main__":
    main()