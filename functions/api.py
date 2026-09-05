from bs4 import BeautifulSoup
import config.settings as cfg
import functions.misc as misc
import requests


def api_status_check(session, api_url, api_name):
    try:
        response = session.get(api_url)
        if response.status_code == 200:
            print(f"{api_name} API status: OK")
        else:
            print(f"{api_name} API status: DOWN")
            print("Try again later or check the network connection.")
            exit(1)
    except requests.RequestException as e:
        print(f"ERROR while checking {api_name} API status:", e)
        exit(1)


def read_password_generator_api_key():
    try:
        with open("config/password_api_key.txt", "r") as api_key_file:
            api_key = api_key_file.read().strip()
            return {"X-Api-Key": api_key}
    except FileNotFoundError:
        misc.print_separator()
        print(
            "ERROR: 'password_api_key.txt' file not found. File has been"
            "created. Please place your API key inside it."
        )
        with open("config/password_api_key.txt", "w") as api_key_file:
            api_key_file.write("Place your API key here...")
    except Exception as e:
        print("ERROR while reading API key:", e)
        exit(1)


def transliterate_name(lastname_ukr, firstname_ukr, patronymic_ukr):
    data = {}
    data["text"] = lastname_ukr + " " + firstname_ukr + " " + patronymic_ukr
    try:
        response = requests.post(
            cfg.transliterate_url, data=data, timeout=30)
    except Exception:
        print("ERROR:", response.status_code, response.text)
        exit(1)

    # Parse the response
    response_page = BeautifulSoup(response.text, features="lxml")
    lastname, firstname, patronymic = misc.split_name(
            response_page.find("textarea", id="translated1").string)

    return lastname, firstname, patronymic
