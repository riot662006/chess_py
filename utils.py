import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREY = (100, 100, 100)

START_POS = {
    "a1": "rook_w", "b1": "knight_w", "c1": "bishop_w",
    "d1": "queen_w", "e1": "king_w",
    "f1": "bishop_w", "g1": "knight_w", "h1": "rook_w",

    "a2": "pawn_w", "b2": "pawn_w", "c2": "pawn_w",
    "d2": "pawn_w", "e2": "pawn_w",
    "f2": "pawn_w", "g2": "pawn_w", "h2": "pawn_w",

    "a7": "pawn_b", "b7": "pawn_b", "c7": "pawn_b",
    "d7": "pawn_b", "e7": "pawn_b",
    "f7": "pawn_b", "g7": "pawn_b", "h7": "pawn_b",

    "a8": "rook_b", "b8": "knight_b", "c8": "bishop_b",
    "d8": "queen_b", "e8": "king_b",
    "f8": "bishop_b", "g8": "knight_b", "h8": "rook_b",

}

game_resources = None

resize = pygame.transform.smoothscale


def create_outline_surface(surface: pygame.Surface | pygame.SurfaceType, width):
    mask = pygame.mask.from_surface(surface)
    outline = mask.outline()

    outline_surface = pygame.Surface(surface.get_size(), flags=pygame.SRCALPHA)
    outline_surface.blit(mask.to_surface(unsetcolor=None, unsetsurface=None, setcolor=BLACK), (0, 0))

    for points in outline:
        pygame.draw.circle(outline_surface, BLACK, points, width)

    return outline_surface


def load_resources():
    global game_resources
    if game_resources is not None:
        return game_resources
    resources = {
        "board_texture": pygame.transform.scale2x(pygame.image.load("images/texture.jpg").convert_alpha()),
        "board_outline": pygame.image.load("images/board.png").convert_alpha(),
    }

    all_piece_img = pygame.transform.smoothscale(pygame.image.load("images/piecesClean.png").convert_alpha(), (1800, 600))
    piece_names = ["king", "queen", "bishop", "knight", "rook", "pawn"]
    sides = ["w", "b"]

    piece_imgs = {}

    for y in range(2):
        for x in range(6):
            piece = pygame.Surface((300, 300), flags=pygame.SRCALPHA)
            piece.blit(all_piece_img, (0, 0), (x * 300, y * 300, 300, 300))

            piece_mask_surface = create_outline_surface(piece, 18)

            piece_imgs[piece_names[x] + "_" + sides[y]] = piece
            piece_imgs[piece_names[x] + "_" + sides[y] + "_out"] = piece_mask_surface

    resources["pieces"] = piece_imgs
    move_img = pygame.Surface((300, 300), flags=pygame.SRCALPHA)
    pygame.draw.circle(move_img, RED, (150, 150), 30, 10)
    move_outline = create_outline_surface(move_img, 18)

    resources["pieces"]["move"] = move_img
    resources["pieces"]["move_out"] = move_outline

    game_resources = resources
    return resources
