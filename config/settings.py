# Global configuration settings for the Moodle Students Bulk Generator

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
    "original_row",
    "lastname",
    "firstname",
    "email",
    "cohort1"
]
