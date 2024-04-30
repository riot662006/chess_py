import pygame
import sys

_temp = {}


def load_image(filename):
    if filename in _temp:
        return _temp[filename]

    try:
        image = pygame.image.load(filename)
    except pygame.error as e:
        print("Error loading image:", filename)
        raise SystemExit(e)

    _temp[filename] = image
    return image


def load_pieces(filename):
    all_pieces = pygame.image.load(filename).convert_alpha()
    pieces: dict[str, dict[str, pygame.Surface | pygame.SurfaceType]] = {}

    dimensions = pygame.Rect((0, 0), all_pieces.get_rect().scale_by(1 / 6, 1 / 2).size)

    for i, side in enumerate(["white", "black"]):
        pieces[side] = {}
        for j, piece in enumerate(["king", "queen", "bishop", "knight", "rook", "pawn"]):
            pieces[side][piece] = pygame.Surface((333, 333), flags=pygame.SRCALPHA)

            pieces[side][piece].blit(all_pieces,
                                     (0, 0),
                                     dimensions.move(j * dimensions.width, i * dimensions.height)
                                     )

    return pieces
