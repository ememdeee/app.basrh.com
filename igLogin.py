#login
def login_function():
    from instagrapi import Client
    from urllib.parse import unquote #for album reupload
    ACCOUNT_USERNAME="successmindset.sch"
    ACCOUNT_PASSWORD="Aizawanarummd218"

    cl = Client()
    cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)

    userName = "successmindset.sch"
    
    print ("Logged in!")
    return cl, userName

#login
def login_function2():
    from instagrapi import Client
    from urllib.parse import unquote #for album reupload
    ACCOUNT_USERNAME="imagine.autos"
    ACCOUNT_PASSWORD="muhammadmmd218"

    cl = Client()
    cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)
    
    userName = "imagine.autos"

    print ("Logged in-2!")
    return cl, userName