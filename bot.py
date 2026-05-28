import time

def main():

    offset = None
    print("🛰 BorykNews bot STARTED")

    while True:

        try:
            updates = get_updates(offset)

            for update in updates.get("result", []):

                offset = update["update_id"] + 1

                if "message" in update:
                    handle_message(update["message"])

                if "callback_query" in update:
                    handle_callback(update["callback_query"])

        except Exception as e:
            print("ERROR:", e)

        time.sleep(1)
