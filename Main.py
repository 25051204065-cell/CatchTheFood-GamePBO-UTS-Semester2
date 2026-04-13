import pygame
import random

pygame.init()
pygame.mixer.init()

# layar
WIDTH = 600
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Food")

BG_COLOR = (135, 206, 235)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

font = pygame.font.SysFont(None, 30)
big_font = pygame.font.SysFont(None, 50)

clock = pygame.time.Clock()

path = "./"

# ================= LOAD IMAGE =================
def load_img(name, size):
    img = pygame.image.load(path + name).convert_alpha()
    img = pygame.transform.scale(img, size)
    return img

player_img = load_img("karakter.png", (80, 80))
apple_img = load_img("objek1.png", (60, 60))
burger_img = load_img("objek2.png", (60, 60))
coin_img = load_img("koin.png", (40, 40))
heart_img = load_img("live.png", (45, 45))

pygame.mixer.music.load(path + "songingame.wav")
pygame.mixer.music.set_volume(0.5)

foods = {
    "apple": apple_img,
    "burger": burger_img,
    "coin": coin_img
}

# ================= HIGH SCORE =================
def load_highscore():
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read())
    except:
        return 0

def save_highscore(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))

highscore = load_highscore()

# ================= GAME RESET =================
def reset_game():
    pygame.mixer.music.play(-1)  # loop terus
    t = random.choice(list(foods.keys()))
    return {
        "player_x": WIDTH//2,
        "food_x": random.randint(0, WIDTH-30),
        "food_y": 0,
        "food_type": t,
        "food_img": foods[t],
        "score": 0,
        "lives": 3,
        "speed": 5,
        "level": 1
    }

game = reset_game()

player_y = HEIGHT - 90
player_speed = 15
running = True
game_over = False

# ================= BACKGROUND =================
bg_y1 = 0
bg_y2 = -HEIGHT
bg_speed = 0

# ================= CLOUD =================
clouds = []
for i in range(5):
    clouds.append([random.randint(0, WIDTH), random.randint(0, HEIGHT//2), random.uniform(0.5, 2)])

# ================= LOOP =================
while running:
    # ===== background animasi =====
    bg_y1 += bg_speed
    bg_y2 += bg_speed

    if bg_y1 >= HEIGHT:
        bg_y1 = -HEIGHT
    if bg_y2 >= HEIGHT:
        bg_y2 = -HEIGHT

    screen.fill(BG_COLOR)

    # ===== awan =====
    for cloud in clouds:
        cloud[1] += cloud[2]
        if cloud[1] > HEIGHT:
            cloud[0] = random.randint(0, WIDTH)
            cloud[1] = -50

        pygame.draw.ellipse(screen, (255,255,255), (cloud[0], cloud[1], 60, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game = reset_game()
                game_over = False

    keys = pygame.key.get_pressed()

    if not game_over:
        if keys[pygame.K_LEFT]:
            game["player_x"] -= player_speed
        if keys[pygame.K_RIGHT]:
            game["player_x"] += player_speed

        game["player_x"] = max(0, min(WIDTH-80, game["player_x"]))

        # ===== gerak objek =====
        game["food_y"] += game["speed"] + game["level"] * 0.0

        # ===== collision =====
        if (game["food_y"]+30 >= player_y and
            game["food_x"]+30 >= game["player_x"] and
            game["food_x"] <= game["player_x"]+80):

            if game["food_type"] == "koin":
                game["score"] += 3
            elif game["food_type"] == "objek1":
                game["lives"] -= 1
            else:
                game["score"] += 1

            game["speed"] += 0.2

            t = random.choice(list(foods.keys()))
            game["food_type"] = t
            game["food_img"] = foods[t]
            game["food_x"] = random.randint(0, WIDTH-30)
            game["food_y"] = 0

        # ===== miss =====
        if game["food_y"] > HEIGHT:
            game["lives"] -= 1

            t = random.choice(list(foods.keys()))
            game["food_type"] = t
            game["food_img"] = foods[t]
            game["food_x"] = random.randint(0, WIDTH-30)
            game["food_y"] = 0

        # ===== level up =====
        if game["score"] >= game["level"] * 10:
            game["level"] += 1
            game["speed"] += 1

        # ===== gambar =====
        screen.blit(player_img, (game["player_x"], player_y))
        screen.blit(game["food_img"], (game["food_x"], game["food_y"]))

        # ===== UI =====
        screen.blit(font.render(f"Score: {game['score']}", True, BLACK), (10,10))
        screen.blit(font.render(f"Level: {game['level']}", True, BLACK), (480,10))
        screen.blit(font.render(f"Highscore: {highscore}", True, BLACK), (10,70))

        for i in range(game["lives"]):
            screen.blit(heart_img, (10+i*30, 40))

        # ===== game over =====
        if game["lives"] <= 0:
            game_over = True
            if game["score"] > highscore:
                highscore = game["score"]
                save_highscore(highscore)

    else:
        screen.blit(big_font.render("GAME OVER", True, RED), (180,130))
        screen.blit(font.render(f"Score: {game['score']}", True, BLACK), (230,180))
        screen.blit(font.render("Tekan R untuk restart", True, BLACK), (180,220))

    pygame.display.update()
    clock.tick(60)

pygame.quit()


