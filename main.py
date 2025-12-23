import sys
from pathlib import Path
from src import bot_generation
from src import gameplay
from src import ship_input
from src.utils import data_path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.append(str(SRC))


def chose_layout_format(path: Path):
    if not path.exists():
        return
    
    while True:
        choice = input("Use existing player ship layout or generate randomly or insert manually? [new/rand]: ").strip().lower()
        if choice == "new":
            ship_input.main(is_random=False)
            break
        if choice == "rand":
            ship_input.main(is_random=True)
            break
        else:
            print("Invalid choice, using existing layout.")


def main():
    player_path = data_path("player_ships.csv")
    chose_layout_format(player_path)

    bot_generation.main()
    gameplay.play()


if __name__ == "__main__":
    main()
