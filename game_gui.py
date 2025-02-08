import pygame
import sys
from nail_game import NailGame
from level_configs import LEVELS, NailType

class GameGUI:
    def __init__(self):
        """
        初始化游戏GUI
        """
        # 1. 基础初始化
        pygame.init()
        self.init_display()
        self.init_fonts()
        self.init_colors()
        
        # 2. 游戏核心属性
        self.init_game_properties()
        
        # 3. UI相关属性
        self.init_ui_properties()
        
        # 4. 计算初始位置
        self.calculate_nail_positions()

    def init_display(self):
        """初始化显示相关"""
        self.screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
        pygame.display.set_caption("拔钉子游戏")

    def init_fonts(self):
        """初始化字体"""
        self.title_font = pygame.font.SysFont("SimHei", 48)
        self.info_font = pygame.font.SysFont("SimHei", 36)
        self.text_font = pygame.font.SysFont("SimHei", 24)

    def init_colors(self):
        """初始化颜色"""
        self.COLORS = {
            'WHITE': (255, 255, 255),
            'BLACK': (0, 0, 0),
            'GRAY': (128, 128, 128),
            'RED': (255, 0, 0)
        }

    def init_game_properties(self):
        """初始化游戏相关属性"""
        # 缩放属性
        self.scale = 50
        self.min_scale = 20
        self.max_scale = 100
        self.scale_step = 5
        
        # 游戏核心属性
        self.NAIL_RADIUS = 20
        self.current_level = 1
        self.game = NailGame(self.current_level)
        
        # 虚拟表面
        self.virtual_width = 2000
        self.virtual_height = 1500
        self.virtual_surface = pygame.Surface((self.virtual_width, self.virtual_height))
        
        # 钉子位置
        self.nail_positions = {}

    def init_ui_properties(self):
        """初始化UI相关属性"""
        # 滚动属性
        self.scroll_x = 0
        self.scroll_y = 0
        self.scrollbar_width = 20
        self.is_dragging_h = False
        self.is_dragging_v = False
        self.scroll_start_x = 0
        self.scroll_start_y = 0
        
        # 滚动条颜色
        self.scrollbar_color = (200, 200, 200)  # 默认颜色
        self.scrollbar_hover_color = (180, 180, 180)  # 鼠标悬停时的颜色
        self.scrollbar_drag_color = (160, 160, 160)   # 拖动时的颜色
        
        # 帮助窗口
        self.help_window = {
            'visible': False,
            'color': (240, 240, 240),
            'border_color': (100, 100, 100),
            'title': "游戏规则说明",
            'scroll_y': 0,
            'scroll_speed': 20,
            'content_padding': 30,
            'line_height': 25
        }
        
        # 关卡选择
        self.level_select_visible = False
        self.level_buttons = []
        
        # 按钮样式
        self.button_style = {
            'width': 150,
            'height': 40,
            'padding': 10,
            'color': (180, 180, 180),
            'hover_color': (160, 160, 160)
        }
        
        # 固定按钮
        self.fixed_buttons = {
            'add_stack': {
                'text': "增加新栈",
                'color': self.button_style['color'],
                'hover_color': self.button_style['hover_color']
            },
            'help': {
                'text': "游戏说明",
                'color': self.button_style['color'],
                'hover_color': self.button_style['hover_color']
            },
            'level_select': {
                'text': "选择关卡",
                'color': self.button_style['color'],
                'hover_color': self.button_style['hover_color']
            }
        }
        
        # 更新关卡按钮
        self.update_level_buttons()

    def calculate_nail_positions(self):
        """
        计算所有钉子的位置，考虑缩放因子
        """
        self.nail_positions = {}
        base_x = 100
        base_y = 150

        # 使用当前缩放因子计算位置
        for nail_id, pos in self.game.level_config.nail_positions.items():
            x = base_x + pos[0] * self.scale
            y = base_y + pos[1] * self.scale
            self.nail_positions[nail_id] = (x, y)

        # 更新虚拟表面的大小
        max_x = max(x for x, y in self.nail_positions.values()) + 200
        max_y = max(y for x, y in self.nail_positions.values()) + 200
        self.virtual_width = max(self.screen.get_width(), max_x)
        self.virtual_height = max(self.screen.get_height(), max_y)

        # 重新创建虚拟表面
        self.virtual_surface = pygame.Surface((self.virtual_width, self.virtual_height))

    def draw_nails(self):
        """
        在虚拟surface上绘制钉子和连接线
        """
        # 添加钉子区域标题
        title = self.info_font.render("钉子区域", True, self.COLORS['BLACK'])
        self.virtual_surface.blit(title, (100, 100))

        # 绘制依赖关系线
        for nail_id, nail in self.game.nails.items():
            if nail_id in self.nail_positions and nail.dependencies:
                for dep in nail.dependencies:
                    if dep.id in self.nail_positions:
                        start_pos = self.nail_positions[nail_id]
                        end_pos = self.nail_positions[dep.id]
                        pygame.draw.line(self.virtual_surface, self.COLORS['GRAY'],
                                       start_pos, end_pos, 2)

        # 绘制钉子
        for nail_id, pos in self.nail_positions.items():
            if nail_id in self.game.nails:  # 确保钉子存在
                nail = self.game.nails[nail_id]
                if not nail.is_removed:
                    color = NailType.get_color(nail.nail_type)
                    if not self.game.can_remove(nail_id):
                        color = tuple(max(0, c - 100) for c in color)
                    pygame.draw.circle(self.virtual_surface, color, pos, self.NAIL_RADIUS)

                    text = self.text_font.render(str(nail_id), True, self.COLORS['WHITE'])
                    text_rect = text.get_rect(center=pos)
                    self.virtual_surface.blit(text, text_rect)

    def draw_stacks(self):
        """
        在虚拟surface上绘制所有栈
        """
        start_x = 650
        start_y = 150
        stack_width = 150
        stack_height = 300
        spacing = 20

        # 绘制栈区域标题
        title = self.info_font.render("栈区域", True, self.COLORS['BLACK'])
        self.virtual_surface.blit(title, (start_x, start_y - 100))

        for i, stack in enumerate(self.game.stacks):
            stack_x = start_x + i * (stack_width + spacing)

            # 绘制栈的边框
            pygame.draw.rect(self.virtual_surface, self.COLORS['GRAY'],
                           (stack_x, start_y, stack_width, stack_height), 2)

            # 绘制栈中的钉子
            for j, nail in enumerate(stack.items):
                y_pos = start_y + 50 + j * 60
                color = NailType.get_color(nail.nail_type)
                pygame.draw.circle(self.virtual_surface, color,
                                 (stack_x + stack_width//2, y_pos), self.NAIL_RADIUS)

                text = self.text_font.render(str(nail.id), True, self.COLORS['WHITE'])
                text_rect = text.get_rect(center=(stack_x + stack_width//2, y_pos))
                self.virtual_surface.blit(text, text_rect)

            # 绘制栈信息
            stack_info = f"栈 {i+1}: {len(stack.items)}/{self.game.level_config.stack_size}"
            text = self.info_font.render(stack_info, True, self.COLORS['BLACK'])
            self.virtual_surface.blit(text, (stack_x, start_y - 40))

            if stack.current_type:
                type_text = f"当前类型: {stack.current_type}"
                text = self.text_font.render(type_text, True, self.COLORS['BLACK'])
                self.virtual_surface.blit(text, (stack_x, start_y - 70))

    def draw_help_window(self):
        """
        在屏幕上直接绘制可滚动的帮助窗口
        """
        if not self.help_window['visible']:
            return

        # 绘制半透明背景
        overlay = pygame.Surface(self.screen.get_size())
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))

        # 计算帮助窗口在屏幕中央的位置
        screen_width, screen_height = self.screen.get_size()
        window_width = 700  # 增加宽度
        window_height = 500  # 增加高度
        window_x = (screen_width - window_width) // 2
        window_y = (screen_height - window_height) // 2

        # 更新帮助窗口的位置
        self.help_window['rect'] = pygame.Rect(window_x, window_y, window_width, window_height)
        self.help_window['close_button'] = pygame.Rect(
            window_x + window_width - 40,
            window_y + 10,
            30, 30
        )

        # 创建帮助窗口的surface
        help_surface = pygame.Surface((window_width, window_height))
        help_surface.fill(self.help_window['color'])

        # 绘制标题
        title = self.info_font.render(self.help_window['title'],
                                    True, self.COLORS['BLACK'])
        title_rect = title.get_rect(
            midtop=(window_width // 2, 20)
        )
        help_surface.blit(title, title_rect)

        # 准备说明文字
        tips = [
            "1. 游戏目标：",
            "   - 按正确顺序拔出所有钉子",
            "   - 遵循依赖关系，只能拔出没有依赖的钉子",
            "",
            "2. 栈规则：",
            "   - 拔出的钉子必须放入栈中",
            "   - 相同颜色的钉子才能放入同一个栈",
            "   - 每个栈有容量限制",
            "   - 栈满时会自动清空",
            "   - 可以增加新的栈继续游戏",
            "",
            "3. 操作说明：",
            "   - 点击钉子进行拔除",
            "   - 点击'增加新栈'按钮添加栈",
            "   - 使用滚动条或鼠标滚轮查看内容",
            "   - F11 切换全屏显示",
            "",
            "4. 游戏结束条件：",
            "   - 成功：所有钉子都被正确拔出",
            "   - 失败：拔出的钉子无法放入任何栈",
            "",
            "5. 界面操作：",
            "   - 可以调整窗口大小",
            "   - 使用滚动条查看完整内容",
            "   - ESC键关闭帮助窗口",
            "",
            "6. 颜色规则：",
            "   - 红色钉子：基础型",
            "   - 蓝色钉子：支撑型",
            "   - 绿色钉子：连接型",
            "   - 黄色钉子：特殊型",
            "   - 紫色钉子：终结型"
        ]

        # 计算内容总高度
        content_height = len(tips) * self.help_window['line_height']

        # 绘制说明文字
        y = 70 - self.help_window['scroll_y']  # 从标题下方开始
        padding = self.help_window['content_padding']

        for tip in tips:
            if -self.help_window['line_height'] <= y <= window_height:
                text = self.text_font.render(tip, True, self.COLORS['BLACK'])
                text_rect = text.get_rect(x=padding, y=y)
                help_surface.blit(text, text_rect)
            y += self.help_window['line_height']

        # 绘制滚动条（如果内容超出窗口）
        if content_height > window_height - 90:  # 90是标题和边距的高度
            scrollbar_height = int((window_height / content_height) * (window_height - 90))
            scrollbar_pos = int((self.help_window['scroll_y'] / content_height) * window_height)
            pygame.draw.rect(help_surface, (180, 180, 180),
                           (window_width - 20, 70, 10, window_height - 90))
            pygame.draw.rect(help_surface, (100, 100, 100),
                           (window_width - 20, 70 + scrollbar_pos, 10, scrollbar_height))

        # 绘制边框
        pygame.draw.rect(help_surface, self.help_window['border_color'],
                        (0, 0, window_width, window_height), 2)

        # 绘制关闭按钮
        pygame.draw.rect(help_surface, (200, 100, 100),
                        (window_width - 40, 10, 30, 30))
        close_text = self.text_font.render("×", True, self.COLORS['WHITE'])
        close_rect = close_text.get_rect(center=(window_width - 25, 25))
        help_surface.blit(close_text, close_rect)

        # 将帮助窗口surface绘制到屏幕上
        self.screen.blit(help_surface, (window_x, window_y))

    def get_button_rect(self, button_name):
        """
        获取固定按钮的位置
        """
        screen_width = self.screen.get_width()

        positions = {
            'add_stack': (screen_width - self.button_style['width'] - 20 - self.scrollbar_width, 10),
            'help': (20, 10),
            'level_select': (20, 10 + self.button_style['height'] + self.button_style['padding'])
        }

        x, y = positions[button_name]
        return pygame.Rect(x, y, self.button_style['width'], self.button_style['height'])

    def draw_fixed_buttons(self):
        """
        绘制所有固定位置的按钮
        """
        mouse_pos = pygame.mouse.get_pos()

        for name, button in self.fixed_buttons.items():
            rect = self.get_button_rect(name)
            # 检查鼠标悬停
            color = button['hover_color'] if rect.collidepoint(mouse_pos) else button['color']

            # 绘制按钮
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, (100, 100, 100), rect, 2)

            # 绘制文字
            text = self.info_font.render(button['text'], True, self.COLORS['BLACK'])
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

    def update_level_buttons(self):
        """
        更新关卡按钮列表
        """
        self.level_buttons = []
        button_width = 500
        button_height = 80
        padding = 20

        for level_num, level_config in LEVELS.items():
            self.level_buttons.append({
                'rect': pygame.Rect(0, 0, button_width, button_height),  # 位置将在绘制时计算
                'level': level_num,
                'text': f"第{level_num}关: {level_config.description}",
                'color': (200, 200, 200),
                'hover_color': (180, 180, 180)
            })

    def draw_level_select(self):
        """
        绘制关卡选择界面
        """
        if not self.level_select_visible:
            return

        # 绘制半透明背景
        overlay = pygame.Surface(self.screen.get_size())
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))

        # 计算关卡选择窗口的大小和位置
        screen_width, screen_height = self.screen.get_size()
        window_width = 600
        window_height = len(self.level_buttons) * 100 + 100
        window_x = (screen_width - window_width) // 2
        window_y = (screen_height - window_height) // 2

        # 绘制窗口背景
        pygame.draw.rect(self.screen, (240, 240, 240),
                        (window_x, window_y, window_width, window_height))
        pygame.draw.rect(self.screen, (100, 100, 100),
                        (window_x, window_y, window_width, window_height), 2)

        # 绘制标题
        title = self.title_font.render("选择关卡", True, self.COLORS['BLACK'])
        title_rect = title.get_rect(
            midtop=(window_x + window_width // 2, window_y + 20)
        )
        self.screen.blit(title, title_rect)

        # 绘制关卡按钮
        for i, button in enumerate(self.level_buttons):
            button['rect'].x = window_x + 50
            button['rect'].y = window_y + 80 + i * 100

            # 检查鼠标悬停
            mouse_pos = pygame.mouse.get_pos()
            color = button['hover_color'] if button['rect'].collidepoint(mouse_pos) else button['color']

            # 绘制按钮
            pygame.draw.rect(self.screen, color, button['rect'])
            pygame.draw.rect(self.screen, (100, 100, 100), button['rect'], 2)

            # 绘制关卡文本
            text = self.info_font.render(button['text'], True, self.COLORS['BLACK'])
            text_rect = text.get_rect(center=button['rect'].center)
            self.screen.blit(text, text_rect)

            # 如果是当前关卡，添加标记
            if button['level'] == self.current_level:
                current_text = self.text_font.render("当前关卡", True, (0, 150, 0))
                self.screen.blit(current_text,
                               (button['rect'].right - 100, button['rect'].centery - 10))

        # 绘制关闭按钮
        close_button = pygame.Rect(window_x + window_width - 40, window_y + 10, 30, 30)
        pygame.draw.rect(self.screen, (200, 100, 100), close_button)
        close_text = self.text_font.render("×", True, self.COLORS['WHITE'])
        close_rect = close_text.get_rect(center=close_button.center)
        self.screen.blit(close_text, close_rect)

        # 存储关闭按钮位置供点击检测使用
        self.level_select_close_button = close_button

    def draw_buttons(self):
        """
        在屏幕上绘制所有按钮
        """
        # 绘制原有按钮
        # ... 原有的按钮绘制代码 ...

        # 绘制关卡选择按钮
        level_select_rect = self.get_button_rect('level_select')
        pygame.draw.rect(self.screen,
                        self.button_style['color'],
                        level_select_rect)
        text = self.info_font.render(self.button_style['text'],
                                   True, self.COLORS['BLACK'])
        text_rect = text.get_rect(center=level_select_rect.center)
        self.screen.blit(text, text_rect)

    def draw_info(self):
        """
        绘制游戏信息和说明文字
        """
        # 绘制标题
        title = self.title_font.render(
            f"第{self.current_level}关: {self.game.level_config.description}",
            True, self.COLORS['BLACK']
        )
        self.virtual_surface.blit(title, (50, 20))

        # 绘制当前玩家
        player_text = self.info_font.render(
            f"当前玩家: {self.game.current_player}",
            True, self.COLORS['BLACK']
        )
        self.virtual_surface.blit(player_text, (300, 50))

        # 绘制提示信息
        info_y = self.info_area['y']
        tips = [
            "游戏说明:",
            "- 使用鼠标拖动窗口边缘可调整窗口大小",
            "- 使用滚动条或鼠标滚轮查看完整内容",
            "- F11 切换全屏显示",
            "- 点击钉子进行操作",
            "- 点击'增加新栈'按钮添加新的栈",
            f"- 每个栈容量: {self.game.level_config.stack_size}",
            f"- 当前栈数量: {len(self.game.stacks)}",
            "- 相同颜色的钉子才能放入同一个栈",
            "- 栈满时会自动清空"
        ]

        # 绘制半透明背景
        info_height = len(tips) * self.info_area['line_height']
        info_surface = pygame.Surface((600, info_height))
        info_surface.fill((255, 255, 255))
        info_surface.set_alpha(200)
        self.virtual_surface.blit(info_surface, (self.info_area['x'] - 10, info_y - 10))

        # 绘制说明文字
        for tip in tips:
            text = self.text_font.render(tip, True, self.COLORS['BLACK'])
            self.virtual_surface.blit(text, (self.info_area['x'], info_y))
            info_y += self.info_area['line_height']

    def handle_click(self, pos):
        """
        处理点击事件
        """
        # 如果帮助窗口可见，优先处理其点击
        if self.help_window['visible']:
            if self.help_window['close_button'].collidepoint(pos):
                self.help_window['visible'] = False
                return
            if not self.help_window['rect'].collidepoint(pos):
                self.help_window['visible'] = False
            return

        # 如果关卡选择界面可见，优先处理其点击
        if self.level_select_visible:
            if hasattr(self, 'level_select_close_button') and \
               self.level_select_close_button.collidepoint(pos):
                self.level_select_visible = False
                return

            for button in self.level_buttons:
                if button['rect'].collidepoint(pos):
                    # 修改这里：直接使用关卡配置
                    level_num = button['level']
                    if level_num in LEVELS:
                        self.current_level = level_num
                        self.game = NailGame(level_num)  # 只传入关卡编号
                        self.calculate_nail_positions()
                        self.level_select_visible = False
                    return

            if not any(button['rect'].collidepoint(pos) for button in self.level_buttons):
                self.level_select_visible = False
            return

        # 处理固定按钮的点击
        for name, button in self.fixed_buttons.items():
            if self.get_button_rect(name).collidepoint(pos):
                if name == 'add_stack':
                    self.game.add_stack()
                elif name == 'help':
                    self.help_window['visible'] = True
                elif name == 'level_select':
                    self.level_select_visible = True
                return

        # 对于游戏元素的点击，需要考虑滚动偏移
        adjusted_pos = (pos[0] + self.scroll_x, pos[1] + self.scroll_y)

        # 检查是否点击了钉子
        for nail_id, nail_pos in self.nail_positions.items():
            distance = ((adjusted_pos[0] - nail_pos[0]) ** 2 +
                       (adjusted_pos[1] - nail_pos[1]) ** 2) ** 0.5
            if distance <= self.NAIL_RADIUS:
                if self.game.remove_nail(nail_id):
                    if self.game.is_level_complete():
                        self.handle_level_complete()
                elif self.game.game_over:
                    self.handle_game_over()
                return

    def handle_level_complete(self):
        """
        处理关卡完成事件
        """
        if self.current_level < len(LEVELS):
            self.current_level += 1
            self.game = NailGame(self.current_level)
            self.calculate_nail_positions()
        else:
            print("恭喜通关！")
            pygame.quit()
            sys.exit()

    def handle_game_over(self):
        """
        处理游戏结束
        """
        print("游戏结束！无法放入栈中")
        pygame.quit()
        sys.exit()

    def update_scrollbars(self):
        """
        更新滚动条位置和大小
        """
        screen_width, screen_height = self.screen.get_size()

        # 水平滚动条
        h_scrollbar_width = max(50, int((screen_width / self.virtual_width) * (screen_width - self.scrollbar_width)))
        self.h_scrollbar_rect = pygame.Rect(
            int((self.scroll_x / self.virtual_width) * (screen_width - self.scrollbar_width)),
            screen_height - self.scrollbar_width,
            h_scrollbar_width,
            self.scrollbar_width
        )

        # 垂直滚动条
        v_scrollbar_height = max(50, int((screen_height / self.virtual_height) * (screen_height - self.scrollbar_width)))
        self.v_scrollbar_rect = pygame.Rect(
            screen_width - self.scrollbar_width,
            int((self.scroll_y / self.virtual_height) * (screen_height - self.scrollbar_width)),
            self.scrollbar_width,
            v_scrollbar_height
        )

    def handle_scroll(self, event):
        """
        处理滚动事件
        """
        screen_width, screen_height = self.screen.get_size()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # 检查是否点击滚动条
            if event.button == 1:
                if self.h_scrollbar_rect.collidepoint(event.pos):
                    self.is_dragging_h = True
                    self.scroll_start_x = event.pos[0] - self.h_scrollbar_rect.x
                elif self.v_scrollbar_rect.collidepoint(event.pos):
                    self.is_dragging_v = True
                    self.scroll_start_y = event.pos[1] - self.v_scrollbar_rect.y

            # 鼠标滚轮滚动
            elif event.button == 4:  # 向上滚动
                self.scroll_y = max(0, self.scroll_y - 30)
            elif event.button == 5:  # 向下滚动
                self.scroll_y = min(self.virtual_height - screen_height, self.scroll_y + 30)

        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_dragging_h = False
            self.is_dragging_v = False

        elif event.type == pygame.MOUSEMOTION:
            if self.is_dragging_h:
                new_x = event.pos[0] - self.scroll_start_x
                max_scroll = screen_width - self.h_scrollbar_rect.width - self.scrollbar_width
                new_x = max(0, min(new_x, max_scroll))
                self.scroll_x = int((new_x / max_scroll) * (self.virtual_width - screen_width))

            if self.is_dragging_v:
                new_y = event.pos[1] - self.scroll_start_y
                max_scroll = screen_height - self.v_scrollbar_rect.height - self.scrollbar_width
                new_y = max(0, min(new_y, max_scroll))
                self.scroll_y = int((new_y / max_scroll) * (self.virtual_height - screen_height))

    def handle_resize(self, event):
        """
        处理窗口大小调整
        """
        new_width = max(self.MIN_WIDTH, event.w)
        new_height = max(self.MIN_HEIGHT, event.h)
        self.screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
        self.update_scrollbars()

    def draw_scrollbars(self):
        """
        绘制滚动条，添加鼠标悬停和拖动效果
        """
        screen_width, screen_height = self.screen.get_size()
        mouse_pos = pygame.mouse.get_pos()
        
        # 水平滚动条
        if self.h_scrollbar_rect.collidepoint(mouse_pos):
            color = self.scrollbar_hover_color if not self.is_dragging_h else self.scrollbar_drag_color
        else:
            color = self.scrollbar_color
        pygame.draw.rect(self.screen, color, self.h_scrollbar_rect)
        
        # 垂直滚动条
        if self.v_scrollbar_rect.collidepoint(mouse_pos):
            color = self.scrollbar_hover_color if not self.is_dragging_v else self.scrollbar_drag_color
        else:
            color = self.scrollbar_color
        pygame.draw.rect(self.screen, color, self.v_scrollbar_rect)

    def handle_help_window_scroll(self, event):
        """
        处理帮助窗口的滚动
        """
        if not self.help_window['visible']:
            return False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # 向上滚动
                self.help_window['scroll_y'] = max(
                    0, 
                    self.help_window['scroll_y'] - self.help_window['scroll_speed']
                )
                return True
            elif event.button == 5:  # 向下滚动
                self.help_window['scroll_y'] = min(
                    500,  # 最大滚动距离
                    self.help_window['scroll_y'] + self.help_window['scroll_speed']
                )
                return True
        return False

    def handle_scale(self, event):
        """
        处理缩放事件
        """
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.key.get_mods() & pygame.KMOD_CTRL:
            # 获取当前鼠标位置
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # 转换为虚拟表面坐标
            virtual_x = mouse_x + self.scroll_x
            virtual_y = mouse_y + self.scroll_y
            
            old_scale = self.scale
            
            # 向上滚动放大，向下滚动缩小
            if event.button == 4:  # 滚轮向上
                self.scale = min(self.max_scale, self.scale + self.scale_step)
            elif event.button == 5:  # 滚轮向下
                self.scale = max(self.min_scale, self.scale - self.scale_step)
            
            # 如果缩放发生变化
            if old_scale != self.scale:
                # 记住缩放中心点（鼠标位置）相对于基准点的比例
                if self.nail_positions:
                    base_x, base_y = next(iter(self.nail_positions.values()))
                    rel_x = (virtual_x - base_x) / old_scale
                    rel_y = (virtual_y - base_y) / old_scale
                    
                    # 重新计算位置
                    self.calculate_nail_positions()
                    
                    # 调整滚动位置以保持鼠标指向的点不变
                    if self.nail_positions:
                        new_base_x, new_base_y = next(iter(self.nail_positions.values()))
                        new_x = new_base_x + rel_x * self.scale
                        new_y = new_base_y + rel_y * self.scale
                        
                        # 更新滚动位置
                        self.scroll_x += new_x - virtual_x
                        self.scroll_y += new_y - virtual_y
                        
                        # 确保滚动范围有效
                        self.clamp_scroll()
                return True
        return False

    def clamp_scroll(self):
        """
        确保滚动范围在有效范围内
        """
        screen_width, screen_height = self.screen.get_size()
        
        # 计算最大滚动范围
        max_scroll_x = max(0, self.virtual_width - screen_width + self.scrollbar_width)
        max_scroll_y = max(0, self.virtual_height - screen_height + self.scrollbar_width)
        
        # 限制滚动范围
        self.scroll_x = max(0, min(self.scroll_x, max_scroll_x))
        self.scroll_y = max(0, min(self.scroll_y, max_scroll_y))

    def draw_scale_info(self):
        """
        绘制当前缩放信息
        """
        scale_text = self.text_font.render(
            f"缩放: {int(self.scale/50*100)}%", 
            True, 
            self.COLORS['BLACK']
        )
        self.screen.blit(scale_text, (10, self.screen.get_height() - 30))

    def run(self):
        """
        运行游戏主循环
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.VIDEORESIZE:
                    self.handle_resize(event)
                elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                    # 优先处理缩放
                    if self.handle_scale(event):
                        continue
                    # 处理其他鼠标事件
                    self.handle_scroll(event)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        pygame.display.toggle_fullscreen()
                    elif event.key == pygame.K_ESCAPE and self.help_window['visible']:
                        self.help_window['visible'] = False

            # 清空虚拟表面
            self.virtual_surface.fill(self.COLORS['WHITE'])
            
            # 绘制游戏元素到虚拟表面
            self.draw_nails()
            self.draw_stacks()
            
            # 将虚拟表面的可见部分绘制到实际屏幕上
            screen_width, screen_height = self.screen.get_size()
            self.screen.fill(self.COLORS['WHITE'])
            self.screen.blit(
                self.virtual_surface,
                (0, 0),
                (self.scroll_x, self.scroll_y, 
                 screen_width - self.scrollbar_width, 
                 screen_height - self.scrollbar_width)
            )
            
            # 绘制滚动条
            self.update_scrollbars()
            self.draw_scrollbars()
            
            # 在最后绘制固定位置的按钮
            self.draw_fixed_buttons()
            
            # 在最后绘制帮助窗口，确保它在最上层
            if self.help_window['visible']:
                self.draw_help_window()
            
            # 在最后绘制关卡选择界面
            self.draw_level_select()
            
            # 在最后绘制缩放信息
            self.draw_scale_info()
            
            pygame.display.flip()

def main():
    game_gui = GameGUI()
    game_gui.run()

if __name__ == "__main__":
    main()
