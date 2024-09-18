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
    lines = win_text.split(' ')
    final_score_text = "Final Score: " + str(self.score)
    line1 = " ".join(lines[0:-1])  # 除了最后一个单词，其他所有单词为第一行
    line2 = lines[-1] + " " + final_score_text  # 最后一个单词和分数为第二行

    line1_render = bold_font.render(line1, 1, (0, 0, 0))  # 黑色
    line2_render = bold_font.render(line2, 1, (0, 0, 0))  # 黑色

    # 计算文本位置
    line1_rect = line1_render.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 - 50))
    line2_rect = line2_render.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 + 20))

    self.screen.blit(line1_render, line1_rect)
    self.screen.blit(line2_render, line2_rect)

    # 绘制按钮
    restart_rect = pygame.Rect(self.screen.get_width() / 2 - 75, self.screen.get_height() / 2 + 100, 150, 50)
    quit_rect = pygame.Rect(self.screen.get_width() / 2 - 75, self.screen.get_height() / 2 + 160, 150, 50)

    self.draw_button("Restart", restart_rect)
    self.draw_button("Quit", quit_rect)

    pygame.display.update()
    mouse_x, mouse_y = 0, 0  # 初始化鼠标位置变量
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos  # 更新鼠标位置
                if restart_rect.collidepoint((mouse_x, mouse_y)):
                    self.reset()
                    return self.start()  # 重新开始游戏
                elif quit_rect.collidepoint((mouse_x, mouse_y)):
                    pygame.quit()
                    sys.exit()