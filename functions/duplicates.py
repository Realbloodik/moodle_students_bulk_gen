import csv


def check_for_duplicate(email, dicts_list):
    row = 1
    for dict in dicts_list:
        row += 1
        if dict["email"] == email:
            return True, row
    return False, 0


def duplicates_file_empty(file):
    try:
        with open(file, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
            if len(rows) <= 1:
                return True
            else:
                return False
    except FileNotFoundError:
        return True
    except Exception as e:
        print("ERROR while checking duplicates file:", e)
        exit(1)
