from cryptography.fernet import Fernet
from os.path import exists
import requests
import secrets
import webbrowser

"""Function to get token to access TODOIST API"""
def get_token():
    key = Fernet.generate_key()
    with open(".key.key", "wb") as key_file:
        key_file.write(key)

    client_id = input("Enter your client ID: ")
    client_secret = input("Enter your client secret: ")

    state1 = secrets.token_urlsafe(16)
    webbrowser.open('https://todoist.com/oauth/authorize?client_id={}&scope=data:read_write,data:delete&state={}'.format(client_id,state1))
    url_example=input("Enter the url you were redirected to: ")
    code = url_example.split('=')[1].split('&')[0]
    state2 = url_example.split('=')[2]

    if state1 == state2:
        res = requests.post('https://todoist.com/oauth/access_token', data={'client_id': client_id, 'client_secret': client_secret, 'code': code})
        token=(res.json())['access_token']
        fin=token.encode()
        f = Fernet(key)
        encrypted = f.encrypt(fin)
        secret = open('.token','wb')
        secret.write(encrypted)
        secret.close()
    else:
        print("Error: state1 != state2\nConnection compromised")

"""Verification of token file"""
def check_token():
    if exists(".token"):
        return
    else:
        get_token()

"""Token Decryption"""
def load_token():
    key = open(".key.key", "rb").read()
    f = Fernet(key)
    return f.decrypt(open(".token", "rb").read()).decode()

"""Main function"""
if '__main__' == __name__:
    get_token()
