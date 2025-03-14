import pygame


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