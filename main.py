from functions import *
clear_screen()
welcome()
name = ask_name("Wat is uw naam? ")
pokemon = get_random_pokemon(6)
player = create_new_player(name,pokemon)
show_pokemon(player)