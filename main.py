import os
import sys
import pygame
from FindTheGrape import pacerGame

# 屏幕设置大小
SCREENSIZE = (700, 700)
# 元素尺寸
NUMGRID = 8
GRIDSIZE = 64
XMARGIN = (SCREENSIZE[0] - GRIDSIZE * NUMGRID) // 2
YMARGIN = (SCREENSIZE[1] - GRIDSIZE * NUMGRID) // 2
# 获取根目录
ROOTDIR = os.getcwd()
# FPS
FPS = 30

'''主程序'''
def main():
    pygame.init()  # 初始化pygame
    pygame.mixer.init()  # 初始化混音器模块
    screen = pygame.display.set_mode(SCREENSIZE)  # 设置显示模式
    font = pygame.font.Font(None, 36)

    # 定义 pacer_imgs 变量，包含所有游戏使用的图片路径
    pacer_imgs = [os.path.join(ROOTDIR, "res/imgs/pacer1.webp"),
                  os.path.join(ROOTDIR, "res/imgs/pacer2.webp"),
                  os.path.join(ROOTDIR, "res/imgs/pacer3.webp"),
                  os.path.join(ROOTDIR, "res/imgs/pacer4.webp"),
                  os.path.join(ROOTDIR, "res/imgs/pacer5.webp")]

    # 创建主菜单实例
    main_menu = MainMenu(screen, font)

    # 显示主菜单
    while main_menu.handle_events():
        main_menu.draw()

    # 主菜单结束后，开始游戏
    pygame.mixer.music.load(os.path.join(ROOTDIR, "res/audios/music.mp3"))
    pygame.mixer.music.set_volume(0.6)
    pygame.mixer.music.play(-1)

    sounds = {}
    try:
        sounds['mismatch'] = pygame.mixer.Sound(os.path.join(ROOTDIR, "res/audios/错误.mp3"))
        sounds['match'] = []
        for i in range(2):
            sounds['match'].append(pygame.mixer.Sound(os.path.join(ROOTDIR, f"res/audios/正确{i}.mp3")))
    except pygame.error as e:
        print(f"无法加载音效: {e}")
        sys.exit()

    # 确保 pacer_imgs 已经定义，然后创建游戏实例
    game = pacerGame(screen, sounds, font, pacer_imgs)
    game.start()

class MainMenu:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.running = True
        self.text_rect = None  # 初始化 text_rect 属性

    def draw(self):
        self.screen.fill((0, 0, 0))  # 填充背景色
        pygame.display.set_caption('Grape Wanted - Main Menu')

        # 加载背景图片
        try:
            background = pygame.image.load(os.path.join(ROOTDIR, "res/imgs/主界面背景.webp"))
            background = pygame.transform.scale(background, self.screen.get_size())
            self.screen.blit(background, (0, 0))
        except pygame.error as e:
            print(f"无法加载背景图片: {e}")

        # 绘制文本框
        text = "GameStart"
        text_render = self.font.render(text, True, (0, 0, 0))  # 文本颜色改为黑色
        self.text_rect = text_render.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 + 150))  # 下移150像素
        pygame.draw.rect(self.screen, (255, 255, 0), self.text_rect.inflate(40, 20), 0)  # 填充黄色
        self.screen.blit(text_render, self.text_rect)

        pygame.display.flip()  # 确保在绘制后更新屏幕

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.text_rect and self.text_rect.collidepoint(event.pos):
                    self.running = False  # 点击文本框后退出主菜单

        return self.running

'''游戏运行'''
if __name__ == '__main__':
    main()