import argparse
import config.settings as cfg
import csv
import functions.api as api
import functions.duplicates as duplicates
import functions.misc as misc
import functions.pswrd_gen as pswrd_gen
import os
import requests


# Main program
def main():
    # Command-line arguments parsing
    parser = argparse.ArgumentParser(
        description="Generate Moodle user accounts information,"
        "email and cohorts lists"
    )
    parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="The file for the program to use",
        type=str,
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
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

    # Command-line arguments validation
    if not args.input.lower().endswith(".csv"):
        parser.error("Input file must be in .csv format.")

    if not args.output:
        name, ext = os.path.splitext(args.input)
        args.output = f"{name}_output{ext}"
    elif not args.output.lower().endswith(".csv"):
        parser.error("Output file must be in .csv format.")

    if os.path.abspath(args.input).lower() == os.path.abspath(
            args.output).lower():
        parser.error("Input and output files must be different.")

    misc.print_separator()
    print(
        "A program for generating Moodle user accounts information"
        "for bulk uploading, emailing, and cohort lists."
    )
    misc.print_separator()

    session = requests.session()

    # APIs status check
    api.api_status_check(
        session, cfg.transliterate_url, "Transliterate API")
    if not args.local_api:
        api.api_status_check(
            session, cfg.web_api_url, "Generate Password Web API")

    misc.print_separator()

    # Create and open files for writing
    files = []

    input_csv = open(
        args.input, newline="", encoding="utf-8")
    files.append(input_csv)
    input_Reader = csv.DictReader(input_csv)

    output_csv = open(
        args.output, "w", newline="", encoding="utf-8")
    files.append(output_csv)
    outputWriter = csv.DictWriter(
        output_csv, fieldnames=cfg.students_fieldnames)
    outputWriter.writeheader()

    email_csv_name = str(args.output).replace(".csv", "_email.csv")
    output_email_csv = open(
        email_csv_name, "w", newline="", encoding="utf-8")
    files.append(output_email_csv)
    output_email_Writer = csv.DictWriter(
        output_email_csv, fieldnames=cfg.email_fieldnames, delimiter=",")
    output_email_Writer.writeheader()

    cohorts_csv_name = str(args.output).replace(".csv", "_cohorts.csv")
    output_cohorts_csv = open(
        cohorts_csv_name, "w", newline="", encoding="utf-8")
    files.append(output_cohorts_csv)
    output_cohorts_Writer = csv.DictWriter(
        output_cohorts_csv, fieldnames=cfg.cohort_fieldnames, delimiter=",")
    output_cohorts_Writer.writeheader()

    duplicates_csv_name = str(args.output).replace(".csv", "_duplicates.csv")
    duplicates_csv = open(
        duplicates_csv_name, "w", newline="", encoding="utf-8")
    files.append(duplicates_csv)
    duplicates_csv_Writer = csv.DictWriter(
        duplicates_csv, fieldnames=cfg.duplicates_fieldnames, delimiter=",")
    duplicates_csv_Writer.writeheader()

    cohorts_temp = []
    processed_users = []
    processed_rows = 0

    for row in input_Reader:
        processed_rows += 1

        # Check E-Mail validity and normalize it
        email = misc.validate_email_address(row["email"].strip())

        cohort = row["cohort"].strip()

        # Receive firstname, lastname and patronymic in Ukrainian
        # from the name field of the input CSV file
        lastname_ukr, firstname_ukr, patronymic_ukr = misc.split_name(
            row["name"].strip())

        # Transliterate name in Ukrainian to English using the transliteration
        # API
        lastname_eng, firstname_eng, patronymic_eng = api.transliterate_name(
            lastname_ukr, firstname_ukr, patronymic_ukr)

        # Generate username based on the transliterated name
        username = misc.generate_username(
            lastname_eng, firstname_eng, patronymic_eng)

        # Check if the generated username or email already exists
        # in the processed users list
        if duplicates.check_for_duplicate(
                username, email, processed_users):
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

        # If not a duplicate, write to the list of processed users
        processed_users.append({"username": username, "email": email})

        if not args.local_api:
            # Web API password generation
            password = pswrd_gen.generate_password_web_api()
        else:
            # Local password generation
            password = pswrd_gen.generate_password_local()

        # Write to main output file for Moodle bulk upload
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

        # Select correct salutation for email based on the first name
        salutation = misc.select_salutation(firstname_ukr)

        # Write to email output file for sending emails to students
        output_email_Writer.writerow(
            {
                "email": email,
                "salutation": salutation,
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

    misc.print_separator()

    # Write unique cohorts list to the output cohorts file
    for cohort in cohorts_temp:
        output_cohorts_Writer.writerow(
            {"name": cohort, "idnumber": cohort, "description": ""}
        )
        print(f"{cohort} - cohort record added")

    # Close all opened files
    for file in files:
        file.close()

    # Remove duplicates file if empty
    if duplicates.duplicates_file_empty(duplicates_csv_name):
        try:
            os.remove(duplicates_csv_name)
        except Exception as e:
            print("Error removing duplicates file:", e)
            exit(1)

    misc.print_separator()
    print("Done!")
    print(f"Processed {processed_rows} rows.")
    misc.print_separator()


if __name__ == "__main__":
    main()
