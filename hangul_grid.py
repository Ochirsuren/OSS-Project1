# hangul_grid.py

import pygame, random, sys
pygame.init()

GRID_SIZE = 5
CELL_SIZE = 100
TOP_OFFSET = 160
WIDTH, HEIGHT = CELL_SIZE * GRID_SIZE, CELL_SIZE * GRID_SIZE + TOP_OFFSET
FPS = 30

try:
    font = pygame.font.Font("C:/Windows/Fonts/malgun.ttf", 44)
except:
    font = pygame.font.SysFont("malgungothic", 44)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangul Grid Test")
clock = pygame.time.Clock()

CONSONANTS = ["ㄱ","ㄲ","ㄴ","ㄷ","ㄸ","ㄹ","ㅁ","ㅂ","ㅃ","ㅅ","ㅆ","ㅇ","ㅈ","ㅉ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"]
VOWELS     = ["ㅏ","ㅐ","ㅑ","ㅒ","ㅓ","ㅔ","ㅕ","ㅖ","ㅗ","ㅘ","ㅙ","ㅚ","ㅛ","ㅜ","ㅝ","ㅞ","ㅟ","ㅠ","ㅡ","ㅢ","ㅣ"]
POOL = CONSONANTS + VOWELS

def make_board_random():
    # simple uniform choices (letters may repeat)
    letters = random.choices(POOL, k=GRID_SIZE*GRID_SIZE)
    board = [letters[i*GRID_SIZE:(i+1)*GRID_SIZE] for i in range(GRID_SIZE)]
    return board

def draw_board(board, highlight=None):
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE + TOP_OFFSET, CELL_SIZE, CELL_SIZE)
            color = (230,230,230)
            if highlight == (x,y):
                color = (170,210,255)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0,0,0), rect, 2)
            letter = board[y][x]
            text = font.render(letter, True, (0,0,0))
            tx = rect.x + (CELL_SIZE - text.get_width())//2
            ty = rect.y + (CELL_SIZE - text.get_height())//2
            screen.blit(text, (tx, ty))

def main():
    board = make_board_random()
    highlight = None
    running = True
    while running:
        dt = clock.tick(FPS)
        screen.fill((255,255,255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                print("CLICK POSITION:", mx, my)
                if my >= TOP_OFFSET:
                    x = mx // CELL_SIZE
                    y = (my - TOP_OFFSET) // CELL_SIZE
                    if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                        print("CLICKED CELL:", x, y, "LETTER:", board[y][x])
                        highlight = (x,y)

        draw_board(board, highlight)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
