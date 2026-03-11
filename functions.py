import os

def clear_screen() -> None:
    # Als iemand op windows zit gebruik cls, en anders clear
    os.system("cls") if os.name == "nt" else os.system("clear")

def welcome() -> None:
    # print welkom!
    print("\nWelkom!")

def is_name_valid(name: str) -> bool:
    # Check of de naam minimaal 2 en maximaal 15 karakters heeft.
    if 2 < len(name) < 16:
        for karakter in name:
            if karakter.isdigit():
                return False
        return True
    else:
        return False

def ask_name(msg: str) -> str:
    name = input(msg)
    while not is_name_valid(name):
        print("Vul a.u.b een naam in van minimaal 2 karakters, maximaal 15 karakters en zonder cijfers.")
        name = input(msg)
    return name
