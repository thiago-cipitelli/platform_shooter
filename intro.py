import pgzrun
import random
import math

# TODO: tela de inicio
# TODO: tela de fim

# ROGUE ALIENS

WIDTH = 1920
HEIGHT = 1080
PLAYER_SPEED = 2
ATTACK_SPEED = 1.5
ENEMY_SPEED = 1
ENEMY_SPAWN_SPEED = 5
SLASH_DURATION = 0.15

game_start = False
menu_screen = Actor("menu", center=(WIDTH / 2, HEIGHT / 2))
score = 0
player = Actor("player", pos=(WIDTH / 2, HEIGHT / 2))
slash = Actor("atack03", (-150, -150))
player.life = 3
player.can_take_damage = True
player.can_attack = True

player.range_boost = 1.0
player.speed_boost = 1.0
player.cooldown_boost = 1.0

lifes = []
for i in range(player.life):
    lifes.append(Actor("hud_heart", topleft=(i * 50, 5)))
enemies = []
powerups = []


def spawn_enemy():
    while True:
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        if abs(x - player.x) > 200 and abs(y - player.y) > 200:
            break
    num = random.randint(1, 2)
    enemies.append(Actor(f"enemy_0{num}", pos=(x, y)))
    clock.schedule_unique(spawn_enemy, max(0.3, ENEMY_SPAWN_SPEED - (score / 10)))


def lose_life():
    if player.life > 1:
        player.life -= 1
        lifes[player.life].image = "hud_heart_empty"
        player.can_take_damage = False
        clock.schedule_unique(reset_damage_cooldown, 3.0)
    else:
        exit()


def reset_damage_cooldown():
    player.can_take_damage = True


def reset_attack_cooldown():
    player.can_attack = True


def enemy_move():
    for enemy in enemies:
        if enemy.x < player.x:
            enemy.x += ENEMY_SPEED
        if enemy.x > player.x:
            enemy.x -= ENEMY_SPEED
        if enemy.y < player.y:
            enemy.y += ENEMY_SPEED
        if enemy.y > player.y:
            enemy.y -= ENEMY_SPEED
        if player.can_take_damage and player.colliderect(enemy):
            lose_life()
            animate(player, angle=360, duration=0.3, tween="linear")


def player_move():
    if keyboard.left:
        player.x -= min(7, PLAYER_SPEED * player.speed_boost)
    if keyboard.right:
        player.x += min(7, PLAYER_SPEED * player.speed_boost)
    if keyboard.up:
        player.y -= min(7, PLAYER_SPEED * player.speed_boost)
    if keyboard.down:
        player.y += min(7, PLAYER_SPEED * player.speed_boost)

    for boost in powerups:
        if player.colliderect(boost):
            collect_upgrade(boost.image)
            powerups.remove(boost)

    player.x = max(player.width / 2, min(WIDTH - player.width / 2, player.x))
    player.y = max(player.height / 2, min(HEIGHT - player.height / 2, player.y))


def on_mouse_down(pos, button):
    global game_start

    if not game_start:
        if pos[0] > 750 and pos[0] < 1160 and pos[1] > 470 and pos[1] < 590:
            game_start = True
            music.play_once("play")
            return

        if pos[0] > 765 and pos[0] < 1150 and pos[1] > 630 and pos[1] < 730:
            exit()

    if player.can_attack:
        attack(pos)


def attack(pos):
    player.can_attack = False
    angle = math.atan2(pos[1] - player.y, pos[0] - player.x)
    distance = min(150, 50 * player.range_boost)
    slash.x = player.x
    slash.y = player.y
    slash.angle = angle * (-180 / math.pi)
    x = player.x + math.cos(angle) * distance
    y = player.y + math.sin(angle) * distance
    music.play_once("attack")
    animate(slash, pos=(x, y), duration=0.1, tween="linear", on_finished=finish_attack)
    clock.schedule_unique(
        reset_attack_cooldown, max(0.1, ATTACK_SPEED - player.cooldown_boost)
    )


def finish_attack():
    global score
    for enemy in enemies[:]:
        if enemy.colliderect(slash):
            score += 1
            if score % 5 == 0:
                spawn_upgrade()
            music.play_once("explosion")
            enemies.remove(enemy)
    slash.x = -100
    slash.y = -100


def generate_random_boost():
    boost_num = random.randint(0, 3)
    match boost_num:
        case 0:
            return "attack_up"
        case 1:
            return "less_cooldown"
        case 2:
            return "speed_up"
        case _:
            return "star"


def collect_upgrade(boost):
    if boost == "attack_up":
        player.range_boost += 0.1

    if boost == "less_cooldown":
        player.cooldown_boost += 0.1

    if boost == "speed_up":
        player.speed_boost += 0.2

    if boost == "star":
        player.cooldown_boost += 0.2
        player.range_boost += 0.2
        player.speed_boost += 0.3


def spawn_upgrade():
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    image = generate_random_boost()
    powerups.append(Actor(image, pos=(x, y)))


def update():
    if game_start:
        player_move()
        enemy_move()


def tutorial():
    screen.draw.text(
        "controles: use as setas direcionais para se mover",
        center=(WIDTH / 2, HEIGHT / 2),
        fontsize=50,
        color="white",
    )


def menu():
    menu_screen.draw()


def game():
    for heart in lifes:
        heart.draw()

    for enemy in enemies:
        enemy.draw()

    for boost in powerups:
        boost.draw()
    player.draw()
    slash.draw()
    draw_player_status()


def calcula_percentagem(a, b):
    a = min(b, (int(round(10 * (a - 1)))))
    return int((a / b) * 100)


def draw_player_status():
    screen.draw.text(
        f"speed: {calcula_percentagem(player.speed_boost, 70)}%",
        topleft=(0, 60),
        fontsize=50,
        color="white",
    )
    screen.draw.text(
        f"range: {calcula_percentagem(player.range_boost, 30)}%",
        topleft=(0, 110),
        fontsize=50,
        color="white",
    )
    screen.draw.text(
        f"attack speed: {calcula_percentagem(player.cooldown_boost, 9)}%",
        topleft=(0, 160),
        fontsize=50,
        color="white",
    )
    screen.draw.text(
        f"Score: {score}", center=(WIDTH / 2, 40), fontsize=50, color="white"
    )


def draw():
    screen.fill((123, 201, 89))
    if game_start:
        game()
    else:
        menu()


clock.schedule_unique(spawn_enemy, 1.0)
pgzrun.go()
