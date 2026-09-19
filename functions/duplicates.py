import functions.moodle as moodle


def check_for_duplicate(email, dicts_list, moodle_rest):
    for user_dict in dicts_list:
        if user_dict.get("email") == email:
            return True, user_dict.get("username", True)

    if moodle_rest:
        moodle_username = moodle.check_if_user_exists(email)
        return bool(moodle_username), moodle_username

    return False, None
