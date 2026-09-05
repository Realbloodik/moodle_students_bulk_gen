import csv


def check_for_duplicate(username, email, dicts_list):
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
        print("ERROR while checking duplicates file:", e)
        exit(1)
