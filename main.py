import pygame, time, random, sys

pygame.init()

win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
x, y = win.get_size()

lanes  = 6
lane_w = x // lanes
car_y  = y * 0.7
car_w  = lane_w * 0.6
car_h  = y * 0.065
car    = pygame.Rect([x // 2, car_y, car_w, car_h])

btn_y = y * 0.855
btn_w = x * 0.35
btn_h = y * 0.1
sensitivity = 10
left_btn  = pygame.Rect([int(x * 0.14),               int(btn_y), int(btn_w), int(btn_h)])
right_btn = pygame.Rect([int(x * (1 - 0.14) - btn_w), int(btn_y), int(btn_w), int(btn_h)])

start_time = time.time()
threashold = 1
score      = 0
enemy_cars = []
coins      = []
coin_r     = lane_w * 0.2

car_colors        = ["blue", "green", (255,255,0), (255,0,255), (0,255,255), "brown", "lightgreen"]
car_label_strings = ["Physics","Maths","Biology","Chemistry","Bengali","English"]

current_finger_pos = [(-1, -1)]
left_btn_color  = "grey"
right_btn_color = "grey"
fingers_down    = False

font      = pygame.font.SysFont("Arial", int(x * 0.07))
bigfont   = pygame.font.SysFont("Arial", int(x * 0.2))
smallfont = pygame.font.SysFont("Arial", int(x * 0.035))
go_font   = pygame.font.SysFont("Arial", int(x * 0.09))

right_btn_label = bigfont.render(">", 1, "black")
left_btn_label  = bigfont.render("<", 1, "black")
car_name_surfs  = [smallfont.render(n, 1, "black") for n in car_label_strings]

speed_const = 100
clock       = pygame.time.Clock()


class EnemyCar:
    def __init__(self, rect, color="red", name=None, speed=5):
        self.car   = rect
        self.color = color
        self.name  = name   # pre-rendered Surface
        self.speed = speed


class Coin:
    def __init__(self, pos, radius=coin_r, color="gold", speed=5):
        self.radius   = radius
        self.diameter = 2 * radius
        self.color    = color
        self.speed    = speed
        self.rect     = pygame.Rect([pos[0], pos[1], self.diameter, self.diameter])

    def draw(self):
        pygame.draw.circle(
            win, self.color,
            (int(self.rect.x + self.radius), int(self.rect.y + self.radius)),
            int(self.radius)
        )


go_box = pygame.Rect([int(x*0.2),  int(y*0.3),  int(x*0.6), int(y*0.4)])
restart_btn_rect = pygame.Rect([int(x*0.25), int(y*0.45), int(x*0.5), int(y*0.07)])
quit_btn_rect = pygame.Rect([int(x*0.25), int(y*0.55), int(x*0.5), int(y*0.07)])
go_title = pygame.font.SysFont("Arial", int(x*0.11)).render("Game Over", 1, "black")
restart_label = go_font.render("Restart", 1, "black")
exit_label = go_font.render("Exit",    1, "black")


def draw_game_over():
    pygame.draw.rect(win, "grey", go_box)
    win.blit(go_title,      (int(x*0.25), int(y*0.31)))
    pygame.draw.rect(win, (150,150,150), restart_btn_rect)
    pygame.draw.rect(win, (150,150,150), quit_btn_rect)
    win.blit(restart_label, (int(x*0.39), int(y*0.46)))
    win.blit(exit_label,    (int(x*0.43), int(y*0.56)))


def reset_game():
    global enemy_cars, coins, score, start_time, threashold
    enemy_cars = []
    coins      = []
    score      = 0
    threashold = 1
    start_time = time.time()
    car.x = x // 2
    car.y = car_y



game_state = 'playing'
frame_prev = time.time()

while True:
    win.fill((100, 100, 100))
    for i in range(lanes):
        pygame.draw.line(win, "black", (lane_w * i, 0), (lane_w * i, y), 2)

    pygame.draw.rect(win, "black", car)

    for ec in enemy_cars:
        pygame.draw.rect(win, ec.color, ec.car)
        if ec.name:
            win.blit(ec.name, (ec.car.x, ec.car.y + 0.1 * car_w))

    for c in coins:
        c.draw()

    if game_state == 'playing':
        pygame.draw.rect(win, left_btn_color,  left_btn)
        pygame.draw.rect(win, right_btn_color, right_btn)
        win.blit(left_btn_label,  (int(x*0.25),        int(btn_y)))
        win.blit(right_btn_label, (int(x - btn_w),     int(btn_y)))

    score_label = font.render("Score: " + str(score), 1, "black")
    win.blit(score_label, (int(x * (1-0.25)), int(y * 0.05)))

    
    for evt in pygame.event.get():

        if evt.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        if evt.type == pygame.KEYDOWN and evt.key == pygame.K_ESCAPE:
            pygame.quit(); sys.exit()

        if game_state == 'playing':
            if evt.type == pygame.FINGERDOWN:
                current_finger_pos.append((evt.x * x, evt.y * y))
                fingers_down = True
            if evt.type == pygame.FINGERUP:
                if len(current_finger_pos) > 1: 
                    current_finger_pos.pop(-1)
                fingers_down = False

        elif game_state == 'game_over':
            tap = None
            if evt.type == pygame.FINGERDOWN:
                tap = (evt.x * x, evt.y * y)
            elif evt.type == pygame.MOUSEBUTTONDOWN: 
                tap = pygame.mouse.get_pos()

            if tap:
                if restart_btn_rect.collidepoint(tap):
                    reset_game()
                    game_state = 'playing'
                elif quit_btn_rect.collidepoint(tap):
                    pygame.quit(); sys.exit()

    if game_state == 'playing':

        frame_now = time.time()
        dt = frame_now - frame_prev

        # Move player
        fp = current_finger_pos[-1]
        if fingers_down and left_btn.collidepoint(fp) and car.x - sensitivity >= 0:
            car.x -= int(sensitivity * dt * speed_const)
            left_btn_color = (170, 170, 170)
        else:
            left_btn_color = "grey"

        if fingers_down and right_btn.collidepoint(fp) and car.x + car.w + sensitivity <= x:
            car.x += int(sensitivity * dt * speed_const)
            right_btn_color = (170, 170, 170)
        else:
            right_btn_color = "grey"

        # Spawn
        time_now = time.time()
        if time_now - start_time >= threashold:
            lane_i = random.randint(0, lanes - 1)
            spd    = random.randint(4, max(5, score // 2))
            if random.random() <= 0.3:
                coins.append(Coin(
                    (lane_w * lane_i + (lane_w // 2 - coin_r), 0), speed=spd
                ))
            else:
                enemy_cars.append(EnemyCar(
                    pygame.Rect([lane_w * lane_i + (lane_w - car_w) // 2, 0, car_w, car_h]),
                    random.choice(car_colors),
                    random.choice(car_name_surfs),
                    spd,
                ))
            start_time = time_now

        # Update enemies
        collision = False
        i = 0
        while i < len(enemy_cars):
            ec = enemy_cars[i]
            if ec.car.y >= y:
                enemy_cars.pop(i)
            elif car.colliderect(ec.car):
                collision = True
                break
            else:
                ec.car.y += int(ec.speed * dt * speed_const)
                i += 1

        if collision:
            game_state = 'game_over'

        # Update coins
        i = 0
        while i < len(coins):
            c = coins[i]
            if c.rect.y >= y:
                coins.pop(i)
            elif car.colliderect(c.rect):
                score += 1
                coins.pop(i)
            else:
                c.rect.y += int(c.speed * dt * speed_const)
                i += 1

        threashold = 1 - score / 100

        frame_prev = frame_now

    elif game_state == 'game_over':
        draw_game_over()

    pygame.display.flip()
    clock.tick(60)
    
