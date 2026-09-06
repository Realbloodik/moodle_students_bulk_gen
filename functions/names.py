from functions.misc import print_separator
import config.settings as cfg
import json
import os


men_names: set = set()
women_names: set = set()


def check_json_file_exists():
    if not os.path.exists(cfg.NAMES_JSON_FILE):
        print_separator()
        print(f"ERROR - Names JSON file not found: {cfg.NAMES_JSON_FILE}")
        print_separator()
        exit(1)

    return True


def load_names_from_json():
    with open(cfg.NAMES_JSON_FILE, "r", encoding="utf-8") as file:
        names_data = json.load(file)
        men_names.update(names_data.get("men", []))
        women_names.update(names_data.get("women", []))

    return None


def add_name_to_json():
    data = {
        "men": sorted(list(men_names)),
        "women": sorted(list(women_names))
    }

    with open(cfg.NAMES_JSON_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    return None


def select_salutation(firstname_ukr):
    if firstname_ukr in men_names:
        return "Шановний"
    elif firstname_ukr in women_names:
        return "Шановна"

    print_separator()
    print(f"ERROR - Name not found in names: {firstname_ukr}")

    while True:
        select = input(
            "Please select a salutation (1 for Шановний, 2 for Шановна): "
            ).strip()
        print_separator()

        if select == "1":
            men_names.add(firstname_ukr)
            salutation = "Шановний"
            break
        elif select == "2":
            women_names.add(firstname_ukr)
            salutation = "Шановна"
            break
        else:
            print("Invalid selection. Please enter 1 or 2.")
            continue

    add_name_to_json()

    return salutation
