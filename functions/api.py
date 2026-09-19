from bs4 import BeautifulSoup
import config.settings as cfg
import functions.misc as misc
import requests


def api_status_check(session, api_url, api_name):
    try:
        response = session.get(api_url)
        if response.status_code in [200, 400, 401, 403]:
            print(f"{api_name} API status: OK")
        else:
            print(f"{api_name} API status: DOWN")
            print("Try again later or check the network connection.")
            exit(1)
    except requests.RequestException as e:
        print(f"ERROR while checking {api_name} API status:", e)
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
