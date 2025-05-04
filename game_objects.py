import pygame
import random


WHITE = (255, 255, 255)  # Белый
BLACK = (0, 0, 0)  # Черный
GRAY = (200, 200, 200)  # Серый
BLUE = (100, 150, 250)  # Синий
GREEN = (50, 200, 50)  # Зеленый
RED = (250, 50, 50)  # Красный
YELLOW = (255, 255, 0)  # Желтый
PURPLE = (128, 0, 128)  # Фиолетовый


class Ending:
    def __init__(self, ending_data, screen_size):
        self.frames = []
        self.current_frame = 0
        self.screen_size = screen_size
        self.text_start_time = pygame.time.get_ticks()
        self.frame_start_time = pygame.time.get_ticks()
        self.finished = False
        self.current_text_index = 0
        self.text_fully_revealed = False
        self.char_delay = 50  # Задержка между символами (мс)
        self.load_frames(ending_data)


    def load_frames(self, ending_data):
        for frame in ending_data:
            try:
                image = pygame.image.load(frame["image"]).convert_alpha()
                # Масштабируем изображение, сохраняя пропорции
                img_ratio = image.get_width() / image.get_height()
                screen_ratio = self.screen_size[0] / self.screen_size[1]

                if img_ratio > screen_ratio:
                    width = self.screen_size[0]
                    height = int(width / img_ratio)
                else:
                    height = self.screen_size[1]
                    width = int(height * img_ratio)

                image = pygame.transform.scale(image, (width, height))

                self.frames.append({
                    "image": image,
                    "text": frame["text"],
                    "duration": frame["duration"],
                    "image_pos": ((self.screen_size[0] - width) // 2,
                                  (self.screen_size[1] - height) // 2)
                })
            except Exception as e:
                print(f"Ошибка загрузки изображения {frame['image']}: {e}")
                dummy = pygame.Surface(self.screen_size)
                dummy.fill((0, 0, 0))
                self.frames.append({
                    "image": dummy,
                    "text": frame["text"],
                    "duration": frame["duration"],
                    "image_pos": (0, 0)
                })


    def update(self):
        if self.current_frame >= len(self.frames):
            self.finished = True
            return

        current_time = pygame.time.get_ticks()
        if not self.text_fully_revealed:
            elapsed_time = current_time - self.text_start_time
            chars_to_show = int(elapsed_time / self.char_delay)
            total_chars = len(self.frames[self.current_frame]["text"])

            if chars_to_show >= total_chars:
                self.current_text_index = total_chars
                self.text_fully_revealed = True
            else:
                self.current_text_index = chars_to_show


    def draw(self, surface):
        if self.finished or self.current_frame >= len(self.frames):
            return

        # Заполняем фон черным
        surface.fill((0, 0, 0))

        # Отрисовка изображения
        current_frame = self.frames[self.current_frame]
        surface.blit(current_frame["image"], current_frame["image_pos"])

        # Создаем полупрозрачное затемнение для текста
        text_overlay = pygame.Surface((self.screen_size[0], 150))
        text_overlay.fill((0, 0, 0))
        text_overlay.set_alpha(180)
        surface.blit(text_overlay, (0, self.screen_size[1] - 150))

        # Отрисовка текста
        current_text = current_frame["text"][:self.current_text_index]
        font = pygame.font.Font(None, 36)

        # Разбиваем текст на строки
        words = current_text.split()
        lines = []
        current_line = []

        for word in words:
            current_line.append(word)
            test_line = ' '.join(current_line)
            if font.size(test_line)[0] > self.screen_size[0] - 40:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
        lines.append(' '.join(current_line))

        # Отрисовка строк текста
        y_offset = self.screen_size[1] - 130
        for line in lines:
            text_surface = font.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.screen_size[0] / 2, y_offset))
            surface.blit(text_surface, text_rect)
            y_offset += 30

        # Индикатор продолжения
        if self.text_fully_revealed:
            indicator_text = font.render("Нажмите любую клавишу для продолжения...", True, (200, 200, 200))
            indicator_rect = indicator_text.get_rect(center=(self.screen_size[0] / 2, self.screen_size[1] - 30))
            surface.blit(indicator_text, indicator_rect)


    def next_frame(self):
        if not self.text_fully_revealed:
            self.text_fully_revealed = True
            self.current_text_index = len(self.frames[self.current_frame]["text"])
            return True

        if self.current_frame < len(self.frames) - 1:
            self.current_frame += 1
            self.text_start_time = pygame.time.get_ticks()
            self.frame_start_time = pygame.time.get_ticks()
            self.text_fully_revealed = False
            self.current_text_index = 0
            return True

        self.finished = True
        return False


    def is_finished(self):
        return self.finished


class Event:
    def __init__(self, event_data, screen_size):
        self.frames = []
        self.current_frame = 0
        self.screen_size = screen_size
        self.text_start_time = pygame.time.get_ticks()
        self.frame_start_time = pygame.time.get_ticks()
        self.finished = False
        self.current_text_index = 0
        self.text_fully_revealed = False
        self.char_delay = 50  # Задержка между символами (мс)
        self.load_frames(event_data)


    def load_frames(self, event_data):
        for frame in event_data:
            try:
                image = pygame.image.load(frame["image"]).convert_alpha()
                # Масштабируем изображение, сохраняя пропорции
                img_ratio = image.get_width() / image.get_height()
                screen_ratio = self.screen_size[0] / self.screen_size[1]

                if img_ratio > screen_ratio:
                    width = self.screen_size[0]
                    height = int(width / img_ratio)
                else:
                    height = self.screen_size[1]
                    width = int(height * img_ratio)

                image = pygame.transform.scale(image, (width, height))

                self.frames.append({
                    "image": image,
                    "text": frame["text"],
                    "duration": frame["duration"],
                    "image_pos": ((self.screen_size[0] - width) // 2,
                                  (self.screen_size[1] - height) // 2)
                })
            except Exception as e:
                print(f"Ошибка загрузки изображения {frame['image']}: {e}")
                dummy = pygame.Surface(self.screen_size)
                dummy.fill((0, 0, 0))
                self.frames.append({
                    "image": dummy,
                    "text": frame["text"],
                    "duration": frame["duration"],
                    "image_pos": (0, 0)
                })


    def update(self):
        if self.current_frame >= len(self.frames):
            self.finished = True
            return

        current_time = pygame.time.get_ticks()
        if not self.text_fully_revealed:
            elapsed_time = current_time - self.text_start_time
            chars_to_show = int(elapsed_time / self.char_delay)
            total_chars = len(self.frames[self.current_frame]["text"])

            if chars_to_show >= total_chars:
                self.current_text_index = total_chars
                self.text_fully_revealed = True
            else:
                self.current_text_index = chars_to_show


    def draw(self, surface):
        if self.finished or self.current_frame >= len(self.frames):
            return

        # Заполняем фон черным
        surface.fill((0, 0, 0))

        # Отрисовка изображения
        current_frame = self.frames[self.current_frame]
        surface.blit(current_frame["image"], current_frame["image_pos"])

        # Создаем полупрозрачное затемнение для текста
        text_overlay = pygame.Surface((self.screen_size[0], 150))
        text_overlay.fill((0, 0, 0))
        text_overlay.set_alpha(180)
        surface.blit(text_overlay, (0, self.screen_size[1] - 150))

        # Отрисовка текста
        current_text = current_frame["text"][:self.current_text_index]
        font = pygame.font.Font(None, 36)

        # Разбиваем текст на строки
        words = current_text.split()
        lines = []
        current_line = []

        for word in words:
            current_line.append(word)
            test_line = ' '.join(current_line)
            if font.size(test_line)[0] > self.screen_size[0] - 40:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
        lines.append(' '.join(current_line))

        # Отрисовка строк текста
        y_offset = self.screen_size[1] - 130
        for line in lines:
            text_surface = font.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.screen_size[0] / 2, y_offset))
            surface.blit(text_surface, text_rect)
            y_offset += 30

        # Индикатор продолжения
        if self.text_fully_revealed:
            indicator_text = font.render("Нажмите любую клавишу для продолжения...", True, (200, 200, 200))
            indicator_rect = indicator_text.get_rect(center=(self.screen_size[0] / 2, self.screen_size[1] - 30))
            surface.blit(indicator_text, indicator_rect)


    def next_frame(self):
        if not self.text_fully_revealed:
            self.text_fully_revealed = True
            self.current_text_index = len(self.frames[self.current_frame]["text"])
            return True

        if self.current_frame < len(self.frames) - 1:
            self.current_frame += 1
            self.text_start_time = pygame.time.get_ticks()
            self.frame_start_time = pygame.time.get_ticks()
            self.text_fully_revealed = False
            self.current_text_index = 0
            return True

        self.finished = True
        return False


    def is_finished(self):
        return self.finished


class DeliveryMinigame:
    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.cell_size = 40
        self.grid_width = screen_size[0] // self.cell_size
        self.grid_height = screen_size[1] // self.cell_size
        self.player_pos = (self.grid_width // 2, self.grid_height // 2)
        self.finish_pos = (random.randint(0, self.grid_width - 1), random.randint(0, self.grid_height - 1))
        self.obstacles = []
        self.generate_obstacles()
        self.completed = False
        self.crashed = False  # Столкновение с препятствием
        self.is_timeout = False  # Истечение времени
        self.time_left = 20  # Время в секундах
        self.start_time = pygame.time.get_ticks()  # Запоминаем время начала игры

    def generate_obstacles(self):
        """Генерирует препятствия на карте"""
        for _ in range(self.grid_width * self.grid_height // 15):  # ~10% клеток - препятствия
            while True:
                pos = (random.randint(0, self.grid_width - 1), random.randint(0, self.grid_height - 1))
                if pos != self.player_pos and pos != self.finish_pos and pos not in self.obstacles:
                    self.obstacles.append(pos)
                    break

    def update(self, keys):
        """Обновляет состояние мини-игры"""
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.start_time) / 1000  # Прошедшее время в секундах
        self.time_left = max(0, 20 - elapsed_time)  # Уменьшаем оставшееся время

        new_pos = list(self.player_pos)
        if keys[pygame.K_UP] or keys[pygame.K_w]:  # Вверх
            new_pos[1] -= 1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:  # Вниз
            new_pos[1] += 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:  # Влево
            new_pos[0] -= 1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:  # Вправо
            new_pos[0] += 1

        new_pos = tuple(new_pos)

        # Проверка столкновений
        if new_pos in self.obstacles or \
                new_pos[0] < 0 or new_pos[0] >= self.grid_width or \
                new_pos[1] < 0 or new_pos[1] >= self.grid_height:
            self.crashed = True  # Игрок врезался в препятствие
            return

        # Обновляем позицию игрока
        self.player_pos = new_pos

        # Проверяем достижение цели
        if self.player_pos == self.finish_pos:
            self.completed = True

        # Проверяем истечение времени
        if self.time_left <= 0:
            self.is_timeout = True  # Таймер закончился

    def draw(self, screen):
        """Отрисовывает мини-игру на экране"""
        screen.fill((43, 45, 48))

        # Рисуем препятствия
        for obstacle in self.obstacles:
            pygame.draw.rect(screen, GRAY, (
                obstacle[0] * self.cell_size, obstacle[1] * self.cell_size, self.cell_size, self.cell_size))

        # Рисуем игрока
        pygame.draw.rect(screen, (102, 170, 111), (
            self.player_pos[0] * self.cell_size, self.player_pos[1] * self.cell_size, self.cell_size, self.cell_size))

        # Рисуем финиш
        pygame.draw.rect(screen, (219, 92, 92), (
            self.finish_pos[0] * self.cell_size, self.finish_pos[1] * self.cell_size, self.cell_size, self.cell_size))

        # Отображаем оставшееся время
        font = pygame.font.Font(None, 36)
        time_text = font.render(f"Time left: {int(self.time_left)}", True, WHITE)
        screen.blit(time_text, (10, 10))

        # Если достигнут финиш, показываем сообщение о заработанных деньгах
        """if self.completed:
            result_text = font.render(f"Вы доставили заказ и получили {self.salary}$", True, WHITE)
            screen.blit(result_text, (
                self.screen_size[0] // 2 - result_text.get_width() // 2,
                self.screen_size[1] // 2 - result_text.get_height() // 2))
        # Если произошло столкновение или истечение времени, показываем сообщение об ошибке
        elif self.crashed or self.is_timeout:
            if self.crashed:
                self.salary = - self.salary
                self.salary /= 2
                result_text = font.render(f"Вы повредили заказ и вам полагается штраф {self.salary}$", True, WHITE)
            else:
                result_text = font.render("Время вышло...", True, WHITE)
            screen.blit(result_text, (
                self.screen_size[0] // 2 - result_text.get_width() // 2,
                self.screen_size[1] // 2 - result_text.get_height() // 2))"""

    def is_completed(self):
        """Возвращает True, если мини-игра завершена успешно"""
        return self.completed

    def is_crashed(self):
        """Возвращает True, если игрок столкнулся с препятствием"""
        return self.crashed

    def is_timeout(self):
        """Возвращает True, если время вышло"""
        return self.is_timeout


class FreelanceCodeMinigame:
    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.cell_size = 60  # Размер каждой ячейки с фрагментом кода
        self.grid_width = screen_size[0] // self.cell_size
        self.grid_height = screen_size[1] // self.cell_size
        self.code_fragments = []
        self.player_fragments = []
        self.generate_code_fragments()
        self.completed = False
        self.failed = False
        self.time_left = 30  # Время в секундах
        self.selected_block_index = 0
        self.is_block_confirmed = False

    def generate_code_fragments(self):
        """Генерирует правильные фрагменты кода"""
        fragment_types = [
            {"type": "def_function", "text": "def function():", "color": BLUE},
            {"type": "if_statement", "text": "if condition:", "color": GREEN},
            {"type": "for_loop", "text": "for i in range(n):", "color": RED},
            {"type": "return_statement", "text": "return result", "color": YELLOW},
            {"type": "print_statement", "text": "print('Success')", "color": PURPLE}
        ]
        # Позиции блоков игрока
        player_positions = [fragment["pos"] for fragment in self.player_fragments]

        for i, fragment in enumerate(fragment_types):
            while True:
                pos = (random.randint(0, self.grid_width - 1), random.randint(0, self.grid_height - 1))
                if pos not in player_positions and pos not in [f["pos"] for f in self.code_fragments]:
                    self.code_fragments.append({"type": fragment["type"], "text": fragment["text"], "color": fragment["color"], "pos": pos})
                    break

    def update(self, keys, mouse_pos, events):
        """Обновляет состояние мини-игры"""
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.start_time) / 1000
        self.time_left = max(0, 30 - elapsed_time)

        # Обработка событий нажатий
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not self.is_block_confirmed:
                        # Подтверждение выбора
                        self.is_block_confirmed = True
                    else:
                        # Отмена выбора
                        self.is_block_confirmed = False

        # Выбор блока (стрелки вверх/вниз или W/S)
        if not self.is_block_confirmed:
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.selected_block_index = max(0, self.selected_block_index - 1)
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.selected_block_index = min(len(self.player_fragments) - 1, self.selected_block_index + 1)

        # Перемещение выбранного блока (стрелки или WASD)
        if self.is_block_confirmed:
            selected_block = self.player_fragments[self.selected_block_index]
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                selected_block["pos"] = (max(0, selected_block["pos"][0] - 1), selected_block["pos"][1])
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                selected_block["pos"] = (min(self.grid_width - 1, selected_block["pos"][0] + 1), selected_block["pos"][1])
            elif keys[pygame.K_UP] or keys[pygame.K_w]:
                selected_block["pos"] = (selected_block["pos"][0], max(0, selected_block["pos"][1] - 1))
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                selected_block["pos"] = (selected_block["pos"][0], min(self.grid_height - 1, selected_block["pos"][1] + 1))

        # Проверяем завершение сборки кода
        if self.check_completion():
            self.completed = True

        if self.time_left <= 0:
            self.failed = True

    def check_completion(self):
        """Проверяет, правильно ли собран код"""
        sorted_player_fragments = sorted(self.player_fragments, key=lambda x: x["pos"][1])
        sorted_code_fragments = sorted(self.code_fragments, key=lambda x: x["pos"][1])

        for player_fragment, code_fragment in zip(sorted_player_fragments, sorted_code_fragments):
            if player_fragment["type"] != code_fragment["type"] or player_fragment["pos"] != code_fragment["pos"]:
                return False
        return True

    def draw(self, screen):
        """Отрисовывает мини-игру на экране"""
        screen.fill(BLACK)

        # Рисуем сетку
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                pygame.draw.rect(screen, WHITE, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size), 1)

        # Рисуем правильные фрагменты кода (прозрачно)
        for fragment in self.code_fragments:
            fragment_rect = pygame.Rect(
                fragment["pos"][0] * self.cell_size,
                fragment["pos"][1] * self.cell_size,
                self.cell_size,
                self.cell_size
            )
            # Создаем поверхность с альфа-каналом для прозрачности
            transparent_surface = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
            transparent_surface.fill(fragment["color"] + (100,))  # Добавляем альфа-канал (прозрачность)

            # Отрисовываем поверхность на экране
            screen.blit(transparent_surface, fragment_rect.topleft)

        # Рисуем блоки игрока
        for i, fragment in enumerate(self.player_fragments):
            fragment_rect = pygame.Rect(
                fragment["pos"][0] * self.cell_size,
                fragment["pos"][1] * self.cell_size,
                self.cell_size,
                self.cell_size
            )

            # Выделение активного блока
            if i == self.selected_block_index and not self.is_block_confirmed:
                border_color = GRAY  # Серая граница для выбранного, но не подтвержденного блока
            elif i == self.selected_block_index and self.is_block_confirmed:
                border_color = (0, 255, 0)  # Ярко зеленая граница для подтвержденного блока
            else:
                border_color = BLACK  # Обычная граница для остальных блоков

            pygame.draw.rect(screen, fragment["color"], fragment_rect)
            pygame.draw.rect(screen, border_color, fragment_rect, 3)  # Граница выделенного блока

        # Отображаем оставшееся время
        font = pygame.font.Font(None, 36)
        time_text = font.render(f"Time left: {int(self.time_left)}", True, WHITE)
        screen.blit(time_text, (10, 10))

    def is_completed(self):
        """Возвращает True, если мини-игра завершена успешно"""
        return self.completed

    def is_failed(self):
        """Возвращает True, если мини-игра провалена"""
        return self.failed

    def start_game(self):
        """Начинает игру, копируя фрагменты кода для редактирования"""
        self.player_fragments = [{"type": frag["type"], "text": frag["text"], "color": frag["color"], "pos": (0, i)} for i, frag in enumerate(self.code_fragments)]
        self.start_time = pygame.time.get_ticks()


class TradingMinigame:
    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.price_history = self.generate_stock_data()
        self.current_step = 0
        self.max_steps = len(self.price_history) - 1
        self.player_balance = 1000  # Начальный баланс
        self.initial_balance = 1000  # Запоминаем начальный баланс
        self.player_shares = 0
        self.cell_size = 40  # Размер ячейки для графика
        self.grid_width = screen_size[0] // self.cell_size
        self.grid_height = screen_size[1] // self.cell_size
        self.time_left = 35  # Время в секундах
        self.start_time = pygame.time.get_ticks()
        self.failed = False
        self.completed = False

        # Параметры анимации графика
        self.graph_reveal_index = 0
        self.graph_reveal_speed = 2  # Скорость построения (точек в секунду)
        self.graph_reveal_timer = pygame.time.get_ticks()

        # Фиксированный диапазон цен для всего графика
        self.max_price = max(self.price_history)
        self.min_price = min(self.price_history)
        self.price_range = self.max_price - self.min_price

        button_width = 100
        button_height = 50
        button_y = self.screen_size[1] - 100

        from Game import Button
        self.buy_button = Button(x=self.screen_size[0] // 2 - 150, y=button_y, width=button_width, height=button_height, text="Купить", color=GREEN, text_color=WHITE)
        self.sell_button = Button(x=self.screen_size[0] // 2 + 50, y=button_y, width=button_width, height=button_height, text="Продать", color=RED, text_color=WHITE)

    def generate_stock_data(self):
        """Генерирует данные для графика цен"""
        price_history = [100]  # Начальная цена акции
        for _ in range(60):  # 60 временных периодов
            volatility = random.uniform(0.5, 2.0)
            change = random.gauss(0, volatility)
            new_price = max(50, price_history[-1] + change)
            price_history.append(new_price)
        return price_history

    def update(self, keys):
        """Обновляет состояние мини-игры"""
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.start_time) / 1000
        self.time_left = max(0, 35 - elapsed_time)

        # Обновление индекса раскрытия графика
        if self.graph_reveal_index < len(self.price_history):
            time_since_last_reveal = current_time - self.graph_reveal_timer
            if time_since_last_reveal > 1000 / self.graph_reveal_speed:
                self.graph_reveal_index += 1
                self.graph_reveal_timer = current_time

        # Переход к следующему шагу графика
        if self.current_step < self.graph_reveal_index - 1:
            self.current_step += 1

            # Проверяем завершение игры
        if self.time_left <= 0:
            self.end_game()

    def handle_event(self, event):
        """Обрабатывает действия игрока (покупка/продажа акций)"""
        if self.graph_reveal_index == 0:
            return  # Ждем появления первой цены

        current_price = self.price_history[self.current_step]
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.buy_button.is_clicked(mouse_pos):
                if self.player_balance >= current_price:
                    self.player_balance -= current_price
                    self.player_shares += 1
            elif self.sell_button.is_clicked(mouse_pos):
                if self.player_shares > 0:
                    self.player_balance += current_price
                    self.player_shares -= 1

    def end_game(self):
        """Завершает игру и подсчитывает результат"""
        if self.player_balance > self.initial_balance:
            self.completed = True
        else:
            self.failed = True

    def draw(self, screen):
        """Отрисовывает мини-игру на экране"""
        screen.fill((30, 31, 34))

        # Отрисовка графика цен
        graph_width = self.screen_size[0] - 300
        graph_height = self.screen_size[1] - 300
        graph_surface = pygame.Surface((graph_width, graph_height))
        graph_surface.fill((40, 40, 40))

        # Рисуем сетку
        grid_color = (80, 80, 80)
        num_vertical_lines = 11  # Количество вертикальных линий
        num_horizontal_lines = 11  # Количество горизонтальных линий

        # Рисуем вертикальные линии
        for x in range(0, graph_width, graph_width // num_vertical_lines):
            pygame.draw.line(graph_surface, grid_color, (x, 0), (x, graph_height), 1)

        # Рисуем горизонтальные линии
        for y in range(0, graph_height, graph_height // num_horizontal_lines):
            pygame.draw.line(graph_surface, grid_color, (0, y), (graph_width, y), 1)

        # Получаем видимые данные графика
        visible_data = self.price_history[:self.graph_reveal_index]
        if visible_data:
            for i in range(1, len(visible_data)):
                x1 = (i - 1) * (graph_width / len(self.price_history))
                y1 = graph_height - ((visible_data[i - 1] - self.min_price) / self.price_range) * graph_height
                x2 = i * (graph_width / len(self.price_history))
                y2 = graph_height - ((visible_data[i] - self.min_price) / self.price_range) * graph_height

                pygame.draw.line(graph_surface, GREEN if visible_data[i] > visible_data[i - 1] else RED, (x1, y1), (x2, y2), 2)

        screen.blit(graph_surface, (150, 150))

        # Отображение интерфейса
        font = pygame.font.Font(None, 36)

        # Текущая цена
        if self.graph_reveal_index > 0:
            current_price = self.price_history[self.current_step]
            price_text = font.render(f"Цена: {current_price:.2f}", True, WHITE)
            screen.blit(price_text, (10, 10))

        # Баланс игрока
        balance_text = font.render(f"Баланс: {self.player_balance:.2f}", True, WHITE)
        screen.blit(balance_text, (10, 50))

        # Количество акций
        shares_text = font.render(f"Акции: {self.player_shares}", True, WHITE)
        screen.blit(shares_text, (10, 90))

        # Время
        time_text = font.render(f"Время: {int(self.time_left)}", True, WHITE)
        screen.blit(time_text, (self.screen_size[0] - 150, 10))

        # Отрисовка кнопок
        self.buy_button.draw(screen)
        self.sell_button.draw(screen)


    def is_completed(self):
        """Проверяет, успешно ли завершена мини-игра"""
        return self.completed

    def is_failed(self):
        """Проверяет, провалена ли мини-игра"""
        return self.failed


class P2PMinigame:
    def __init__(self, screen_size, Button):
        self.screen_size = screen_size
        self.Button = Button
        self.documents = [self.generate_document() for _ in range(5)]
        self.current_document_index = 0
        self.lives = 3
        self.completed = False
        self.failed = False

        # Область подписи
        self.drawing_area = pygame.Rect(0, 0, 200, 100)  # Размер области подписи

        # Центрирование области
        self.drawing_area.x = (screen_size[0] - self.drawing_area.width) // 2
        self.drawing_area.y = (screen_size[1] - self.drawing_area.height) // 2 + 150

        # Поверхность для подписи
        self.signature_surface = pygame.Surface((self.drawing_area.width, self.drawing_area.height))
        self.signature_surface.fill(WHITE)

        self.is_drawing = False
        self.last_pos = None
        self.signature_drawn = False  # Флаг — была ли подпись сделана

        # Предупреждение о подписи
        self.show_signature_warning = False
        self.warning_timer = 0
        self.warning_duration = 2000

        # Сообщение об ошибке
        self.show_error_message = False
        self.error_start_time = 0
        self.error_duration = 2000

        # Кнопки
        button_width = 100
        button_height = 50
        button_y = self.screen_size[1] - 100

        self.approve_button = self.Button(
            x=self.screen_size[0] // 2 - 150,
            y=button_y,
            width=button_width,
            height=button_height,
            text="Одобрить",
            color=GREEN,
            text_color=WHITE
        )
        self.reject_button = self.Button(
            x=self.screen_size[0] // 2 + 50,
            y=button_y,
            width=button_width,
            height=button_height,
            text="Отклонить",
            color=RED,
            text_color=WHITE
        )

    def generate_document(self):
        """Генерирует документ с данными о сделке"""
        trust_rating = random.randint(1, 5)  # Рейтинг доверия от 1 до 5

        # Определяем, выгодна ли сделка на основе рейтинга
        if trust_rating <= 2:
            is_profitable = False  # Низкий рейтинг → сделка невыгодна
        elif trust_rating == 3:
            is_profitable = random.random() < 0.5  # Средний рейтинг → 50% шанс на успех
        else:
            is_profitable = True  # Высокий рейтинг → сделка выгодна

        risk_level = "Низкий" if trust_rating >= 4 else "Средний" if trust_rating == 3 else "Высокий"

        return {
            "client_name": random.choice(["Алексей", "Мария", "Иван", "Екатерина", "Дмитрий"]),
            "deal_type": random.choice(["Обмен валют", "Микрозайм", "Гарантия"]),
            "amount": random.randint(100, 1000),
            "trust_rating": trust_rating,
            "risk_level": risk_level,
            "region": random.choice(["Россия", "США", "Китай", "Бразилия", "Индия"]),
            "successful_deals": random.randint(0, 50),
            "failed_deals": random.randint(0, 20),
            "system_recommendation": "Одобрить" if is_profitable else "Отклонить",
            "is_profitable": is_profitable
        }

    def handle_event(self, event):
        """Обработка событий мыши и рисования"""
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Проверяем клик по области подписи
            if self.drawing_area.collidepoint(mouse_pos):
                self.is_drawing = True
                self.last_pos = (mouse_pos[0] - self.drawing_area.x, mouse_pos[1] - self.drawing_area.y)

            elif self.approve_button.is_clicked(mouse_pos):
                if not self.signature_drawn:
                    self.show_signature_warning = True
                    self.warning_timer = pygame.time.get_ticks()
                else:
                    doc = self.documents[self.current_document_index]
                    if doc["is_profitable"]:
                        if self.current_document_index + 1 < len(self.documents):
                            self.current_document_index += 1
                        else:
                            self.completed = True
                    else:
                        self.lives -= 1
                        self.show_error_message = True
                        self.error_start_time = pygame.time.get_ticks()
                    self.reset_signature()

            elif self.reject_button.is_clicked(mouse_pos):
                doc = self.documents[self.current_document_index]
                if not doc["is_profitable"]:
                    if self.current_document_index + 1 < len(self.documents):
                        self.current_document_index += 1
                    else:
                        self.completed = True
                else:
                    self.lives -= 1
                    self.show_error_message = True
                    self.error_start_time = pygame.time.get_ticks()
                self.reset_signature()

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_drawing = False
            self.last_pos = None
            self.signature_drawn = self.check_signature()

        elif event.type == pygame.MOUSEMOTION and self.is_drawing:
            current_pos = (mouse_pos[0] - self.drawing_area.x, mouse_pos[1] - self.drawing_area.y)
            if self.last_pos:
                pygame.draw.line(self.signature_surface, BLACK, self.last_pos, current_pos, 3)
            self.last_pos = current_pos

        # Сброс предупреждения через время
        if self.show_signature_warning and pygame.time.get_ticks() - self.warning_timer > self.warning_duration:
            self.show_signature_warning = False

        # Проверка завершения игры
        if self.current_document_index >= len(self.documents):
            self.completed = True
        elif self.lives <= 0:
            self.failed = True

    def check_signature(self):
        """Проверяет, есть ли подпись"""
        for x in range(200):
            for y in range(100):
                if self.signature_surface.get_at((x, y)) != (255, 255, 255, 255):
                    return True
        return False

    def reset_signature(self):
        """Сбрасывает область подписи"""
        self.signature_surface.fill(WHITE)
        self.signature_drawn = False

    def draw(self, screen):
        """Отрисовка интерфейса миниигры"""
        screen.fill((30, 31, 34))
        font = pygame.font.Font(None, 28)
        if self.current_document_index >= len(self.documents):
            return  # Не рисуем ничего, если документы закончились
        document = self.documents[self.current_document_index]

        #  Создание поверхности документа
        doc_width = 700
        doc_height = 450
        doc_x = (self.screen_size[0] - doc_width) // 2
        doc_y = (self.screen_size[1] - doc_height) // 2 - 40

        doc_surface = pygame.Surface((doc_width, doc_height))
        doc_surface.fill((240, 240, 240))

        # Рамка документа
        pygame.draw.rect(doc_surface, BLACK, (0, 0, doc_width, doc_height), 3)

        # Заголовок
        title_font = pygame.font.SysFont(None, 30)
        title_text = title_font.render("Информация о сделке", True, BLACK)
        doc_surface.blit(title_text, (doc_width // 2 - title_text.get_width() // 2, 20))

        # Номер документа
        number_font = pygame.font.SysFont(None, 20)
        number_text = number_font.render(f"Документ #{self.current_document_index + 1} из {len(self.documents)}", True, (80, 80, 80))
        doc_surface.blit(number_text, (doc_width - number_text.get_width() - 30, 30))

        # Информационные строки
        info_font = pygame.font.SysFont(None, 24)
        info_lines = [
            f"Клиент: {document['client_name']}",
            f"Тип сделки: {document['deal_type']}",
            f"Сумма: {document['amount']} $",
            f"Регион: {document['region']}",
            f"Рейтинг доверия: {'I' * document['trust_rating']}",
            f"Уровень риска: {document['risk_level']}",
            f"Рекомендация системы: {document['system_recommendation']}",
            f"Жизни: {self.lives}"
        ]

        y_offset = 80
        for line in info_lines:
            text_surface = info_font.render(line, True, BLACK)
            doc_surface.blit(text_surface, (40, y_offset))
            y_offset += 30

        # Расчёт области подписи по центру документа
        signature_width = self.signature_surface.get_width()
        signature_height = self.signature_surface.get_height()

        signature_x = (doc_width - signature_width) // 2
        signature_y = y_offset + 25

        signature_rect_in_doc = pygame.Rect(signature_x, signature_y, signature_width, signature_height)

        # Рисуем рамку вокруг области подписи
        pygame.draw.rect(doc_surface, BLACK, signature_rect_in_doc, 2)

        # Рисуем подпись внутри документа
        doc_surface.blit(self.signature_surface, signature_rect_in_doc.topleft)

        # Сообщение "Подпись обязательна!" над областью подписи
        if self.show_signature_warning:
            warning_text = info_font.render("Подпись обязательна!", True, RED)
            warning_x = signature_rect_in_doc.x + signature_rect_in_doc.width // 2 - warning_text.get_width() // 2
            warning_y = signature_rect_in_doc.y - 30
            doc_surface.blit(warning_text, (warning_x, warning_y))

        # Вставляем документ на экран
        screen.blit(doc_surface, (doc_x, doc_y))

        self.drawing_area.x = doc_x + signature_rect_in_doc.x
        self.drawing_area.y = doc_y + signature_rect_in_doc.y

        # Сообщение об ошибке
        if self.show_error_message and pygame.time.get_ticks() - self.error_start_time < self.error_duration:
            error_text = font.render("Ошибка, повторите операцию", True, RED)
            error_x = (self.screen_size[0] - error_text.get_width()) // 2
            error_y = doc_y + doc_height + 20
            screen.blit(error_text, (error_x, error_y))
        else:
            self.show_error_message = False

        # Отрисовка кнопок
        self.approve_button.draw(screen)
        self.reject_button.draw(screen)

    def is_completed(self):
        return self.completed

    def is_failed(self):
        return self.failed