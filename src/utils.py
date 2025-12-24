import csv
from pathlib import Path
from colorama import init, Fore, Style
init()

BOARD_SIZE = 10

SIZE_1_COUNT = 4
SIZE_2_COUNT = 3
SIZE_3_COUNT = 2
SIZE_4_COUNT = 1

SHIP_SIZES = {
    1: SIZE_1_COUNT,
    2: SIZE_2_COUNT,
    3: SIZE_3_COUNT,
    4: SIZE_4_COUNT,
}

SHIP_LAYOUT = [size for size in (4, 3, 2, 1) for _ in range(SHIP_SIZES[size])]

PLAYER_COLOR = Fore.GREEN
BOT_COLOR = Fore.BLUE
DEFAULT_COLOR = Style.RESET_ALL

def parse_input(inp: str):
    parts = inp.split()
    coordinate, size, orientation = parts

    size = int(size)
    x = int(coordinate[1:]) - 1
    y = ord(coordinate[0].upper()) - ord('A')
    return size, x, y, orientation

def validate_input(inp: str) -> bool:
    """Validate user input for ship placement.

    Args:
        inp (str): The input string to validate."""
    
    message = None
    
    parts = inp.split()
    if len(parts) != 3:
        message = "Input must consist of size, coordinate, and orientation."
        return False, message

    coordinate, size, orientation = parts
    size = int(size)
    coordinate = coordinate.upper()

    if size not in SHIP_SIZES.keys():
        message = "Invalid ship size."
        return False, message

    if  not coordinate[1:].isdigit():
        message = "Invalid coordinate format."
        return False, message
    
    if (coordinate[0] not in 'ABCDEFGHIJ' ) or (int(coordinate[1:]) <= 0 or int(coordinate[1:]) > BOARD_SIZE):
        message = "Coordinate out of board range."
        return False, message

    if orientation not in 'udrl':
        message = "Invalid orientation. Use 'u', 'd', 'l', or 'r'."
        return False, message

    return True, message


def get_ship_coords(size: int, x: int, y: int, direction: str):

    dx = dy = 0
    if direction == "u":
        dy = -1
    elif direction == "d":
        dy = 1
    elif direction == "r":
        dx = 1
    elif direction == "l":
        dx = -1

        
    coords = []
    for i in range(size):
        cx = x  + dx * i
        cy = y  + dy * i

        if cx < 0 or cx >= BOARD_SIZE or cy < 0 or cy >= BOARD_SIZE:
            return None

        coords.append((cx, cy))
    return coords


def is_valid_ship(coords, occupied) -> bool:
    for cx, cy in coords:
        for nx in range(cx - 1, cx + 2):
            for ny in range(cy - 1, cy + 2):
                if (nx, ny) in occupied:
                    return False
    return True

def empty_board(fill="."):
    return [[fill for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


def render_board(board):
    top = "  " + " ".join(str(i+1) for i in range(BOARD_SIZE))
    lines = [top]
    for y, row in enumerate(board):
        lines.append(f"{chr(ord('A') + y)} " + " ".join(row))
    return "\n".join(lines)

def render_occupied(occupied):
    board = empty_board(".")
    for x, y in occupied:
        if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
            board[y][x] = "O"
    return render_board(board)

def board_to_string(board):
    return "".join("".join(row) for row in board)

def data_path(filename):
    base = Path(__file__).resolve().parents[1]
    return base / "data" / filename

def save_ships(ships, path):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["size", "coords"])
        for coords in ships:
            size = len(coords)
            coords_str = " ".join(f"({x};{y})" for x, y in coords)
            writer.writerow([size, coords_str])

def load_ships(path):
    ships = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw = row["coords"]
            coords = []
            for pair in raw.split():
                cleaned = pair.strip("()")
                if not cleaned:
                    continue
                x_str, y_str = cleaned.split(";")
                coords.append((int(x_str), int(y_str)))
            ships.append(coords)
    return ships


def build_board(ships, show_ships=False):
    grid = empty_board(".")
    ship_sets = [set(ship) for ship in ships]
    coord_to_ship = {}
    for idx, ship in enumerate(ship_sets):
        for coord in ship:
            coord_to_ship[coord] = idx
            if show_ships:
                x, y = coord
                grid[y][x] = "O"
    return {
        "ships": ship_sets,
        "coord_to_ship": coord_to_ship,
        "hits": [set() for _ in ships],
        "sunk": [False for _ in ships],
        "grid": grid,
        "shots": set(),
    }

def reset_game_state(path):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "turn",
                "player_move",
                "player_result",
                "bot_move",
                "bot_result",
                "player_board",
                "bot_board",
            ]
        )

def board_snapshot(board):
    return board_to_string(board["grid"])

def board_display(board):
    return render_board(board["grid"])

def print_boards(player_board, bot_board):
    print_player_board(player_board)
    print()
    print_bot_board(bot_board)


def print_player_board(player_board):
    print(PLAYER_COLOR + "Your board:" + DEFAULT_COLOR)
    print(PLAYER_COLOR + board_display(player_board) + DEFAULT_COLOR)


def print_bot_board(bot_board):
    print(BOT_COLOR + "Bot board:" + DEFAULT_COLOR)
    print(BOT_COLOR + board_display(bot_board) + DEFAULT_COLOR)


def prompt_player_move(bot_board):
    while True:
        inp = input("Enter target as 'yx' ([A-J][1-10]): ").strip()
        
        if inp[0].upper() not in 'ABCDEFGHIJ' or not inp[1:].isdigit():
            print("Invalid format, try again")
            continue
            
        x, y = int(inp[1:]) - 1, ord(inp[0].upper()) - ord('A')
        if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE):
            print("Coordinates out of bounds, try again")
            continue
        if (x, y) in bot_board["shots"]:
            print("You already tried that cell, pick another")
            continue
        return (x, y)
    
def format_coord(coord):
    if coord is None:
        return ""
    x, y = coord
    return f"{x},{y}"

def format_coord_to_print(coord):
    if coord is None:
        return ""
    x, y = coord
    return f"{chr(y + ord('A'))}{x + 1}"


def record_state(
    path,
    turn,
    player_move,
    player_result,
    bot_move,
    bot_result,
    player_board,
    bot_board,
):
    with open(path, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                turn,
                format_coord(player_move),
                player_result,
                format_coord(bot_move),
                bot_result,
                board_snapshot(player_board),
                board_snapshot(bot_board),
            ]
        )

def add_surrounding_misses(board, ship_cells):
    for cx, cy in ship_cells:
        for nx in range(cx - 1, cx + 2):
            for ny in range(cy - 1, cy + 2):
                if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                    if board["grid"][ny][nx] in ("H", "X"):
                        continue
                    board["grid"][ny][nx] = "M"
                    board["shots"].add((nx, ny))

def apply_shot(board, coord):
    if coord in board["shots"]:
        return "repeat"
    board["shots"].add(coord)
    x, y = coord
    if coord in board["coord_to_ship"]:
        ship_idx = board["coord_to_ship"][coord]
        board["hits"][ship_idx].add(coord)
        if len(board["hits"][ship_idx]) == len(board["ships"][ship_idx]):
            board["sunk"][ship_idx] = True
            for cx, cy in board["ships"][ship_idx]:
                board["grid"][cy][cx] = "X"
                board["shots"].add((cx, cy))
            add_surrounding_misses(board, board["ships"][ship_idx])
            return "sunk"
        board["grid"][y][x] = "H"
        return "hit"
    board["grid"][y][x] = "M"
    return "miss"

def all_sunk(board):
    return all(board["sunk"])

def available_targets(board):
    coords = []
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if (x, y) not in board["shots"]:
                coords.append((x, y))
    return coords






