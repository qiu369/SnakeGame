import pygame
import random

# 游戏的初始化
pygame.init()

# 设置屏幕大小
screen = pygame.display.set_mode((640, 640))

# 设置游戏的时钟
clock = pygame.time.Clock()

# 设置初始方向
direction = 'RIGHT'
change_to = direction

# 设置颜色
snake_color = (0,255,0) # 绿色
food_color = (255,0,0) # 红色
background_color = (0,0,0) # 黑色
text_color = (255, 255, 255) # 白色

font = pygame.font.Font(None, 36)

# 设置 "restart" 和 "exit" 按钮的位置和大小
restart_button = pygame.Rect(260, 400, 120, 50)
exit_button = pygame.Rect(260, 500, 120, 50)
start_button = pygame.Rect(260, 300, 120, 50)

# 设置初始分数
score = 0

def show_score():
    score_text = font.render(f'Score: {score}', True, text_color)
    screen.blit(score_text, (0, 0))

def game_over():
    global direction, score

    # 设置要显示的文字
    text = font.render('Game Over', True, text_color)
    # 设置显示的位置
    screen.blit(text, (250, 300))

    # 绘制 "restart" 和 "exit" 按钮
    pygame.draw.rect(screen, text_color, restart_button, 2)
    text = font.render('Restart', True, text_color)
    screen.blit(text, (restart_button.x + 10, restart_button.y + 10))

    pygame.draw.rect(screen, text_color, exit_button, 2)
    text = font.render('Exit', True, text_color)
    screen.blit(text, (exit_button.x + 20, exit_button.y + 10))

    pygame.display.update()

    # 检测鼠标点击事件，判断用户是否点击了 "restart" 或 "exit" 按钮
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.MOUSEBUTTONDOWN and exit_button.collidepoint(event.pos)):
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and restart_button.collidepoint(event.pos):
                direction = 'RIGHT' # 重置蛇的移动方向
                score = 0 # 重置分数
                return True # 返回 True，表示用户选择了重新开始游戏

# 显示开始界面，等待用户点击 "start" 按钮
def start_screen():
    screen.fill(background_color)

    text = font.render('Click "Start" to begin', True, text_color)
    screen.blit(text, (160, 200))

    pygame.draw.rect(screen, text_color, start_button, 2)
    text = font.render('Start', True, text_color)
    screen.blit(text, (start_button.x + 30, start_button.y + 10))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.MOUSEBUTTONDOWN and exit_button.collidepoint(event.pos)):
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and start_button.collidepoint(event.pos):
                return

# 显示开始界面
start_screen()

# 设置蛇和食物的初始位置
snake_pos = [[100, 50], [90, 50], [80, 50]]
food_pos = [random.randrange(1, 64)*10, random.randrange(1, 64)*10]
food_spawn = True

while True:
    # 控制方向
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                change_to = 'UP'
            if event.key == pygame.K_DOWN and direction != 'UP':
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT and direction != 'RIGHT':
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT and direction != 'LEFT':
                change_to = 'RIGHT'
    direction = change_to

    # 更新蛇的位置
    if direction == 'UP':
        snake_pos.insert(0, [snake_pos[0][0], snake_pos[0][1]-10])
    if direction == 'DOWN':
        snake_pos.insert(0, [snake_pos[0][0], snake_pos[0][1]+10])
    if direction == 'LEFT':
        snake_pos.insert(0, [snake_pos[0][0]-10, snake_pos[0][1]])
    if direction == 'RIGHT':
        snake_pos.insert(0, [snake_pos[0][0]+10, snake_pos[0][1]])

    # 判断是否吃到食物
    if snake_pos[0] == food_pos:
        score += 1
        food_spawn = False
    else:
        snake_pos.pop()

    # 生成新的食物
    if not food_spawn:
        food_pos = [random.randrange(1, 64)*10, random.randrange(1, 64)*10]
    food_spawn = True

    # 刷新屏幕
    screen.fill(background_color)
    for pos in snake_pos:
        pygame.draw.rect(screen, snake_color, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(screen, food_color, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    # 显示分数
    show_score()

    # 判断是否撞到墙或者自己
    if snake_pos[0][0] >= 640 or snake_pos[0][0] < 0 or snake_pos[0][1] >= 640 or snake_pos[0][1] < 0:
        if game_over():
            snake_pos = [[100, 50], [90, 50], [80, 50]]
            direction = 'RIGHT'
    for pos in snake_pos[1:]:
        if snake_pos[0] == pos:
            if game_over():
                snake_pos = [[100, 50], [90, 50], [80, 50]]
                direction = 'RIGHT'

    pygame.display.update()
    # 减慢蛇的移动速度
    clock.tick(10)
