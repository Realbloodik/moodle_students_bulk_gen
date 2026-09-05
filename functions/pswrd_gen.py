import config.pswrd_gen_local_api as cfg_local
import config.pswrd_gen_web_api as cfg_web
import requests
import secrets
import string


# Local password generation function
def generate_password_local():
    specials = cfg_local.specials
    alphabet = string.ascii_letters + string.digits + specials

    while True:
        password = "".join(
            secrets.choice(alphabet) for i in range(cfg_local.length))
        if (
            sum(c.islower() for c in password) >= cfg_local.lowercase
            and sum(c.isupper() for c in password) >= cfg_local.uppercase
            and sum(c.isdigit() for c in password) >= cfg_local.digits
            and sum(c in specials for c in password) == cfg_local.special_chars
            and all(c not in cfg_local.exclude_chars for c in password)
        ):
            return password


# Web API password generation function
def generate_password_web_api():
    response = requests.get(
        cfg_web.api_url, headers=cfg_web.api_key)
    if response.status_code == requests.codes.ok:
        pass_result = response.json()

        return pass_result["random_password"]
    else:
        print("ERROR:", response.status_code, response.text)
        exit(1)
