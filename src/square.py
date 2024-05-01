class SquareException(Exception):
    pass


class Square:
    def __init__(self, x: int, y: int):
        if not Square.is_valid(x, y):
            raise SquareException(f"Invalid Square ({x}, {y})")

        self._x = x
        self._y = y

    def __repr__(self):
        return f"Square('{str(self)}')"

    def __str__(self):
        return "abcdefgh"[self._x] + str(self._y + 1)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise SquareException("Cannot equate type of " + str(self.__class__) + " with " + str(other.__class__))

        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        if not isinstance(other, tuple):
            raise SquareException("Cannot add type of " + str(other.__class__) + " to " + str(self.__class__))

        if len(other) != 2 or not isinstance(other[0], int) or not isinstance(other[1], int):
            raise SquareException("Tuple must have 2 integers only")

        return Square(self.x + other[0], self.y + other[1])

    def __sub__(self, other):
        if isinstance(other, tuple):
            other = Square(*other)

        if isinstance(other, self.__class__):
            return self.x - other.x, self.y - other.y

        raise SquareException("Cannot subtract type " + str(other.__class__) + " from " + str(self.__class__))

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def copy(self):
        return Square(self._x, self._y)

    @staticmethod
    def is_valid(x: int, y: int):
        if not isinstance(x, int) or not isinstance(y, int):
            return False

        if 0 <= x < 8 and 0 <= y < 8:
            return True

        return False

    def to_board_str_index(self):
        return self.y * 8 + self.x
