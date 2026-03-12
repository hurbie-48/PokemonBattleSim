from functions import *
clear_screen()
welcome()
name = ask_name("Wat is uw naam? ")
pokemon = get_random_pokemon(6)
player = create_new_player(name,pokemon, 20)
show_player_stats(player)
pokemon = get_random_pokemon(6)
trainers = []
trainer_kai = create_new_trainer("Kai", "Trainer Kai is onvoorspelbaar en kan verrassend aanvallen. Een echte test van je vaardigheden.", pokemon, 1200)
trainers.append(trainer_kai)
show_all_trainers(trainers)