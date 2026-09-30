from email_validator import (
    validate_email, EmailNotValidError, EmailUndeliverableError
)
import config.settings as cfg
import csv
import random
import re
import string


def file_empty(file):
    try:
        with open(file, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)
            has_second_row = next(reader, None)
            return has_second_row is None

    except FileNotFoundError:
        return True
    except Exception as e:
        print(f"ERROR while checking '{file}':", e)
        exit(1)


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


def normalize_name(full_name):
    for symbol in ["`", "ʼ", "’", "‘"]:
        full_name = full_name.replace(symbol, "'")

    text = re.sub(r'[\(\[\{].*?[\)\]\}]', '', full_name)
    text = re.sub(r"[^\w\s'-]", '', text, flags=re.UNICODE)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'-+', '-', text)

    return text.strip(" -")


def print_separator():
    print("----------------------------------------")


def split_name(full_name):
    items = normalize_name(full_name).split()[:3]

    lastname = items[0] if len(items) > 0 else ""
    firstname = items[1] if len(items) > 1 else ""
    patronymic = items[2] if len(items) == 3 else ""

    return lastname, firstname, patronymic


def _check_email(email):
    normalized = validate_email(email, check_deliverability=False).normalized

    LOCAL_PART_RE = re.compile(r"^[a-zA-Z0-9._+-]+$")
    local_part, _domain = normalized.rsplit("@", 1)
    if not LOCAL_PART_RE.match(local_part):
        raise EmailNotValidError(
            "Email contains invalid characters "
            "(like '/' or non-English letters)"
        )

    validate_email(normalized, check_deliverability=True)

    return normalized


def _ask_override(email):
    while True:
        choice = input(
            "[R]etry with a new address / [O]verride and use it anyway? "
        ).strip().lower()
        if choice in ("r", "retry", ""):
            return False
        if choice in ("o", "override"):
            confirm = input(
                f"Use '{email}' even though it failed validation? (yes/no): "
            ).strip().lower()
            if confirm in ("y", "yes"):
                return True
        else:
            print("Please enter R or O.")


def validate_email_address(email):
    given_email = email.strip()

    while True:
        try:
            return _check_email(given_email)

        except EmailUndeliverableError as e:
            print_separator()
            print(
                f"WARNING - Address looks valid but is undeliverable:"
                f" {given_email}"
            )
            print(f"Details: {e}")
            print_separator()

            if _ask_override(given_email):
                return validate_email(
                    given_email, check_deliverability=False
                ).normalized

        except EmailNotValidError as e:
            print_separator()
            print(f"ERROR - Invalid E-Mail address: {given_email}")
            print(f"Details: {e}")
            print_separator()

            if _ask_override(given_email):
                return given_email

        given_email = input("Please input a valid E-Mail address: ").strip()
        print("Validating the provided E-Mail address...")
        print_separator()
