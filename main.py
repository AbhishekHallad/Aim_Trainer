import math
import random
import time
import pygame
pygame.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AIM Trainer")

TRAGET_INCREMENT = 400
TRAGET_EVENT = pygame.USEREVENT
TARGET_PADDING = 30
LIVES = 3
TOP_BAR_HEIGHT = 50

BG_COLOR = (0,25,40)

LABEL_FONT = pygame.font.SysFont("comicsans", 24)

class Target:
    MAX_SIZE = 30
    GROWTH_RATE = 0.2
    COLOR = 'red'
    SECONDARY_COLOR = 'white'

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True

    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False

        if self.grow:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE

    def draw(self,win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size)
        pygame.draw.circle(win, self.SECONDARY_COLOR, (self.x, self.y), self.size * 0.8)
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size * 0.6)
        pygame.draw.circle(win, self.SECONDARY_COLOR, (self.x, self.y), self.size * 0.4)

    def collide(self,x,y):
        dis = math.sqrt((self.x - x)**2 + (self.y - y)**2)
        return dis <= self.size

def draw(win, targets):
    win.fill(BG_COLOR)

    for target in targets:
        target.draw(win)

def format_time(secs):
    milli = math.floor(int(secs * 1000 % 1000)/ 100)
    seconds = int(round(secs%60, 1))
    minutes = int(secs // 60)

    return f"{minutes:02d}:{seconds:02d}.{milli}"

def top_bar(win, elapsed_time, targets_pressed, misses):
    pygame.draw.rect(win, "grey", (0, 0, WIDTH, TOP_BAR_HEIGHT))
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "black")
    speed = round(targets_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "black")
    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "black")
    lives_label = LABEL_FONT.render(f"Lives: {LIVES - misses}", 1, "black")

    win.blit(time_label, (5,5))
    win.blit(speed_label, (200,5))
    win.blit(hits_label, (450,5))
    win.blit(lives_label, (650,5))

def end_screen(win, elapsed_time, tragets_pressed, clicks):
    win.fill(BG_COLOR)
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "white")
    speed = round(targets_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "white")
    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "white")
    accuracy = round(tragets_pressed/clicks*100, 1)
    accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}", 1, "white")

    win.blit(time_label, (get_middle(time_label),100))
    win.blit(speed_label, (get_middle(speed_label),200))
    win.blit(hits_label, (get_middle(hits_label),300))
    win.blit(accuracy_label, (get_middle(accuracy_label),400))

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.KEYDOWN:
                run = False
                break

def get_middle(surface):
    return WIDTH/2 - surface.get_widht()/2

def main():
    flag = True
    targets = []
    clock = pygame.time.Clock()

    target_pressed = 0
    clicks = 0
    start_time = time.time()
    misses = 0

    pygame.time.set_timer(TRAGET_EVENT, TRAGET_INCREMENT)

    while flag:
        clock.tick(60)
        click = False
        mouse_pos = pygame.mouse.get_pos()
        time_elapsed = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
                break

            if event.type == TRAGET_EVENT:
                x = random.randint(TARGET_PADDING, WIDTH-TARGET_PADDING)
                y = random.randint(TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT-TARGET_PADDING)
                target = Target(x,y)
                targets.append(target)

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1

        for target in targets:
            target.update()

            if target.size <= 0:
                targets.remove(target)
                misses += 1

            if click and target.collide(*mouse_pos):
                targets.remove(target)
                target_pressed += 1

        if misses >= LIVES:
            end_screen(WIN, time_elapsed, target_pressed, clicks)

        draw(WIN, targets)
        top_bar(WIN, time_elapsed, target_pressed, misses)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()