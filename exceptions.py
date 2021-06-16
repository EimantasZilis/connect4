class GameOver(Exception):
    """
    An exception to indicate that the game has been completed.
    This can only be achieved if the game has been won by one
    of the players or if there is a draw.
    """


class GameError(Exception):
    """An exception to indicate that there was an error in the game"""
