import requests
import json
import time

CONFIG_FILE = "config.json"
PROGRAM_FILE = "programs.json"
STATUS_FILE = "status.json"


def load_json(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return {}


def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)


def get_program_status(program_id, headers):

    url = f"https://api.intigriti.com/external/researcher/v1/programs/{program_id}"

    try:
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()

        name = data.get("name")
        status = data.get("status", {}).get("value")

        return name, status

    except:
        return None, None


def send_telegram(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    try:
        requests.post(url, data={
            "chat_id": chat_id,
            "text": message
        }, timeout=10)
    except:
        pass


def main():

    config = load_json(CONFIG_FILE)
    status_data = load_json(STATUS_FILE)

    status_data.setdefault("previous_status", {})
    status_data.setdefault("current_status", {})

    headers = {
        "Authorization": f"Bearer {config['intigriti_api_key']}"
    }

    while True:

        programs_data = load_json(PROGRAM_FILE)
        program_ids = programs_data.get("programs", [])

        if not program_ids:
            print("No programs configured.")
            time.sleep(5)
            continue

        previous_status = status_data["previous_status"]
        current_status = status_data["current_status"]

        for program_id in program_ids:

            name, new_status = get_program_status(program_id, headers)

            if not name or not new_status:
                print("API failure:", program_id)
                continue

            if new_status not in ["Open", "Suspended"]:
                print("Invalid status:", new_status)
                continue

            # First run
            if program_id not in previous_status:

                previous_status[program_id] = new_status
                current_status[program_id] = new_status

                save_json(STATUS_FILE, status_data)

                print("Init:", name, new_status)
                continue

            prev = previous_status[program_id]
            curr = current_status[program_id]

            # Possible change
            if new_status != curr:

                current_status[program_id] = new_status
                save_json(STATUS_FILE, status_data)

                print("Possible change:", name, curr, "→", new_status)
                continue

            # Confirmed change
            if new_status == curr and prev != curr:

                message = f"{name} is now {curr}"

                send_telegram(
                    config["telegram_token"],
                    config["chat_id"],
                    message
                )

                previous_status[program_id] = curr
                save_json(STATUS_FILE, status_data)

                print("ALERT:", message)

        # AUTO CLEANUP REMOVED PROGRAMS
        valid_ids = set(program_ids)

        for pid in list(previous_status.keys()):
            if pid not in valid_ids:
                print("Removing stale program:", pid)
                previous_status.pop(pid, None)
                current_status.pop(pid, None)

        save_json(STATUS_FILE, status_data)

        time.sleep(config["check_interval"])


if __name__ == "__main__":
    main()