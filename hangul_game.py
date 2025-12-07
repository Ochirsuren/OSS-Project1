# hangul_game.py
import pygame, random, sys, time

pygame.init()

# === CONFIG ===
GRID_SIZE = 5
CELL_SIZE = 120
TOP_OFFSET = 260
WIDTH, HEIGHT = CELL_SIZE * GRID_SIZE, CELL_SIZE * GRID_SIZE + TOP_OFFSET
FPS = 30
GAME_TIME = 60  # seconds


# === FONT ===
try:
    font = pygame.font.Font("C:/Windows/Fonts/malgun.ttf", 44)
    big_font = pygame.font.Font("C:/Windows/Fonts/malgun.ttf", 60)
except:
    font = pygame.font.SysFont("malgungothic", 44)
    big_font = pygame.font.SysFont("malgungothic", 60)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangul Grid Game")
clock = pygame.time.Clock()

# === Compatibility Jamo ===
CONSONANTS = ["ㄱ","ㄲ","ㄴ","ㄷ","ㄸ","ㄹ","ㅁ","ㅂ","ㅃ","ㅅ","ㅆ","ㅇ","ㅈ","ㅉ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"]
VOWELS     = [
    "ㅏ","ㅐ","ㅑ","ㅒ","ㅓ","ㅔ","ㅕ","ㅖ","ㅗ","ㅘ","ㅙ","ㅚ",
    "ㅛ","ㅜ","ㅝ","ㅞ","ㅟ","ㅠ","ㅡ","ㅢ","ㅣ"
]
POOL = CONSONANTS + VOWELS

# === Hangul decomposition ===
def decompose_hangul(syllable):
    code = ord(syllable)
    if code < 0xAC00 or code > 0xD7A3:
        return [syllable]

    base = code - 0xAC00
    cho  = base // 588
    jung = (base % 588) // 28
    jong = base % 28

    CHO = ["ㄱ","ㄲ","ㄴ","ㄷ","ㄸ","ㄹ","ㅁ","ㅂ","ㅃ","ㅅ","ㅆ","ㅇ","ㅈ","ㅉ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"]
    JUNG = [
        "ㅏ","ㅐ","ㅑ","ㅒ","ㅓ","ㅔ","ㅕ","ㅖ","ㅗ","ㅘ","ㅙ","ㅚ",
        "ㅛ","ㅜ","ㅝ","ㅞ","ㅟ","ㅠ","ㅡ","ㅢ","ㅣ"
    ]
    JONG = ["","ㄱ","ㄲ","ㄳ","ㄴ","ㄵ","ㄶ","ㄷ","ㄹ","ㄺ","ㄻ","ㄼ","ㄽ","ㄾ","ㄿ","ㅀ","ㅁ",
            "ㅂ","ㅄ","ㅅ","ㅆ","ㅇ","ㅈ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"]

    parts = [CHO[cho], JUNG[jung]]
    if JONG[jong] != "":
        parts.append(JONG[jong])
    return parts

# === Ensure components exist in board ===
def ensure_components(letters, target_parts):
    result = letters.copy()
    for p in target_parts:
        if p not in result:
            replace_i = random.randrange(len(result))
            result[replace_i] = p
    return result

# === Make new 5x5 board ===
def make_board_for_target(target_parts):
    letters = random.choices(POOL, k=GRID_SIZE*GRID_SIZE)
    letters = ensure_components(letters, target_parts)
    board = [letters[i*GRID_SIZE:(i+1)*GRID_SIZE] for i in range(GRID_SIZE)]
    return board

# === Drawing the grid and highlight glow ===
def draw_board(board, highlight=None, glow_color=None):
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE + TOP_OFFSET, CELL_SIZE, CELL_SIZE)

            # 기본 배경
            color = (235,235,235)

            # glow effect
            if highlight == (x,y) and glow_color is not None:
                color = glow_color

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0,0,0), rect, 2)

            letter = board[y][x]
            text = font.render(letter, True, (0,0,0))
            tx = rect.x + (CELL_SIZE - text.get_width()) // 2
            ty = rect.y + (CELL_SIZE - text.get_height()) // 2
            screen.blit(text, (tx, ty))

# === Korean praise messages ===
PRAISE = ["잘했어요!", "정답입니다!", "완벽해요!", "멋져요!", "좋아요!"]

def random_praise():
    return random.choice(PRAISE)

# === Word List ===
WORD_LIST = ["산","물","불","달","별","손","눈","밤","밥",
             "집","길","꽃","꿈","강","빛","차","안","열","힘","점"]

def random_word():
    return random.choice(WORD_LIST)

# === Main Game ===
def game():
    feedback_text = "잘했어요!"
    feedback_timer = pygame.time.get_ticks()


    target = random_word()
    parts = decompose_hangul(target)
    board = make_board_for_target(parts)

    index = 0
    score = 0
    highlight = None
    glow_color = None
    glow_timer = 0

    praise_text = ""
    praise_timer = 0

    start_ticks = pygame.time.get_ticks()
    running = True

    while running:
        dt = clock.tick(FPS)
        screen.fill((255,255,255))

        # Time
        elapsed = (pygame.time.get_ticks() - start_ticks) / 1000
        time_left = max(0, GAME_TIME - int(elapsed))
        if time_left <= 0:
            running = False

        # Glow timer reduce
        if glow_timer > 0:
            glow_timer -= dt
            if glow_timer <= 0:
                glow_color = None
                highlight = None

        # Praise timer reduce
        if praise_timer > 0:
            praise_timer -= dt
            if praise_timer <= 0:
                praise_text = ""

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()

                if my >= TOP_OFFSET:
                    x = mx // CELL_SIZE
                    y = (my - TOP_OFFSET) // CELL_SIZE

                    if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                        letter = board[y][x]
                        needed = parts[index]

                        if letter == needed:
                            # Correct click
                            highlight = (x, y)
                            glow_color = (100, 255, 120)  # green glow
                            glow_timer = 150  # ms

                            index += 1

                            # Completed word
                            if index >= len(parts):
                                score += 1
                                praise_text = random_praise()
                                praise_timer = 1000  # 1 sec

                                target = random_word()
                                parts = decompose_hangul(target)
                                board = make_board_for_target(parts)
                                index = 0

                        else:
                            # Wrong click
                            highlight = (x, y)
                            glow_color = (255, 100, 100)  # red glow
                            glow_timer = 250

                            index = 0

        # UI
        title = font.render("한글 조합 게임", True, (0,0,0))
        screen.blit(title, (20, 12))

        word_text = font.render(f"제시어: {target}", True, (0,80,200))
        screen.blit(word_text, (20, 60))

        score_text = font.render(f"점수: {score}", True, (0,0,0))
        screen.blit(score_text, (WIDTH - 200, 12))

        time_text = font.render(f"남은시간: {time_left}s", True, (200,0,0))
        screen.blit(time_text, (WIDTH - 260, 60))


        # Praise display
        if praise_text:
            t = big_font.render(praise_text, True, (20,150,20))
            screen.blit(t, (WIDTH//2 - t.get_width()//2, 150))

        draw_board(board, highlight, glow_color)
        pygame.display.flip()

    # End screen
    screen.fill((255,255,255))
    end_text = font.render(f"게임 종료! 점수: {score}", True, (0,0,0))
    screen.blit(end_text, (WIDTH//2 - end_text.get_width()//2, HEIGHT//2))
    pygame.display.flip()
    pygame.time.wait(2500)


if __name__ == "__main__":
    game()