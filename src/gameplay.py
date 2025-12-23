import csv
import random
import time

from src.utils import BOARD_SIZE, board_to_string, data_path, empty_board
from src.utils import load_ships, render_board, build_board, reset_game_state
from src.utils import print_boards, prompt_player_move, apply_shot, all_sunk
from src.utils import format_coord, record_state, print_bot_board, print_player_board



def play():
    player_ships = load_ships(data_path("player_ships.csv"))
    bot_ships = load_ships(data_path("bot_ships.csv"))
    player_board = build_board(player_ships, show_ships=True)
    bot_board = build_board(bot_ships, show_ships=False)
    
    game_state_path = data_path("game_state.csv")
    reset_game_state(game_state_path)

    turn = 1
    print("Starting Battleship!")
    print_boards(player_board, bot_board)

    while True:
        player_move = prompt_player_move(bot_board)
        player_result = apply_shot(bot_board, player_move)
        print(f"You fired at {format_coord(player_move)} -> {player_result}")
        print_bot_board(bot_board)
        record_state(
            game_state_path,
            turn,
            player_move,
            player_result,
            None,
            "",
            player_board,
            bot_board,
        )
        turn += 1

        if all_sunk(bot_board):
            print("You win! All bot ships destroyed.")
            break

        if player_result in ("hit", "sunk"):
            continue

        while True:
            #TODO: Implement bot logic
            
            print_player_board(player_board)
            record_state(
                game_state_path,
                turn,
                None,
                "",
                None, #TODO bot move
                None, #TODO bot result
                player_board,
                bot_board,
            )
            turn += 1
            if all_sunk(player_board):
                print("Bot wins! Your fleet is sunk.")
                return
            
            time.sleep(1)

if __name__ == "__main__":
    play()