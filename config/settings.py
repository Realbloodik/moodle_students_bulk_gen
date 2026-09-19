from dotenv import load_dotenv
import os


# Global configuration settings for the Moodle Students Bulk Generator
load_dotenv()

# Moodle REST API settings
MOODLE_URL = os.getenv("MOODLE_URL")
MOODLE_REST_URL = os.getenv("MOODLE_REST_URL")
MOODLE_API_TOKEN = os.getenv("MOODLE_API_TOKEN")

# Path to the JSON file containing names
NAMES_JSON_FILE = "config/names.json"

# Enable additional hex characters in usernames (e.g., for duplicate usernames)
enable_hex_characters = True

# Name transliteration API
transliterate_url = "https://slovnyk.ua/translit.php"

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
    "salutation",
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
    "username",
    "email",
    "cohort1"
]


def check_for_moodle_api_token():
    if not MOODLE_API_TOKEN:
        raise ValueError(
            "ERROR: --moodle_rest is on, but MOODLE_API_TOKEN"
            "is not found in .env file!"
        )
