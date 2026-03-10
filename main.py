from functions import *

load_from_json()
clearScreen()
welcome()
if not jsonExists():
    name = askName(f"What is your name?: ")
    player_id = addNewPlayer(name)
    givePokemonToPlayer(player_id, 6)
    save_to_json()
clearScreen()
showAllPlayers()