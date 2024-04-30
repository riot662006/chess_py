class SquareException(Exception):
    pass


class Square:
    def __init__(self, x: int, y: int):
        if not Square.is_valid(x, y):
            raise SquareException(f"Invalid Square ({x}, {y})")

        self._x = x
        self._y = y

    @property
    def x(self):
        return self.x

    @property
    def y(self):
        return self.y

    @staticmethod
    def is_valid(x: int, y: int):
        if not isinstance(x, int) or not isinstance(y, int):
            return False

        if 0 <= x < 8 and 0 <= y < 8:
            return True

        return False