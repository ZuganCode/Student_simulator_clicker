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
        self.time_left = 10  # Время в секундах (например, 60 секунд)
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
        self.time_left = max(0, 10 - elapsed_time)  # Уменьшаем оставшееся время

        new_pos = list(self.player_pos)
        if keys[pygame.K_UP]:
            new_pos[1] -= 1
        elif keys[pygame.K_DOWN]:
            new_pos[1] += 1
        elif keys[pygame.K_LEFT]:
            new_pos[0] -= 1
        elif keys[pygame.K_RIGHT]:
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