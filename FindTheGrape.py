import sys
import time
import random
import pygame
import os

class pacerSprite(pygame.sprite.Sprite):
    def __init__(self, img_path, size, position):
        pygame.sprite.Sprite.__init__(self)
        try:
            self.image = pygame.image.load(img_path)
            self.image = pygame.transform.smoothscale(self.image, size)
        except pygame.error as e:
            print(f"无法加载图片 {img_path}: {e}")
            sys.exit()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.type = img_path.split('/')[-1].split('.')[0]
        self.fixed = False

    def setPosition(self, position):
        self.rect.left, self.rect.top = position

class pacerGame():
    def __init__(self, screen, sounds, font, pacer_imgs):
        self.screen = screen
        self.sounds = sounds
        self.font = font
        self.pacer_imgs = pacer_imgs
        self.reset()
        self.game_time = 60  # 设置游戏时间为60秒
        
    def start(self):
        clock = pygame.time.Clock()
        selected_img1 = None
        selected_img2 = None
        time_pre = int(time.time())
        game_over = False  # 初始化 game_over 变量

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    position = pygame.mouse.get_pos()
                    if selected_img1 is None:
                        selected_img1 = self.checkSelected(position)
                    else:
                        selected_img2 = self.checkSelected(position)
                        if selected_img2 is not None:
                            if self.checkMatch(selected_img1, selected_img2):
                                self.removeImages(selected_img1, selected_img2)
                                if self.sounds['match']:
                                    random.choice(self.sounds['match']).play()
                                selected_img1 = None
                                selected_img2 = None
                            else:
                                if self.sounds['mismatch']:
                                    self.sounds['mismatch'].play()
                                selected_img1 = None

            # 检查是否所有图片都已消除
            if len(self.all_pacers) == 0:
                game_over = True
                self.showResult("Congratulations! You Win!")

            # 更新屏幕
            self.screen.fill((135, 206, 235))
            self.pacers_group.draw(self.screen)

            # 显示得分
            score_text = "Score: " + str(self.score)
            score_render = self.font.render(score_text, 1, (255, 255, 255))
            score_rect = score_render.get_rect(topleft=(10, 10))
            self.screen.blit(score_render, score_rect)

            # 显示剩余时间
            time_elapsed = int(time.time()) - time_pre
            time_left = max(self.game_time - time_elapsed, 0)
            time_text = "Time Left: " + str(time_left)
            time_render = self.font.render(time_text, 1, (255, 255, 255))
            time_rect = time_render.get_rect(topright=(self.screen.get_width() - 10, 10))
            self.screen.blit(time_render, time_rect)

            pygame.display.update()
            clock.tick(30)
            current_time = int(time.time())
            if current_time - time_pre > self.game_time:
                game_over = True

        self.showResult()

    def draw_button(self, text, rect):
        button_color = (255, 255, 0)  # 黄色
        text_color = (0, 0, 0)  # 黑色
        pygame.draw.rect(self.screen, button_color, rect)
        text_render = self.font.render(text, 1, text_color)
        text_rect = text_render.get_rect(center=(rect[0] + rect[2] // 2, rect[1] + rect[3] // 2))
        self.screen.blit(text_render, text_rect)
        return rect  # 返回一个pygame.Rect对象

    def showResult(self, win_text="Game Over!"):
        try:
            # 加载结束页面的背景图片
            background = pygame.image.load(os.path.join(r"C:\Users\86183\Desktop\software\-\res\imgs\结束背景.png"))
            background = pygame.transform.scale(background, self.screen.get_size())
        except pygame.error as e:
            print(f"无法加载结束页面背景图片: {e}")
            background = None

        self.screen.fill((135, 206, 235))  # 用默认颜色填充屏幕，以防图片加载失败
        if background:
            self.screen.blit(background, (0, 0))  # 显示背景图片

        # 设置字体为加粗并渲染文本
        bold_font = pygame.font.Font(None, 36)  # 假设系统有默认的加粗字体，否则需要指定具体路径
        bold_font.set_bold(True)  # 设置字体为加粗

        # 分行显示文本
        win_text_render = bold_font.render(win_text, 1, (0, 0, 0))  # 黑色
        final_score_text = "Final Score: " + str(self.score)
        final_score_render = bold_font.render(final_score_text, 1, (0, 0, 0))  # 黑色

        # 计算文本位置
        win_text_rect = win_text_render.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 - 50))
        final_score_rect = final_score_render.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 + 20))

        self.screen.blit(win_text_render, win_text_rect)
        self.screen.blit(final_score_render, final_score_rect)

        # 绘制按钮
        restart_rect = pygame.Rect(self.screen.get_width() / 2 - 75, self.screen.get_height() / 2 + 100, 150, 50)
        quit_rect = pygame.Rect(self.screen.get_width() / 2 - 75, self.screen.get_height() / 2 + 160, 150, 50)

        self.draw_button("Restart", restart_rect)
        self.draw_button("Quit", quit_rect)

        pygame.display.update()
        mouse_x, mouse_y = 0, 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_x, mouse_y = event.pos
                    if restart_rect.collidepoint((mouse_x, mouse_y)):
                        self.reset()
                        return self.start()  # 重新开始游戏
                    elif quit_rect.collidepoint((mouse_x, mouse_y)):
                        pygame.quit()
                        sys.exit()
                        
    def reset(self):
        self.all_pacers = []
        self.pacers_group = pygame.sprite.Group()
        # 确保图片总数是偶数
        num_pacers = 24  # 你可以根据需要调整这个数字，但必须是偶数
        for _ in range(num_pacers // 2):
            img_path = random.choice(self.pacer_imgs)
            size = (64, 64)
            position1 = (random.randint(0, 700 - 64), random.randint(0, 700 - 64))
            position2 = (random.randint(0, 700 - 64), random.randint(0, 700 - 64))
            pacer1 = pacerSprite(img_path, size, position1)
            pacer2 = pacerSprite(img_path, size, position2)
            self.all_pacers.append(pacer1)
            self.all_pacers.append(pacer2)
            self.pacers_group.add(pacer1)
            self.pacers_group.add(pacer2)
        self.score = 0
        
    def checkSelected(self, position):
        for pacer in self.all_pacers:
            if pacer.rect.collidepoint(position):
                return pacer
        return None

    def checkMatch(self, img1, img2):
        if img1 is None or img2 is None:
            return False
        return img1.type == img2.type and img1 is not img2

    def removeImages(self, img1, img2):
        self.pacers_group.remove(img1)
        self.pacers_group.remove(img2)
        self.all_pacers.remove(img1)
        self.all_pacers.remove(img2)
        self.score += 20  # Increment score

        # 检查是否只剩下最后两张图片
        if len(self.all_pacers) == 0:
            self.showResult("Congratulations! You Win!")
        else:
            # 清除所有图片
            '''for pacer in self.all_pacers:
                self.pacers_group.remove(pacer)
                self.all_pacers.remove(pacer)'''

def main():
    pygame.init()
    screen = pygame.display.set_mode((700, 700))
    pygame.display.set_caption('Grape Wanted')

    sounds = {}
    try:
        sounds['mismatch'] = pygame.mixer.Sound("错误.mp3")
        sounds['match'] = [pygame.mixer.Sound("正确.mp3")]
    except pygame.error as e:
        print(f"无法加载音效: {e}")
        sys.exit()

    font = pygame.font.Font(None, 36)

    pacer_imgs = ["pacer1.webp", "pacer2.webp", "pacer3.webp", "pacer4.webp", "pacer5.webp"]
    game = pacerGame(screen, sounds, font, pacer_imgs)
    game.start()

if __name__ == '__main__':
    main()