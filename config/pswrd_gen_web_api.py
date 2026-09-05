import functions.api as api


# Password generator Web API settings
length = "12"
uppercase = "true"
lowercase = "true"
numbers = "true"
special = "true"
api_url = "https://api-ninjas.com/"
api_url = (
    "https://api.api-ninjas.com/v1/passwordgenerator"
    f"?length={length}"
    f"&uppercase={uppercase}"
    f"&lowercase={lowercase}"
    f"&numbers={numbers}"
    f"&special={special}"
)
# To use the password generator Web API, you need to get your own API key from
# https://api-ninjas.com/ and write it in the "password_api_key.txt" file
api_key = api.read_password_generator_api_key()
