import random
from utils import BOARD_SIZE, SHIP_LAYOUT, data_path, save_ships
from utils import get_ship_coords, is_valid_ship

DIRECTIONS = ['u', 'd', 'l', 'r']

def generate_bot_ships():
    occupied = set()
    ships = []
    for size in SHIP_LAYOUT:
        placed = False
        while not placed:
            x = random.randint(0, BOARD_SIZE - 1)
            y = random.randint(0, BOARD_SIZE - 1)
            direction = random.choice(DIRECTIONS)
            coords = get_ship_coords(size, x, y, direction)
            if (coords is None) or (not is_valid_ship(coords, occupied)):
                continue

            ships.append(coords)
            for c in coords:
                occupied.add(c)
            placed = True
    return ships

def main():
    ships = generate_bot_ships()
    save_ships(ships, data_path("bot_ships.csv"))


if __name__ == "__main__":
    main()