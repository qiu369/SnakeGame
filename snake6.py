import pygame
import random

# 游戏的初始化
pygame.init()

# 设置屏幕大小
screen = pygame.display.set_mode((640, 640))

# 设置游戏的时钟
clock = pygame.time.Clock()

# 设置食物的初始位置
food_pos = [random.randrange(1, 64)*10, random.randrange(1, 64)*10]
food_spawn = True

# 设置初始方向
direction = 'RIGHT'

# 设置颜色
snake_color = (0,255,0) # 绿色
food_color = (255,0,0) # 红色
background_color = (0,0,0) # 黑色
text_color = (255, 255, 255) # 白色

font = pygame.font.Font(None, 36)

# 设置 "restart" 按钮的位置和大小
restart_button = pygame.Rect(260, 400, 120, 50)

def game_over():
    global direction

    # 设置要显示的文字
    text = font.render('Game Over', True, text_color)
    # 设置显示的位置
    screen.blit(text, (250, 300))

    # 绘制 "restart" 按钮
    pygame.draw.rect(screen, text_color, restart_button, 2)
    text = font.render('Restart', True, text_color)
    screen.blit(text, (restart_button.x + 10, restart_button.y + 10))

    pygame.display.update()

    # 检测鼠标点击事件，判断用户是否点击了 "restart" 按钮
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 如果点击了 "restart" 按钮，就开始新一轮游戏
                if restart_button.collidepoint(event.pos):
                    direction = 'RIGHT' # 重置蛇的移动方向
                    return True # 返回 True，表示用户选择了重新开始游戏

# 设置蛇的初始位置
snake_pos = [[100, 50], [90, 50], [80, 50]]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        # 控制方向
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                direction = 'UP'
            if event.key == pygame.K_DOWN and direction != 'UP':
                direction = 'DOWN'
            if event.key == pygame.K_LEFT and direction != 'RIGHT':
                direction = 'LEFT'
            if event.key == pygame.K_RIGHT and direction != 'LEFT':
                direction = 'RIGHT'

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
