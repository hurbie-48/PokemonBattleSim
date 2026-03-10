from functions import *
from unittest.mock import patch

clearScreen()
showAscii()
if not jsonExists():
    name = askName(f"What is your name?: ")
    player_id = addNewPlayer(name)
    givePokemonToPlayer(player_id, 6)
    save_to_json()
showTrainers()
askTrainer("Choose a trainer to battle against (type the name): ")