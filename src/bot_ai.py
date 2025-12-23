import random
from src.utils import BOARD_SIZE, available_targets

class BotAI:
    def __init__(self):
        self.active_hits = []
        self.axis = None

    def choose_move(self, target_board):
        if self.axis and self.active_hits:
            move = self._axis_move(target_board)
            if move:
                return move
        if self.active_hits:
            move = self._neighbor_move(target_board)
            if move:
                return move
        return self._random_move(target_board)

    def record_result(self, coord, result):
        if result in ("hit", "sunk") and coord not in self.active_hits:
            self.active_hits.append(coord)
        if result == "sunk":
            self.active_hits.clear()
            self.axis = None
            return
        if len(self.active_hits) >= 2 and self.axis is None:
            x0, y0 = self.active_hits[0]
            x1, y1 = self.active_hits[1]
            if x0 == x1:
                self.axis = (0, 1)
            elif y0 == y1:
                self.axis = (1, 0)

    def _neighbor_move(self, target_board):
        candidates = []
        for hx, hy in self.active_hits:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = hx + dx, hy + dy
                if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                    if (nx, ny) not in target_board["shots"]:
                        candidates.append((nx, ny))
        if not candidates:
            return None
        return random.choice(candidates)

    def _axis_move(self, target_board):
        if not self.axis:
            return None
        dx, dy = self.axis
        if dx != 0:
            hits_sorted = sorted(self.active_hits, key=lambda c: c[0])
        else:
            hits_sorted = sorted(self.active_hits, key=lambda c: c[1])
        first = hits_sorted[0]
        last = hits_sorted[-1]
        forward = (last[0] + dx, last[1] + dy)
        backward = (first[0] - dx, first[1] - dy)
        for candidate in (forward, backward):
            cx, cy = candidate
            if 0 <= cx < BOARD_SIZE and 0 <= cy < BOARD_SIZE:
                if (cx, cy) not in target_board["shots"]:
                    return candidate
        return None
    

    def _random_move(self, target_board):
        options = available_targets(target_board)
        return random.choice(options)