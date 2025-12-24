Battleship Game

-- How input works --

To place ships, the user enters a line in the format "coordinate size direction"
Coordinate format "A1" ([A-J][1-10]) direction one of the this options ('u' (up), 'd' (down), 'r' (right), 'l' (left))

-- How placement is validated --

Each ship has his own coordinates, for all coordinates we check to be in board range, and not to touch each other
If user inputs invalid ship we ask him to re-enter

-- How game state updated and displayed --

After move (player or bot) we calculate it hits, sunk miss or incorrect, then we update the boards of both players and print again

-- Design decisions and trade-offs --

You can see all the design decisions during the game.