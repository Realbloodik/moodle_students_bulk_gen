from bs4 import BeautifulSoup
from names import men_names, women_names
import argparse
import csv
import os
import requests
import secrets
import string


### Subfunctions
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
        print(f"Error checking {api_name} API status:", e)
        exit(1)


def check_duplicate(username, email, dicts_list):
    for dict in dicts_list:
        if dict["username"] == username or dict["email"] == email:
            return True
    return False


def duplicates_file_empty(file):
    try:
        with open(file, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
            if len(rows) <= 1:  # Only header or empty
                return True
            else:
                return False
    except FileNotFoundError:
        return True
    except Exception as e:
        print("Error checking duplicates file:", e)
        exit(1)


def generate_password(length, special_characters, exclude_characters):
    specials = "!@#$%&*()_"
    alphabet = string.ascii_letters + string.digits + specials

    while True:
        password = "".join(secrets.choice(alphabet) for i in range(length))
        if (
            sum(c.islower() for c in password) >= 4
            and sum(c.isupper() for c in password) >= 2
            and sum(c.isdigit() for c in password) >= 2
            and sum(c in specials for c in password) == special_characters
            and all(c not in exclude_characters for c in password)
        ):
            return password


def print_separator():
    print("----------------------------------------")


def read_password_generator_api_key():
    try:
        with open("password_api_key.txt", "r") as api_key_file:
            api_key = api_key_file.read().strip()
            return {"X-Api-Key": api_key}
    except FileNotFoundError:
        print(
            "Error: 'password_api_key.txt' file not found. File has been created. Please place your API key inside it."
        )
        with open("password_api_key.txt", "w") as api_key_file:
            api_key_file.write("Place your API key here...")
        exit(1)
    except Exception as e:
        print("Error reading API key:", e)
        exit(1)


def split_name(full_name):
    for symbol in ["`", "ʼ", "’", "‘"]:
        full_name = full_name.replace(symbol, "'")

    split_name = full_name.split()
    lastname = split_name[0]
    firstname = split_name[1]
    if len(split_name) == 3:
        patronymic = split_name[2]
    elif len(split_name) == 2:
        patronymic = ""

    return lastname, firstname, patronymic


### Settings
# Name transliteration API
transliterate_url = "https://slovnyk.ua/translit.php"

# Password generator Web API
web_length = "12"
web_uppercase = "true"
web_lowercase = "true"
web_numbers = "true"
web_special = "true"
password_web_api_url = "https://api.api-ninjas.com/v1/passwordgenerator?length={}&uppercase={}&lowercase={}&numbers={}&special={}".format(
    web_length, web_uppercase, web_lowercase, web_numbers, web_special
)
# To use the password generator Web API, you need to get your own API key from https://api-ninjas.com/
# and write it in the "password_api_key.txt" file
password_web_api_key = read_password_generator_api_key()

# Local password generator
local_length = 12
local_special_characters = 2
local_exclude_characters = "lI"

# .csv fieldnames
students_fieldnames = [
    "username",
    "password",
    "lastname",
    "firstname",
    "email",
    "lang",
    "cohort1",
]
email_fieldnames = [
    "email",
    "addressing",
    "lastname",
    "firstname",
    "username",
    "password",
]
cohort_fieldnames = [
    "name",
    "idnumber",
    "description"
]
duplicates_fieldnames = [
    "lastname",
    "firstname",
    "username",
    "email",
    "cohort1"
]


### Main program
def main():
    parser = argparse.ArgumentParser(
        description="Generate Moodle user accounts information, email and cohorts lists"
    )
    parser.add_argument(
        "-i", "--input", help="The file for the program to use", type=str
    )
    parser.add_argument(
        "-o",
        "--output",
        default="output.csv",
        help="The destination of the output file",
        type=str,
    )
    parser.add_argument(
        "-l",
        "--local_api",
        action="store_true",
        help="Use local password generator instead of Web API",
    )
    args = parser.parse_args()

    # Arguments validation
    if not args.input:
        print("Usage: script.py -i <input_file> [-o] <output_file> [-l]")
        exit(1)
    elif args.output and args.input == args.output:
        print("Input and output files must be different.")
        exit(1)
    elif not str(args.input).endswith(".csv") or (
        args.output and not str(args.output).endswith(".csv")
    ):
        print("Input and output files must be .csv format.")
        exit(1)

    # Open files
    input_csv = open(args.input, newline="", encoding="utf-8")
    input_Reader = csv.DictReader(input_csv)

    output_csv = open(args.output, "w", newline="", encoding="utf-8")
    outputWriter = csv.DictWriter(output_csv, fieldnames=students_fieldnames)
    outputWriter.writeheader()

    email_csv_name = str(args.output).replace(".csv", "_email.csv")
    output_email_csv = open(email_csv_name, "w", newline="", encoding="utf-8")
    output_email_Writer = csv.DictWriter(
        output_email_csv, fieldnames=email_fieldnames, delimiter=","
    )
    output_email_Writer.writeheader()

    cohorts_csv_name = str(args.output).replace(".csv", "_cohorts.csv")
    output_cohorts_csv = open(cohorts_csv_name, "w", newline="", encoding="utf-8")
    output_cohorts_Writer = csv.DictWriter(
        output_cohorts_csv, fieldnames=cohort_fieldnames, delimiter=","
    )
    output_cohorts_Writer.writeheader()

    duplicates_csv_name = str(args.output).replace(".csv", "_duplicates.csv")
    duplicates_csv = open(duplicates_csv_name, "w", newline="", encoding="utf-8")
    duplicates_csv_Writer = csv.DictWriter(
        duplicates_csv, fieldnames=duplicates_fieldnames, delimiter=","
    )
    duplicates_csv_Writer.writeheader()

    print_separator()
    print(
        "A program for generating Moodle user accounts information for bulk uploading, emailing, and cohort lists."
    )
    print_separator()

    session = requests.session()

    # APIs status check
    api_status_check(session, transliterate_url, "Transliteration")
    if not args.local_api:
        api_status_check(session, "https://api-ninjas.com/", "Password Generation")

    print_separator()

    cohorts_temp = []
    duplicates_check_dicts = []
    processed_rows = 0

    for row in input_Reader:
        processed_rows += 1

        email = row["email"]
        cohort = row["cohort"]

        # Ukrainian name, last name and patronymic
        lastname_ukr, firstname_ukr, patronymic_ukr = split_name(row["name"])

        # Transliteration
        data = {}
        data["text"] = lastname_ukr + " " + firstname_ukr + " " + patronymic_ukr
        try:
            response = requests.post(transliterate_url, data=data, timeout=30)
        except Exception:
            print("Error:", response.status_code, response.text)
            exit(1)

        # Parse the response
        response_page = BeautifulSoup(response.text, features="lxml")

        # English name, last name and patronymic
        lastname_eng, firstname_eng, patronymic_eng = split_name(
            response_page.find("textarea", id="translated1").string
        )
        if patronymic_eng:
            username = (
                firstname_eng.lower()[0:1]
                + "."
                + patronymic_eng.lower()[0:1]
                + "."
                + lastname_eng.lower()
            )
        else:
            username = firstname_eng.lower()[0:1] + "." + lastname_eng.lower()

        # Check for duplicate user
        if check_duplicate(username, email, duplicates_check_dicts):
            duplicates_csv_Writer.writerow(
                {
                    "lastname": lastname_ukr,
                    "firstname": firstname_ukr + " " + patronymic_ukr,
                    "username": username,
                    "email": email,
                    "cohort1": cohort,
                }
            )
            print(f"{processed_rows} - {username} - duplicate user found!")
            continue

        # Write duplicates temp list of dicts
        duplicates_check_dicts.append({"username": username, "email": email})

        if not args.local_api:
            # Web API password generation
            response = requests.get(password_web_api_url, headers=password_web_api_key)
            if response.status_code == requests.codes.ok:
                pass_result = response.json()
            else:
                print("Error:", response.status_code, response.text)
                exit(1)

            password = pass_result["random_password"]
        else:
            # Local password generation
            password = generate_password(
                local_length, local_special_characters, local_exclude_characters
            )

        # Write main result file
        outputWriter.writerow(
            {
                "username": username,
                "password": password,
                "lastname": lastname_ukr,
                "firstname": firstname_ukr + " " + patronymic_ukr,
                "email": email,
                "lang": "UK",
                "cohort1": cohort,
            }
        )
        print(f"{processed_rows} - {username} - user account info generated")

        # Select correct addressing
        if firstname_ukr in men_names:
            addressing = "Шановний"
        elif firstname_ukr in women_names:
            addressing = "Шановна"
        else:
            addressing = "Шановний/Шановна"

        # Write email info file
        output_email_Writer.writerow(
            {
                "email": email,
                "addressing": addressing,
                "lastname": lastname_ukr,
                "firstname": firstname_ukr + " " + patronymic_ukr,
                "username": username,
                "password": password,
            }
        )
        print(f"     {username} - email info generated")

        # Cohorts temp list
        if cohort not in cohorts_temp:
            cohorts_temp.append(cohort)

    print_separator()

    # Write unique cohorts list
    for cohort in cohorts_temp:
        output_cohorts_Writer.writerow(
            {"name": cohort, "idnumber": cohort, "description": ""}
        )
        print(f"{cohort} - cohort record added")

    # Close all files
    for file in [
        input_csv,
        output_csv,
        output_email_csv,
        output_cohorts_csv,
        duplicates_csv,
    ]:
        file.close()

    # Remove duplicates file if empty
    if duplicates_file_empty(duplicates_csv_name):
        try:
            os.remove(duplicates_csv_name)
        except Exception as e:
            print("Error removing duplicates file:", e)
            exit(1)

    print_separator()
    print("Done!")
    print(f"Processed {processed_rows} rows.")
    print_separator()


if __name__ == "__main__":
    main()
