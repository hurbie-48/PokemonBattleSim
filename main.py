from functions import *

load_from_json()
clear_screen()
welcome()
if not jsonExists():
    number = askNumber("How many players would you like to add? (1-10): ")

    for i in range(number):
        name = askName(f"Please enter the name for player #{i+1}: ")
        player_id = addNewPlayer(name)
        givePokemonToPlayer(player_id, 6)
        save_to_json()
clear_screen()
showAllPlayers()