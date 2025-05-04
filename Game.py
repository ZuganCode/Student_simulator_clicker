import json
import random
import sys
import os
from data import PLOT_EVENTS, ENDING_ARMY, ENDING_PRISON, ENDING_BORING_JOB, ENDING_DREAM, SUMMER_1, SUMMER_2, SUMMER_3, HNY, PROLOGUE_DATA
from game_objects import Event, Ending, DeliveryMinigame, FreelanceCodeMinigame, TradingMinigame, P2PMinigame
os.environ['SDL_VIDEO_CENTERED'] = '1'
import pygame
from pygame.locals import RESIZABLE
from pygame.examples.sprite_texture import event

"""O Great God of Code!

You who breathed life into strings, grant us clarity of mind so that every command works together,
may the compiler know no errors, and logic be flawless, like an algorithm of eternal harmony.

O Mighty Architect of the Binary World!
We call upon You: grant us wisdom to optimize even the most tricky fragment,
protecting us from enemies who sow chaos in variables and loops,
may our functions always return the right values, and exceptions are avoided.

O Angels of debugging, cover our IDEs with blessings,
so that in every commit our code finds perfection,
and deployment to servers burns with purity and reliability.

O Supreme Guardian of Logic,
let us walk the path of pure architecture,
where every variable is meaningful, every function is a work of art,
and every bug that goes unnoticed dissolves in the ancient scrolls of Your wisdom.

Amen."""


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
pygame.font.init()
HAND_FONT = pygame.font.SysFont('Comic Sans MS', 36)
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


cheat_input_active = False
cheat_code = ""
cheat_message = ""


def init_cheat_window(screen):
    global CHEAT_BACKGROUND
    # Создаем полупрозрачный фон (50% прозрачности)
    CHEAT_BACKGROUND = pygame.Surface((screen.get_width(), screen.get_height()))
    CHEAT_BACKGROUND.set_alpha(128)  # 50% прозрачности
    CHEAT_BACKGROUND.fill((0, 0, 0))  # Черный фон


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
        dialog_height = surface.get_height() // 4
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

        # Индикатор продолжения
        if self.text_fully_revealed:
            indicator_text = font.render("Нажмите любую клавишу для продолжения...", True, (200, 200, 200))
            indicator_rect = indicator_text.get_rect(center=(self.screen_size[0] / 2, self.screen_size[1] - 30))
            surface.blit(indicator_text, indicator_rect)


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
    def __init__(self, x, y, width, height, text, color, text_color, icon=None):
        assert isinstance(color, tuple) and len(color) == 3, "Цвет должен быть кортежем из 3 чисел!"
        assert all(0 <= c <= 255 for c in color), "Каждый канал цвета должен быть от 0 до 255!"

        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.default_color = color
        self.hover_color = (min(color[0] + 30, 255), min(color[1] + 30, 255), min(color[2] + 30, 255))
        self.current_color = color
        self.icon = icon

    def is_hovered(self, mouse_pos):
        """Проверяет, находится ли курсор над кнопкой"""
        return self.rect.collidepoint(mouse_pos)


    def draw(self, surface):
        """Рисует кнопку"""
        pygame.draw.rect(surface, self.current_color, self.rect)
        if self.icon:
            screen.blit(self.icon, (self.rect.x, self.rect.y))
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


class GradientButton(Button):
    """
    Кнопка с градиентом прозрачности: центр менее прозрачный, края более.
    """
    def __init__(self, x, y, width, height, text, color, text_color, icon=None):
        super().__init__(x, y, width, height, text, color, text_color, icon)
        self.mask = self.create_gradient_mask(width, height)
        self.default_color = color  # Сохраняем исходный цвет без альфа


    def create_gradient_mask(self, width, height):
        """Создает маску градиента альфа-канала."""
        mask = pygame.Surface((width, height), pygame.SRCALPHA)
        center_x, center_y = width // 2, height // 2
        max_distance = ((width/2)**2 + (height/2)**2)**0.5
        for y in range(height):
            for x in range(width):
                dx = x - center_x
                dy = y - center_y
                distance = (dx**2 + dy**2)**0.5
                # Альфа-канал: 0 (прозрачно) на краях, 255 (непрозрачно) в центре
                alpha = int(255 * (distance / max_distance))  # Обратный градиент
                alpha = 255 - alpha  # Центрopaque, края прозрачные
                alpha = max(alpha, 50)  # Минимум 50% прозрачности в центре
                mask.set_at((x, y), (255, 255, 255, alpha))
        return mask


    def draw(self, surface):
        """Отрисовывает кнопку с градиентом."""
        # Основная поверхность кнопки с цветом и маской
        base_color = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        base_color.fill(self.color)  # Цвет кнопки без альфа
        # Применяем маску для градиента прозрачности
        masked = base_color.copy()
        masked.blit(self.mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        # Отрисовываем на экране
        surface.blit(masked, self.rect)
        # Отрисовываем текст и иконку поверх градиента
        text_surface = SMALL_FONT.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        if self.icon:
            surface.blit(self.icon, (self.rect.x + 10, self.rect.y + 10))  # Отступ для иконки


CHEAT_CODES = {
    "`godmode": lambda game, _: setattr(game, "money", 999999),
    "`max_energy": lambda game, _: setattr(game, "energy", game.max_energy),
    "`invincible": lambda game, _: setattr(game, "illegal_activity_score", -50),
    "`win": lambda game, _: setattr(game, "total_days", 465),
    "`addmoney": lambda game, param: game.add_money(int(param)),
    "`set_day": lambda game, param: setattr(game, "total_days", int(param)),
}


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
        self.failed_exam = False
        self.start_stat_time = None
        self.illegal_activity_score = 0
        self.last_scholarship_amount = None
        self.s_money = 0
        self.s_karma = 0
        self.s_study_progress = 0
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
        self.karma = 0  # Новая статистика "карма"
        self.endurance = 100  # Стойкость к выгоранию
        self.startup_participated = False  # Участие в стартапе (одноразово)
        self.gym_participated = False  # Участие в секции (одноразово)
        self.startup_phase = 0  # Фаза стартапа
        self.startup_started = False  # Начало стартапа
        self.sport_endurance_bonus = 0  # Бонус от секции
        self.plot_events = []  # Список активных событий
        self.screen_size = pygame.display.get_surface().get_size()
        self.current_plot_text = None
        self.message_timer = 0
        self.used_events = set()
        self.event_day = 0  # Текущий день в цикле вероятности
        self.max_event_days = 5  # Максимальное число дней в цикле
        self.military_ID = False
        self.start_money = 0
        self.start_karma = 0
        self.start_study_progress = 0.0
        self.monthly_money_change = 0
        self.monthly_karma_change = 0
        self.monthly_study_progress = 0.0
        self.monthly_money_history = []  # История денег
        self.monthly_study_history = []  # История обучения
        self.current_month_day = 0  # Текущий день в месяце
        self.monthly_start_money = self.money  # Начальное значение месяца
        self.monthly_start_karma = self.karma
        self.monthly_start_study_progress = self.study_progress
        self.is_summer1_been = False
        self.is_summer2_been = False
        self.is_summer3_been = False
        self.work_manager = WorkManager(pygame.display.get_surface().get_size())
        self.study_goal = 200
        self.study_points = 0
        self.university_passed = False

        self.purchased_items = set()  # Сет для хранения купленных предметов


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
            "work": Button(start_x + (button_width + button_spacing), button_y,
                           button_width, button_height, "Работать", GREEN, WHITE),
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
                    {"name": "Курс по SEO", "price": 500, "desc": "+10% к доходу от копирайтинга (Требуется 500 энергии)", "icon": "seo.png", "energy_cost": 500},
                    {"name": "Портфолио", "price": 200, "desc": "+5% к доверию заказчиков (Требуется 300 энергии)", "icon": "portfolio.png", "energy_cost": 300}
                ],
                "Дизайн": [
                    {"name": "Фigma", "price": 800, "desc": "Обучение Figma +15% к скорости работы  (Требуется 500 энергии)",
                     "icon": "figma.png", "energy_cost": 500},
                    {"name": "Иллюстратор", "price": 1200, "desc": "+20% к качеству работ  (Требуется 500 энергии)", "icon": "illustrator.png", "energy_cost": 500}
                ],
                "Программирование": [
                    {"name": "Python курс", "price": 1000, "desc": "+20% к доходу от программирования  (Требуется 500 энергии)",
                     "icon": "python.png", "energy_cost": 500},
                    {"name": "Git", "price": 300, "desc": "+10% к эффективности  (Требуется 400 энергии)", "icon": "git.png", "energy_cost": 400}
                ]
            },
            "Пассивный заработок": {
                "Арбитраж": [
                    {"name": "Нанять сотрудника", "price": 2500, "desc": "+5% от баланса  (Требуется 200 энергии)", "icon": "stocks.png", "energy_cost": 200},
                    # для команды необходимо хотя бы 2
                    {"name": "Дроповод", "price": 2000, "desc": "+3% от баланса  (Требуется 200 энергии)", "icon": "stocks.png", "energy_cost": 200},
                    # для команды необходим хотя бы 1(на 2 человека)
                    {"name": "Мерчант Биржи", "price": 10000, "desc": "+10% от баланса", "icon": "stocks.png",  "energy_cost": 0},
                    {"name": "Обучение связке", "price": 3000, "desc": "+6% от баланса  (Требуется 500 энергии)", "icon": "stocks.png", "energy_cost": 500},
                    {"name": "Увеличить баланс", "price": 1000, "desc": "+1000 к балансу", "icon": "stocks.png",  "energy_cost": 0},
                    {"name": "Телефон", "price": 1500, "desc": "+5% от баланса", "icon": "stocks.png",  "energy_cost": 0}
                ],
                "Обработка трафика": [
                    {"name": "Нанять сотрудника", "price": 4000, "desc": "+10% от баланса  (Требуется 200 энергии)", "icon": "stocks.png", "energy_cost": 200},
                    # для команды необходимо хотя бы 2
                    {"name": "Дроповод", "price": 2000, "desc": "+5% от баланса  (Требуется 200 энергии)", "icon": "stocks.png", "energy_cost": 200},
                    # для команды необходим хотя бы 1(на 2 человека)
                    {"name": "Телефон", "price": 1500, "desc": "+5% от баланса", "icon": "stocks.png",  "energy_cost": 0},
                    {"name": "Увеличить баланс", "price": 1000, "desc": "+1000 к балансу", "icon": "stocks.png",  "energy_cost": 0},
                    {"name": "Мерчант Площадки", "price": 10000, "desc": "+5% от баланса", "icon": "stocks.png",  "energy_cost": 0}
                ],
                "Трейдинг": [
                    {"name": "Курс 'Понятие рынка'", "price": 2500, "desc": "Высокий риск, возможен ×3  (Требуется 500 энергии)", "icon": "futures.png", "energy_cost": 500},
                    {"name": "Курс 'межбиржевое влияние'", "price": 3000, "desc": "Очень высокий риск, возможен ×4  (Требуется 500 энергии)", "icon": "options.png", "energy_cost": 500},
                ]
            },
            "Улучшения": [
                {"name": "Нормальная еда", "price": 100, "desc": "даёт +100 к максимуму энергии", "icon": "food.png",  "energy_cost": 0},
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

        self.has_shown_tutorial = False
        self.has_shown_tutorial_f = False
        self.has_shown_tutorial_t = False
        self.has_shown_tutorial_p2p = False


    def update_screen_size(self):
        self.screen_size = pygame.display.get_surface().get_size()




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

    #обновление метода study
    def check_study_progress(self):
        if self.study_progress >= self.study_goal:
            self.university_passed = True
            return True
        return False

    def study_lab(self):
        if self.energy >= 300 and not self.university_passed:
            self.energy -= 300
            self.study_progress += 3
            self.check_study_progress()
            return "Лабораторная работа завершена! +3 очка"
        return "Недостаточно энергии или учеба завершена"

    def study_lecture(self):
        if self.energy >= 150 and not self.university_passed:
            self.energy -= 150
            self.study_progress += 1
            self.check_study_progress()
            return "Лекция прослушана! +1 очко"
        return "Недостаточно энергии или учеба завершена"

    def study_exam(self):
        if self.energy >= 2000 and not self.university_passed:
            self.energy -= 2000
            self.study_progress += 10
            self.check_study_progress()
            return "Экзамен сдан! +10 очков"
        return "Недостаточно энергии или учеба завершена"


    def get_daily_stats(self):
        """Возвращает изменения за текущий день."""
        return {
            "money_change": self.money - self.start_money - self.s_money,
            "karma_change": self.karma - self.start_karma - self.s_karma,
            "study_change": self.study_progress - self.start_study_progress - self.s_study_progress
        }


    def start_day(self):
        """Сохраняет текущие значения как начальные для текущего дня."""
        self.start_money = self.money
        self.start_karma = self.karma
        self.start_study_progress = self.study_progress


    def process_day(self):
        """
    Обрабатывает переход к следующему дню.

    Returns:
        str: Случайное событие дня из plot_inserts
    """
        self.s_money = self.money
        self.s_karma = self.karma
        self.s_study_progress = self.study_progress

        # Обновляем историю каждого дня
        self.monthly_money_history.append(self.money)
        self.monthly_study_history.append(self.study_progress)


        # Начало нового месяца
        if self.total_days % 30 == 1:
            self.monthly_start_money = self.money
            self.monthly_start_karma = self.karma
            self.monthly_start_study_progress = self.study_progress
            self.monthly_money_history = [self.money]
            self.monthly_study_history = [self.study_progress]
            self.monthly_money_history.append(self.money)  # Добавляем начальное значение
            self.monthly_study_history.append(self.study_progress)

        # Конец месяца (день 30, 60, 90 и т.д.)
        if self.total_days % 30 == 0:
            # Рассчитываем изменения за месяц
            self.monthly_money_change = self.money - self.monthly_start_money
            self.monthly_karma_change = self.karma - self.monthly_start_karma
            self.monthly_study_progress = self.study_progress - self.monthly_start_study_progress

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
        self.event_day += 1
        current_day = self.event_day
        chances = [1, 15, 30, 75, 100]

        if current_day > 5:
            current_day = 5  # Ограничение до 5 дней

        current_chance = chances[current_day - 1]
        trigger_event = False

        # Проверка шанса или завершения цикла
        if random.random() * 100 <= current_chance:
            trigger_event = True
        elif current_day == 5:
            trigger_event = True

        if trigger_event:
            available_events = []
            for event in PLOT_EVENTS:
                available_events.append(event)

            if available_events:
                selected_event = random.choice(available_events)
                self.plot_events.append(selected_event)

            # Сброс счетчика после события
            self.event_day = 0
        else:
            # Если не дошли до 5 дня, сохраняем текущий день
            if current_day < 5:
                self.event_day = current_day
        if self.startup_started:
            self.startup_phase += 1
            if self.startup_phase == 5:
                pass

        self.s_money -= self.money
        self.s_karma -= self.karma
        self.s_study_progress -= self.study_progress


        return random.choice(self.plot_inserts)


    def update(self):
        if self.total_days == 465:
            if self.money >= 4000000:
                self.total_days +=1
                return "dream"
            elif self.military_ID:
                self.total_days += 1
                return "boring_job"
            else:
                self.total_days += 1
                return "army"

        if self.illegal_activity_score >= 50:
            return "prison"

        if self.failed_exam:
            return "army"

        if self.total_days == 105 and self.is_summer1_been == False:
            state = "summer1"
            return state

        if self.total_days == 225 and self.is_summer2_been == False:
            return "summer2"

        if self.total_days == 345 and self.is_summer3_been == False:
            return "summer3"
        if self.total_days == 45 or self.total_days == 165 or self.total_days ==285:
            return "summer4"

        return None


    def handle_event(self, event_data):
        current_screen_size = pygame.display.get_surface().get_size()  # Получаем актуальный размер
        try:
            bg = pygame.image.load(event_data["bg"]).convert()
            bg = pygame.transform.scale(bg, current_screen_size)  # Масштабируем под текущее разрешение
        except:
            bg = pygame.Surface(current_screen_size)
            bg.fill(PURPLE)


        # Создаем поверхность для текста события
        text_height = int(current_screen_size[1] * 0.15)
        text_surface = pygame.Surface((current_screen_size[0], text_height), pygame.SRCALPHA)
        text_surface.fill((0, 0, 0, 128))  # Полупрозрачный чёрный фон (30% прозрачности)

        # Формируем текст
        text = "\n".join(event_data["text"])  # Если text список строк
        max_width = current_screen_size[0] - 40  # Ширина с отступами (20 пикселей слева/справа)
        lines = self.wrap_text(text, max_width, MAIN_FONT)  # Переносим текст

        y = 10
        for line in lines:
            text_line = MAIN_FONT.render(line, True, WHITE)
            text_surface.blit(text_line, (20, y))  # Отступ слева 20 пикселей
            y += MAIN_FONT.get_height() + 10

        buttons = []
        total_buttons = len(event_data["options"])
        button_height = 50
        spacing = 10
        start_y = (current_screen_size[1] - text_height) - 100
        k = 0
        for i, option in enumerate(event_data["options"]):
            k+=1
            start_y = start_y - (button_height + spacing) * i
        if k == 3:
            start_y = start_y + 60
        button_width = 800
        for i, option in enumerate(event_data["options"]):
            y = start_y + (button_height + spacing) * i
            btn_color = BLACK
            # Используем GradientButton вместо Button
            btn = GradientButton(
                (current_screen_size[0] - button_width) // 2,  # Центрирование
                y,
                button_width,
                button_height,
                option["text"],
                btn_color,
                WHITE
            )
            buttons.append(btn)

        return bg, buttons, text_surface

    def wrap_text(self, text, max_width, font):
        """
        Разбивает текст на строки, чтобы он помещался в заданную ширину.
        Args:
            text (str): Исходный текст.
            font (pygame.font.Font): Шрифт для расчета размера текста.
            max_width (int): Максимальная ширина строки.
        Returns:
            list: Список строк, разбитых по ширине.
        """
        if not isinstance(text, str):
            text = str(text)  # Преобразуем в строку, если это не строка
        words = text.split(' ')
        lines = []
        current_line = ''
        for word in words:
            test_line = current_line + word + ' '
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + ' '
        lines.append(current_line.strip())
        return lines


    def apply_event_effects(self, selected_option):
        # Базовые эффекты (всегда применяются)
        base_effects = selected_option.get("effects", {})
        for key, value in base_effects.items():
            if key == "max_energy":
                self.max_energy += value
                # Не допускаем превышение текущей энергии
                if self.energy > self.max_energy:
                    self.energy = self.max_energy
            elif key == "energy":
                self.energy += value
            elif key == "karma":
                self.karma += value
            elif key == "startup_participated":
                self.startup_participated = value
            elif key == "gym_participated":
                self.gym_participated = value
            elif key == "study_bonus":
                self.study_progress += value
            elif key == "money":
                self.add_money(value)
            elif key == "endurance":
                self.endurance += value
            elif key == "startup_started":
                self.startup_started = True
                self.startup_phase = 0
            elif key == "discount":
                self.daily_expense_buff -= value  # Пример обработки скидки
            elif key == "study_score":
                self.study_progress += value
            elif key == "energy_cost":
                self.energy -= value  # Затраты энергии

        # Определяем, есть ли вероятностные исходы в опции
        has_probability = any(
            key in selected_option for key in ["chance", "success", "failure", "mid"]
        )

        if has_probability:
            # Обработка вероятностных исходов
            success_chance = selected_option.get("success", {}).get("chance", 0.0)
            mid_chance = selected_option.get("mid", {}).get("chance", 0.0)
            failure_chance = selected_option.get("failure", {}).get("chance", 0.0)

            # Убедимся, что сумма вероятностей не превышает 100%
            total_chance = success_chance + mid_chance + failure_chance
            if total_chance > 1.0:
                # Нормализуем вероятности, если сумма превышает 100%
                success_chance /= total_chance
                mid_chance /= total_chance
                failure_chance /= total_chance

            random_num = random.random()

            # Определяем исход
            if random_num < success_chance:
                outcome = selected_option.get("success", {})
                self.set_current_plot_text(outcome.get("message", "Успех!"))
            elif random_num < success_chance + mid_chance:
                outcome = selected_option.get("mid", {})
                self.set_current_plot_text(outcome.get("message", "Средний результат"))
            else:
                outcome = selected_option.get("failure", {})
                self.set_current_plot_text(outcome.get("message", "Провал..."))

            # Применяем эффекты выбранного исхода
            for key, value in outcome.items():
                if key == "money":
                    self.add_money(value)
                elif key == "study_score":
                    self.study_score += value
                elif key == "endurance":
                    self.endurance += value
                elif key == "karma":
                    self.karma += value
                elif key == "startup_phase":
                    self.startup_phase = value
                elif key == "max_energy":
                    self.max_energy += value
                    if self.energy > self.max_energy:
                        self.energy = self.max_energy
        else:
            # Для опций без вероятностных исходов
            self.current_plot_text = selected_option.get("message", "Без сообщения")

        # Обработка специфических эффектов
        if "startup_started" in base_effects:
            self.startup_participated = True
        if "gym_participated" in base_effects:
            self.gym_participated = True

        # Сохраняем время для таймера сообщения
        self.message_timer = pygame.time.get_ticks()


    def set_current_plot_text(self, text):
        """Устанавливает текст и обновляет таймер"""
        self.current_plot_text = text


    def check_message_timeout(self):
        """Проверяет, прошло ли время для скрытия сообщения"""
        if self.current_plot_text is not None:
            current_time = pygame.time.get_ticks()
            if current_time - self.message_timer > 5000:
                self.current_plot_text = None
                self.message_timer = 0  # Сброс таймера


    def draw_game_screen(self, screen):
        screen.fill((255, 255, 255))

        # Отрисовка current_plot_text
        if self.current_plot_text:
            font = pygame.font.Font(None, 36)
            text = font.render(self.current_plot_text, True, (0, 0, 0))
            screen.blit(text, (10, 10))

            study_progress = f"Учеба: {self.study_progress}/{self.study_goal}"
            study_text = MAIN_FONT.render(study_progress, True, WHITE)
            screen.blit(study_text, (600, 10))


    def lottery(self):
        """
        Обрабатывает участие в лотерее.

        Returns:
            str: Сообщение о результате участия в лотерее
        """
        if self.money >= self.lottery_cost:
            self.add_money(-self.lottery_cost)
            if random.random() < 0.5:
                self.lottery_prize = random.randint(200, 1000)
                self.add_money(self.lottery_prize)
                # Устанавливаем сообщение через set_current_plot_text:
                self.set_current_plot_text(f"Поздравляем! Вы выиграли {self.lottery_prize}")
                return f"Поздравляем! Вы выиграли {self.lottery_prize}"
            else:
                self.set_current_plot_text("Извините, вам не повезло в этот раз.")
                return "Извините, вам не повезло в этот раз."
        else:
            self.set_current_plot_text("Недостаточно денег для участия в лотерее.")
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
            "start_money": self.start_money,
            "start_karma": self.start_karma,
            "start_study_progress": self.start_study_progress,
            "current_season_index": self.current_season_index,
            "monthly_money_change": self.monthly_money_change,
            "monthly_karma_change": self.monthly_karma_change,
            "monthly_study_progress": self.monthly_study_progress,
            "monthly_money_history": self.monthly_money_history,
            "monthly_study_history": self.monthly_study_history,
            "monthly_start_money": self.monthly_start_money,
            "monthly_start_karma": self.monthly_start_karma,
            "monthly_start_study_progress": self.monthly_start_study_progress,
            "failed_exam": self.failed_exam,
            "illegal_activity_score": self.illegal_activity_score,
            "last_scholarship_amount": self.last_scholarship_amount,
            "s_money": self.s_money,
            "s_karma": self.s_karma,
            "s_study_progress": self.s_study_progress,
            "max_energy": self.max_energy,
            "mining_income": self.mining_income,
            "work_income": self.work_income,
            "scholarship": self.scholarship,
            "rent_paid": self.rent_paid,
            "rent_cost": self.rent_cost,
            "housing_bonus": self.housing_bonus,
            "expensive_item_goal": self.expensive_item_goal,
            "current_item_savings": self.current_item_savings,
            "daily_expenses": self.daily_expenses,
            "daily_expense_buff": self.daily_expense_buff,
            "endurance": self.endurance,
            "startup_participated": self.startup_participated,
            "gym_participated": self.gym_participated,
            "startup_phase": self.startup_phase,
            "startup_started": self.startup_started,
            "sport_endurance_bonus": self.sport_endurance_bonus,
            "plot_events": self.plot_events,
            "current_plot_text": self.current_plot_text,
            "message_timer": self.message_timer,
            "used_events": list(self.used_events),  # Преобразуем множество в список
            "event_day": self.event_day,
            "max_event_days": self.max_event_days,
            "military_ID": self.military_ID,
            "is_summer1_been": self.is_summer1_been,
            "is_summer2_been": self.is_summer2_been,
            "is_summer3_been": self.is_summer3_been,

            # Добавляем сохранение купленных предметов
            "purchased_items": list(self.purchased_items),
            "current_month_day": self.current_month_day,

            "has_shown_tutorial": self.has_shown_tutorial,
            "has_shown_tutorial_f": self.has_shown_tutorial_f,
            "has_shown_tutorial_t": self.has_shown_tutorial_t,
            "has_shown_tutorial_p2p": self.has_shown_tutorial_p2p
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
                self.start_money = data.get("start_money", self.money)
                self.start_karma = data.get("start_karma", self.karma)
                self.start_study_progress = data.get("start_study_progress", self.study_progress)
                self.monthly_money_change = data.get("monthly_money_change", 0)
                self.monthly_karma_change = data.get("monthly_karma_change", 0)
                self.monthly_study_progress = data.get("monthly_study_progress", 0.0)
                self.monthly_money_history = data.get("monthly_money_history", [])
                self.monthly_study_history = data.get("monthly_study_history", [])
                self.monthly_start_money = data.get("monthly_start_money", self.money)
                self.monthly_start_karma = data.get("monthly_start_karma", self.karma)
                self.monthly_start_study_progress = data.get("monthly_start_study_progress", self.study_progress)
                self.current_month_day = data.get("current_month_day", 0)
                self.failed_exam = data.get("failed_exam", False)
                self.illegal_activity_score = data.get("illegal_activity_score", 0)
                self.last_scholarship_amount = data.get("last_scholarship_amount", None)
                self.s_money = data.get("s_money", 0)
                self.s_karma = data.get("s_karma", 0)
                self.s_study_progress = data.get("s_study_progress", 0)
                self.max_energy = data.get("max_energy", 3000)
                self.mining_income = data.get("mining_income", 10)
                self.work_income = data.get("work_income", 20)
                self.scholarship = data.get("scholarship", 1000)
                self.rent_paid = data.get("rent_paid", True)
                self.rent_cost = data.get("rent_cost", 100)
                self.housing_bonus = data.get("housing_bonus", 0)
                self.expensive_item_goal = data.get("expensive_item_goal", 5000)
                self.current_item_savings = data.get("current_item_savings", 0)
                self.daily_expenses = data.get("daily_expenses", 10)
                self.daily_expense_buff = data.get("daily_expense_buff", 0)
                self.endurance = data.get("endurance", 100)
                self.startup_participated = data.get("startup_participated", False)
                self.gym_participated = data.get("gym_participated", False)
                self.startup_phase = data.get("startup_phase", 0)
                self.startup_started = data.get("startup_started", False)
                self.sport_endurance_bonus = data.get("sport_endurance_bonus", 0)
                self.plot_events = data.get("plot_events", [])
                self.current_plot_text = data.get("current_plot_text", None)
                self.message_timer = data.get("message_timer", 0)
                self.used_events = set(data.get("used_events", []))  # Преобразуем список обратно во множество
                self.event_day = data.get("event_day", 0)
                self.max_event_days = data.get("max_event_days", 5)
                self.military_ID = data.get("military_ID", False)
                self.is_summer1_been = data.get("is_summer1_been", False)
                self.is_summer2_been = data.get("is_summer2_been", False)
                self.is_summer3_been = data.get("is_summer3_been", False)

                # Загрузка купленных предметов
                self.purchased_items = set(data.get("purchased_items", []))

                self.has_shown_tutorial = data.get("has_shown_tutorial", False)
                self.has_shown_tutorial_f = data.get("has_shown_tutorial_f", False)
                self.has_shown_tutorial_t = data.get("has_shown_tutorial_t", False)
                self.has_shown_tutorial_p2p = data.get("has_shown_tutorial_p2p", False)

        except FileNotFoundError:
            print("Сохранение не найдено. Начинаем новую игру.")


    def whats_day(self):
        return self.total_days


    def show_delivery_tutorial(self, screen):
        """Отображает обучение для мини-игры доставки"""
        tutorial_running = True
        clock = pygame.time.Clock()

        # Заливка фона
        screen.fill(BLACK)

        # Создаем поверхность для текста обучения
        tutorial_text = [
            "Правила мини-игры доставки:",
            "Вы — зеленый квадрат.",
            "Ваша задача — добраться до финишной точки (красного квадрата).",
            "Избегайте препятствия (серые квадраты).",
            "Управление: стрелки или клавиши WASD.",
            "Закончите доставку за отведенное время."
        ]

        font = MAIN_FONT
        text_height = font.get_height() + 10
        y_offset = 50

        # Отрисовываем текст обучения
        for line in tutorial_text:
            text_surface = font.render(line, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.screen_size[0] // 2, y_offset))
            screen.blit(text_surface, text_rect)
            y_offset += text_height

        # Кнопка "Начать игру"
        start_button = Button(
            self.screen_size[0] // 2 - 100,
            self.screen_size[1] - 100,
            200,
            50,
            "Начать игру",
            GREEN,
            WHITE
        )
        start_button.draw(screen)

        while tutorial_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if start_button.is_clicked(mouse_pos):
                        tutorial_running = False

            pygame.display.flip()
            clock.tick(10)

    def show_freelance_tutorial(self, screen):
        """Отображает обучение для мини-игры Фриланса"""
        tutorial_running = True
        clock = pygame.time.Clock()

        # Заливка фона
        screen.fill(BLACK)

        # Создаем поверхность для текста обучения
        tutorial_text = [
            "Правила мини-игры Фриланса:",
            "Разместите все блоки на правильных позициях, чтобы завершить заказ.",
            "Блоки можно выбирать в помощью стрелок вверх/вниз или W/S.",
            "Подтверждать выбор или размещение блока можно нажатием SPACE.",
            "Блоки кода можно перемещать с помощью стрелок или клавиш WASD.",
            "У вас есть ограниченное время для выполнения задания."
        ]

        font = MAIN_FONT
        text_height = font.get_height() + 10  
        y_offset = 50

        # Отрисовываем текст обучения
        for line in tutorial_text:
            text_surface = font.render(line, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.screen_size[0] // 2, y_offset))
            screen.blit(text_surface, text_rect)
            y_offset += text_height

        # Кнопка "Начать игру"
        start_button = Button(
            self.screen_size[0] // 2 - 100,
            self.screen_size[1] - 100,
            200,
            50,
            "Начать игру",
            GREEN,
            WHITE
        )
        start_button.draw(screen)

        # Основной цикл туториала
        while tutorial_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if start_button.is_clicked(mouse_pos):
                        tutorial_running = False  # Завершаем туториал

            pygame.display.flip()
            clock.tick(10)

    def show_trading_tutorial(self, screen):
        """Отображает обучение для мини-игры Трейдинга"""
        tutorial_running = True
        clock = pygame.time.Clock()

        # Заливка фона
        screen.fill(BLACK)

        # Создаем поверхность для текста обучения
        tutorial_text = [
            "Правила мини-игры Трейдинга:",
            "Ваша задача — покупать акции по низкой цене и продавать их по высокой.",
            "Используйте кнопки 'Купить' и 'Продать', чтобы управлять акциями.",
            "Успешная сделка увеличивает ваш баланс.",
            "Если ваш баланс станет меньше начального, вы проиграете.",
            "Игра завершается, когда истечет время или вы выполните цель.",
            "Цель: сохранить или увеличить свой начальный баланс."
        ]

        font = MAIN_FONT
        text_height = font.get_height() + 10
        y_offset = 50

        # Отрисовываем текст обучения
        for line in tutorial_text:
            text_surface = font.render(line, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.screen_size[0] // 2, y_offset))
            screen.blit(text_surface, text_rect)
            y_offset += text_height

        # Кнопка "Начать игру"
        start_button = Button(
            self.screen_size[0] // 2 - 100,
            self.screen_size[1] - 100,
            200,
            50,
            "Начать игру",
            GREEN,
            WHITE
        )
        start_button.draw(screen)

        # Основной цикл туториала
        while tutorial_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if start_button.is_clicked(mouse_pos):
                        tutorial_running = False  # Завершаем туториал

            pygame.display.flip()
            clock.tick(10)

    def show_p2p_tutorial(self, screen):
        """Отображает обучение для мини-игры Трейдинга"""
        tutorial_running = True
        clock = pygame.time.Clock()

        # Заливка фона
        screen.fill(BLACK)

        # Создаем поверхность для текста обучения
        tutorial_text = [
            "Правила мини-игры P2P:",
            "Вы будете проверять документы клиентов.",
            "",
            "Вам нужно решить: одобрить или отклонить сделку.",
            "Решение принимается на основе информации о клиенте:",
            "- Рейтинг доверия",
            "- Уровень риска",
            "",
            "Чтобы одобрить — подпишите документ мышью внутри области.",
            "Подпись обязательна для подтверждения решения!",
            "",
            "У вас есть 3 жизни. За каждую ошибку теряется одна жизнь.",
            "Если жизни закончатся — вы получите штраф.",
            "",
            "Система может давать рекомендации...",
            "...но не всегда стоит ей слепо доверять."
        ]

        font = MAIN_FONT
        text_height = font.get_height() + 10
        y_offset = 50

        # Отрисовываем текст обучения
        for line in tutorial_text:
            text_surface = font.render(line, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.screen_size[0] // 2, y_offset))
            screen.blit(text_surface, text_rect)
            y_offset += text_height

        # Кнопка "Начать игру"
        start_button = Button(
            self.screen_size[0] // 2 - 100,
            self.screen_size[1] - 100,
            200,
            50,
            "Начать игру",
            GREEN,
            WHITE
        )
        start_button.draw(screen)

        # Основной цикл туториала
        while tutorial_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if start_button.is_clicked(mouse_pos):
                        tutorial_running = False  # Завершаем туториал

            pygame.display.flip()
            clock.tick(10)

    def play_delivery_game(self, order_salary):
        """Мини-игра доставки"""
        # Проверяем, нужно ли показать обучение
        if not self.has_shown_tutorial:
            self.show_delivery_tutorial(screen)
            self.has_shown_tutorial = True

        # Вычисляем energy_cost на основе зарплаты
        energy_cost = (
            100 if order_salary <= 1000 else
            200 if order_salary <= 5000 else 300
        )

        # Проверяем достаточно ли энергии перед запуском мини-игры
        if self.energy < energy_cost:
            self.set_current_plot_text("Недостаточно энергии!")
            return
        delivery_game = DeliveryMinigame(self.screen_size)
        clock = pygame.time.Clock()
        running = True
        message_start_time = 0
        message_duration = 3000
        game_result = None

        while running:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        break

            delivery_game.update(keys)

            # Проверяем условия завершения игры
            if delivery_game.is_completed():
                game_result = "completed"
                running = False
            elif delivery_game.is_crashed():
                game_result = "crashed"
                running = False
            elif delivery_game.is_timeout:
                game_result = "timeout"
                running = False

            screen.fill(BLACK)
            delivery_game.draw(screen)
            pygame.display.flip()
            clock.tick(10)

        # Обработка результата игры
        if game_result == "completed":
            self.add_money(order_salary)
            self.energy -= 100
            self.set_current_plot_text(f"Вы доставили заказ и получили {order_salary}$")
        elif game_result in ["crashed", "timeout"]:
            if game_result == "crashed":
                order_salary = - order_salary
                order_salary /= 2
                self.set_current_plot_text(f"Вы повредили заказ и вам полагается штраф {order_salary}$")
                self.add_money(order_salary)
            elif game_result == "timeout":
                self.set_current_plot_text("Время вышло... Вы не смогли доставить заказ.")
            self.energy -= 100

        # Установка времени начала показа сообщения
        message_start_time = pygame.time.get_ticks()

        # Показываем сообщение дольше
        while pygame.time.get_ticks() - message_start_time < message_duration:
            screen.fill(BLACK)
            if self.current_plot_text:
                text_surface = MAIN_FONT.render(self.current_plot_text, True, WHITE)
                screen.blit(text_surface, (
                    self.screen_size[0] // 2 - text_surface.get_width() // 2,
                    self.screen_size[1] // 2 - text_surface.get_height() // 2))
            pygame.display.flip()
            clock.tick(10)

    def play_freelance_game(self, order_salary):
        """Мини-игра Фриланса"""
        # Проверяем, нужно ли показать обучение
        if not self.has_shown_tutorial_f:
            self.show_freelance_tutorial(screen)
            self.has_shown_tutorial_f = True

        # Вычисляем energy_cost на основе зарплаты
        energy_cost = (
            100 if order_salary <= 1000 else
            200 if order_salary <= 5000 else 300
        )

        # Проверяем достаточно ли энергии перед запуском мини-игры
        if self.energy < energy_cost:
            self.set_current_plot_text("Недостаточно энергии!")
            return
        freelance_game = FreelanceCodeMinigame(self.screen_size)
        freelance_game.start_game()
        clock = pygame.time.Clock()
        running = True
        message_start_time = 0
        message_duration = 3000

        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        break

            keys = pygame.key.get_pressed()
            mouse_pos = pygame.mouse.get_pos()

            freelance_game.update(keys, mouse_pos, events)

            if freelance_game.is_completed() or freelance_game.is_failed():
                running = False

            screen.fill(BLACK)
            freelance_game.draw(screen)
            pygame.display.flip()
            clock.tick(10)

        # Обработка результата игры
        if freelance_game.is_completed():
            self.add_money(order_salary)
            self.energy -= energy_cost
            self.set_current_plot_text(f"Вы выполнили заказ и получили {order_salary}$")
        elif freelance_game.is_failed():
            order_salary = - order_salary
            order_salary /= 2
            self.set_current_plot_text(f"Время вышло... Вы не смогли завершить проект и вам полагается штраф {order_salary}$")
            self.energy -= energy_cost
            self.add_money(order_salary)

        # Установка времени начала показа сообщения
        message_start_time = pygame.time.get_ticks()

        # Показываем сообщение дольше
        while pygame.time.get_ticks() - message_start_time < message_duration:
            screen.fill(BLACK)
            if self.current_plot_text:
                text_surface = MAIN_FONT.render(self.current_plot_text, True, WHITE)
                screen.blit(text_surface, (
                    self.screen_size[0] // 2 - text_surface.get_width() // 2,
                    self.screen_size[1] // 2 - text_surface.get_height() // 2))
            pygame.display.flip()
            clock.tick(10)

    def play_trading_game(self, order_salary):
        """Мини-игра Трейдинга"""
        # Проверяем, нужно ли показать обучение
        if not self.has_shown_tutorial_t:
            self.show_trading_tutorial(screen)
            self.has_shown_tutorial_t = True

        energy_cost = (100 if order_salary <= 1000 else 200 if order_salary <= 5000 else 300)
        if self.energy < energy_cost:
            self.set_current_plot_text("Недостаточно энергии!")
            return
        trading_game = TradingMinigame(self.screen_size)
        clock = pygame.time.Clock()
        running = True
        message_start_time = 0
        message_duration = 3000

        while running:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                trading_game.handle_event(event)

            # Обновляем состояние мини-игры
            trading_game.update(keys)

            if trading_game.is_completed() or trading_game.is_failed():
                running = False

            screen.fill(BLACK)
            trading_game.draw(screen)
            pygame.display.flip()
            clock.tick(10)

            # Обработка результата игры
        if trading_game.is_completed():
            self.add_money(order_salary)
            self.energy -= energy_cost
            self.set_current_plot_text(f"Вы успешно заработали {order_salary}$")
        elif trading_game.is_failed():
            order_salary = - order_salary
            order_salary /= 2
            self.set_current_plot_text(f"Вы не смогли увеличить свой баланс. Вам полагается штраф {order_salary}$")
            self.energy -= energy_cost
            self.add_money(order_salary)

            # Установка времени начала показа сообщения
        message_start_time = pygame.time.get_ticks()

        # Показываем сообщение дольше
        while pygame.time.get_ticks() - message_start_time < message_duration:
            screen.fill(BLACK)
            if self.current_plot_text:
                text_surface = MAIN_FONT.render(self.current_plot_text, True, WHITE)
                screen.blit(text_surface, (
                    self.screen_size[0] // 2 - text_surface.get_width() // 2,
                    self.screen_size[1] // 2 - text_surface.get_height() // 2))
            pygame.display.flip()
            clock.tick(10)

    def play_p2p_game(self, order_salary):
        """Мини-игра P2P"""
        # Проверяем, нужно ли показать обучение
        if not self.has_shown_tutorial_p2p:
            self.show_p2p_tutorial(screen)
            self.has_shown_tutorial_p2p = True

        energy_cost = (100 if order_salary <= 1000 else 200 if order_salary <= 5000 else 300)
        if self.energy < energy_cost:
            self.set_current_plot_text("Недостаточно энергии!")
            return

        p2p_game = P2PMinigame(self.screen_size, Button)
        clock = pygame.time.Clock()
        running = True
        message_start_time = 0
        message_duration = 3000

        while running:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                p2p_game.handle_event(event)

            screen.fill(BLACK)
            p2p_game.draw(screen)
            pygame.display.flip()
            clock.tick(30)

            if p2p_game.is_completed() or p2p_game.is_failed():
                running = False

            # Обработка результата игры
        if p2p_game.is_completed():
            self.add_money(order_salary)
            self.energy -= energy_cost
            self.set_current_plot_text(f"Вы приняли верное решение для каждой сделки и получили {order_salary}$")
        elif p2p_game.is_failed():
            order_salary = - order_salary
            order_salary /= 2
            self.set_current_plot_text(f"Вы допустили слишком много ошибок. Вам полагается штраф {order_salary}$")
            self.energy -= energy_cost
            self.add_money(order_salary)

            # Установка времени начала показа сообщения
        message_start_time = pygame.time.get_ticks()

        # Показываем сообщение дольше
        while pygame.time.get_ticks() - message_start_time < message_duration:
            screen.fill(BLACK)
            if self.current_plot_text:
                text_surface = MAIN_FONT.render(self.current_plot_text, True, WHITE)
                screen.blit(text_surface, (
                    self.screen_size[0] // 2 - text_surface.get_width() // 2,
                    self.screen_size[1] // 2 - text_surface.get_height() // 2))
            pygame.display.flip()
            clock.tick(10)


class WorkManager:
    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.work_categories = ["Курьерство", "Фриланс", "Трейдинг", "P2P"]
        self.current_category = "Курьерство"
        self.selected_order = None

        # Новая структура данных для заказов
        self.orders = {
            "Курьерство": [
                {"name": "Доставка еды", "desc": "Доставка из ресторана", "salary": 300, "enrg": 100},
                {"name": "Посылка", "desc": "Доставка небольшой посылки", "salary": 500, "enrg": 300},
                {"name": "Документы", "desc": "Срочная доставка документов", "salary": 700, "enrg": 500}
            ],
            "Фриланс": [
                {"name": "Лендинг", "desc": "Создание одностраничного сайта", "salary": 2000, "enrg": 100},
                {"name": "Мобильное приложение", "desc": "Простое приложение", "salary": 5000, "enrg": 300},
                {"name": "CRM система", "desc": "Система управления клиентами", "salary": 10000, "enrg": 500}
            ],
            "Трейдинг": [
                {"name": "Фьючерсы", "desc": "Высокий риск", "salary": 1500, "enrg": 100},
                {"name": "Опционы", "desc": "Очень высокий риск", "salary": 2500, "enrg": 300},
                {"name": "Акции", "desc": "Средний риск", "salary": 1000, "enrg": 500}
            ],
            "P2P": [
                {"name": "Обмен валют", "desc": "Наличные/Безнал", "salary": 800, "enrg": 100},
                {"name": "Гарант сервис", "desc": "Обеспечение сделки", "salary": 1200, "enrg": 300},
                {"name": "Кредитование", "desc": "Микрозаймы", "salary": 1500, "enrg": 500}
            ]
        }
        self.requirements = {
            "Фриланс": ["Курс по SEO", "Фigma", "Python курс"],
            "Трейдинг": ["Курс 'Понятие рынка'", "Курс 'межбиржевое влияние'"],
            "P2P": [
                "Нанять сотрудника",
                "Дроповод",
                "Мерчант Биржи",
                "Обучение связке",
                "Увеличить баланс",
                "Телефон"
            ]
        }

    def draw_p2p_screen(self, screen, game, current_width):
        required_items = [
            "Нанять сотрудника",
            "Дроповод",
            "Мерчант Биржи",
            "Обучение связке",
            "Увеличить баланс",
            "Телефон"
        ]

        missing_items = [item for item in required_items if item not in game.purchased_items]

        if missing_items:
            # Отображение окна с просьбой приобрести недостающие предметы
            overlay = pygame.Surface((current_width, screen.get_height()))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(128)
            screen.blit(overlay, (0, 0))

            message = "Для работы в P2P необходимо приобрести:"
            text_surface = MAIN_FONT.render(message, True, WHITE)
            screen.blit(text_surface, (current_width // 2 - text_surface.get_width() // 2, 200))

            y_offset = 250
            for item in missing_items:
                item_text = SMALL_FONT.render(f"- {item}", True, YELLOW)
                screen.blit(item_text, (current_width // 2 - item_text.get_width() // 2, y_offset))
                y_offset += 30

            shop_button = Button(current_width // 2 - 100, y_offset + 20,
                                 200, 50, "Перейти в магазин", GREEN, WHITE)
            shop_button.draw(screen)

            exit_button = Button(current_width - 150, 20, 100, 50, "Выход", RED, WHITE)
            exit_button.draw(screen)

            return [], shop_button, exit_button

        else:
            # Отображение заказов для P2P
            orders = self.orders["P2P"]
            order_buttons = []
            for i, order in enumerate(orders):
                order_rect = pygame.Rect(50, 50 + i * 100, current_width - 100, 90)
                pygame.draw.rect(screen, (50, 80, 50), order_rect)

                name_text = f"{order['name']} — {order['desc']}"
                salary_text = f"Оплата: {order['salary']}$"

                name_surface = SMALL_FONT.render(name_text, True, WHITE)
                salary_surface = SMALL_FONT.render(salary_text, True, YELLOW)

                screen.blit(name_surface, (60, 60 + i * 100))
                screen.blit(salary_surface, (60, 80 + i * 100))

                order_button = Button(order_rect.x, order_rect.y,
                                      order_rect.width, order_rect.height,
                                      "", GREEN, WHITE)
                order_buttons.append(order_button)

            exit_button = Button(current_width - 150, 20, 100, 50, "Выход", RED, WHITE)
            exit_button.draw(screen)

            return order_buttons, None, exit_button


    def handle_order_click(self, mouse_pos, game):
        """Обрабатывает клик по заказу и выдает вознаграждение или запускает мини-игру"""
        orders = self.orders[self.current_category]
        for i, order in enumerate(orders):
            order_rect = pygame.Rect(50, 50 + i * 100, game.screen_size[0] - 100, 90)
            if order_rect.collidepoint(mouse_pos):
                if self.current_category == "Курьерство":
                    game.play_delivery_game(order['salary'])
                elif self.current_category == "Фриланс":
                    game.play_freelance_game(order['salary'])
                elif self.current_category == "Трейдинг":
                    game.play_trading_game(order['salary'])
                elif self.current_category == "P2P":
                    game.play_p2p_game(order['salary'])
                else:
                    # Для других категорий работ
                    energy_cost = 100 if order['salary'] <= 1000 else \
                        200 if order['salary'] <= 5000 else 300
                    if game.energy >= energy_cost:
                        game.add_money(order['salary'])
                        game.energy -= energy_cost
                        self.orders[self.current_category].remove(order)
                        self.generate_new_order(self.current_category)
                        game.set_current_plot_text(
                            f"Вы выполнили заказ: {order['name']} и получили {order['salary']}$"
                        )
                        return True
                    else:
                        game.set_current_plot_text("Недостаточно энергии!")
                        return False
        return False

    def generate_new_order(self, category):
        """Генерирует новый заказ для указанной категории"""
        base_orders = {
            "Курьерство": [
                {"name": "Доставка еды", "desc": "Доставка из ресторана", "salary": random.randint(300, 700)},
                {"name": "Посылка", "desc": "Доставка небольшой посылки", "salary": random.randint(500, 900)},
                {"name": "Документы", "desc": "Срочная доставка документов", "salary": random.randint(700, 1200)}
            ],
            "Фриланс": [
                {"name": "Лендинг", "desc": "Создание одностраничного сайта", "salary": random.randint(2000, 3000)},
                {"name": "Мобильное приложение", "desc": "Простое приложение", "salary": random.randint(5000, 7000)},
                {"name": "CRM система", "desc": "Система управления клиентами", "salary": random.randint(10000, 15000)}
            ],
            "Трейдинг": [
                {"name": "Фьючерсы", "desc": "Высокий риск", "salary": random.randint(1000, 1500)},
                {"name": "Опционы", "desc": "Очень высокий риск", "salary": random.randint(2000, 2500)},
                {"name": "Акции", "desc": "Средний риск", "salary": random.randint(800, 1200)}
            ],
            "P2P": [
                {"name": "Обмен валют", "desc": "Наличные/Безнал", "salary": random.randint(600, 800)},
                {"name": "Гарант сервис", "desc": "Обеспечение сделки", "salary": random.randint(1000, 1200)},
                {"name": "Кредитование", "desc": "Микрозаймы", "salary": random.randint(1300, 1500)}
            ]
        }

        new_order = random.choice(base_orders[category])
        self.orders[category].append(new_order)

    def draw_work_screen(self, screen, game, current_width, mouse_pos):
        """Отрисовывает экран работы"""
        screen.fill((30, 60, 30))  # Заливка фона

        category_buttons = []  # Список кнопок категорий
        subcategory_buttons = []  # Пустой список подкатегорий
        exit_button = None  # Кнопка выхода

        # Отрисовка категорий работ
        category_x = 50
        category_y = screen.get_height() - 100
        button_width = (current_width - 300) // len(self.work_categories)
        button_height = 50
        button_spacing = 10

        day_season_text = MAIN_FONT.render(f"День {game.total_days} ({game.season})", True, WHITE)
        screen.blit(day_season_text, (50, 10))


        try:
            energy_icon = pygame.image.load('png/energe.png').convert_alpha()
            energy_icon = pygame.transform.scale(energy_icon, (40, 40))
        except Exception as e:
            print(f"Ошибка загрузки energe.png: {e}")
            energy_icon = pygame.Surface((40, 40))
            energy_icon.fill(BLUE)

        try:
            money_icon = pygame.image.load('png/money.png').convert_alpha()
            money_icon = pygame.transform.scale(money_icon, (40, 40))
        except Exception as e:
            print(f"Ошибка загрузки money.png: {e}")
            money_icon = pygame.Surface((40, 40))
            money_icon.fill(YELLOW)

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

        if game.current_plot_text:
            font = pygame.font.Font(None, 36)
            text = font.render(game.current_plot_text, True, WHITE)
            screen.blit(text, (50, 45))



        for i, category in enumerate(self.work_categories):
            color = GREEN if category == self.current_category else BLUE

            # Проверяем требования для категории
            missing_items = []
            if category in self.requirements:
                missing_items = [item for item in self.requirements[category]
                                 if item not in game.purchased_items]

            if missing_items:
                color = RED  # Красный цвет если не хватает предметов
            elif category == self.current_category:
                color = GREEN
            else:
                color = BLUE

            # Создаем и отрисовываем кнопку категории
            button = Button(category_x + i * (button_width + button_spacing),
                            category_y,
                            button_width,
                            button_height,
                            category,
                            color,
                            WHITE)
            button.draw(screen)
            category_buttons.append(button)

            # Выводим информацию о требованиях при наведении
            if button.is_hovered(mouse_pos):  # Теперь работает, так как mouse_pos передан
                if missing_items:
                    text = SMALL_FONT.render(
                        f"Требуется: {', '.join(missing_items)}",
                        True, YELLOW
                    )
                    screen.blit(text, (button.rect.x, button.rect.y - 20))

        # Обработка специальных условий для текущей категории
        if self.current_category in self.requirements:
            missing_items = [item for item in self.requirements[self.current_category]
                             if item not in game.purchased_items]
            if missing_items:
                return self.draw_missing_items_screen(screen, current_width,
                                                      missing_items, "Работа")

        # Отображение заказов для текущей категории
        orders = self.orders[self.current_category]
        order_buttons = []
        for i, order in enumerate(orders):
            order_rect = pygame.Rect(50, 100 + i * 100, current_width - 100, 90)
            pygame.draw.rect(screen, (50, 80, 50), order_rect)

            name_text = f"{order['name']} — {order['desc']}"
            salary_text = f"Оплата: {order['salary']}$"

            name_surface = SMALL_FONT.render(name_text, True, WHITE)
            salary_surface = SMALL_FONT.render(salary_text, True, YELLOW)

            screen.blit(name_surface, (60, 110 + i * 100))
            screen.blit(salary_surface, (60, 130 + i * 100))

            # Добавляем кнопку "Выполнить"
            complete_button = Button(order_rect.x + order_rect.width - 120,
                                     order_rect.y + 10,
                                     100, 30,
                                     "Выполнить", GREEN, WHITE)
            complete_button.draw(screen)
            order_buttons.append(complete_button)

        # Кнопка выхода
        exit_button = Button(current_width - 150, 20, 100, 50, "Выход", RED, WHITE)
        exit_button.draw(screen)

        return category_buttons, subcategory_buttons, exit_button

    def draw_missing_items_screen(self, screen, current_width, missing_items, shop_category):
        """Отрисовывает экран с недостающими предметами"""
        overlay = pygame.Surface((current_width, screen.get_height()))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))

        message = "Для работы в этой категории необходимо приобрести:"
        text_surface = MAIN_FONT.render(message, True, WHITE)
        screen.blit(text_surface, (current_width // 2 - text_surface.get_width() // 2, 200))

        y_offset = 250
        for item in missing_items:
            item_text = SMALL_FONT.render(f"- {item}", True, YELLOW)
            screen.blit(item_text, (current_width // 2 - item_text.get_width() // 2, y_offset))
            y_offset += 30

        shop_button = Button(current_width // 2 - 100, y_offset + 20,
                             200, 50, "Перейти в магазин", GREEN, WHITE)
        shop_button.draw(screen)

        exit_button = Button(current_width - 150, 20, 100, 50, "Выход", RED, WHITE)
        exit_button.draw(screen)

        return [], shop_button, exit_button

    def handle_work_events(self, mouse_pos, game):
        """Обрабатывает события на рабочем экране"""
        new_state = None

        # Проверяем клики по категориям
        category_x = 50
        category_y = game.screen_size[1]/1.1
        button_width = (game.screen_size[0] - 300) // len(self.work_categories)
        button_height = 50
        button_spacing = 10

        for i, category in enumerate(self.work_categories):
            rect = pygame.Rect(category_x + i * (button_width + button_spacing),
                               category_y,
                               button_width,
                               button_height)
            if rect.collidepoint(mouse_pos):
                # Проверяем требования для выбранной категории
                if category in self.requirements:
                    missing_items = [item for item in self.requirements[category]
                                     if item not in game.purchased_items]

                    if missing_items:
                        # Если есть недостающие предметы, показываем предупреждение
                        game.set_current_plot_text(
                            f"Для работы в категории '{category}' нужны: "
                            f"{', '.join(missing_items)}"
                        )
                        return "work", game.current_plot_text

                # Если все требования выполнены, меняем категорию
                self.current_category = category
                break

        # Обработка заказов
        if not new_state:
            order_completed = self.handle_order_click(mouse_pos, game)

        # Проверка кнопки выхода
        exit_button_rect = pygame.Rect(game.screen_size[0] - 150, 20, 100, 50)
        if exit_button_rect.collidepoint(mouse_pos):
            new_state = "game"

        if new_state is not None:
            return new_state, game.current_plot_text



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
            if hasattr(pygame.display, 'get_desktop_sizes'):
                # Для pygame 2.0+
                monitor_sizes = pygame.display.get_desktop_sizes()
                monitor_size = monitor_sizes[0]
            else:
                # Для старых версий
                info = pygame.display.Info()
                monitor_size = (info.current_w, info.current_h)

            # Сброс текущих настроек окна
            pygame.display.set_mode((1, 1))

            # Устанавливаем позицию окна в (0,0)
            os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"

            # Создаем безрамочное окно размером с монитор
            screen = pygame.display.set_mode(
                monitor_size,
                pygame.NOFRAME | pygame.HWSURFACE | pygame.DOUBLEBUF
            )

            # Обновляем экран
            pygame.display.flip()

            return screen
        else:  # windowed
            screen = pygame.display.set_mode(resolution, pygame.RESIZABLE)

            # Центрирование окна через SDL environ
            os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (
                (screen.get_width() - resolution[0]) // 2,
                (screen.get_height() - resolution[1]) // 2
            )
            return screen
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
                    game.start_day()
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
        if game.plot_events:
            current_event = game.plot_events[-1]
            _, event_buttons, _ = game.handle_event(current_event)  # Не используем текст_поверхность здесь
            # Проверяем клик по кнопкам вариантов
            for i, btn in enumerate(event_buttons):
                if btn.is_clicked(mouse_pos):
                    selected_option = current_event["options"][i]
                    game.apply_event_effects(selected_option)
                    game.plot_events.pop()  # Удаляем событие из очереди
                    if selected_option.get("one_time", False):
                        game.used_events.add(current_event["name"])
                    current_plot_text = game.current_plot_text
                    return state, current_plot_text

        if settings_button.is_clicked(mouse_pos):
            current_settings_section = SETTINGS_SECTIONS["main"]
            return "game_settings", current_plot_text

        for action, button in game.buttons.items():
            if button.is_clicked(mouse_pos):
                if action == "study":
                    return "study_menu", current_plot_text
                elif action == "work":
                    return "work", current_plot_text
                elif action == "next_day":
                    stats = game.get_daily_stats()
                    if game.total_days % 30 == 0:
                        game.process_day()
                        return "end_of_month_stat", current_plot_text
                    else:
                        return "end_of_day_stat", current_plot_text
                elif action == "lottery":
                    return "game", game.lottery()
                elif action == "shop":
                    return "shop", current_plot_text

    elif state == "study_menu":  # <-- НОВЫЙ БЛОК ЗДЕСЬ
        if buttons["study_menu"]["lab"].is_clicked(mouse_pos):
            return "game", game.study_lab()
        elif buttons["study_menu"]["lecture"].is_clicked(mouse_pos):
            return "game", game.study_lecture()
        elif buttons["study_menu"]["exam"].is_clicked(mouse_pos):
            return "game", game.study_exam()
        elif buttons["study_menu"]["back"].is_clicked(mouse_pos):
            return "game", current_plot_text

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

            # Проверяем клики по кнопкам настроек экрана
        if current_settings_section == SETTINGS_SECTIONS["display"]:
            settings = load_settings()
            current_resolution = settings["resolution"]
            current_mode = settings["display_mode"]

            # Обработка кнопок разрешения
            if buttons["settings"]["display"]["hd"].is_clicked(mouse_pos):
                current_resolution = [1280, 720]
            elif buttons["settings"]["display"]["fhd"].is_clicked(mouse_pos):
                current_resolution = [1920, 1080]
            elif buttons["settings"]["display"]["qhd"].is_clicked(mouse_pos):
                current_resolution = [2560, 1440]

            # Обработка кнопок режима отображения
            for mode in DISPLAY_MODES:
                if buttons["settings"]["display"]["display_mode"][mode].is_clicked(mouse_pos):
                    current_mode = mode

            # Применяем настройки
            save_settings(current_resolution, current_mode)
            game.update_screen_size()
            screen = apply_display_mode(current_resolution, current_mode)

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
                    item_rect = pygame.Rect(50, 200 + (i * 80), current_width - 200, 40)
                    if item_rect.collidepoint(mouse_pos):
                        if game.money >= item["price"]:
                            if game.energy >= item["energy_cost"]:
                                print(item["energy_cost"])
                                game.energy -= item["energy_cost"]
                                game.money -= item["price"]
                                return state, f"Вы купили {item['name']}!"
                            return state, "Недостаточно энергии!"
                        return state, "Недостаточно денег!"

            # Кнопка выхода из магазина
            exit_button_rect = pygame.Rect(current_width - 150, 20, 100, 50)
            if exit_button_rect.collidepoint(mouse_pos):
                return "game", current_plot_text


    elif state == "work":
        new_state = game.work_manager.handle_work_events(mouse_pos, game)
        if new_state:
            return new_state, current_plot_text

    return state, current_plot_text


def draw_shop_screen(screen, game, current_width):
    """Отрисовывает экран магазина."""
    screen.fill((30, 30, 60))

    screen_size = pygame.display.get_surface().get_size()

    category_x = 50
    category_y = 20
    button_width = 200
    button_height = 50
    button_spacing = 20

    category_buttons = []
    subcategory_buttons = []

    for category in game.shop_items.keys():
        color = GREEN if category == game.current_shop_category else BLUE
        button = Button(category_x, category_y, button_width, button_height,
                        category, color, WHITE)
        button.draw(screen)
        category_buttons.append(button)
        category_x += button_width + button_spacing

    # Отрисовка подкатегорий
    if game.current_shop_category in game.shop_items:
        items = game.shop_items[game.current_shop_category]
        if isinstance(items, dict):
            subcategory_x = 50
            subcategory_y = 100
            for subcategory in items.keys():
                color = GREEN if subcategory == game.current_shop_subcategory else BLUE
                button = Button(subcategory_x, subcategory_y, button_width,
                                button_height, subcategory, color, WHITE)
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
        item_rect = pygame.Rect(50, items_start_y + (i * 80),
                                current_width - 200, 60)
        pygame.draw.rect(screen, (50, 50, 80), item_rect)

        text_surface = SMALL_FONT.render(item['name'], True, WHITE)
        price_surface = SMALL_FONT.render(f"{item['price']}$", True, YELLOW)

        desc = item.get('desc', '')
        if desc:
            desc_surface = SMALL_FONT.render(desc, True, GRAY)
            screen.blit(desc_surface, (item_rect.x + 10, item_rect.y + 20))  # Позиция под названием

        if item['name'] in game.purchased_items:
            purchased_text = SMALL_FONT.render("КУПЛЕНО", True, GREEN)
            screen.blit(purchased_text, (item_rect.x + item_rect.width - 100, item_rect.y + 5))
        else:
            buy_button = Button(item_rect.x + item_rect.width - 100,
                                item_rect.y + 5, 80, 30, "Купить", GREEN, WHITE)
            buy_button.draw(screen)

        screen.blit(text_surface, (item_rect.x + 10, item_rect.y + 5))
        screen.blit(price_surface, (item_rect.x + item_rect.width - screen_size[0] / 10,
                                    item_rect.y + 5))

    exit_button = Button(current_width - 150, 20, 100, 50, "Выход", RED, WHITE)
    exit_button.draw(screen)

    return category_buttons, subcategory_buttons, exit_button


def handle_shop_events(mouse_pos, game, category_buttons,
                       subcategory_buttons, exit_button):
    # Обработка кнопки выхода
    if exit_button.is_clicked(mouse_pos):
        return "game"

    # Обработка категорий
    for i, button in enumerate(category_buttons):
        if button.is_clicked(mouse_pos):
            categories = list(game.shop_items.keys())
            game.current_shop_category = categories[i]
            game.current_shop_subcategory = None
            return None

    # Обработка подкатегорий
    if game.current_shop_category in game.shop_items:
        items = game.shop_items[game.current_shop_category]
        if isinstance(items, dict):
            for i, button in enumerate(subcategory_buttons):
                if button.is_clicked(mouse_pos):
                    subcategories = list(items.keys())
                    game.current_shop_subcategory = subcategories[i]
                    return None

    # Обработка покупок
    if game.current_shop_category in game.shop_items:
        items = game.shop_items[game.current_shop_category]
        current_items = []

        if game.current_shop_subcategory and isinstance(items, dict):
            current_items = items[game.current_shop_subcategory]
        elif isinstance(items, list):
            current_items = items

        for i, item in enumerate(current_items):
            item_rect = pygame.Rect(50, 200 + (i * 80),
                                    game.screen_size[0] - 200, 60)
            buy_button_rect = pygame.Rect(item_rect.x + item_rect.width - 100,
                                          item_rect.y + 5, 80, 30)

            if buy_button_rect.collidepoint(mouse_pos) and \
                    item['name'] not in game.purchased_items:
                if game.money >= item["price"]:
                    if game.energy >= item.get("energy_cost", 0):
                        game.energy -= item["energy_cost"]
                        game.money -= item["price"]
                        game.purchased_items.add(item['name'])
                        name = item['name']
                        game.set_current_plot_text(f"Вы купили {name}!")
                        return None
                    else:
                        game.set_current_plot_text("Недостаточно энергии!")
                        return None
                else:
                    game.set_current_plot_text("Недостаточно денег!")
                    return None
    return None

def draw_state(screen, state, game, current_plot_text, settings_button, settings_icon,
               money_icon, energy_icon, current_width, current_height, prologue, buttons, stat_bg, event, mouse_pos):
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
    if state == "end_of_day_stat":
        current_time = pygame.time.get_ticks()

        if game.start_stat_time is None:
            game.start_stat_time = current_time
        elapsed_time = current_time - game.start_stat_time

        current_width, current_height = pygame.display.get_surface().get_size()  # Получаем текущие размеры экрана
        current_screen_size = pygame.display.get_surface().get_size()

        # Адаптивные размеры окна (80% ширины и 60% высоты экрана)
        window_width = int(current_width)
        window_height = int(current_height)
        window_x = (current_width - window_width) // 2
        window_y = (current_height - window_height) // 2
        window_rect = pygame.Rect(window_x, window_y, window_width, window_height)

        # Масштабируем фон под размер окна
        scaled_stat_bg = pygame.transform.scale(stat_bg, current_screen_size)
        screen.blit(scaled_stat_bg, window_rect.topleft)


        title_text = HAND_FONT.render("Статистика дня", True, BLACK)
        screen.blit(title_text, (current_width / 3.8, current_height / 12.2))

        title_text = HAND_FONT.render("Заработал:", True, BLACK)
        screen.blit(title_text, (current_width / 5, current_height / 7.5))

        stats = game.get_daily_stats()
        lines = [
            f"Деньги: {stats['money_change']} монет",
            f"Карма: {stats['karma_change']}",
            f"Знания: {stats['study_change']:.1f}"
        ]

        y = current_height / 7.5 + 60
        for line in lines:
            text = HAND_FONT.render(line, True, BLACK)
            screen.blit(text, (current_width / 5, y))
            y += 60

        if elapsed_time >= 500:
            # Создаем кнопку и отрисовываем её
            continue_button = Button(
                x=current_width // 1.3,
                y=current_height - 80,
                width=200,
                height=50,
                text="Продолжить",
                color=YELLOW,
                text_color=BLACK
            )
            continue_button.draw(screen)

            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.is_clicked(mouse_pos):
                    game.process_day()
                    game.start_day()
                    game.start_stat_time = None
                    return "game", current_plot_text  # Возвращаем новое состояние


    elif state == "end_of_month_stat":
        current_width, current_height = pygame.display.get_surface().get_size()
        current_screen_size = pygame.display.get_surface().get_size()

        current_time = pygame.time.get_ticks()

        # Устанавливаем время при первом входе в состояние
        if game.start_stat_time is None:
            game.start_stat_time = current_time

        elapsed_time = current_time - game.start_stat_time

        window_width = int(current_width)
        window_height = int(current_height)
        window_x = (current_width - window_width) // 2
        window_y = (current_height - window_height) // 2
        window_rect = pygame.Rect(window_x, window_y, window_width, window_height)

        scaled_stat_bg = pygame.transform.scale(stat_bg, current_screen_size)
        screen.blit(scaled_stat_bg, window_rect.topleft)

        title_text = HAND_FONT.render("Месячная статистика", True, BLACK)
        screen.blit(title_text, (current_width / 3.8, current_height / 12.2))

        title_text = HAND_FONT.render("Заработал", True, BLACK)
        screen.blit(title_text, (current_width / 5, current_height / 7.5))

        title_text = HAND_FONT.render("Деньги", True, BLACK)
        screen.blit(title_text, (current_width / 1.9, current_height / 7.3))

        title_text = HAND_FONT.render("Знания", True, BLACK)
        screen.blit(title_text, (current_width / 1.9, current_height / 7.5 + (current_height / 21) * 7))

        stats = {
            "Деньги:": game.monthly_money_change,
            "Карма:": game.monthly_karma_change,
            "Знания:": game.monthly_study_progress
        }

        y = current_height / 7.5 + 60
        for key, value in stats.items():
            text = HAND_FONT.render(f"{key} {value}", True, BLACK)
            screen.blit(text, (current_width / 5, y))
            y += 60

        # Отрисовка графика
        graph_rect = pygame.Rect(current_width / 1.9, current_height / 5, current_width / 4.8, current_height / 2)
        draw_monthly_graph(screen, game.monthly_money_history, game.monthly_study_history, graph_rect, game)

        if elapsed_time >= 500:
            # Создаем кнопку и отрисовываем её
            continue_button = Button(
                x=current_width // 1.3,
                y=current_height - 80,
                width=200,
                height=50,
                text="Продолжить",
                color=YELLOW,
                text_color=BLACK
            )
            continue_button.draw(screen)

            # Проверяем клик по кнопке
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.is_clicked(mouse_pos):
                    game.monthly_money_change = 0
                    game.monthly_karma_change = 0
                    game.monthly_study_progress = 0.0
                    game.start_stat_time = None  # Сбрасываем время
                    return "game", current_plot_text

    elif state == "main_menu":
        draw_main_menu(screen, buttons["main_menu"])
    elif state == "new_game_warning":
        draw_new_game_warning(screen, current_width, buttons["new_game_warning"])
    elif state == "prologue":
        if prologue:
            prologue.draw(screen)
    elif state == "game":
        draw_game_screen(screen, game, current_plot_text, settings_button, settings_icon,
                         money_icon, energy_icon, current_width, current_height)
        if game.plot_events:
            current_event = game.plot_events[-1]
            bg, event_buttons, text_surface = game.handle_event(current_event)
            screen.blit(bg, (0, 0))  # Фон события

            # Отрисовываем кнопки вариантов
            for btn in event_buttons:
                btn.draw(screen)

            # Отрисовываем текст события внизу
            screen.blit(text_surface, (0, screen.get_height() - text_surface.get_height()))


    elif state == "work":

        mouse_pos = pygame.mouse.get_pos()  # Получаем текущую позицию мыши

        category_buttons, subcategory_buttons, exit_button = game.work_manager.draw_work_screen(

            screen, game, current_width, mouse_pos

        )

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

    elif state == "study_menu":
        draw_study_menu(screen, game, current_width, current_height, buttons["study_menu"], current_width, current_height)

    if state not in ["end_of_day_stat", "end_of_month_stat"]:
        game.start_stat_time = None

    return state, current_plot_text


def draw_study_menu(screen, game, width, height, buttons, current_width, current_height):
    # Полупрозрачный фон
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    screen.blit(game_bg, (0, 0))
    scaled_game_bg = pygame.transform.scale(game_bg, (current_width, current_height))
    screen.blit(scaled_game_bg, (0, 0))

    day_season_text = MAIN_FONT.render(f"День {game.total_days} ({game.season})", True, WHITE)
    screen.blit(day_season_text, (50, 10))

    study_progress = f"Учеба: {game.study_progress}/{game.study_goal}"
    study_text = MAIN_FONT.render(study_progress, True, WHITE)
    screen.blit(study_text, (600, 10))

    try:
        energy_icon = pygame.image.load('png/energe.png').convert_alpha()
        energy_icon = pygame.transform.scale(energy_icon, (40, 40))
    except Exception as e:
        print(f"Ошибка загрузки energe.png: {e}")
        energy_icon = pygame.Surface((40, 40))
        energy_icon.fill(BLUE)

    try:
        money_icon = pygame.image.load('png/money.png').convert_alpha()
        money_icon = pygame.transform.scale(money_icon, (40, 40))
    except Exception as e:
        print(f"Ошибка загрузки money.png: {e}")
        money_icon = pygame.Surface((40, 40))
        money_icon.fill(YELLOW)

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

    # Окно меню (центрированное)
    menu_width = 800
    menu_height = 700
    menu_rect = pygame.Rect(
        (width - menu_width) // 2,
        (height - menu_height) // 2,
        menu_width,
        menu_height
    )
    pygame.draw.rect(screen, (30, 30, 60), menu_rect)

    # Прогресс учебы
    progress_text = MAIN_FONT.render(
        f"Прогресс: {game.study_progress}",
        True,
        WHITE
    )
    screen.blit(progress_text, (menu_rect.x + 20, menu_rect.y + 20))

    if game.university_passed:
        # Сообщение о завершении
        text = MAIN_FONT.render("Учеба завершена!", True, GREEN)
        text_rect = text.get_rect(center=menu_rect.center)
        screen.blit(text, text_rect)
    else:
        # Кнопки (центрированные по вертикали)
        button_y = menu_rect.y + 100
        i=0
        for btn in buttons.values():
            i +=1
            btn.rect.centerx = menu_rect.centerx
            btn.rect.y = button_y
            btn.draw(screen)
            button_y += 100
            if i == 3:
                button_y += 150



def draw_monthly_graph(screen, money_history, study_history, rect, game):
    if len(money_history) < 2:
        return  # Не рисуем график, если данных мало
    current_width, current_height = game.screen_size

    # Разделяем прямоугольник на две части: верхняя 2/3 для денег, нижняя 1/3 для обучения
    split_height = rect.height * (1 / 2)
    money_rect = pygame.Rect(rect.x, rect.y, rect.width, split_height)
    study_rect = pygame.Rect(rect.x, rect.y + split_height, rect.width, rect.height - split_height)

    # Нормализация данных для отображения
    max_money = max(money_history) if money_history else 1
    max_study = max(study_history) if study_history else 1
    days = len(money_history)

    # Анимация: показываем по одному дню за 100 мс
    frame = min(pygame.time.get_ticks() // 300, days)

    # Отрисовка линий между точками
    if frame >= 2:
        # Деньги (зеленый)
        for i in range(1, frame):
            x1 = money_rect.x + (i - 1) / days * money_rect.width
            y1 = money_rect.bottom - (money_history[i - 1] / max_money) * money_rect.height
            x2 = money_rect.x + i / days * money_rect.width
            y2 = money_rect.bottom - (money_history[i] / max_money) * money_rect.height
            pygame.draw.line(screen, GREEN, (x1, y1), (x2, y2), 2)

        # Обучение (красный)
        for i in range(1, frame):
            x1 = study_rect.x + (i - 1) / days * study_rect.width
            y1 = study_rect.bottom - (study_history[i - 1] / max_study) * study_rect.height
            x2 = study_rect.x + i / days * study_rect.width
            y2 = study_rect.bottom - (study_history[i] / max_study) * study_rect.height
            pygame.draw.line(screen, RED, (x1, y1), (x2, y2), 1)

    # Отрисовка точек
    for i in range(frame):
        # Координаты для денег
        x_money = money_rect.x + i / days * money_rect.width
        y_money = money_rect.bottom - (money_history[i] / max_money) * money_rect.height
        pygame.draw.circle(screen, GREEN, (x_money, y_money), 3)

        # Координаты для обучения
        x_study = study_rect.x + i / days * study_rect.width
        y_study = study_rect.bottom - (study_history[i] / max_study) * study_rect.height
        pygame.draw.circle(screen, RED, (x_study, y_study), 2)


def draw_main_menu(screen, buttons):
    """
    Отрисовывает главное меню игры.

    Args:
        screen (pygame. Surface): Поверхность для отрисовки
        buttons (dict): Словарь кнопок главного меню
    """
    # Отрисовка фона
    screen.blit(main_menu_bg, (0, 0))

    # Масштабируем фон под текущее разрешение (если нужно)
    screen_width, screen_height = screen.get_size()
    scaled_bg = pygame.transform.scale(main_menu_bg, (screen_width, screen_height))
    screen.blit(scaled_bg, (0, 0))

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
                     money_icon, energy_icon, current_width,current_height):
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
    # Отрисовка фона
    screen.blit(game_bg, (0, 0))
    scaled_game_bg = pygame.transform.scale(game_bg, (current_width, current_height))
    screen.blit(scaled_game_bg, (0, 0))

    # Отрисовка текста "День (Сезон)"
    day_season_text = MAIN_FONT.render(f"День {game.total_days} ({game.season})", True, WHITE)
    screen.blit(day_season_text, (50, 10))

    study_progress = f"Учеба: {game.study_progress}/{game.study_goal}"
    study_text = MAIN_FONT.render(study_progress, True, WHITE)
    screen.blit(study_text, (600, 10))

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

    '''# Статистика
    stat_y = 100
    stat_lines = [
        f"Стипендия: {game.scholarship}",
    ]
    for line in stat_lines:
        stat_text = MAIN_FONT.render(line, True, WHITE)
        screen.blit(stat_text, (50, stat_y))
        stat_y += 40  # Расстояние между строками'''


    # Отрисовка кнопок
    for button in game.buttons.values():
        button.draw(screen)

    # Кнопка настроек
    settings_button.draw(screen)
    if settings_icon:
        screen.blit(settings_icon, (settings_button.rect.x, settings_button.rect.y))


    if game.plot_events:
            current_event = game.plot_events[-1]
            bg, event_buttons, text_surface = game.handle_event(current_event)
            screen.blit(bg, (0, 0))  # Важно отрисовать фон поверх основного интерфейса
            for btn in event_buttons:
                btn.draw(screen)
            screen.blit(text_surface, (0, screen.get_height() - 150))  # Добавлено


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


def handle_ending(screen, ending_type, screen_size, clock):
    """
    Обрабатывает показ концовки и возврат в главное меню.
    """
    ending_data = {
        "army": ENDING_ARMY,
        "boring_job": ENDING_BORING_JOB,
        "dream": ENDING_DREAM,
        "prison": ENDING_PRISON
    }

    if ending_type in ending_data:
        ending = Ending(ending_data[ending_type], screen_size)
        fade_surface = pygame.Surface(screen_size)
        fade_surface.fill((0, 0, 0))

        # Плавное затемнение текущего экрана
        for alpha in range(0, 255, 5):
            screen.blit(fade_surface, (0, 0))
            fade_surface.set_alpha(alpha)
            pygame.display.flip()
            clock.tick(200)

        # Показ концовки
        while not ending.is_finished():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    ending.next_frame()

            ending.update()
            ending.draw(screen)
            pygame.display.flip()
            clock.tick(60)

        # Пауза перед возвратом в меню
        pygame.time.wait(100)

        # Плавное появление главного меню
        fade_surface.set_alpha(255)
        for alpha in range(255, 0, -5):
            screen.blit(fade_surface, (0, 0))
            fade_surface.set_alpha(alpha)
            pygame.display.flip()
            clock.tick(200)

        return "main_menu"
    return None


def handle_summer_event(screen, summer_type, screen_size, clock):
    """
    Обрабатывает показ концовки и возврат в главное меню.
    """
    if not summer_type.startswith("summer"):
        return None

    event_data = {
        "summer1": SUMMER_1,
        "summer2": SUMMER_2,
        "summer3": SUMMER_3,
        "summer4": HNY
    }

    if summer_type in event_data:
        summer = Event(event_data[summer_type], screen_size)
        fade_surface = pygame.Surface(screen_size)
        fade_surface.fill((0, 0, 0))

        # Плавное затемнение текущего экрана
        for alpha in range(0, 255, 5):
            screen.blit(fade_surface, (0, 0))
            fade_surface.set_alpha(alpha)
            pygame.display.flip()
            clock.tick(200)

        while not summer.is_finished():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    summer.next_frame()

            summer.update()
            summer.draw(screen)
            pygame.display.flip()
            clock.tick(60)

        # Пауза перед возвратом в меню
        pygame.time.wait(100)

        # Плавное появление главного меню
        fade_surface.set_alpha(255)
        for alpha in range(255, 0, -5):
            screen.blit(fade_surface, (0, 0))
            fade_surface.set_alpha(alpha)
            pygame.display.flip()
            clock.tick(200)

        return "game"
    return None


def main():
    """
    Главная функция игры.
    """
    global current_settings_section, screen, subcategory_buttons, exit_button, category_buttons, main_menu_bg, game_bg
    global cheat_input_active, cheat_code, cheat_message

    try:
        pygame.init()
    except pygame.error:
        print("Ошибка инициализации pygame")
        return

    try:
        main_menu_bg = pygame.image.load('png/main_menu.png').convert()
        game_bg = pygame.image.load('png/game_bg.png').convert()
    except pygame.error as e:
        print(f"Ошибка загрузки фона: {e}")
        main_menu_bg = pygame.Surface((1280, 720))
        main_menu_bg.fill(PURPLE)
        game_bg = pygame.Surface((1280, 720))
        game_bg.fill(GRAY)

    current_settings_section = SETTINGS_SECTIONS["main"]
    clock = pygame.time.Clock()
    game = Game()
    running = True
    current_plot_text = ""
    state = "main_menu"
    prologue = None
    buttons = {}
    settings = load_settings()
    try:
        screen = apply_display_mode(settings["resolution"], settings["display_mode"])
    except pygame.error:
        print("Ошибка создания окна, использую настройки по умолчанию")
        screen = pygame.display.set_mode((1280, 720))

    # Получаем текущие размеры экрана
    current_width, current_height = screen.get_size()
    init_cheat_window(screen)

    # Загрузка иконок
    try:
        money_icon = pygame.image.load('png/money.png').convert_alpha()
        money_icon = pygame.transform.scale(money_icon, (40, 40))
    except Exception as e:
        print(f"Ошибка загрузки money.png: {e}")
        money_icon = pygame.Surface((40, 40))
        money_icon.fill(YELLOW)

    try:
        stat_bg = pygame.image.load('png/stat.png').convert_alpha()
        stat_bg = pygame.transform.scale(stat_bg, game.screen_size)
    except pygame.error as e:
        print(f"Ошибка загрузки stat.png: {e}")
        # Создайте fallback-фон, если файл не загрузился
        stat_bg = pygame.Surface(game.screen_size)
        stat_bg.fill((100, 100, 255))  # Синий цвет для теста

    try:
        energy_icon = pygame.image.load('png/energe.png').convert_alpha()
        energy_icon = pygame.transform.scale(energy_icon, (40, 40))
    except Exception as e:
        print(f"Ошибка загрузки energe.png: {e}")
        energy_icon = pygame.Surface((40, 40))
        energy_icon.fill(BLUE)

    try:
        settings_icon = pygame.image.load('png/setting.png').convert_alpha()
        settings_icon = pygame.transform.scale(settings_icon, (40, 40))
    except Exception as e:
        print(f"Ошибка загрузки setting.png: {e}")
        settings_icon = pygame.Surface((40, 40))
        settings_icon.fill(RED)

    has_save_file = os.path.exists("save.json")

    # Создаём кнопки меню

    main_menu_buttons = {
        "new_game": Button(50, 300, 300, 50, "Новая игра", BLUE, WHITE),
        "settings": Button(50, 400, 300, 50, "Настройки", YELLOW, BLACK),
        "quit": Button(50, 500, 300, 50, "Выйти", RED, WHITE)
    }

    if has_save_file:
        main_menu_buttons["continue"] = Button(50, 200, 300, 50, "Продолжить", GREEN, WHITE)

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

    study_menu_buttons = {
        "lab": Button(
            0, 0, 600, 50,
            "Лабораторная (300 энергии) + 3 к знаниям",
            BLUE, WHITE
        ),
        "lecture": Button(
            0, 0, 600, 50,
            "Лекция (150 энергии) + 1 к знаниям",
            GREEN, WHITE
        ),
        "exam": Button(
            0, 0, 600, 50,
            "Экзамен (2000 энергии) + 10 к знаниям",
            RED, WHITE
        ),
        "back": Button(
            0, 0, 600, 50,
            "Назад",
            GRAY, BLACK
        )
    }

    # Собираем все группы кнопок
    buttons = {
        "main_menu": main_menu_buttons,
        "new_game_warning": new_game_warning_buttons,
        "prologue_choice": prologue_choice_buttons,
        "settings": settings_buttons,
        "study_menu": study_menu_buttons,
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
        main_menu_bg_scaled = pygame.transform.scale(main_menu_bg, (current_width, current_height))
        game_bg_scaled = pygame.transform.scale(game_bg, (current_width, current_height))

        # Обновляем позиции кнопок настроек в игре
        buttons["game_settings"]["back"].rect.y = current_height - 70
        buttons["game_settings"]["exit_to_menu"].rect.y = current_height - 70

        mouse_pos = pygame.mouse.get_pos()
        screen.fill(PURPLE)

        # Обновление позиций
        settings_button.rect.x = current_width - 60
        settings_button.update(mouse_pos)

        # Обновление состояния игры
        ending_check = game.update()
        if ending_check:
            state = f"ending_{ending_check}"

        # Проверяем, является ли state кортежем
        if isinstance(state, tuple):
            state = state[0]  # Извлекаем первый элемент, если это кортеж


        if state.startswith("ending_"):
            ending_type = state.split("_")[1]
            new_state = handle_ending(screen, ending_type, (current_width, current_height), clock)
            if new_state:
                state = new_state
                game.total_days += 1
            else:
                state = "game"

        summer_check = game.update()
        if summer_check and summer_check.startswith("summer"):
            new_state = handle_summer_event(screen, summer_check, (current_width, current_height), clock)
            if new_state:
                state = new_state
                if summer_check == "summer1":
                    game.is_summer1_been = True
                    game.energy -= 500
                elif summer_check == "summer2":
                    game.is_summer2_been = True
                    game.energy -= 500
                elif summer_check == "summer3":
                    game.is_summer3_been = True
                    game.energy -= 500
                elif summer_check == "summer4":
                    game.total_days += 1
            else:
                state = "game"

        if state == "game":
            game.update_button_positions((current_width, current_height))
            for button in game.buttons.values():
                button.update(mouse_pos)


        '''Интеграция состояния в основной игровой цикл'''
        if state == "shop":
            category_buttons, buy_buttons, exit_button = draw_shop_screen(screen, game, current_width)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    result = handle_shop_events(mouse_pos, game, category_buttons, buy_buttons, exit_button)
                    if result:
                        if result == "game":
                            state = "game"
                        else:
                            current_plot_text = result

        if game.current_plot_text is not None:
            current_time = pygame.time.get_ticks()
            if current_time - game.message_timer > 3000:  # 3 секунды
                game.current_plot_text = None  # Скрываем сообщение

        # Обработка событий в зависимости от состояния
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            elif event.type == pygame.KEYDOWN:
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

                if event.key == pygame.K_BACKQUOTE:
                    cheat_input_active = not cheat_input_active
                    cheat_code = ""
                    cheat_message = ""
                if cheat_input_active:
                    if event.key == pygame.K_RETURN:
                        cheat_code = cheat_code.strip()
                        parts = cheat_code.split()
                        if not parts:
                            cheat_message = "Неверный формат"
                        else:
                            command = parts[0]
                            if command in CHEAT_CODES:
                                try:
                                    param = parts[1] if len(parts) > 1 else ""
                                    CHEAT_CODES[command](game, param)
                                    cheat_message = f"Чит '{command}' активирован!"
                                except (ValueError, IndexError) as e:
                                    cheat_message = f"Ошибка: {e}"
                            else:
                                cheat_message = "Неизвестный чит"
                        cheat_code = ""
                    elif event.key == pygame.K_BACKSPACE:
                        cheat_code = cheat_code[:-1]
                    else:
                        cheat_code += event.unicode


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
        if state == "main_menu":
            # Проверяем наличие файла save.json
            has_save_file = os.path.exists("save.json")

            # Создаем кнопки главного меню
            main_menu_buttons = {
                "new_game": Button(50, 300, 300, 50, "Новая игра", BLUE, WHITE),
                "settings": Button(50, 400, 300, 50, "Настройки", YELLOW, BLACK),
                "quit": Button(50, 500, 300, 50, "Выйти", RED, WHITE)
            }

            # Добавляем кнопку "Продолжить" только если файл существует
            if has_save_file:
                main_menu_buttons["continue"] = Button(50, 200, 300, 50, "Продолжить", GREEN, WHITE)

            # Обновляем группу кнопок главного меню в общем списке
            buttons["main_menu"] = main_menu_buttons  # Обновляем кнопки в глобальном словаре

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

        events = pygame.event.get()  # Получаем события единожды

        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Обработка сюжетных событий
                if game.plot_events:
                    current_event = game.plot_events[-1]
                    _, event_buttons, _ = game.handle_event(current_event)  # Перезагружаем кнопки
                    for i, btn in enumerate(event_buttons):
                        if btn.is_clicked(mouse_pos):
                            selected_option = current_event["options"][i]
                            game.apply_event_effects(selected_option)
                            game.plot_events.pop()
                else:
                    # Обработка остальных кнопок
                    state, current_plot_text = handle_mouse_events(
                        mouse_pos,
                        state,
                        game,
                        current_plot_text,
                        settings_button,
                        buttons,
                        (current_width, current_height)
                    )
        else:
            # Остальная отрисовка
            state, current_plot_text = draw_state(screen, state, game, current_plot_text, settings_button,
                       settings_icon, money_icon, energy_icon, current_width,
                       current_height, prologue, buttons, stat_bg, event, mouse_pos)

        game.check_message_timeout()  # Проверяем таймер сообщения

        if cheat_input_active:
            window_rect = pygame.Rect(20, 20, 760, 200)
            window_surface = pygame.Surface((window_rect.width, window_rect.height), pygame.SRCALPHA)
            window_surface.fill((0, 0, 0, 128))
            screen.blit(window_surface, (window_rect.x, window_rect.y))

            pygame.draw.rect(screen, (200, 200, 200), window_rect, 2)

            input_rect = pygame.Rect(window_rect.x + 5, window_rect.y + 5, 750, 40)
            pygame.draw.rect(screen, (40, 40, 40), input_rect)
            input_text = HAND_FONT.render(cheat_code, True, (255, 255, 255))
            screen.blit(input_text, (input_rect.x + 5, input_rect.y + 5))

            if cheat_message:
                message_rect = pygame.Rect(
                    window_rect.x + 5,
                    input_rect.bottom + 5,
                    750,
                    40
                )
                pygame.draw.rect(screen, (40, 40, 40), message_rect)
                message_text = HAND_FONT.render(cheat_message, True, (255, 0, 0))
                screen.blit(message_text, (message_rect.x + 5, message_rect.y + 5))

        # Обновление экрана
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()