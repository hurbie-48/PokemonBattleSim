from functions import *

clear_screen()
randomPokemon = getRandomPokemon()
number = askNumber("Please enter the amount of players: ")
for i in range(number):
    name = askName(f"Please enter the name for player #{i+1}: ")
    player_id = addNewPlayer(name)
    givePokemonToPlayer(player_id, 6)

showAllPlayers()