# 贪吃蛇1.0
import sys     # 自带，用来通过键盘操控蛇
import random
import pygame  # 需要额外安装，用来设计很多小游戏

# 全局定义
SCREEN_X = 600      # 界面宽度
SCREEN_Y = 600      # 界面长度
speed = 0           # 蛇的行进速度
snake_body = []     # 蛇的各个坐标
local = sys.argv[0].replace('贪吃蛇1.0.py','') # 当前文件位置

# 蛇类
class Snake(object):

    def __init__(self):      # 初始化,蛇的属性
        self.dirction = pygame.K_RIGHT  # 初始蛇的朝向
        self.body = []  # 蛇的长度

        for x in range(5):
            self.addnode()

    def addnode(self):        # 蛇的动作吃
        left, top = (0, 0)
        if self.body:
            left, top = (self.body[0].left, self.body[0].top)
        node = pygame.Rect(left, top, 25, 25)   # 像素方格以25为一个单位

        global snake_body
        snake_body.insert(0,(left,top))

        if self.dirction == pygame.K_LEFT:
            node.left -= 25
        elif self.dirction == pygame.K_RIGHT:
            node.left += 25
        elif self.dirction == pygame.K_UP:
            node.top -= 25
        elif self.dirction == pygame.K_DOWN:
            node.top += 25
        self.body.insert(0, node)


    def delnode(self):     # 蛇的移动中尾端的删除
        self.body.pop()

        global snake_body
        snake_body.pop()

    def isdead(self):      # 蛇的死亡判断
        if self.body[0].x not in range(SCREEN_X):   # 撞墙
            return True
        if self.body[0].y not in range(SCREEN_Y):
            return True
        if self.body[0] in self.body[1:]:    # 撞自己
            return True
        return False

    def move(self):    # 蛇的移动
        self.addnode()
        self.delnode()

    def changedirection(self, curkey):          # 蛇的方向的改变
        LR = [pygame.K_LEFT, pygame.K_RIGHT]
        UD = [pygame.K_UP, pygame.K_DOWN]
        if curkey in LR + UD:
            if (curkey in LR) and (self.dirction in LR):
                return   # 结束函数
            if (curkey in UD) and (self.dirction in UD):
                return
            self.dirction = curkey

# 食物类
class Food:
    def __init__(self):       # 初始化食物的位置，之后随机产生
        self.rect = pygame.Rect(-25, 0, 25, 25)

    def remove(self):   # 食物被吃后被清除
        self.rect.x = -25

    def set(self):   # 食物放置的方法
        if self.rect.x == -25:
            allpos = []
            for x in range(25, SCREEN_X - 25, 25):  # 防止食物靠墙太近
                for y in range(25, SCREEN_Y - 25, 25):
                    allpos.append((x,y))
            pos1 = [x for x in allpos if x not in snake_body] # 防止食物出现在蛇的身上
            pos2 = random.choice(pos1)
            self.rect.left,self.rect.top = pos2
            print(self.rect)

def show_text(screen, pos, text, color, font_bold=False, font_size=60, font_italic=False):
    cur_font = pygame.font.Font('C:/Windows/Fonts/simkai.ttf', font_size)   # 获取黑体字体，并设置文字大小
    cur_font.set_bold(font_bold)   # 设置是否加粗属性
    cur_font.set_italic(font_italic)   # 设置是否斜体属性
    text_fmt = cur_font.render(text, 1, color)   # 设置文字内容
    screen.blit(text_fmt, pos)  # 绘制文字

def body():
    screen_size = (SCREEN_X, SCREEN_Y)
    screen = pygame.display.set_mode(screen_size)  # 设置界面
    clock = pygame.time.Clock()
    scores = 0  # 成绩
    isdead = False    # 判定是否死亡

    snake = Snake()
    food = Food()

    while True:
        myimage = pygame.image.load(local + '/ld.jpg')
        screen.blit(myimage, [0, 0])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                snake.changedirection(event.key)
                if event.key == pygame.K_SPACE and isdead:
                    return main()
                elif event.key == pygame.K_SPACE and isdead == 0:
                    zt=1
                    while zt == 1:
                        for event2 in pygame.event.get():
                            if event2.type == pygame.QUIT:
                                sys.exit()
                            if event2.type == pygame.KEYDOWN:
                                if event2.key == pygame.K_SPACE:
                                    zt=0

        if not isdead:  # 画蛇身
            snake.move()
        for rect in snake.body:
            pygame.draw.rect(screen, (20, 220, 39), rect, 0)

        isdead = snake.isdead()   # 显示死亡文字
        if isdead:
            show_text(screen, (200, 200), '你输了！', (27, 29, 18), False, 50)
            show_text(screen, (75, 260), '请按下空格键以重新开始游戏……', (0, 0, 22), False, 30)

        if food.rect == snake.body[0]:   # 食物的处理  吃到+50  食物与蛇头   蛇长度+1方块
            scores += 50
            food.remove()
            snake.addnode()

        food.set()
        pygame.draw.rect(screen, (136, 0, 24), food.rect, 0)

        show_text(screen, (50, 500), '分数:' + str(scores), (0, 0, 0))   # 显示分数文字

        show_text(screen, (300, 560), '按空格键可以暂停或者继续游戏', (0, 0, 0), False, 20)

        pygame.display.update()  # 更新
        clock.tick(speed)

def main():
    pygame.init()  # 初始化
    screen_size = (SCREEN_X, SCREEN_Y)
    screen = pygame.display.set_mode(screen_size)  # 设置界面
    pygame.display.set_caption('贪吃蛇')  # 设置窗口标题
    myimage0 = pygame.image.load(local+'fm.jpg')  # 把变量myimage赋给导入的图片
    myimage1 = pygame.image.load(local+'cj.jpg')
    myimage2 = pygame.image.load(local+'zj.jpg')
    myimage3 = pygame.image.load(local+'gj.jpg')
    screen.blit(myimage0, [0, 0])      # 画出主界面背景图片
    screen.blit(myimage1, [148, 106])  # 画出难度图片
    screen.blit(myimage2, [148, 252])
    screen.blit(myimage3, [148, 398])
    pygame.display.flip()
    global speed
    while True:
        for event in pygame.event.get():  # 获得事件
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and 106 <= event.pos[1] <= 202 and \
                    148 <= event.pos[0] <= 452:  # 判断鼠标位置以及是否摁了下去。
                speed = 5
                body()
            elif event.type == pygame.MOUSEBUTTONDOWN and 252 <= event.pos[1] <= 348 and \
                    148 <= event.pos[0] <= 452:
                speed = 10
                body()
            elif event.type == pygame.MOUSEBUTTONDOWN and 398 <= event.pos[1] <= 494 and \
                    148 <= event.pos[0] <= 452:
                speed = 20
                body()

main()
