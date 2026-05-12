import pygame, time, random, sys

pygame.init()

win = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

x, y = win.get_size()
lanes = 6
lane_w = x//(lanes)
car_y = y*0.7
car_w = lane_w*0.8
car_h = y*0.065
car = pygame.Rect([x//2,car_y,car_w,car_h])
btn_y = y*0.855
btn_w = x*0.35
btn_h = y*0.1
sensitivity = 10
left_btn = pygame.Rect([int(x*0.14),int(btn_y),int(btn_w),int(btn_h)])
right_btn = pygame.Rect([int(x*(1-0.14)-btn_w),int(btn_y),int(btn_w),int(btn_h)])
start_time = time.time()
threashold = 1
score = 0
enemy_cars = []
coins = []
coin_r = lane_w*0.2
car_colors = ["blue", "green", (255, 255, 0), (255,0,255), (0, 255, 255), "brown", "lightgreen"]
car_names = ["Physics","Maths","Biology","Chemistry","Bengali","English"]

current_finger_pos = [(0,0)]
left_btn_color = "grey"
right_btn_color = "grey"
fingers_down = False


font = pygame.font.SysFont("Arial", int(x*0.07))
bigfont = pygame.font.SysFont("Arial", int(x*0.2))
smallfont = pygame.font.SysFont("Arial", int(x*0.035))
right_btn_label = bigfont.render(">", 1, "black")
left_btn_label = bigfont.render("<", 1, "black")

car_names = [smallfont.render(i, 1, "black") for i in car_names]

speed_const = 100

clock = pygame.time.Clock()
class EnemyCar:
    def __init__(self, rect: pygame.Rect, color="red", name="", speed=5):
        self.car = rect
        self.color = color
        self.name=name
        self.speed = speed

class Coin:
    def __init__(self, pos, radius=coin_r, color="gold", speed=5):
        self.radius = radius
        self.diameter = 2*radius
        self.color = color
        self.speed = speed
        self.rect = pygame.Rect([pos[0], pos[1], self.diameter, self.diameter])
    
    def draw(self):
        pygame.draw.circle(win, self.color, (self.rect.x+self.radius, self.rect.y+self.radius), self.radius)
       
frame_prev = time.time()
while True:
    game_reset = False
    win.fill((100,100,100))
    # lanes
    for i in range(lanes):
        pygame.draw.line(win, "black", (lane_w*i, 0), (lane_w*i, y), 2)
    
    # car
    pygame.draw.rect(win, "black", car)
    
    for i in enemy_cars:
        pygame.draw.rect(win, i.color, i.car)
        win.blit(i.name, (i.car.x, i.car.y+0.1*car_w))
    for i in coins:
        i.draw()

    
    #btns
    pygame.draw.rect(win, left_btn_color, left_btn)
    pygame.draw.rect(win, right_btn_color, right_btn)
    
    win.blit(left_btn_label, (int(x*0.25),int(btn_y)))
    win.blit(right_btn_label, (int(x*(1)-btn_w),int(btn_y)))
    
    
    # score
    label = font.render("Score: "+str(score), 1, "black")
    win.blit(label, (int(x*(1-0.25)), int(y*0.05)))
    
    # logic
    for evt in pygame.event.get():
        if evt.type == pygame.FINGERDOWN:
            current_finger_pos.append((evt.x*x, evt.y*y))
            fingers_down = True
        if evt.type == pygame.FINGERUP:
            if len(current_finger_pos):
                current_finger_pos.pop(-1)
            fingers_down = False
    
    frame_now = time.time()
    dt = frame_now - frame_prev
    if left_btn.collidepoint(current_finger_pos[-1]) and fingers_down and (car.x-sensitivity) >= 0:
        car.x -= sensitivity*dt*speed_const
        left_btn_color = (170, 170, 170)
    else:
        left_btn_color = "grey"
    if right_btn.collidepoint(current_finger_pos[-1]) and fingers_down and (car.x+car.w+sensitivity) <= x:
        car.x += sensitivity*dt*speed_const
        right_btn_color = (170, 170, 170)
    else:
        right_btn_color = "grey"
    
    time_now = time.time()
    if time_now-start_time >= threashold or time_now-start_time <= 0:
        i = random.randint(0, lanes-1)
        
        if random.random() <= 0.3:
            coins.append(
                Coin(
                    (lane_w*i+(lane_w//2-coin_r), 0),
                    speed=random.randint(4, max(5,score//2))
                )
            )
        else:
            enemy_cars.append(
                EnemyCar(
                    pygame.Rect([lane_w*i+(lane_w-car_w)//2, 0, car_w, car_h]), 
                    random.choice(car_colors), 
                    random.choice(car_names), 
                    random.randint(4, max(5,score//2))
                )
            )
        start_time = time_now
    
    i = 0
    
    while i < len(enemy_cars) and not game_reset:
        if enemy_cars[i].car.y >= y:
            enemy_cars.pop(i)
        else:
            if car.colliderect(enemy_cars[i].car):
                pygame.display.flip()
                time.sleep(0.5)
                pygame.draw.rect(win, "grey", [int(x*0.2), int(y*0.3), int(x*0.6), int(y*0.4)])
                win.blit(pygame.font.SysFont("Arial", int(x*0.14)).render("Game Over", 1, "black"), (int(x*0.25), int(y*0.35)))
                
                restart_btn_rect = pygame.Rect([int(x*0.25), int(y*0.45), int(x*0.5), int(y*0.07)])
                quit_btn_rect = pygame.Rect([int(x*0.25), int(y*0.55), int(x*0.5), int(y*0.07)])
                
                pygame.draw.rect(win, (150, 150, 150), restart_btn_rect)
                pygame.draw.rect(win, (150, 150, 150), quit_btn_rect)
                go_font = pygame.font.SysFont("Arial", int(x*0.09))
                restart_font = go_font.render("Restart", 1, "black")
                exit_font = go_font.render("Exit", 1, "black")
                win.blit(restart_font, (int(x*0.39), int(y*0.46)))
                win.blit(exit_font, (int(x*0.43), int(y*0.56)))
                pygame.display.flip()
                restart = False
                quit_game = False
                while True:
                    mouse = pygame.mouse.get_pos()
                    click = pygame.mouse.get_pressed()[0]
                    
                    if restart and not click:
                        enemy_cars = []
                        coins = []
                        score = 0
                        car.x, car.y = x//2,car_y
                        game_reset = True
                        break
                    if quit_game and not click:
                        time.sleep(0.2)
                        sys.exit()
                    
                    if restart_btn_rect.collidepoint(mouse) and click:
                        restart = True
                        pygame.draw.rect(win, (120, 120, 120), restart_btn_rect)
                        win.blit(restart_font, (int(x*0.39), int(y*0.46)))
                        pygame.display.update(restart_btn_rect)
                    else:
                        restart = False
                        pygame.draw.rect(win, (150, 150, 150), restart_btn_rect)
                        win.blit(restart_font, (int(x*0.39), int(y*0.46)))
                        pygame.display.update(restart_btn_rect)
                    if quit_btn_rect.collidepoint(mouse) and click:
                        quit_game = True
                        pygame.draw.rect(win, (120, 120, 120), quit_btn_rect)
                        win.blit(exit_font, (int(x*0.43), int(y*0.56)))
                        pygame.display.update(quit_btn_rect)
                    else:
                        quit_game = False
                        pygame.draw.rect(win, (150, 150, 150), quit_btn_rect)
                        win.blit(exit_font, (int(x*0.43), int(y*0.56)))
                        pygame.display.update(quit_btn_rect)
                    
                    
                        
            if game_reset:
                break
            enemy_cars[i].car.y += enemy_cars[i].speed*dt*speed_const
            i += 1

    i = 0
    while i < len(coins) and not game_reset:
        if coins[i].rect.y >= y:
            coins.pop(i)
        elif car.colliderect(coins[i].rect):
            score += 1
            coins.pop(i)
        else:
            coins[i].rect.y += coins[i].speed*dt*speed_const
            i += 1
    
    threashold = 1 - score/100
    
    #render
    pygame.display.flip()
    
    clock.tick(60)
    frame_prev = frame_now
    
