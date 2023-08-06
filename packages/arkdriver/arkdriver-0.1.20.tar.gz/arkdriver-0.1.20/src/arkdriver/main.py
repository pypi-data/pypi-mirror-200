from arkdriver.presentation.presentation import main as presentation
from arkdriver.driver import Driver
from arklibrary.admin import Admin
from time import sleep
import requests


def fetch_commands(interval=10, wait=5):
    while True:
        res = requests.get('http://loadingproductions.com/command')
        try:
            data = [c for c in res.json() if not c['executed']]
        except:
            print("Error: request to api crashed")
            data = []
        if len(data) == 0:
            sleep(wait)
            continue
        i = 0
        while i < len(data):
            yield [c['code'] for c in data[i:i+interval]]
            i += interval


def run(interval=10, wait=5):
    print("Sign into the server.")
    input("Press enter to continue...")
    print()

    print("Create your character and spawn without dying.")
    input("Press enter to continue...")
    print()

    password = input("What is the server ADMIN PASSWORD: ")
    while len(password) == 0:
        print("ERROR: The admin password must be longer than 0 characters.")
        password = input("What is the server's ADMIN PASSWORD: ")
    print()

    admin_id = input("What is the ADMIN specimen implant id: ")
    while len(admin_id) != 9 or not admin_id.isnumeric():
        print("ERROR: The specimen implant id must be length 9 and all numbers.")
        admin_id = input("What is the ADMIN specimen implant id: ")
    print()
    driver = Driver()
    admin = Admin(driver=driver, password=password, player_id=admin_id)
    for commands in fetch_commands(interval=interval, wait=wait):
        for command in commands:
            admin.command_list.append(command)
        admin.execute()


def main():
    print("[1] driver listening for server requests")
    print("[2] presentation")
    response = input("What would you like to run?")
    choices = ['1', '2']
    while response not in choices:
        print(f"ERROR: your response should be a choice of: {choices}")
        print("[1] driver listening for server requests")
        print("[2] presentation")
        response = input("What would you like to run?")

    if response == '1':
        run(interval=5)
    elif response == '2':
        presentation()


if __name__ == "__main__":
    main()