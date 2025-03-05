import pygame
import json
import random
import sys
import os
from pygame.locals import RESIZABLE


# Инициализация Pygame
pygame.init()

# Настройка экрана
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), RESIZABLE)
pygame.display.set_caption("Симулятор Студенческой Жизни")

# Цвета
WHITE = (255, 255, 255)  # Белый
BLACK = (0, 0, 0)  # Черный
GRAY = (200, 200, 200)  # Серый
BLUE = (100, 150, 250)  # Синий
GREEN = (50, 200, 50)  # Зеленый
RED = (250, 50, 50)  # Красный
YELLOW = (255, 255, 0)  # Желтый
PURPLE = (128, 0, 128)  # Фиолетовый

# Шрифты
MAIN_FONT = pygame.font.Font(None, 36)  # Основной шрифт
SMALL_FONT = pygame.font.Font(None, 24)  # Маленький шрифт

# Константы для файла настроек
SETTINGS_FILE = "settings.json"


current_settings_section = None

SETTINGS_SECTIONS = {
    "main": "main",  # Главное меню настроек
    "display": "display",  # Настройки экрана
    "sound": "sound"  # Настройки звука
}

# Режимы отображения
DISPLAY_MODES = {
    "windowed": "Оконный режим",
    "borderless": "Без рамки",
    "fullscreen": "Полноэкранный",
}


# Пролог
PROLOGUE_DATA = [
    {"image": "prologue1.png", "text": "Вы начинаете свой путь в университете...", "duration": 1000},
    {"image": "prologue2.png", "text": "Мама: Учись, сынок, диплом — это твоё будущее", "duration": 1000},
    {"image": "prologue3.png", "text": "Новенький? На вахте узнай куда тебе.", "duration": 1000},
    {"image": "prologue3.png", "text": "* сосед храпит, а за стенкой, кто-то играет на гитаре и поёт песни* \n Не могу уснуть, посмотрю, что в соцсетях. ", "duration": 1000},
    {"image": "prologue3.png", "text": "Кто-то из одногруппников купил машину, а кто-то только вернулся из поездки в Дубай. А я тут, в этой клетке 3x4 метра, с мечтой о дипломе, который, как уверяют, «откроет все двери». ", "duration": 1000},
    {"image": "prologue3.png", "text": "Но двери — это не то, что я хотел. Всю ночь я ворочался, слушая, как за стеной кто-то играл на гитаре.", "duration": 1000},
    {"image": "prologue3.png", "text": "Почему я должен жить в этом сером мире, когда хочу туда. Мне нужен не диплом и выживание. Мне нужна та жизнь, та машина и хороший дом. То что скажет за меня, что я не из чёртовой общаги. ", "duration": 1000},
    {"image": "prologue3.png", "text": "Сосед: Да, есть килл!", "duration": 1000},
    {"image": "prologue3.png", "text": "«Четыре года, — прошептал я. — Четыре года, чтобы заработать на ту жизнь. Но как?».", "duration": 1000},
    {"image": "prologue3.png", "text": "«Учёба, лабы, сессии... А если не сдашь — армия. Но если только учиться, когда зарабатывать?»", "duration": 1000},
    {"image": "prologue3.png", "text": "В интернете нашёл и прочитал про майнинг, подработки, трейдин и как прокачаться с нуля. «Надо крутиться. Учёба – чтобы не отчислили. Заработок – чтобы не сойти с ума от безнадёги»  ", "duration": 1000},
    {"image": "prologue3.png", "text": "Пока сосед играл я не могу уснуть и изучал всё что мне может пригодиться, чтобы вылезти из этой ситуации. Так я и просидел до 3-х ночи.  ", "duration": 1000},
    {"image": "prologue3.png", "text": "Аааа, спать охота.  ", "duration": 1000},
    {"image": "prologue3.png", "text": "Преподаватель: «Молодой человек, если не сдадите лабу до пятницы, будете в армии отсыпаться!».  ", "duration": 1000},
    {"image": "prologue3.png", "text": "Чем же в итоге заниматься?  ", "duration": 1000},
]

def get_monitor_resolution():
    """
    Получает разрешение основного монитора.
    Returns:
        list: [width, height] разрешение монитора
    """
    info = pygame.display.Info()
    return [info.current_w, info.current_h]

def load_settings():
    """
    Загружает настройки из файла или возвращает значения по умолчанию.
    """
    try:
        with open(SETTINGS_FILE, "r") as f:
            data = json.load(f)
            return {
                "resolution": data.get("resolution", [1280, 720]),
                "display_mode": data.get("display_mode", "windowed")
            }
    except (FileNotFoundError, json.JSONDecodeError):
        # Возвращаем безопасные значения по умолчанию
        return {
            "resolution": [1280, 720],
            "display_mode": "windowed"
        }


def save_settings(resolution, display_mode):
    """
    Сохраняет настройки в файл.
    """
    data = {
        "resolution": resolution,
        "display_mode": display_mode
    }
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f)

# Инициализация экрана с загруженными настройками
settings = load_settings()
resolution = settings["resolution"]  # Получаем список с разрешением
screen = pygame.display.set_mode((resolution[0], resolution[1]), RESIZABLE)
pygame.display.set_caption("Симулятор Студенческой Жизни")


class Button:
    """
       Класс для создания и управления кнопками интерфейса.

       Атрибуты:
           rect (pygame.Rect): Прямоугольник кнопки
           text (str): Текст на кнопке
           color (tuple): Цвет кнопки RGB
           text_color (tuple): Цвет текста RGB
           hover_color (tuple): Цвет при наведении

       Методы:
           draw(surface): Отрисовывает кнопку на поверхности
           is_clicked(pos): Проверяет клик по кнопке
           update(mouse_pos): Обновляет состояние при наведении
       """
    def __init__(self, x, y, width, height, text, color, text_color):
        assert isinstance(color, tuple) and len(color) == 3, "Цвет должен быть кортежем из 3 чисел!"
        assert all(0 <= c <= 255 for c in color), "Каждый канал цвета должен быть от 0 до 255!"

        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.default_color = color
        self.hover_color = (min(color[0] + 30, 255), min(color[1] + 30, 255), min(color[2] + 30, 255))
        self.current_color = color

    def draw(self, surface):
        """Рисует кнопку"""
        pygame.draw.rect(surface, self.current_color, self.rect)
        text_surface = SMALL_FONT.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        """Проверяет, нажата ли кнопка"""
        return self.rect.collidepoint(pos)

    def update(self, mouse_pos):
        """Изменяет цвет кнопки при наведении"""
        if self.rect.collidepoint(mouse_pos):
            self.color = self.hover_color  # Меняем цвет при наведении
        else:
            self.color = self.default_color  # Возвращаем стандартный цвет

    def handle_hover(self, mouse_pos):
        """Обработка наведения мыши"""
        if self.rect.collidepoint(mouse_pos):
            self.current_color = self.hover_color
        else:
            self.current_color = self.default_color


class Prologue:
    """
        Класс для управления вступительной частью игры.

        Атрибуты:
            frames (list): Список кадров пролога
            current_frame (int): Текущий кадр
            text_start_time (int): Время начала показа текста
            screen_size (tuple): Размер экрана

        Методы:
            load_frames(): Загружает кадры пролога
            update(): Обновляет состояние пролога
            draw(surface): Отрисовывает текущий кадр
        """
    def __init__(self, screen_size):
        self.frames = []
        self.current_frame = 0
        self.start_time = pygame.time.get_ticks()
        self.text_start_time = pygame.time.get_ticks()
        self.screen_size = screen_size
        self.load_frames()
        self.current_text_index = 0
        self.text_fully_revealed = False
        self.char_delay = 50  # Задержка между символами (в миллисекундах)

    def load_frames(self):
        for data in PROLOGUE_DATA:
            try:
                image = pygame.image.load(data["image"]).convert()
                image = pygame.transform.scale(image, self.screen_size)
                self.frames.append({
                    "image": image,
                    "text": data["text"],
                    "duration": data["duration"]
                })
            except Exception as e:
                print(f"Ошибка загрузки: {data['image']} - {e}")
                surf = pygame.Surface(self.screen_size)
                surf.fill(PURPLE)
                self.frames.append({
                    "image": surf,
                    "text": data["text"],
                    "duration": data["duration"]
                })

    def handle_input(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                if self.text_fully_revealed:
                    # Если текст полностью показан, переходим к следующему кадру
                    if self.current_frame < len(self.frames) - 1:
                        self.current_frame += 1
                        self.text_start_time = pygame.time.get_ticks()
                        self.current_text_index = 0
                        self.text_fully_revealed = False
                        return True
                    else:
                        return False  # Пролог завершён
                else:
                    # Если текст ещё не полностью показан, показываем его целиком
                    self.current_text_index = len(self.frames[self.current_frame]["text"])
                    self.text_fully_revealed = True
                    return True
        return True

    def update(self):
        """Обновляет текущий кадр пролога"""
        if not self.text_fully_revealed:
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.text_start_time
            # Вычисляем, сколько символов должно быть показано
            should_show_chars = int(elapsed_time / self.char_delay)
            total_chars = len(self.frames[self.current_frame]["text"])

            if should_show_chars >= total_chars:
                self.current_text_index = total_chars
                self.text_fully_revealed = True
            else:
                self.current_text_index = should_show_chars

        return True

    def draw(self, surface):
        """Отображает текущий кадр пролога"""
        frame = self.frames[self.current_frame]
        surface.blit(frame["image"], (0, 0))

        # Полупрозрачное окно для текста
        dialog_height = surface.get_height() // 3
        dialog = pygame.Surface((surface.get_width(), dialog_height), pygame.SRCALPHA)
        dialog.fill((0, 0, 0, 180))

        # Параметры текста
        text = frame["text"][:self.current_text_index]
        font = MAIN_FONT
        text_color = WHITE
        padding = 20
        line_spacing = 10
        max_width = dialog.get_width() - 2 * padding

        # Разбиваем текст на строки
        lines = []
        paragraphs = text.split('\n')
        for paragraph in paragraphs:
            words = paragraph.split(' ')
            current_line = ''
            for word in words:
                test_line = current_line + ' ' + word if current_line else word
                test_width, _ = font.size(test_line)
                if test_width <= max_width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)
            lines.append('')

        # Отрисовка текста
        y = padding
        for line in lines:
            if not line:
                y += font.get_height() + line_spacing
                continue
            text_surface = font.render(line, True, text_color)
            dialog.blit(text_surface, (padding, y))
            y += font.get_height() + line_spacing

        surface.blit(dialog, (0, surface.get_height() - dialog_height))


class Game:
    """
    Главный класс игры, управляющий игровой логикой и состоянием.

    Атрибуты:
        money (int): Текущее количество денег игрока
        energy (int): Текущий уровень энергии игрока
        max_energy (int): Максимальный уровень энергии
        total_days (int): Количество прошедших дней
        season (str): Текущий сезон
        study_progress (float): Прогресс обучения
        study_score (int): Очки обучения
        buttons (dict): Словарь игровых кнопок
        shop_items (dict): Словарь предметов магазина
    """
    def __init__(self):
        self.money = 5000
        self.energy = 3000
        self.max_energy = 3000
        self.total_days = 1
        self.current_season_index = 0
        self.season_list = ["Осень", "Зима", "Весна", "Лето"]
        self.season = self.season_list[self.current_season_index]
        self.study_progress = 0
        self.lab_completed = False
        self.study_score = 0
        self.knowledge_check_passed = False
        self.mining_income = 10
        self.work_income = 20
        self.scholarship = 1000
        self.rent_paid = True
        self.rent_cost = 100
        self.housing_bonus = 0
        self.expensive_item_goal = 5000
        self.current_item_savings = 0
        self.daily_expenses = 10
        self.daily_expense_buff = 0

        screen_size = pygame.display.get_surface().get_size()
        button_width = 180
        button_height = 50
        button_spacing = 20
        total_buttons = 5
        total_width = (button_width * total_buttons) + (button_spacing * (total_buttons - 1))
        start_x = (screen_size[0] - total_width) // 2
        button_y = screen_size[1] - button_height - 30  # 30 пикселей отступ от низа

        self.buttons = {
            "shop": Button(start_x, button_y, button_width, button_height, "Магазин", PURPLE, WHITE),
            "work": Button(start_x + (button_width + button_spacing), button_y, button_width, button_height, "Работать",
                           GREEN, WHITE),
            "study": Button(start_x + (button_width + button_spacing) * 2, button_y, button_width, button_height,
                            "Учиться", BLUE, WHITE),
            "lottery": Button(start_x + (button_width + button_spacing) * 3, button_y, button_width, button_height,
                              "Лотерея", GRAY, BLACK),
            "next_day": Button(start_x + (button_width + button_spacing) * 4, button_y, button_width, button_height,
                               "Отдых", YELLOW, BLACK),
        }

        self.shop_items = {
            "Активный заработок": {
                "Копирайтинг": [
                    {"name": "Курс по SEO", "price": 500, "desc": "+10% к доходу от копирайтинга", "icon": "seo.png"},
                    {"name": "Портфолио", "price": 200, "desc": "+5% к доверию заказчиков", "icon": "portfolio.png"}
                ],
                "Дизайн": [
                    {"name": "Фigma", "price": 800, "desc": "Обучение Figma +15% к скорости работы",
                     "icon": "figma.png"},
                    {"name": "Иллюстратор", "price": 1200, "desc": "+20% к качеству работ", "icon": "illustrator.png"}
                ],
                "Программирование": [
                    {"name": "Python курс", "price": 1000, "desc": "+20% к доходу от программирования",
                     "icon": "python.png"},
                    {"name": "Git", "price": 300, "desc": "+10% к эффективности", "icon": "git.png"}
                ]
            },
            "Пассивный заработок": {
                "Арбитраж": [
                    {"name": "Нанять сотрудника", "price": 2500, "desc": "+5% от баланса", "icon": "stocks.png"},
                    # для команды необходимо хотя бы 2
                    {"name": "Дроповод", "price": 2000, "desc": "+3% от баланса", "icon": "stocks.png"},
                    # для команды необходим хотя бы 1(на 2 человека)
                    {"name": "Мерчант Биржи", "price": 10000, "desc": "+10% от баланса", "icon": "stocks.png"},
                    {"name": "Обучение связке", "price": 3000, "desc": "+6% от баланса", "icon": "stocks.png"},
                    {"name": "Увеличить баланс", "price": 1000, "desc": "+1000 к балансу", "icon": "stocks.png"},
                    {"name": "Телефон", "price": 1500, "desc": "+5% от баланса", "icon": "stocks.png"}
                ],
                "Обработка трафика": [
                    {"name": "Нанять сотрудника", "price": 4000, "desc": "+10% от баланса", "icon": "stocks.png"},
                    # для команды необходимо хотя бы 2
                    {"name": "Дроповод", "price": 2000, "desc": "+5% от баланса", "icon": "stocks.png"},
                    # для команды необходим хотя бы 1(на 2 человека)
                    {"name": "Телефон", "price": 1500, "desc": "+5% от баланса", "icon": "stocks.png"},
                    {"name": "Увеличить баланс", "price": 1000, "desc": "+1000 к балансу", "icon": "stocks.png"},
                    {"name": "Мерчант Площадки", "price": 10000, "desc": "+5% от баланса", "icon": "stocks.png"}
                ],
                "Трейдинг": [
                    {"name": "Фьючерсы", "price": 2500, "desc": "Высокий риск, возможен ×3", "icon": "futures.png"},
                    {"name": "Опционы", "price": 3000, "desc": "Очень высокий риск, возможен ×4", "icon": "options.png"}
                ]
            },
            "Лотереи": [
                {"name": "Дешмань", "price": 100, "desc": "от 10 до 300", "icon": "money.png"},
            ],
            "Улучшения": [
                {"name": "Нормальная еда", "price": 100, "desc": "даёт +20 к максимуму энергии", "icon": "food.png"},
            ]
        }
        self.current_shop_category = "Активный заработок"
        self.current_shop_subcategory = None
        self.shop_page = 0
        self.items_per_page = 4
        self.lottery_cost = 50
        self.lottery_prize = 0
        self.energy_items = 0
        self.plot_inserts = [
            "Вы пришли в университет, чувствуя решимость достичь своих целей.",
            "Ночные занятия становятся вашей новой нормой.",
            "Мечта о покупке дорогой вещи мотивирует вас."
        ]
        self.update_button_positions(pygame.display.get_surface().get_size())

    def add_money(self, amount):
        """
    Изменяет количество денег игрока.

    Args:
        amount (int/float): Сумма для добавления (может быть отрицательной)
    """
        if amount >= 0:
            self.money += int(amount + 0.999999)
        else:
            self.money += int(amount)

    def update_button_positions(self, screen_size):
        """
    Обновляет позиции всех кнопок при изменении размера экрана.

    Args:
        screen_size (tuple): Новый размер экрана (width, height)
    """
        button_width = 180
        button_height = 50
        button_spacing = 20
        total_buttons = 5
        total_width = (button_width * total_buttons) + (button_spacing * (total_buttons - 1))
        start_x = (screen_size[0] - total_width) // 2
        button_y = screen_size[1] - button_height - 30

        # Обновляем позиции кнопок
        buttons_data = [
            ("shop", "Магазин", PURPLE),
            ("work", "Работать", GREEN),
            ("study", "Учиться", BLUE),
            ("lottery", "Лотерея", GRAY),
            ("next_day", "Отдых", YELLOW)
        ]

        for i, (key, text, color) in enumerate(buttons_data):
            new_x = start_x + (button_width + button_spacing) * i
            if key not in self.buttons:
                self.buttons[key] = Button(new_x, button_y, button_width, button_height, text, color, WHITE)
            else:
                self.buttons[key].rect.x = new_x
                self.buttons[key].rect.y = button_y


    def study(self, energy_cost):
        """
    Выполняет действие учебы.

    Args:
        energy_cost (int): Затраты энергии на учебу
    """
        if self.energy >= energy_cost:
            efficiency = random.uniform(0.5, 1.5)
            self.study_progress += energy_cost * efficiency
            self.energy -= energy_cost
            if random.random() < 0.3:
                self.lab_completed = True
                self.study_score += 10

    def work(self, energy_cost):
        """
    Выполняет действие работы.

    Args:
        energy_cost (int): Затраты энергии на работу
    """
        if self.energy >= energy_cost:
            efficiency = random.uniform(0.8, 1.2)  # Эффективность работы (случайное значение)
            income = self.work_income * (energy_cost / 20) * efficiency
            self.add_money(income)
            self.energy -= energy_cost

    def process_day(self):
        """
    Обрабатывает переход к следующему дню.

    Returns:
        str: Случайное событие дня из plot_inserts
    """
        expense = self.daily_expenses + self.daily_expense_buff
        self.add_money(-expense)
        if self.total_days % 10 == 0:  # Начисление стипендии каждые 10 дней
            scholarship_amount = 10000 if self.current_season_index < 2 else 2500
            self.add_money(scholarship_amount)
            self.last_scholarship_amount = scholarship_amount  # Сохраняем последнюю сумму стипендии
        if not self.rent_paid:
            self.add_money(-self.rent_cost)
        self.total_days += 1
        self.current_season_index = (self.total_days // 30) % 4  # Обновление сезона каждые 30 дней
        self.season = self.season_list[self.current_season_index]
        if self.total_days % 30 == 0:  # Проверка знаний каждые 30 дней
            self.knowledge_check_passed = random.random() > 0.3
            if not self.knowledge_check_passed:
                self.study_score -= 20
        self.energy = self.max_energy
        return random.choice(self.plot_inserts)

    def lottery(self):
        """
    Обрабатывает участие в лотерее.

    Returns:
        str: Сообщение о результате участия в лотерее
    """
        if self.money >= self.lottery_cost:
            self.add_money(-self.lottery_cost)
            if random.random() < 0.9:  # Вероятность выигрыша 90%
                self.lottery_prize = random.randint(200, 100000)
                self.add_money(self.lottery_prize)
                return f"Поздравляем! Вы выиграли {self.lottery_prize}"
            return "Извините, вам не повезло в этот раз."
        return "Недостаточно денег для участия в лотерее."

    def save_game(self):
        """
    Сохраняет текущее состояние игры в файл.
    """
        data = {
            "money": self.money,
            "energy": self.energy,
            "total_days": self.total_days,
            "season": self.season,
            "study_progress": self.study_progress,
            "lab_completed": self.lab_completed,
            "study_score": self.study_score,
            "knowledge_check_passed": self.knowledge_check_passed,
            "current_season_index": self.current_season_index
        }
        with open("save.json", "w") as f:
            json.dump(data, f)

    def load_game(self):
        """
    Загружает сохраненное состояние игры из файла.
    В случае отсутствия файла создает новую игру.
    """
        try:
            with open("save.json", "r") as f:
                data = json.load(f)
                self.money = data.get("money", 100)
                self.energy = data.get("energy", 100)
                self.total_days = data.get("total_days", 1)
                self.season = data.get("season", "Осень")
                self.study_progress = data.get("study_progress", 0)
                self.lab_completed = data.get("lab_completed", False)
                self.study_score = data.get("study_score", 0)
                self.knowledge_check_passed = data.get("knowledge_check_passed", False)
                self.current_season_index = data.get("current_season_index", 0)
        except FileNotFoundError:
            print("Сохранение не найдено. Начинаем новую игру.")


def apply_display_mode(resolution, mode):
    """
    Применяет выбранный режим отображения.
    Args:
        resolution: список [width, height]
        mode: строка с режимом отображения
    Returns:
        pygame.Surface: новая поверхность экрана
    """
    try:
        if mode == "fullscreen":
            return pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
        elif mode == "borderless":
            # Получаем информацию о текущем дисплее
            info = pygame.display.Info()
            monitor_size = (info.current_w, info.current_h)

            # Сначала установим обычный режим, чтобы сбросить текущие настройки окна
            pygame.display.set_mode((1, 1))

            # Устанавливаем позицию окна в (0,0)
            os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"

            # Создаем безрамочное окно размером с монитор
            screen = pygame.display.set_mode(
                monitor_size,
                pygame.NOFRAME | pygame.HWSURFACE | pygame.DOUBLEBUF
            )

            # Принудительно обновляем размер окна
            pygame.display.get_surface().get_size()
            return screen
        else:  # windowed
            os.environ['SDL_VIDEO_CENTERED'] = '1'
            return pygame.display.set_mode(
                resolution,
                RESIZABLE | pygame.HWSURFACE | pygame.DOUBLEBUF
            )
    except pygame.error as e:
        print(f"Ошибка при установке режима отображения: {e}")
        return pygame.display.set_mode((1280, 720), RESIZABLE)


def handle_mouse_events(mouse_pos, state, game, current_plot_text, settings_button, buttons, screen_size):
    """
    Обрабатывает события мыши.

    Args:
        mouse_pos (tuple): Позиция курсора (x, y)
        state (str): Текущее состояние игры
        game (Game): Экземпляр игры
        current_plot_text (str): Текущий текст сюжета
        settings_button (Button): Кнопка настроек
        buttons (dict): Словарь всех кнопок
        screen_size (tuple): Размер экрана (width, height)

    Returns:
        tuple: (state, current_plot_text) - новое состояние и текст
    """
    global current_settings_section
    current_width, current_height = screen_size

    if state == "main_menu":
        for action, button in buttons["main_menu"].items():
            if button.is_clicked(mouse_pos):
                if action == "continue":
                    game.load_game()
                    return "game", current_plot_text
                elif action == "new_game":
                    return "new_game_warning", current_plot_text
                elif action == "settings":
                    current_settings_section = SETTINGS_SECTIONS["main"]
                    return "settings", current_plot_text
                elif action == "quit":
                    pygame.quit()
                    sys.exit()

    elif state == "new_game_warning":
        if buttons["new_game_warning"]["yes"].is_clicked(mouse_pos):
            return "prologue_choice", current_plot_text
        elif buttons["new_game_warning"]["no"].is_clicked(mouse_pos):
            return "main_menu", current_plot_text

    elif state == "exit_confirmation":
        if buttons["exit_confirmation"]["yes"].is_clicked(mouse_pos):
            game.save_game()
            pygame.quit()
            sys.exit()
        elif buttons["exit_confirmation"]["no"].is_clicked(mouse_pos):
            pygame.quit()
            sys.exit()

    elif state == "prologue_choice":
        if buttons["prologue_choice"]["watch"].is_clicked(mouse_pos):
            return "prologue", current_plot_text
        elif buttons["prologue_choice"]["skip"].is_clicked(mouse_pos):
            game = Game()
            return "game", current_plot_text

    elif state == "game":
        if settings_button.is_clicked(mouse_pos):
            current_settings_section = SETTINGS_SECTIONS["main"]
            return "game_settings", current_plot_text

        for action, button in game.buttons.items():
            if button.is_clicked(mouse_pos):
                if action == "study":
                    return "game", game.study(20)
                elif action == "work":
                    return "game", game.work(20)
                elif action == "next_day":
                    return "game", game.process_day()
                elif action == "lottery":
                    return "game", game.lottery()
                elif action == "shop":
                    return "shop", current_plot_text

    elif state in ["settings", "game_settings"]:
        source_state = "game" if state == "game_settings" else "main_menu"

        # Обработка кнопок бокового меню
        if buttons["settings"]["main"]["display"].is_clicked(mouse_pos):
            current_settings_section = SETTINGS_SECTIONS["display"]
            return state, current_plot_text
        elif buttons["settings"]["main"]["sound"].is_clicked(mouse_pos):
            current_settings_section = SETTINGS_SECTIONS["sound"]
            return state, current_plot_text
        elif buttons["settings"]["main"]["back"].is_clicked(mouse_pos):
            return source_state, current_plot_text
        elif buttons["settings"]["main"]["continue"].is_clicked(mouse_pos):
            return "game", current_plot_text
        elif buttons["settings"]["main"]["exit"].is_clicked(mouse_pos) and state == "game_settings":
            return "exit_confirmation", current_plot_text
        elif buttons["settings"]["main"]["main_menu"].is_clicked(mouse_pos):
            if state == "game_settings":
                game.save_game()
            return "main_menu", current_plot_text

        # Обработка кнопок раздела "display"
        if current_settings_section == SETTINGS_SECTIONS["display"]:
            settings = load_settings()
            current_resolution = settings["resolution"]
            current_mode = settings["display_mode"]
            if buttons["settings"]["display"]["hd"].is_clicked(mouse_pos):
                pygame.display.set_mode((1280, 720), RESIZABLE)
                save_settings([1280, 720])
            elif buttons["settings"]["display"]["fhd"].is_clicked(mouse_pos):
                pygame.display.set_mode((1920, 1080), RESIZABLE)
                save_settings([1920, 1080])
            elif buttons["settings"]["display"]["qhd"].is_clicked(mouse_pos):
                pygame.display.set_mode((2560, 1440), RESIZABLE)
                save_settings([2560, 1440])

        # Обработка кнопок раздела "sound"
        elif current_settings_section == SETTINGS_SECTIONS["sound"]:
            pass  # Здесь будет код для настроек звука

    elif state == "shop":
        if game.current_shop_category in game.shop_items:
            items = game.shop_items[game.current_shop_category]

            # Проверяем клики по категориям
            category_x = 50
            for category in game.shop_items.keys():
                category_rect = pygame.Rect(category_x, 20, 200, 50)
                if category_rect.collidepoint(mouse_pos):
                    game.current_shop_category = category
                    game.current_shop_subcategory = None
                    return state, current_plot_text
                category_x += 220

            # Проверяем клики по подкатегориям
            if isinstance(items, dict):
                subcategory_x = 50
                for subcategory in items.keys():
                    subcategory_rect = pygame.Rect(subcategory_x, 100, 200, 50)
                    if subcategory_rect.collidepoint(mouse_pos):
                        game.current_shop_subcategory = subcategory
                        return state, current_plot_text
                    subcategory_x += 220

                # Проверяем клики по товарам
                current_items = items[game.current_shop_subcategory] if game.current_shop_subcategory else []
                for i, item in enumerate(current_items):
                    item_rect = pygame.Rect(50, 200 + (i * 40), current_width - 200, 40)
                    if item_rect.collidepoint(mouse_pos):
                        if game.money >= item["price"]:
                            game.money -= item["price"]
                            return state, f"Вы купили {item['name']}!"
                        return state, "Недостаточно денег!"

            # Кнопка выхода из магазина
            exit_button_rect = pygame.Rect(current_width - 150, 20, 100, 50)
            if exit_button_rect.collidepoint(mouse_pos):
                return "game", current_plot_text

    return state, current_plot_text


def draw_shop_screen(screen, game, current_width):
    """
    Отрисовывает экран магазина.
    """
    # Задаём фон
    screen.fill((30, 30, 60))

    # Отрисовка категорий
    category_x = 50
    category_y = 20
    button_width = 200
    button_height = 50
    button_spacing = 20

    category_buttons = []
    for category in game.shop_items.keys():
        color = GREEN if category == game.current_shop_category else BLUE
        button = Button(category_x, category_y, button_width, button_height, category, color, WHITE)
        button.draw(screen)
        category_buttons.append(button)
        category_x += button_width + button_spacing

    # Отрисовка подкатегорий
    subcategory_buttons = []
    if game.current_shop_category in game.shop_items:
        items = game.shop_items[game.current_shop_category]
        if isinstance(items, dict):
            subcategory_x = 50
            subcategory_y = 100
            for subcategory in items.keys():
                color = GREEN if subcategory == game.current_shop_subcategory else BLUE
                button = Button(subcategory_x, subcategory_y, button_width, button_height,
                                subcategory, color, WHITE)
                button.draw(screen)
                subcategory_buttons.append(button)
                subcategory_x += button_width + button_spacing

    # Отрисовка товаров
    items_start_y = 200
    current_items = []

    if game.current_shop_category in game.shop_items:
        items = game.shop_items[game.current_shop_category]
        if game.current_shop_subcategory and isinstance(items, dict):
            current_items = items[game.current_shop_subcategory]
        elif isinstance(items, list):
            current_items = items

    for i, item in enumerate(current_items):
        if isinstance(item, dict):
            text = f"{item['name']} — {item['desc']}"
            price = f"${item['price']}"

            # Отрисовка фона элемента
            item_rect = pygame.Rect(50, items_start_y + (i * 40), current_width - 200, 35)
            pygame.draw.rect(screen, (50, 50, 80), item_rect)

            # Отрисовка текста
            text_surface = SMALL_FONT.render(text, True, WHITE)
            price_surface = SMALL_FONT.render(price, True, YELLOW)

            screen.blit(text_surface, (60, items_start_y + (i * 40) + 10))
            screen.blit(price_surface, (current_width - 150, items_start_y + (i * 40) + 10))

    # Кнопка выхода
    exit_button = Button(current_width - 150, 20, 100, 50, "Выход", RED, WHITE)
    exit_button.draw(screen)

    return category_buttons, subcategory_buttons, exit_button


def handle_shop_events(mouse_pos, game, category_buttons, subcategory_buttons, exit_button):
    # Проверяем нажатие на кнопку выхода
    if exit_button.is_clicked(mouse_pos):
        return "game"

    # Проверяем нажатие на категории
    for i, button in enumerate(category_buttons):
        if button.is_clicked(mouse_pos):
            game.current_shop_category = list(game.shop_items.keys())[i]
            game.current_shop_subcategory = None
            return None

    # Проверяем нажатие на подкатегории
    if game.current_shop_category in game.shop_items:
        items = game.shop_items[game.current_shop_category]
        if isinstance(items, dict):
            for i, button in enumerate(subcategory_buttons):
                if button.is_clicked(mouse_pos):
                    game.current_shop_subcategory = list(items.keys())[i]
                    return None

    return None


def draw_state(screen, state, game, current_plot_text, settings_button, settings_icon,
               money_icon, energy_icon, current_width, current_height, prologue, buttons):
    """
    Отрисовывает текущее состояние игры.

    Args:
        screen (pygame.Surface): Поверхность для отрисовки
        state (str): Текущее состояние игры
        game (Game): Экземпляр игры
        current_plot_text (str): Текущий текст сюжета
        settings_button (Button): Кнопка настроек
        settings_icon (pygame.Surface): Иконка настроек
        money_icon (pygame.Surface): Иконка денег
        energy_icon (pygame.Surface): Иконка энергии
        current_width (int): Текущая ширина экрана
        current_height (int): Текущая высота экрана
        prologue (Prologue): Экземпляр пролога
        buttons (dict): Словарь всех кнопок
    """
    if state == "main_menu":
        draw_main_menu(screen, buttons["main_menu"])
    elif state == "new_game_warning":
        draw_new_game_warning(screen, current_width, buttons["new_game_warning"])
    elif state == "prologue":
        if prologue:
            prologue.draw(screen)
    elif state == "game":
        draw_game_screen(screen, game, current_plot_text, settings_button, settings_icon,
                         money_icon, energy_icon, current_width)
    elif state in ["settings", "game_settings"]:
        source_state = "game" if state == "game_settings" else "main_menu"
        draw_settings_screen(screen, current_width, buttons["settings"],
                             current_settings_section, source_state)
    elif state == "exit_confirmation":
        # Сначала отрисовываем предыдущий экран настроек
        draw_settings_screen(screen, current_width, buttons["settings"],
                             current_settings_section, "game")
        # Затем поверх него отрисовываем окно подтверждения
        draw_exit_confirmation(screen, current_width, buttons["exit_confirmation"])


def draw_main_menu(screen, buttons):
    """
    Отрисовывает главное меню игры.

    Args:
        screen (pygame. Surface): Поверхность для отрисовки
        buttons (dict): Словарь кнопок главного меню
    """
    title = MAIN_FONT.render("Симулятор Студенческой Жизни", True, WHITE)
    screen.blit(title, (50, 100))
    for button in buttons.values():
        button.draw(screen)


def draw_new_game_warning(screen, current_width, buttons):
    """
    Отрисовывает предупреждение при начале новой игры.

    Args:
        screen (pygame.Surface): Поверхность для отрисовки
        current_width (int): Текущая ширина экрана
        buttons (dict): Словарь кнопок предупреждения
    """
    title = MAIN_FONT.render("Внимание!", True, WHITE)
    screen.blit(title, (current_width // 2 - title.get_width() // 2, 100))

    warning_text = ["Начиная новую игру,", "вы потеряете прошлое сохранение."]
    for i, line in enumerate(warning_text):
        text = MAIN_FONT.render(line, True, WHITE)
        screen.blit(text, (current_width // 2 - text.get_width() // 2, 200 + i * 40))

    for button in buttons.values():
        button.draw(screen)


def draw_game_screen(screen, game, current_plot_text, settings_button, settings_icon,
                     money_icon, energy_icon, current_width):
    """
    Отрисовывает основной игровой экран.

    Args:
        screen (pygame.Surface): Поверхность для отрисовки
        game (Game): Экземпляр игры
        current_plot_text (str): Текущий текст сюжета
        settings_button (Button): Кнопка настроек
        settings_icon (pygame.Surface): Иконка настроек
        money_icon (pygame.Surface): Иконка денег
        energy_icon (pygame.Surface): Иконка энергии
        current_width (int): Текущая ширина экрана
    """
    # Отрисовка текста "День (Сезон)"
    day_season_text = MAIN_FONT.render(f"День {game.total_days} ({game.season})", True, WHITE)
    screen.blit(day_season_text, (50, 10))

    # Деньги: иконка и текст
    if money_icon:
        screen.blit(money_icon, (250, 5))
    money_text = MAIN_FONT.render(f"{game.money}", True, WHITE)
    screen.blit(money_text, (300, 10))

    # Энергия: иконка и текст
    if energy_icon:
        screen.blit(energy_icon, (400, 5))
    energy_text = MAIN_FONT.render(f"{game.energy}/{game.max_energy}", True, WHITE)
    screen.blit(energy_text, (450, 10))

    # Сообщение о лотерее, ошибке или другом действии (например, заработке)
    if current_plot_text:
        plot_text = MAIN_FONT.render(current_plot_text, True, WHITE)
        screen.blit(plot_text, (50, 50))  # Размещаем под строкой "День (Сезон)"

    # Статистика
    stat_y = 100
    stat_lines = [
        f"Стипендия: {game.scholarship}",
        f"Прогресс учёбы: {game.study_progress:.1f}",
        f"Лабораторная выполнена: {game.lab_completed}"
    ]
    for line in stat_lines:
        stat_text = MAIN_FONT.render(line, True, WHITE)
        screen.blit(stat_text, (50, stat_y))
        stat_y += 40  # Расстояние между строками

    # Отрисовка кнопок
    for button in game.buttons.values():
        button.draw(screen)

    # Кнопка настроек
    settings_button.draw(screen)
    if settings_icon:
        screen.blit(settings_icon, (settings_button.rect.x, settings_button.rect.y))


def handle_settings_events(mouse_pos, event, state, game, buttons, source_state="main_menu"):
    """
    Универсальная функция обработки событий настроек.
    """
    global current_settings_section, screen

    # Получаем размер монитора
    info = pygame.display.Info()
    monitor_size = (info.current_w, info.current_h)

    if event.type == pygame.MOUSEBUTTONDOWN:
        if current_settings_section == SETTINGS_SECTIONS["display"]:
            try:
                # Оконный режим
                if buttons["display"]["display_mode"]["windowed"].is_clicked(mouse_pos):
                    pygame.display.quit()
                    pygame.display.init()
                    os.environ['SDL_VIDEO_CENTERED'] = '1'
                    screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
                    pygame.display.set_caption("Симулятор Студенческой Жизни")
                    save_settings([1280, 720], "windowed")

                # Безрамочный режим
                elif buttons["display"]["display_mode"]["borderless"].is_clicked(mouse_pos):
                    pygame.display.quit()
                    pygame.display.init()
                    if 'SDL_VIDEO_CENTERED' in os.environ:
                        del os.environ['SDL_VIDEO_CENTERED']
                    os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'
                    screen = pygame.display.set_mode(monitor_size, pygame.NOFRAME)
                    save_settings(list(monitor_size), "borderless")

                # Полноэкранный режим
                elif buttons["display"]["display_mode"]["fullscreen"].is_clicked(mouse_pos):
                    pygame.display.quit()
                    pygame.display.init()
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    save_settings(list(monitor_size), "fullscreen")

                # Ждем немного для стабилизации
                pygame.time.wait(100)

                # Принудительно обновляем экран
                pygame.display.flip()

                # Перезагружаем все изображения и шрифты
                # Здесь должен быть код для перезагрузки ваших ресурсов

            except Exception as e:
                print(f"Ошибка при смене режима экрана: {e}")
                # Аварийное восстановление
                screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
                save_settings([1280, 720], "windowed")

    return state


def draw_settings_screen(screen, current_width, buttons, current_section, source_state="main_menu"):
    """
    Универсальная функция отрисовки настроек.

    Args:
        screen: поверхность для отрисовки
        current_width: текущая ширина экрана
        buttons: словарь кнопок
        current_section: текущий раздел настроек
        source_state: откуда вызваны настройки ("main_menu" или "game")
    """
    screen.fill(PURPLE)

    # Константы для бокового меню
    SIDEBAR_WIDTH = 200
    SIDEBAR_COLOR = (100, 0, 100)
    BUTTON_HEIGHT = 50
    BUTTON_MARGIN = 10

    # Отрисовка бокового меню
    sidebar_rect = pygame.Rect(0, 0, SIDEBAR_WIDTH, screen.get_height())
    pygame.draw.rect(screen, SIDEBAR_COLOR, sidebar_rect)

    # Определяем список кнопок в зависимости от источника
    if source_state == "game":
        button_list = ["display", "sound", "continue", "main_menu", "exit"]
    else:
        button_list = ["display", "sound", "back"]

    # Отрисовка кнопок в боковом меню
    y_position = BUTTON_MARGIN
    for button_name in button_list:
        buttons["main"][button_name].rect.x = BUTTON_MARGIN
        buttons["main"][button_name].rect.y = y_position
        buttons["main"][button_name].rect.width = SIDEBAR_WIDTH - (BUTTON_MARGIN * 2)
        y_position += BUTTON_HEIGHT + BUTTON_MARGIN

    # Подсветка активного раздела и отрисовка кнопок
    for button_name, button in buttons["main"].items():
        if button_name in button_list:  # Проверяем, должна ли кнопка быть видимой
            if (button_name == "display" and current_section == SETTINGS_SECTIONS["display"]) or \
                    (button_name == "sound" and current_section == SETTINGS_SECTIONS["sound"]):
                button.current_color = GREEN
            else:
                button.current_color = button.default_color
            button.draw(screen)

    # Центральная область контента
    CONTENT_X = SIDEBAR_WIDTH + 50
    CONTENT_Y = 50
    CONTENT_WIDTH = current_width - SIDEBAR_WIDTH - 100

    # Отрисовка содержимого выбранного раздела

    if current_section == SETTINGS_SECTIONS["display"]:
        settings = load_settings()
        current_mode = settings["display_mode"]

        # Заголовок раздела экрана
        title = MAIN_FONT.render("Настройки экрана", True, WHITE)
        title_rect = title.get_rect(center=(CONTENT_X + CONTENT_WIDTH // 2, CONTENT_Y))
        screen.blit(title, title_rect)

        # Режим отображения (отображается всегда)
        mode_title = MAIN_FONT.render("Режим отображения:", True, WHITE)
        screen.blit(mode_title, (CONTENT_X, CONTENT_Y + 60))

        button_y = CONTENT_Y + 100
        for mode, button in buttons["display"]["display_mode"].items():
            button.rect.x = CONTENT_X
            button.rect.y = button_y
            button.rect.width = CONTENT_WIDTH
            button.draw(screen)
            button_y += BUTTON_HEIGHT + BUTTON_MARGIN

        # Разрешение экрана (только для оконного режима)
        if current_mode == "windowed":
            resolution_title = MAIN_FONT.render("Разрешение экрана:", True, WHITE)
            screen.blit(resolution_title, (CONTENT_X, button_y + 20))

            button_y += 60
            for button_key in ["hd", "fhd", "qhd"]:
                buttons["display"][button_key].rect.x = CONTENT_X
                buttons["display"][button_key].rect.y = button_y
                buttons["display"][button_key].rect.width = CONTENT_WIDTH
                buttons["display"][button_key].draw(screen)
                button_y += BUTTON_HEIGHT + BUTTON_MARGIN


    elif current_section == SETTINGS_SECTIONS["sound"]:
        # Заголовок раздела звука
        title = MAIN_FONT.render("Настройки звука", True, WHITE)
        title_rect = title.get_rect(center=(CONTENT_X + CONTENT_WIDTH // 2, CONTENT_Y))
        screen.blit(title, title_rect)

        # Текст заглушки
        text = MAIN_FONT.render("Настройки звука временно недоступны", True, WHITE)
        text_rect = text.get_rect(center=(CONTENT_X + CONTENT_WIDTH // 2, CONTENT_Y + 100))
        screen.blit(text, text_rect)


def draw_prologue_choice(screen, current_width, buttons):
    """
    Отрисовывает экран выбора просмотра пролога.

    Args:
        screen (pygame.Surface): Поверхность для отрисовки
        current_width (int): Текущая ширина экрана
        buttons (dict): Словарь кнопок выбора пролога
    """
    text = MAIN_FONT.render("Хотите посмотреть предысторию?", True, WHITE)
    screen.blit(text, (current_width // 2 - text.get_width() // 2, 150))

    # Просто отрисовываем кнопки
    for button in buttons.values():
        button.draw(screen)

def handle_shop_purchase(game, item):
    if game.money >= item["price"]:
        game.money -= item["price"]
        # Добавить логику применения эффекта предмета
        return True, f"Вы купили {item['name']}!"
    return False, "Недостаточно денег!"

def draw_exit_confirmation(screen, current_width, buttons):
    """
    Отрисовывает окно подтверждения выхода.
    """
    # Затемнение фона
    overlay = pygame.Surface((current_width, screen.get_height()))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(128)
    screen.blit(overlay, (0, 0))

    # Текст подтверждения
    text = MAIN_FONT.render("Сохранить игру перед выходом?", True, WHITE)
    screen.blit(text, (current_width // 2 - text.get_width() // 2, 250))

    # Отрисовка кнопок
    for button in buttons.values():
        button.draw(screen)


def main():
    """
    Главная функция игры.
    """
    global current_settings_section, screen, subcategory_buttons, exit_button, category_buttons

    try:
        pygame.init()
    except pygame.error:
        print("Ошибка инициализации pygame")
        return

    current_settings_section = SETTINGS_SECTIONS["main"]
    clock = pygame.time.Clock()
    game = Game()
    running = True
    current_plot_text = ""
    state = "main_menu"
    prologue = None
    settings = load_settings()
    try:
        screen = apply_display_mode(settings["resolution"], settings["display_mode"])
    except pygame.error:
        print("Ошибка создания окна, использую настройки по умолчанию")
        screen = pygame.display.set_mode((1280, 720))

    # Получаем текущие размеры экрана
    current_width, current_height = screen.get_size()

    # Загрузка иконок
    try:
        money_icon = pygame.image.load('money.png').convert_alpha()
        money_icon = pygame.transform.scale(money_icon, (40, 40))
    except Exception as e:
        print(f"Ошибка загрузки money.png: {e}")
        money_icon = pygame.Surface((40, 40))
        money_icon.fill(YELLOW)

    try:
        energy_icon = pygame.image.load('energe.png').convert_alpha()
        energy_icon = pygame.transform.scale(energy_icon, (40, 40))
    except Exception as e:
        print(f"Ошибка загрузки energe.png: {e}")
        energy_icon = pygame.Surface((40, 40))
        energy_icon.fill(BLUE)

    try:
        settings_icon = pygame.image.load('setting.png').convert_alpha()
        settings_icon = pygame.transform.scale(settings_icon, (40, 40))
    except Exception as e:
        print(f"Ошибка загрузки setting.png: {e}")
        settings_icon = pygame.Surface((40, 40))
        settings_icon.fill(RED)

    # Создаём кнопки меню
    main_menu_buttons = {
        "continue": Button(50, 200, 300, 50, "Продолжить", GREEN, WHITE),
        "new_game": Button(50, 300, 300, 50, "Новая игра", BLUE, WHITE),
        "settings": Button(50, 400, 300, 50, "Настройки", YELLOW, BLACK),
        "quit": Button(50, 500, 300, 50, "Выйти", RED, WHITE)
    }

    new_game_warning_buttons = {
        "yes": Button(SCREEN_WIDTH // 2 - 120, 350, 100, 50, "Да", GREEN, WHITE),
        "no": Button(SCREEN_WIDTH // 2 + 20, 350, 100, 50, "Нет", RED, WHITE)
    }

    prologue_choice_buttons = {
        "watch": Button(SCREEN_WIDTH // 2 - 120, 250, 200, 50, "Да, показать историю", GREEN, WHITE),
        "skip": Button(SCREEN_WIDTH // 2 - 120, 350, 200, 50, "Нет, пропустить", RED, WHITE)
    }

    settings_buttons = {
        "main": {
            "display": Button(0, 0, 180, 50, "Экран", BLUE, WHITE),
            "sound": Button(0, 0, 180, 50, "Звук", BLUE, WHITE),
            "continue": Button(0, 0, 180, 50, "Продолжить", GREEN, WHITE),
            "main_menu": Button(0, 0, 180, 50, "Главное меню", YELLOW, BLACK),
            "exit": Button(0, 0, 180, 50, "Выход из игры", RED, WHITE),
            "back": Button(0, 0, 180, 50, "Назад", RED, WHITE)
        },
        "display": {
            "hd": Button(0, 0, 400, 50, "HD (1280x720)", GREEN, WHITE),
            "fhd": Button(0, 0, 400, 50, "FHD (1920x1080)", BLUE, WHITE),
            "qhd": Button(0, 0, 400, 50, "QHD (2560x1440)", YELLOW, BLACK),
            "display_mode": {
                "windowed": Button(0, 0, 400, 50, "Оконный режим", BLUE, WHITE),
                "borderless": Button(0, 0, 400, 50, "Без рамки", BLUE, WHITE),
                "fullscreen": Button(0, 0, 400, 50, "Полноэкранный", BLUE, WHITE),
            }
        },
        "sound": {}
    }


    # Собираем все группы кнопок
    buttons = {
        "main_menu": main_menu_buttons,
        "new_game_warning": new_game_warning_buttons,
        "prologue_choice": prologue_choice_buttons,
        "settings": settings_buttons,
        "game_settings": {
            "back": Button(50, current_height - 70, 200, 50, "Назад", RED, WHITE),
            "exit_to_menu": Button(300, current_height - 70, 200, 50, "Выход в меню", YELLOW, BLACK)
        },
        "exit_confirmation": {
            "yes": Button(SCREEN_WIDTH // 2 - 120, 350, 100, 50, "Да", GREEN, WHITE),
            "no": Button(SCREEN_WIDTH // 2 + 20, 350, 100, 50, "Нет", RED, WHITE)
        }
    }

    # Кнопка настроек
    settings_button = Button(SCREEN_WIDTH - 60, 10, 50, 50, "", PURPLE, WHITE)

    while running:
        current_width, current_height = screen.get_size()

        # Обновляем позиции кнопок настроек в игре
        buttons["game_settings"]["back"].rect.y = current_height - 70
        buttons["game_settings"]["exit_to_menu"].rect.y = current_height - 70

        mouse_pos = pygame.mouse.get_pos()
        screen.fill(PURPLE)

        # Обновление позиций
        settings_button.rect.x = current_width - 60
        settings_button.update(mouse_pos)

        if state == "game":
            game.update_button_positions((current_width, current_height))
            for button in game.buttons.values():
                button.update(mouse_pos)

        # Обработка событий в зависимости от состояния
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if state == "shop":
                        state = "game"
                    elif state == "exit_confirmation":
                        state = "game_settings"
                    elif state == "game":
                        current_settings_section = SETTINGS_SECTIONS["main"]
                        state = "game_settings"
                    elif state in ["settings", "game_settings"]:
                        state = "main_menu" if state == "settings" else "game"
                    elif state == "new_game_warning":
                        state = "main_menu"
                    elif state == "prologue_choice":
                        state = "new_game_warning"


            if event.type == pygame.MOUSEBUTTONDOWN:
                if state == "prologue":
                    if prologue and not prologue.handle_input([event]):
                        prologue = None
                        game = Game()
                        state = "game"
                elif state == "prologue_choice":
                    if buttons["prologue_choice"]["watch"].is_clicked(mouse_pos):
                        prologue = Prologue((current_width, current_height))
                        state = "prologue"
                    elif buttons["prologue_choice"]["skip"].is_clicked(mouse_pos):
                        game = Game()
                        state = "game"
                elif state == "new_game_warning":
                    if buttons["new_game_warning"]["yes"].is_clicked(mouse_pos):
                        state = "prologue_choice"
                    elif buttons["new_game_warning"]["no"].is_clicked(mouse_pos):
                        state = "main_menu"
                elif state == "shop":
                    new_state = handle_shop_events(event.pos, game, category_buttons,
                                                 subcategory_buttons, exit_button)
                    if new_state:
                        state = new_state
                else:
                    state, current_plot_text = handle_mouse_events(
                        event.pos, state, game, current_plot_text,
                        settings_button, buttons, (current_width, current_height)
                    )

        # Отрисовка текущего состояния
        if state == "prologue" and prologue:
            prologue.update()
            prologue.draw(screen)
        elif state == "prologue_choice":
            draw_prologue_choice(screen, current_width, buttons["prologue_choice"])
        elif state == "new_game_warning":
            draw_new_game_warning(screen, current_width, buttons["new_game_warning"])
        elif state == "shop":
            category_buttons, subcategory_buttons, exit_button = draw_shop_screen(screen, game, current_width)
        else:
            draw_state(
                screen, state, game, current_plot_text, settings_button, settings_icon,
                money_icon, energy_icon, current_width, current_height, prologue, buttons
            )

        # Обновление экрана
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()