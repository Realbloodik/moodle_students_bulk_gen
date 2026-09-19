import config.settings as cfg
import requests


def check_if_user_exists(email):
    payload = {
        "wstoken": cfg.MOODLE_API_TOKEN,
        "wsfunction": "core_user_get_users_by_field",
        "field": "email",
        "values[0]": email,
        "moodlewsrestformat": "json"
    }

    res = requests.post(cfg.MOODLE_REST_URL, data=payload).json()

    if isinstance(res, list) and res:
        return res[0]["username"]

    return None


def check_if_cohort_exists(cohort):
    payload = {
        "wstoken": cfg.MOODLE_API_TOKEN,
        "wsfunction": "core_cohort_search_cohorts",
        "query": cohort,
        "context[contextid]": 1,
        "moodlewsrestformat": "json"
    }

    res = requests.post(cfg.MOODLE_REST_URL, data=payload).json()

    return bool(res.get("cohorts"))
