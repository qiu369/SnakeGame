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

# 设置颜色
snake_color = (0,255,0) # 绿色
food_color = (255,0,0) # 红色
background_color = (0,0,0) # 黑色
text_color = (255,255,255) # 白色

# 设置字体
font = pygame.font.Font(None, 30)

# 创建一个表示 "restart" 按钮的矩形
restart_button = pygame.Rect(250, 400, 100, 50)

# def game_over():
#     # 设置要显示的文字
#     text = font.render('Game Over', True, text_color)
#     # 设置显示的位置
#     screen.blit(text, (250, 300))

#     # 绘制 "restart" 按钮
#     pygame.draw.rect(screen, text_color, restart_button, 2)
#     text = font.render('Restart', True, text_color)
#     screen.blit(text, (restart_button.x + 10, restart_button.y + 10))

#     pygame.display.update()

def game_over():
    # 设置要显示的文字
    text = font.render('Game Over', True, text_color)
    # 设置显示的位置
    screen.blit(text, (250, 300))

    # 绘制 "restart" 按钮
    pygame.draw.rect(screen, text_color, restart_button, 2)
    text = font.render('Restart', True, text_color)
    screen.blit(text, (restart_button.x + 10, restart_button.y + 10))

    # 绘制 "exit" 按钮
    exit_button = pygame.Rect(400, 400, 100, 50)
    pygame.draw.rect(screen, text_color, exit_button, 2)
    text = font.render('Exit', True, text_color)
    screen.blit(text, (exit_button.x + 20, exit_button.y + 10))

    pygame.display.update()

    # 检测鼠标点击事件，判断用户是否点击了 "exit" 或 "restart" 按钮
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 如果点击了 "exit" 按钮，就退出游戏
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    quit()
                # 如果点击了 "restart" 按钮，就开始新一轮游戏
                elif restart_button.collidepoint(event.pos):
                    return


def start_screen():
    # 设置要显示的文字
    text = font.render('Click "Restart" to start the game', True, text_color)
    # 设置显示的位置
    screen.blit(text, (100, 300))

    # 绘制 "restart" 按钮
    pygame.draw.rect(screen, text_color, restart_button, 2)
    text = font.render('Restart', True, text_color)
    screen.blit(text, (restart_button.x + 10, restart_button.y + 10))

    pygame.display.update()

# 显示开始画面
start_screen()

# 游戏主循环
while True:
    for event in pygame.event.get():
        # 检测鼠标点击事件
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 如果点击了 "restart" 按钮，就开始新一轮游戏
            if restart_button.collidepoint(event.pos):
                # 设置蛇和食物的初始位置
                snake_pos = [[100, 50], [90, 50], [80, 50]]
                food_pos = [random.randrange(1, 64)*10, random.randrange(1, 64)*10]
                food_spawn = True

                # 设置分数
                score = 0

                # 游戏循环
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
                        score += 1
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

                    # 绘制当前分数
                    text = font.render('Score: ' + str(score), True, text_color)
                    screen.blit(text, (0, 0))

                    # 判断是否撞到墙或者自己
                    if snake_pos[0][0] >= 640 or snake_pos[0][0] < 0 or snake_pos[0][1] >= 640 or snake_pos[0][1] < 0:
                        game_over()
                        break
                    for pos in snake_pos[1:]:
                        if snake_pos[0] == pos:
                            game_over()
                            break

                    pygame.display.update()
                    # 减慢蛇的移动速度
                    clock.tick(10)
