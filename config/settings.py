# Global configuration settings for the Moodle Students Bulk Generator

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
    "lastname",
    "firstname",
    "username",
    "email",
    "cohort1"
]
