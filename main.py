from functions import *

def start_game():
    clear_screen()
    welcome()
    
    name = ask_name("Wat is uw naam? ")
    player = Player(name, get_random_pokemon(6), 20)
    trainers = load_trainers_from_json("trainers.json")

    playing = True
    while playing and any(not t.is_beaten for t in trainers):
        show_player_stats(player)
        show_all_trainers(trainers)
        
        chosen_name = input("\nKies een trainer om te vechten (of 'stop'): ")
        if chosen_name.lower() == 'stop': break
            
        selected_trainer = next((t for t in trainers if t.name.lower() == chosen_name.lower() and not t.is_beaten), None)
        
        if selected_trainer:
            victory = battle(player, selected_trainer)

            if victory:
                selected_trainer.is_beaten = True
                reward = get_money_reward(selected_trainer)
                player.money += reward
                print(f"Je hebt {color_text(f'${reward}', 'yellow')} gewonnen!")
                trainers = [t for t in trainers if not t.is_beaten] 
            else:
                print(color_text("Je hebt geen bruikbare Pokémon meer! Je hebt verloren.", "red"))
        else:
            print(color_text("Trainer niet gevonden of al verslagen.", "red"))

    print("\nBedankt voor het spelen!")

if __name__ == "__main__":
    start_game()