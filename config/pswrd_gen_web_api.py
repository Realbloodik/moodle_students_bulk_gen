from dotenv import load_dotenv
import os


load_dotenv()

# Password generator Web API settings
length = "12"
uppercase = "true"
lowercase = "true"
numbers = "true"
special = "true"
api_url = "https://api-ninjas.com/api"
api_gen_url = (
    "https://api.api-ninjas.com/v1/passwordgenerator"
    f"?length={length}"
    f"&uppercase={uppercase}"
    f"&lowercase={lowercase}"
    f"&numbers={numbers}"
    f"&special={special}"
)
# To use the password generator Web API, you need to get your own API key from
# https://api-ninjas.com/ and write it in the "password_api_key.txt" file
PASSWORD_GEN_WEB_API_TOKEN = os.getenv("PASSWORD_GEN_WEB_API_TOKEN")


def check_for_pswrd_gen_web_api_token():
    if not PASSWORD_GEN_WEB_API_TOKEN:
        raise ValueError(
            "ERROR: --local_api for password gen is on, but"
            "PASSWORD_GEN_WEB_API_TOKEN is not found in .env file!"
        )
