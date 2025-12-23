import csv
from pathlib import Path

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
            board[y][x] = "◻"
    return render_board(board)

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