import pgzrun
import random
import math

WIDTH = 1920
HEIGHT = 1080
PLAYER_SPEED = 3
ENEMY_SPEED = 1
ENEMY_SPAWN_SPEED = 10
SLASH_DURATION = 0.15

player = Actor("player", pos=(WIDTH / 2, HEIGHT / 2))
player.life = 3
player.can_take_damage = True
slashes = []
lifes = []
for i in range(player.life):
    lifes.append(Actor("hud_heart", topleft=(i * 40, 0)))

enemies = []


def spawn_enemy():
    while True:
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        if abs(x - player.x) > 200 and abs(y - player.y) > 200:
            break
    enemies.append(Actor("enemy", pos=(x, y)))
    clock.schedule_unique(spawn_enemy, ENEMY_SPAWN_SPEED)


def lose_life():
    if player.life > 0:
        player.life -= 1
        lifes[player.life].image = "hud_heart_empty"
        player.can_take_damage = False
        clock.schedule_unique(reset_damage_cooldown, 3.0)


def reset_damage_cooldown():
    player.can_take_damage = True


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


def on_mouse_down(pos, button):
    angle = math.atan2(pos[1] - player.y, pos[0] - player.x)
    distance = 50
    x = player.x + math.cos(angle) * distance
    y = player.y + math.sin(angle) * distance
    slash = Rect((x - 15, y - 15), (30, 30))
    slashes.append(slash)
    clock.schedule_unique(lambda: slashes.remove(slash), SLASH_DURATION)


def update():
    player_move()
    enemy_move()


def draw():
    screen.fill((128, 0, 0))
    for heart in lifes:
        heart.draw()
    for enemy in enemies:
        enemy.draw()
    player.draw()
    for slash in slashes:
        screen.draw.filled_rect(slash, (255, 255, 255))


clock.schedule_unique(spawn_enemy, 1.0)
pgzrun.go()
