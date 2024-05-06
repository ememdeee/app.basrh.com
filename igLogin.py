#login
def login_function():
    from instagrapi import Client
    from urllib.parse import unquote #for album reupload
    ACCOUNT_USERNAME="successmindset.sch"
    ACCOUNT_PASSWORD="Aizawanarummd218"

    cl = Client()
    cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)

    # user_id = cl.user_id_from_username(ACCOUNT_USERNAME)
    # medias = cl.user_medias(user_id, 20)
    print ("Logged in!")
    return cl