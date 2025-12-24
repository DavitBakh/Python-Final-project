import random
from src.utils import SHIP_SIZES, BOARD_SIZE, SHIP_LAYOUT
from src.utils import validate_input, parse_input, is_valid_ship, get_ship_coords, render_occupied
from src.utils import save_ships, data_path

DIRECTIONS = ['u', 'd', 'l', 'r']

def get_input():
    isValid = False
    while not isValid:
        inp = input()
        isValid, message = validate_input(inp)

        if message:
            print(message)
    
    return inp

def collect_player_ships():
    remaining = SHIP_SIZES.copy()
    inputs = []
    occupied = set()

    print("Input format: yx size direction \n" \
		f"y: [A-J] x: [1-10] \n" \
		"direction is character from [u,d,l,r]")

    while sum(remaining.values()) > 0:
        inp = get_input()   
        size, x, y, direction = parse_input(inp)

        if remaining[size] == 0:
            print(f"All ships of size {size} is placed")
            continue

        coords = get_ship_coords(size, x, y, direction)
        if coords is None:
            print("Ship goes out of bounds, try again")
            continue

        if not is_valid_ship(coords, occupied):
            print("Ship overlaps or touches another ship, try again")
            continue

        inputs.append(coords)
        for c in coords:
            occupied.add(c)
        remaining[size] -= 1

        print(render_occupied(occupied))

    return inputs

def generate_player_ships():
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

def main(is_random=False):
    if is_random:
        ships = generate_player_ships()
    else:
        ships = collect_player_ships()
    save_ships(ships, data_path("player_ships.csv"))

if __name__ == "__main__":
    main()