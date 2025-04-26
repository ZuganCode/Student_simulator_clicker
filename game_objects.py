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
    def __init__(self, screen_size, salary):
        self.screen_size = screen_size
        self.cell_size = 40
        self.grid_width = screen_size[0] // self.cell_size
        self.grid_height = screen_size[1] // self.cell_size
        self.player_pos = (self.grid_width // 2, self.grid_height // 2)
        self.finish_pos = (random.randint(0, self.grid_width - 1), random.randint(0, self.grid_height - 1))
        self.obstacles = []
        self.generate_obstacles()
        self.salary = salary
        self.completed = False
        self.crashed = False  # Столкновение с препятствием
        self.is_timeout = False  # Истечение времени
        self.time_left = 20  # Время в секундах (например, 60 секунд)
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
        screen.fill((30, 60, 30))

        # Рисуем препятствия
        for obstacle in self.obstacles:
            pygame.draw.rect(screen, GRAY, (
                obstacle[0] * self.cell_size, obstacle[1] * self.cell_size, self.cell_size, self.cell_size))

        # Рисуем игрока
        pygame.draw.rect(screen, (255, 165, 0), (
            self.player_pos[0] * self.cell_size, self.player_pos[1] * self.cell_size, self.cell_size, self.cell_size))

        # Рисуем финиш
        pygame.draw.rect(screen, RED, (
            self.finish_pos[0] * self.cell_size, self.finish_pos[1] * self.cell_size, self.cell_size, self.cell_size))

        # Отображаем оставшееся время
        font = pygame.font.Font(None, 36)
        time_text = font.render(f"Time left: {int(self.time_left)}", True, WHITE)
        screen.blit(time_text, (10, 10))

        # Если достигнут финиш, показываем сообщение о заработанных деньгах
        if self.completed:
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
                self.screen_size[1] // 2 - result_text.get_height() // 2))

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
    def __init__(self, screen_size, salary):
        self.screen_size = screen_size
        self.cell_size = 60  # Размер каждой ячейки с фрагментом кода
        self.grid_width = screen_size[0] // self.cell_size
        self.grid_height = screen_size[1] // self.cell_size
        self.code_fragments = []
        self.player_fragments = []
        self.generate_code_fragments()
        self.salary = salary
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
        elapsed_time = (current_time - self.start_time) / 1000  # Прошедшее время в секундах
        self.time_left = max(0, 30 - elapsed_time)

        # Обработка событий нажатий (а не состояния клавиш!)
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