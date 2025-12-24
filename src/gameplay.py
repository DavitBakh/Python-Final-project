import time

from src.utils import BOARD_SIZE, format_coord_to_print, data_path
from src.utils import load_ships, build_board, reset_game_state
from src.utils import print_boards, prompt_player_move, apply_shot, all_sunk
from src.utils import record_state
from src.bot_ai import BotAI



def play():
    player_ships = load_ships(data_path("player_ships.csv"))
    bot_ships = load_ships(data_path("bot_ships.csv"))
    player_board = build_board(player_ships, show_ships=True)
    bot_board = build_board(bot_ships, show_ships=False)
    bot_ai = BotAI()
    game_state_path = data_path("game_state.csv")
    reset_game_state(game_state_path)

    turn = 1
    print("Starting Battleship!")
    print_boards(player_board, bot_board)

    while True:
        player_move = prompt_player_move(bot_board)
        player_result = apply_shot(bot_board, player_move)
        print(f"You fired at {format_coord_to_print(player_move)} -> {player_result}")
        print_boards(player_board, bot_board)
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
            bot_move = bot_ai.choose_move(player_board)
            bot_result = apply_shot(player_board, bot_move)
            bot_ai.record_result(bot_move, bot_result)

            print(f"Bot fired at {format_coord_to_print(bot_move)} -> {bot_result}")
            print_boards(player_board, bot_board)
            record_state(
                game_state_path,
                turn,
                None,
                "",
                bot_move,
                bot_result,
                player_board,
                bot_board,
            )
            turn += 1
            if all_sunk(player_board):
                print("Bot wins! Your fleet is sunk.")
                return
            
            if bot_result not in ("hit", "sunk"):
                break
            time.sleep(2)

if __name__ == "__main__":
    play()