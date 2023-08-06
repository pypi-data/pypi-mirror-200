from arkdriver.presentation.presentation import main as presentation
from arkclient import GameBotClient
from arklibrary.lib import Ini
from arkdriver import Admin
from pathlib import Path
from time import sleep

__testing__ = False


def run(interval=30):
    path = Path.cwd() / Path('config.ini')
    config = Ini(path)
    password = config['ADMIN']['password']
    host = config['ARK-SERVER']['host']
    port = config['ARK-SERVER']['port']
    admin = Admin(password=password)
    admin.enable_admin()
    admin.execute()

    if not __testing__:
        with GameBotClient(host=host, port=port, server_id=123) as bot:
            while bot.connected:
                data = bot.ping()
                if data:
                    if isinstance(data, list):
                        admin.command_list += data
                        admin.execute()
                sleep(interval)


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