from email_validator import validate_email, EmailNotValidError
import config.names as names
import config.settings as cfg
import random
import re
import string


def print_separator():
    print("----------------------------------------")


def normalize_name(full_name):
    for symbol in ["`", "ʼ", "’", "‘"]:
        full_name = full_name.replace(symbol, "'")

    text = re.sub(r'[\(\[\{].*?[\)\]\}]', '', full_name)
    text = re.sub(r"[^\w\s'-]", '', text, flags=re.UNICODE)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'-+', '-', text)

    return text.strip(" -")


def split_name(full_name):
    items = normalize_name(full_name).split()[:3]

    lastname = items[0] if len(items) > 0 else ""
    firstname = items[1] if len(items) > 1 else ""
    patronymic = items[2] if len(items) == 3 else ""

    return lastname, firstname, patronymic


def generate_username(lastname, firstname, patronymic):
    if patronymic:
        username = (
            firstname.lower()[0:1]
            + "."
            + patronymic.lower()[0:1]
            + "."
            + lastname.lower()
        )
    else:
        username = firstname.lower()[0:1] + "." + lastname.lower()

    if cfg.enable_hex_characters:
        hex_characters = string.hexdigits.lower()
        random_hex = "".join(random.choice(hex_characters) for _ in range(4))
        username += "_" + random_hex

    return username


# TODO: Implement a function to add new names to the men_names and women_names
# lists in config/names.py on the fly
def select_salutation(firstname_ukr):
    if firstname_ukr in names.men:
        salutation = "Шановний"
    elif firstname_ukr in names.women:
        salutation = "Шановна"
    else:
        salutation = "Шановний/Шановна"

    return salutation


def validate_email_address(email):
    given_email = email

    while True:
        try:
            emailinfo = validate_email(given_email, check_deliverability=False)

            return emailinfo.normalized
        except EmailNotValidError as e:
            print_separator()
            print(f"ERROR - Invalid E-Mail address: {given_email}")
            print(f"Details: {str(e)}")
            print_separator()

            given_email = input("Please input a valid E-Mail address:").strip()
            print("Validating the provided E-Mail address...")
            print_separator()
