import pgzrun
import random
import math

# TODO: tela de inicio
# TODO: tela de fim
# TODO: powerup


WIDTH = 1920
HEIGHT = 1080
PLAYER_SPEED = 3
ATTACK_SPEED = 0.1
ENEMY_SPEED = 1
ENEMY_SPAWN_SPEED = 5
SLASH_DURATION = 0.15

score = 0
player = Actor("player", pos=(WIDTH / 20, HEIGHT / 20))
slash = Actor("atack01", (-150, -150))
player.life = 3
player.can_take_damage = True
player.can_attack = True
lifes = []
for i in range(player.life):
    lifes.append(Actor("hud_heart", topleft=(i * 50, 5)))

enemies = []


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
    if player.life > 0:
        player.life -= 1
        lifes[player.life].image = "hud_heart_empty"
        player.can_take_damage = False
        clock.schedule_unique(reset_damage_cooldown, 3.0)


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
        player.x -= PLAYER_SPEED
    if keyboard.right:
        player.x += PLAYER_SPEED
    if keyboard.up:
        player.y -= PLAYER_SPEED
    if keyboard.down:
        player.y += PLAYER_SPEED

    player.x = max(player.width / 2, min(WIDTH - player.width / 2, player.x))
    player.y = max(player.height / 2, min(HEIGHT - player.height / 2, player.y))


def on_mouse_down(pos, button):
    if player.can_attack:
        attack(pos)


def attack(pos):
    player.can_attack = False
    angle = math.atan2(pos[1] - player.y, pos[0] - player.x)
    distance = 50
    slash.x = player.x
    slash.y = player.y
    slash.angle = angle * (-180 / math.pi)
    x = player.x + math.cos(angle) * distance
    y = player.y + math.sin(angle) * distance
    animate(slash, pos=(x, y), duration=0.1, tween="linear", on_finished=finish_attack)
    clock.schedule_unique(reset_attack_cooldown, ATTACK_SPEED)


def finish_attack():
    global score
    for enemy in enemies[:]:
        if enemy.colliderect(slash):
            score += 1
            enemies.remove(enemy)
    slash.x = -100
    slash.y = -100


def spawn_upgrade():
    upgrade = Actor("")


def update():
    player_move()
    enemy_move()


def tutorial():
    screen.draw.text(
        "controles: use as setas direcionais para se mover",
        center=(WIDTH / 2, HEIGHT / 2),
        fontsize=50,
        color="white",
    )


def draw():
    screen.blit("bg", (0, 0))
    for heart in lifes:
        heart.draw()
    for enemy in enemies:
        enemy.draw()
    player.draw()
    slash.draw()
    screen.draw.text(
        f"Score: {score}", center=(WIDTH / 2, 40), fontsize=50, color="white"
    )
    tutorial()


clock.schedule_unique(spawn_enemy, 1.0)
pgzrun.go()
