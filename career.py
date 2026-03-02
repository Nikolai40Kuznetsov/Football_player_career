import sys
import random
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Player:
    """Класс игрока (футболиста)"""
    def __init__(self, name):
        self.name = name
        self.age = 14  # Минимальный возраст 14
        self.overall = 1  # Начальная сила 1
        self.position = "CF"
        
        # Основные характеристики (0-100)
        self.stats = {
            'pace': 1,
            'shooting': 1,
            'passing': 1,
            'dribbling': 1,
            'defending': 1,
            'physical': 1,
            'stamina': 1
        }
        
        # Карьерная статистика
        self.career_stats = {
            'matches': 0,
            'goals': 0,
            'assists': 0,
            'salary': 500,
            'club': 'Молодежная академия',
            'reputation': 1,
            'energy': 100,
            'club_tier': 0  # 0-начальный, 1-слабый, 2-средний, 3-сильный, 4-топ, 5-супертоп
        }
        
        # Контракт
        self.contract = {
            'start_date': QDate(2024, 1, 1),
            'end_date': QDate(2025, 1, 1),  # По умолчанию 1 год
            'duration_months': 12,
            'weekly_salary': 500,
            'club': 'Молодежная академия'
        }
        
        # Трофеи и достижения
        self.trophies = []
        self.injured = False
        self.injury_weeks = 0
        
        # Дата рождения (для поздравлений)
        self.birth_day = 7
        self.birth_month = 12  # 7 декабря
        self.last_birthday_year = 2024  # Год последнего дня рождения
        
        # Флаги для юбилейных сообщений
        self.milestones = {
            'matches': {1: False, 5: False, 10: False, 50: False, 100: False, 200: False, 300: False},
            'goals': {1: False, 5: False, 10: False, 50: False, 100: False, 200: False, 300: False},
            'assists': {1: False, 5: False, 10: False, 50: False, 100: False, 200: False, 300: False}
        }

class Club:
    """Класс для представления клуба"""
    def __init__(self, name, country, tier, league, reputation):
        self.name = name
        self.country = country
        self.tier = tier  # 0-5 (чем выше, тем сильнее клуб)
        self.league = league
        self.reputation = reputation

class TransferOffer:
    """Класс для предложения о трансфере"""
    def __init__(self, club, weekly_salary, contract_months):
        self.club = club
        self.weekly_salary = weekly_salary
        self.contract_months = contract_months
        self.date_received = QDate.currentDate()

class FootballCareerSimulator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.player = None
        self.current_date = QDate(2024, 1, 1)
        self.weeks_passed = 0
        self.transfer_offers = []
        self.clubs = []
        self.init_clubs()
        self.initUI()
        
    def init_clubs(self):
        """Инициализация базы клубов"""
        
        # Топ-клубы (tier 5)
        top_clubs = [
            Club("Реал Мадрид", "Испания", 5, "Ла Лига", 99),
            Club("Барселона", "Испания", 5, "Ла Лига", 98),
            Club("Атлетико Мадрид", "Испания", 5, "Ла Лига", 92),
            Club("Манчестер Сити", "Англия", 5, "АПЛ", 99),
            Club("Ливерпуль", "Англия", 5, "АПЛ", 96),
            Club("Манчестер Юнайтед", "Англия", 5, "АПЛ", 94),
            Club("Челси", "Англия", 5, "АПЛ", 93),
            Club("Арсенал", "Англия", 5, "АПЛ", 92),
            Club("Тоттенхэм", "Англия", 5, "АПЛ", 90),
            Club("Ювентус", "Италия", 5, "Серия А", 93),
            Club("Интер", "Италия", 5, "Серия А", 92),
            Club("Милан", "Италия", 5, "Серия А", 91),
            Club("Бавария", "Германия", 5, "Бундеслига", 97),
            Club("Боруссия Дортмунд", "Германия", 5, "Бундеслига", 91),
            Club("ПСЖ", "Франция", 5, "Лига 1", 95),
            Club("Аякс", "Нидерланды", 5, "Эредивизи", 89),
            Club("Фейеноорд", "Нидерланды", 5, "Эредивизи", 86),
            Club("ПСВ", "Нидерланды", 5, "Эредивизи", 87),
            Club("Бенфика", "Португалия", 5, "Примейра", 88),
            Club("Порту", "Португалия", 5, "Примейра", 88),
            Club("Спортинг", "Португалия", 5, "Примейра", 87),
        ]
        
        # Сильные клубы (tier 4)
        strong_clubs = [
            Club("Реал Сосьедад", "Испания", 4, "Ла Лига", 86),
            Club("Вильярреал", "Испания", 4, "Ла Лига", 85),
            Club("Севилья", "Испания", 4, "Ла Лига", 84),
            Club("Атлетик Бильбао", "Испания", 4, "Ла Лига", 83),
            Club("Валенсия", "Испания", 4, "Ла Лига", 83),
            Club("Бетис", "Испания", 4, "Ла Лига", 82),
            Club("Ньюкасл", "Англия", 4, "АПЛ", 88),
            Club("Астон Вилла", "Англия", 4, "АПЛ", 86),
            Club("Вест Хэм", "Англия", 4, "АПЛ", 85),
            Club("Лестер", "Англия", 4, "АПЛ", 84),
            Club("Эвертон", "Англия", 4, "АПЛ", 82),
            Club("Вулверхэмптон", "Англия", 4, "АПЛ", 81),
            Club("Наполи", "Италия", 4, "Серия А", 89),
            Club("Лацио", "Италия", 4, "Серия А", 86),
            Club("Рома", "Италия", 4, "Серия А", 86),
            Club("Аталанта", "Италия", 4, "Серия А", 85),
            Club("Фиорентина", "Италия", 4, "Серия А", 82),
            Club("РБ Лейпциг", "Германия", 4, "Бундеслига", 88),
            Club("Байер Леверкузен", "Германия", 4, "Бундеслига", 87),
            Club("Вольфсбург", "Германия", 4, "Бундеслига", 83),
            Club("Боруссия Менхенгладбах", "Германия", 4, "Бундеслига", 82),
            Club("Айнтрахт Франкфурт", "Германия", 4, "Бундеслига", 82),
            Club("Марсель", "Франция", 4, "Лига 1", 86),
            Club("Лион", "Франция", 4, "Лига 1", 85),
            Club("Монако", "Франция", 4, "Лига 1", 84),
            Club("Лилль", "Франция", 4, "Лига 1", 83),
            Club("Ренн", "Франция", 4, "Лига 1", 81),
        ]
        
        # Клубы из Чемпионшипа (Англия, tier 2-3)
        championship_clubs = [
            Club("Лидс Юнайтед", "Англия", 3, "Чемпионшип", 78),
            Club("Саутгемптон", "Англия", 3, "Чемпионшип", 77),
            Club("Ипсвич Таун", "Англия", 3, "Чемпионшип", 75),
            Club("Рексем", "Англия", 2, "Чемпионшип", 65),
            Club("Бирмингем Сити", "Англия", 2, "Чемпионшип", 70),
            Club("Мидлсбро", "Англия", 2, "Чемпионшип", 72),
            Club("Сток Сити", "Англия", 2, "Чемпионшип", 71),
            Club("Вест Бромвич", "Англия", 2, "Чемпионшип", 73),
            Club("Норвич Сити", "Англия", 2, "Чемпионшип", 74),
            Club("Уотфорд", "Англия", 2, "Чемпионшип", 72),
            Club("Сандерленд", "Англия", 2, "Чемпионшип", 71),
            Club("Ковентри Сити", "Англия", 2, "Чемпионшип", 69),
            Club("Халл Сити", "Англия", 2, "Чемпионшип", 68),
        ]
        
        # Клубы из Сегунды (Испания, tier 2-3)
        segunda_clubs = [
            Club("Эспаньол", "Испания", 3, "Сегунда", 76),
            Club("Реал Сарагоса", "Испания", 2, "Сегунда", 72),
            Club("Спортинг Хихон", "Испания", 2, "Сегунда", 71),
            Club("Реал Овьедо", "Испания", 2, "Сегунда", 70),
            Club("Леванте", "Испания", 3, "Сегунда", 75),
            Club("Альбасете", "Испания", 2, "Сегунда", 68),
            Club("Картахена", "Испания", 2, "Сегунда", 67),
            Club("Тенерифе", "Испания", 2, "Сегунда", 69),
            Club("Лас-Пальмас", "Испания", 2, "Сегунда", 70),
            Club("Эйбар", "Испания", 2, "Сегунда", 73),
        ]
        
        # Клубы из Второй Бундеслиги (Германия, tier 2-3)
        zweite_bundesliga_clubs = [
            Club("Шальке 04", "Германия", 3, "Вторая Бундеслига", 77),
            Club("Гамбург", "Германия", 3, "Вторая Бундеслига", 78),
            Club("Герта Берлин", "Германия", 3, "Вторая Бундеслига", 76),
            Club("Фортуна Дюссельдорф", "Германия", 2, "Вторая Бундеслига", 72),
            Club("Санкт-Паули", "Германия", 2, "Вторая Бундеслига", 71),
            Club("Ганновер 96", "Германия", 2, "Вторая Бундеслига", 73),
            Club("Нюрнберг", "Германия", 2, "Вторая Бундеслига", 70),
            Club("Кайзерслаутерн", "Германия", 2, "Вторая Бундеслига", 69),
            Club("Магдебург", "Германия", 2, "Вторая Бундеслига", 68),
            Club("Гройтер Фюрт", "Германия", 2, "Вторая Бундеслига", 67),
        ]
        
        # Клубы из Серии Б (Италия, tier 2-3)
        serie_b_clubs = [
            Club("Палермо", "Италия", 2, "Серия Б", 72),
            Club("Сампдория", "Италия", 3, "Серия Б", 75),
            Club("Парма", "Италия", 3, "Серия Б", 74),
            Club("Комо", "Италия", 2, "Серия Б", 70),
            Club("Кремонезе", "Италия", 2, "Серия Б", 71),
            Club("Бари", "Италия", 2, "Серия Б", 72),
            Club("Модена", "Италия", 2, "Серия Б", 69),
            Club("Пиза", "Италия", 2, "Серия Б", 70),
            Club("Читтаделла", "Италия", 2, "Серия Б", 68),
            Club("Козенца", "Италия", 2, "Серия Б", 67),
        ]
        
        # Средние клубы Европы (tier 3)
        medium_european_clubs = [
            Club("Шахтер", "Украина", 3, "УПЛ", 82),
            Club("Динамо Киев", "Украина", 3, "УПЛ", 80),
            Club("Заря", "Украина", 3, "УПЛ", 72),
            Club("Днепр-1", "Украина", 3, "УПЛ", 71),
            Club("Црвена Звезда", "Сербия", 3, "Суперлига", 78),
            Club("Партизан", "Сербия", 3, "Суперлига", 76),
            Club("Славия Прага", "Чехия", 3, "Первая лига", 77),
            Club("Спарта Прага", "Чехия", 3, "Первая лига", 76),
            Club("Виктория Пльзень", "Чехия", 3, "Первая лига", 73),
            Club("Легия", "Польша", 3, "Экстракласса", 75),
            Club("Лех", "Польша", 3, "Экстракласса", 74),
            Club("Ракув", "Польша", 3, "Экстракласса", 73),
            Club("Базель", "Швейцария", 3, "Суперлига", 78),
            Club("Янг Бойз", "Швейцария", 3, "Суперлига", 77),
            Club("Цюрих", "Швейцария", 3, "Суперлига", 72),
            Club("Селтик", "Шотландия", 3, "Премьершип", 80),
            Club("Рейнджерс", "Шотландия", 3, "Премьершип", 79),
            Club("Абердин", "Шотландия", 3, "Премьершип", 68),
            Club("Брюгге", "Бельгия", 3, "Про-лига", 79),
            Club("Генк", "Бельгия", 3, "Про-лига", 76),
            Club("Андерлехт", "Бельгия", 3, "Про-лига", 75),
            Club("Стандард", "Бельгия", 3, "Про-лига", 73),
            Club("Копенгаген", "Дания", 3, "Суперлига", 76),
            Club("Мидтьюлланд", "Дания", 3, "Суперлига", 73),
            Club("Брондбю", "Дания", 3, "Суперлига", 71),
            Club("Русенборг", "Норвегия", 3, "Элитсерия", 72),
            Club("Будё-Глимт", "Норвегия", 3, "Элитсерия", 74),
            Club("Молде", "Норвегия", 3, "Элитсерия", 71),
            Club("Мальме", "Швеция", 3, "Аллсвенскан", 73),
            Club("Юргорден", "Швеция", 3, "Аллсвенскан", 70),
            Club("АИК", "Швеция", 3, "Аллсвенскан", 69),
            Club("Олимпиакос", "Греция", 3, "Суперлига", 77),
            Club("ПАОК", "Греция", 3, "Суперлига", 75),
            Club("Панатинаикос", "Греция", 3, "Суперлига", 74),
            Club("АЕК", "Греция", 3, "Суперлига", 74),
            Club("Фенербахче", "Турция", 3, "Суперлиг", 80),
            Club("Галатасарай", "Турция", 3, "Суперлиг", 80),
            Club("Бешикташ", "Турция", 3, "Суперлиг", 78),
            Club("Трабзонспор", "Турция", 3, "Суперлиг", 75),
            Club("Динамо Загреб", "Хорватия", 3, "ХНЛ", 76),
            Club("Хайдук", "Хорватия", 3, "ХНЛ", 72),
            Club("Осиек", "Хорватия", 3, "ХНЛ", 68),
            Club("Слован Братислава", "Словакия", 3, "Суперлига", 68),
            Club("Жилина", "Словакия", 3, "Суперлига", 65),
            Club("Лудогорец", "Болгария", 3, "Первая лига", 70),
            Club("ЦСКА София", "Болгария", 3, "Первая лига", 67),
            Club("Ференцварош", "Венгрия", 3, "НБ I", 71),
            Club("Види", "Венгрия", 3, "НБ I", 65),
            Club("Шериф", "Молдова", 3, "Дивизия Националь", 65),
        ]
        
        # Слабые европейские клубы (tier 2)
        weak_european_clubs = [
            Club("Астана", "Казахстан", 2, "Премьер-лига", 62),
            Club("Кайрат", "Казахстан", 2, "Премьер-лига", 60),
            Club("Тобол", "Казахстан", 2, "Премьер-лига", 58),
            Club("Ордабасы", "Казахстан", 2, "Премьер-лига", 57),
            Club("Актобе", "Казахстан", 2, "Премьер-лига", 56),
            Club("Жетысу", "Казахстан", 2, "Премьер-лига", 55),
            Club("Карабах", "Азербайджан", 2, "Премьер-лига", 64),
            Club("Нефтчи", "Азербайджан", 2, "Премьер-лига", 58),
            Club("БАТЭ", "Беларусь", 2, "Высшая лига", 62),
            Club("Динамо Минск", "Беларусь", 2, "Высшая лига", 60),
            Club("Шахтер Солигорск", "Беларусь", 2, "Высшая лига", 59),
            Club("Неман", "Беларусь", 2, "Высшая лига", 55),
            Club("Гомель", "Беларусь", 2, "Высшая лига", 54),
            Club("Торпедо-БелАЗ", "Беларусь", 2, "Высшая лига", 53),
            Club("ХИК", "Финляндия", 2, "Вейккауслига", 58),
            Club("КуПС", "Финляндия", 2, "Вейккауслига", 56),
            Club("Линфилд", "Северная Ирландия", 2, "Премьершип", 48),
            Club("Крусейдерс", "Северная Ирландия", 2, "Премьершип", 46),
            Club("Шемрок Роверс", "Ирландия", 2, "Премьер-дивизион", 52),
            Club("Дандолк", "Ирландия", 2, "Премьер-дивизион", 51),
            Club("ТНС", "Уэльс", 2, "Премьер-лига", 47),
            Club("Конас-Ки", "Уэльс", 2, "Премьер-лига", 44),
            Club("Ла Фиорита", "Сан-Марино", 2, "Чемпионат", 30),
            Club("Тре Пенне", "Сан-Марино", 2, "Чемпионат", 29),
            Club("Вадуц", "Лихтенштейн", 2, "Челлендж-лига", 52),
            Club("Биркиркара", "Мальта", 2, "Премьер-лига", 45),
            Club("Хибернианс", "Мальта", 2, "Премьер-лига", 44),
            Club("Будучност", "Черногория", 2, "Первая лига", 48),
            Club("Сутьеска", "Черногория", 2, "Первая лига", 46),
            Club("Зриньски", "Босния", 2, "Премьер-лига", 50),
            Club("Сараево", "Босния", 2, "Премьер-лига", 49),
            Club("Шкендия", "Македония", 2, "Первая лига", 48),
            Club("Академия Пандев", "Македония", 2, "Первая лига", 45),
            Club("Дрита", "Косово", 2, "Суперлига", 46),
            Club("Балкани", "Косово", 2, "Суперлига", 45),
            Club("Пюник", "Армения", 2, "Премьер-лига", 48),
            Club("Арарат-Армения", "Армения", 2, "Премьер-лига", 47),
            Club("Динамо Тбилиси", "Грузия", 2, "Эровнули лига", 55),
            Club("Сабуртало", "Грузия", 2, "Эровнули лига", 52),
            Club("Клаксвик", "Фареры", 2, "Премьер-лига", 38),
            Club("ХБ Торсхавн", "Фареры", 2, "Премьер-лига", 37),
            Club("Брейдаблик", "Исландия", 2, "Премьер-лига", 45),
            Club("Викингур", "Исландия", 2, "Премьер-лига", 44),
            Club("Люксембург", "Люксембург", 2, "Национальный дивизион", 40),
            Club("Дифферданж", "Люксембург", 2, "Национальный дивизион", 39),
        ]
        
        # Клубы России и СНГ (tier 1-3)
        russian_clubs = [
            # Топ-клубы России (tier 3)
            Club("Зенит", "Россия", 3, "РПЛ", 85),
            Club("Спартак", "Россия", 3, "РПЛ", 82),
            Club("ЦСКА", "Россия", 3, "РПЛ", 80),
            Club("Локомотив", "Россия", 3, "РПЛ", 79),
            Club("Краснодар", "Россия", 3, "РПЛ", 78),
            Club("Динамо", "Россия", 3, "РПЛ", 77),
            Club("Ростов", "Россия", 3, "РПЛ", 76),
            Club("Сочи", "Россия", 3, "РПЛ", 75),
            Club("Ахмат", "Россия", 2, "РПЛ", 70),
            Club("Крылья Советов", "Россия", 2, "РПЛ", 69),
            Club("Рубин", "Россия", 2, "РПЛ", 68),
            Club("Нижний Новгород", "Россия", 2, "РПЛ", 65),
            Club("Урал", "Россия", 2, "РПЛ", 64),
            Club("Факел", "Россия", 1, "РПЛ", 60),
            Club("Оренбург", "Россия", 1, "РПЛ", 60),
            Club("Балтика", "Россия", 1, "РПЛ", 58),
            
            # Первая лига России (tier 1)
            Club("Торпедо", "Россия", 1, "ФНЛ", 55),
            Club("Шинник", "Россия", 1, "ФНЛ", 52),
            Club("Алания", "Россия", 1, "ФНЛ", 54),
            Club("Енисей", "Россия", 1, "ФНЛ", 51),
            Club("СКА-Хабаровск", "Россия", 1, "ФНЛ", 50),
            Club("Черноморец", "Россия", 1, "ФНЛ", 48),
            Club("Родина", "Россия", 1, "ФНЛ", 47),
            Club("Волгарь", "Россия", 1, "ФНЛ", 46),
            Club("Нефтехимик", "Россия", 1, "ФНЛ", 45),
            Club("Акрон", "Россия", 1, "ФНЛ", 44),
            Club("КАМАЗ", "Россия", 1, "ФНЛ", 43),
            Club("Сокол", "Россия", 1, "ФНЛ", 42),
            Club("Тюмень", "Россия", 1, "ФНЛ", 41),
            Club("Ленинградец", "Россия", 1, "ФНЛ", 40),
        ]
        
        # Неевропейские клубы (tier 1-4)
        # Южная Америка (tier 3-4)
        south_america = [
            Club("Фламенго", "Бразилия", 4, "Бразилейрао", 88),
            Club("Палмейрас", "Бразилия", 4, "Бразилейрао", 88),
            Club("Сантос", "Бразилия", 4, "Бразилейрао", 85),
            Club("Коринтианс", "Бразилия", 4, "Бразилейрао", 85),
            Club("Сан-Паулу", "Бразилия", 4, "Бразилейрао", 84),
            Club("Гремио", "Бразилия", 4, "Бразилейрао", 83),
            Club("Интернасьонал", "Бразилия", 4, "Бразилейрао", 82),
            Club("Атлетико Минейро", "Бразилия", 4, "Бразилейрао", 82),
            Club("Крузейро", "Бразилия", 3, "Бразилейрао", 78),
            Club("Ботафого", "Бразилия", 3, "Бразилейрао", 77),
            Club("Флуминенсе", "Бразилия", 3, "Бразилейрао", 77),
            Club("Васко да Гама", "Бразилия", 3, "Бразилейрао", 75),
            Club("Бока Хуниорс", "Аргентина", 4, "Примера", 86),
            Club("Ривер Плейт", "Аргентина", 4, "Примера", 86),
            Club("Индепендьенте", "Аргентина", 3, "Примера", 80),
            Club("Расинг", "Аргентина", 3, "Примера", 79),
            Club("Сан-Лоренсо", "Аргентина", 3, "Примера", 78),
            Club("Велес Сарсфилд", "Аргентина", 3, "Примера", 77),
            Club("Эстудиантес", "Аргентина", 3, "Примера", 76),
            Club("Ньюэллс Олд Бойз", "Аргентина", 2, "Примера", 72),
            Club("Насьональ", "Уругвай", 3, "Примера", 78),
            Club("Пеньяроль", "Уругвай", 3, "Примера", 77),
            Club("Дефенсор Спортинг", "Уругвай", 2, "Примера", 65),
            Club("Коло-Коло", "Чили", 3, "Примера", 75),
            Club("Универсидад де Чили", "Чили", 2, "Примера", 70),
            Club("Католика", "Чили", 2, "Примера", 69),
            Club("Олимпия", "Парагвай", 2, "Примера", 68),
            Club("Серро Портеньо", "Парагвай", 2, "Примера", 67),
            Club("Либертад", "Парагвай", 2, "Примера", 66),
            Club("Атлетико Насьональ", "Колумбия", 3, "Примера", 74),
            Club("Мильонариос", "Колумбия", 2, "Примера", 70),
            Club("Санта-Фе", "Колумбия", 2, "Примера", 68),
            Club("Хуниор", "Колумбия", 2, "Примера", 67),
        ]
        
        # Северная Америка (tier 1-3)
        north_america = [
            Club("Монтеррей", "Мексика", 3, "Лига МХ", 78),
            Club("Америка", "Мексика", 3, "Лига МХ", 77),
            Club("Гвадалахара", "Мексика", 3, "Лига МХ", 76),
            Club("Крус Асуль", "Мексика", 3, "Лига МХ", 75),
            Club("Тигрес", "Мексика", 3, "Лига МХ", 75),
            Club("Леон", "Мексика", 2, "Лига МХ", 72),
            Club("Толука", "Мексика", 2, "Лига МХ", 71),
            Club("Пачука", "Мексика", 2, "Лига МХ", 70),
            Club("Лос-Анджелес", "США", 2, "MLS", 68),
            Club("Нью-Йорк Сити", "США", 2, "MLS", 67),
            Club("Атланта Юнайтед", "США", 2, "MLS", 66),
            Club("Сиэтл", "США", 2, "MLS", 65),
            Club("Торонто", "Канада", 2, "MLS", 64),
            Club("Монреаль", "Канада", 1, "MLS", 60),
            Club("Ванкувер", "Канада", 1, "MLS", 59),
        ]
        
        # Азия (tier 1-4)
        asia = [
            Club("Касима Антлерс", "Япония", 3, "J-лига", 72),
            Club("Кавасаки Фронтале", "Япония", 3, "J-лига", 71),
            Club("Урава Редс", "Япония", 3, "J-лига", 70),
            Club("Иокогама Ф. Маринос", "Япония", 3, "J-лига", 70),
            Club("Гамба Осака", "Япония", 2, "J-лига", 65),
            Club("Ульсан", "Южная Корея", 3, "K-лига", 71),
            Club("Чонбук", "Южная Корея", 3, "K-лига", 70),
            Club("Сеул", "Южная Корея", 2, "K-лига", 65),
            Club("Сувон", "Южная Корея", 2, "K-лига", 63),
            Club("Шанхай Порт", "Китай", 3, "Суперлига", 70),
            Club("Шаньдун Тайшань", "Китай", 3, "Суперлига", 68),
            Club("Гуанчжоу", "Китай", 2, "Суперлига", 65),
            Club("Бэйцзин Гоань", "Китай", 2, "Суперлига", 64),
            Club("Аль-Хиляль", "Саудовская Аравия", 4, "Про-лига", 80),
            Club("Аль-Наср", "Саудовская Аравия", 4, "Про-лига", 79),
            Club("Аль-Иттихад", "Саудовская Аравия", 4, "Про-лига", 78),
            Club("Аль-Ахли", "Саудовская Аравия", 3, "Про-лига", 72),
            Club("Аль-Айн", "ОАЭ", 3, "Про-лига", 70),
            Club("Аль-Васл", "ОАЭ", 2, "Про-лига", 65),
            Club("Шабаб Аль-Ахли", "ОАЭ", 2, "Про-лига", 64),
            Club("Аль-Садд", "Катар", 3, "Звездная лига", 72),
            Club("Аль-Духаиль", "Катар", 3, "Звездная лига", 70),
            Club("Аль-Араби", "Катар", 2, "Звездная лига", 62),
            Club("Персеполис", "Иран", 2, "Про-лига", 62),
            Club("Эстегляль", "Иран", 2, "Про-лига", 60),
            Club("Пахтакор", "Узбекистан", 2, "Суперлига", 58),
            Club("Насаф", "Узбекистан", 1, "Суперлига", 52),
            Club("АГМК", "Узбекистан", 1, "Суперлига", 50),
            Club("Мельбурн Сити", "Австралия", 1, "A-лига", 52),
            Club("Сидней", "Австралия", 1, "A-лига", 51),
            Club("Мельбурн Виктори", "Австралия", 1, "A-лига", 50),
        ]
        
        # Африка (tier 1-3)
        africa = [
            Club("Аль-Ахли", "Египет", 3, "Премьер-лига", 72),
            Club("Замалек", "Египет", 2, "Премьер-лига", 65),
            Club("Пирамидз", "Египет", 2, "Премьер-лига", 62),
            Club("Эсперанс", "Тунис", 2, "Про-лига", 63),
            Club("Этуаль дю Сахель", "Тунис", 2, "Про-лига", 60),
            Club("Клуб Африкэн", "Тунис", 1, "Про-лига", 55),
            Club("Видад", "Марокко", 2, "Ботола", 62),
            Club("Раджа", "Марокко", 2, "Ботола", 61),
            Club("ФАР", "Марокко", 1, "Ботола", 54),
            Club("Саншайн Старз", "Нигерия", 1, "Про-лига", 48),
            Club("Эньимба", "Нигерия", 1, "Про-лига", 47),
            Club("Мамелоди Сандаунз", "ЮАР", 2, "Премьер-лига", 60),
            Club("Орландо Пайретс", "ЮАР", 2, "Премьер-лига", 58),
            Club("Кайзер Чифс", "ЮАР", 1, "Премьер-лига", 55),
        ]
        
        # Объединяем все клубы
        self.clubs.extend(top_clubs)
        self.clubs.extend(strong_clubs)
        self.clubs.extend(championship_clubs)
        self.clubs.extend(segunda_clubs)
        self.clubs.extend(zweite_bundesliga_clubs)
        self.clubs.extend(serie_b_clubs)
        self.clubs.extend(medium_european_clubs)
        self.clubs.extend(weak_european_clubs)
        self.clubs.extend(russian_clubs)
        self.clubs.extend(south_america)
        self.clubs.extend(north_america)
        self.clubs.extend(asia)
        self.clubs.extend(africa)
        
        print(f"Загружено клубов: {len(self.clubs)}")
    
    def sign_contract(self, club, salary, duration_months):
        """Подписание контракта с клубом"""
        if not self.player:
            return False
        
        old_club = self.player.career_stats['club']
        old_tier = self.player.career_stats['club_tier']
        
        # Обновляем информацию о клубе
        self.player.career_stats['club'] = club.name
        self.player.career_stats['club_tier'] = club.tier
        self.player.career_stats['salary'] = salary
        
        # Обновляем контракт
        self.player.contract['start_date'] = self.current_date
        self.player.contract['end_date'] = self.current_date.addMonths(duration_months)
        self.player.contract['duration_months'] = duration_months
        self.player.contract['weekly_salary'] = salary
        self.player.contract['club'] = club.name
        
        # Добавляем событие
        tier_names = {0: "Любительский", 1: "Низший дивизион", 2: "Первая лига", 
                     3: "Высшая лига", 4: "Топ-клуб", 5: "Суперклуб"}
        
        old_tier_name = tier_names.get(old_tier, "Неизвестно")
        new_tier_name = tier_names.get(club.tier, "Неизвестно")
        
        contract_text = f"📝 ПОДПИСАН КОНТРАКТ! {old_club} ({old_tier_name}) → {club.name} ({new_tier_name}, {club.country})"
        self.add_event(contract_text)
        self.add_event(f"💰 Зарплата: ${salary}/неделя | Срок: {duration_months} месяцев")
        
        # Очищаем предложения
        self.transfer_offers = []
        
        return True
    
    def check_contract_expiry(self):
        """Проверка истечения контракта"""
        if not self.player:
            return
        
        if self.current_date >= self.player.contract['end_date']:
            self.add_event("⚠️ Контракт истек! Теперь вы можете искать новый клуб или ждать предложений")
    
    def check_birthday(self):
        """Проверка дня рождения (каждый год после 7 декабря)"""
        if not self.player:
            return
        
        current_year = self.current_date.year()
        birthday_this_year = QDate(current_year, self.player.birth_month, self.player.birth_day)
        
        # Если сегодняшняя дата больше или равна дню рождения в этом году
        # И мы еще не отмечали день рождения в этом году
        if self.current_date >= birthday_this_year and self.player.last_birthday_year < current_year:
            self.player.age += 1
            self.player.last_birthday_year = current_year
            self.add_event(f"🎉🎂 С ДНЕМ РОЖДЕНИЯ! {self.player.name} исполнилось {self.player.age} лет! 🎂🎉")
    
    def check_milestones(self, stat_type, current_value):
        """Проверка юбилейных достижений"""
        if not self.player:
            return
        
        milestones = [1, 5, 10, 50, 100, 200, 300]
        milestone_messages = {
            'matches': {
                1: "⚽ ДЕБЮТ! Первый матч в карьере!",
                5: "🎯 5 матчей! Первый небольшой юбилей!",
                10: "🔟 Уже 10 матчей! Набираем опыт!",
                50: "🎉 ПОЛВЕКА! 50 матчей в профессиональном футболе!",
                100: "💯 СОТНЯ! 100 матчей — настоящий ветеран!",
                200: "🌟 200 МАТЧЕЙ! Легендарная цифра!",
                300: "👑 300 МАТЧЕЙ! Ты вошел в историю!"
            },
            'goals': {
                1: "⚽ ПЕРВЫЙ ГОЛ! Мечта сбылась!",
                5: "🎯 5 голов! Пятерка лучших!",
                10: "🔟 10 голов! Двузначное число!",
                50: "🎉 ПОЛВЕКА! 50 голов — грозный снайпер!",
                100: "💯 СОТНЯ ГОЛОВ! Настоящий бомбардир!",
                200: "🌟 200 ГОЛОВ! Легендарный результат!",
                300: "👑 300 ГОЛОВ! Ты среди величайших!"
            },
            'assists': {
                1: "🎯 ПЕРВАЯ ГOЛЕВАЯ! Отличный пас!",
                5: "📊 5 передач! Ассистент хорошего уровня!",
                10: "🔟 10 голевых! Плеймейкер растет!",
                50: "🎉 50 ПЕРЕДАЧ! Мастер ассистов!",
                100: "💯 100 ПЕРЕДАЧ! Элитный распасовщик!",
                200: "🌟 200 ПЕРЕДАЧ! Великий плеймейкер!",
                300: "👑 300 ПЕРЕДАЧ! Ты — легенда ассистов!"
            }
        }
        
        for milestone in milestones:
            if current_value >= milestone and not self.player.milestones[stat_type].get(milestone, False):
                self.player.milestones[stat_type][milestone] = True
                message = milestone_messages[stat_type].get(milestone, f"🏆 Юбилей! {milestone} {stat_type}!")
                # Добавляем более яркое сообщение для крупных юбилеев
                if milestone >= 100:
                    message = "⭐ " + message + " ⭐"
                self.add_event(message)
    
    def generate_transfer_offers(self):
        """Генерация входящих предложений о трансфере"""
        if not self.player:
            return
        
        # Игроки любого возраста могут получать предложения
        # Шанс получить предложение (5% каждую неделю)
        if random.random() < 0.05:
            available_clubs = self.get_available_clubs()
            
            if available_clubs:
                # Исключаем текущий клуб
                available_clubs = [c for c in available_clubs if c.name != self.player.career_stats['club']]
                
                if available_clubs:
                    # Генерируем 1-2 предложения
                    num_offers = random.randint(1, 2)
                    for _ in range(min(num_offers, len(available_clubs))):
                        club = random.choice(available_clubs)
                        available_clubs.remove(club)
                        
                        # Расчет зарплаты с большим разбросом
                        base_salary = 100  # Минимальная зарплата
                        tier_multipliers = {0: 1, 1: 5, 2: 20, 3: 50, 4: 200, 5: 500}
                        salary_multiplier = tier_multipliers.get(club.tier, 1)
                        
                        # Зарплата от 100 до 200,000 в зависимости от уровня клуба и рейтинга игрока
                        salary = int(base_salary * salary_multiplier * (self.player.overall / 50) * random.uniform(0.7, 1.5))
                        salary = max(100, min(200000, salary))
                        
                        # Длительность контракта
                        contract_options = [6, 12, 18, 24, 30, 36, 42, 48, 54, 60]
                        contract_months = random.choice(contract_options)
                        
                        offer = TransferOffer(club, salary, contract_months)
                        self.transfer_offers.append(offer)
                        
                        self.add_event(f"📨 Поступило предложение от {club.name}! Зарплата: ${salary}/неделя, контракт: {contract_months} мес.")
    
    def show_transfer_offers(self):
        """Показать диалог с предложениями о трансфере"""
        if not self.player:
            return
        
        if not self.transfer_offers:
            QMessageBox.information(self, "Предложения", "Нет входящих предложений о трансфере.")
            return
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Входящие предложения")
        dialog.setStyleSheet(self.styleSheet())
        dialog.setMinimumWidth(500)
        dialog.setMinimumHeight(400)
        
        layout = QVBoxLayout()
        
        title = QLabel(f"📨 Предложения для {self.player.name}")
        title.setStyleSheet("font-size: 14px; color: #FFD700; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Список предложений
        offers_list = QListWidget()
        offers_list.setMinimumHeight(200)
        
        for i, offer in enumerate(self.transfer_offers):
            item_text = f"{offer.club.name} ({offer.club.country}, {offer.club.league})\n💰 ${offer.weekly_salary}/неделя | 📅 {offer.contract_months} мес."
            offers_list.addItem(item_text)
        
        layout.addWidget(offers_list)
        
        # Кнопки для каждого предложения
        buttons_layout = QVBoxLayout()
        
        for i, offer in enumerate(self.transfer_offers):
            offer_group = QGroupBox(f"Предложение от {offer.club.name}")
            offer_layout = QVBoxLayout()
            
            info_label = QLabel(f"Страна: {offer.club.country}\nЛига: {offer.club.league}\n"
                               f"Уровень клуба: {offer.club.tier}\n"
                               f"Зарплата: ${offer.weekly_salary}/неделя\n"
                               f"Контракт: {offer.contract_months} месяцев")
            info_label.setWordWrap(True)
            offer_layout.addWidget(info_label)
            
            buttons_row = QHBoxLayout()
            
            accept_btn = QPushButton("✅ Принять")
            accept_btn.clicked.connect(lambda checked, o=offer: self.accept_transfer_offer(o, dialog))
            
            decline_btn = QPushButton("❌ Отклонить")
            decline_btn.clicked.connect(lambda checked, idx=i: self.decline_transfer_offer(idx))
            
            buttons_row.addWidget(accept_btn)
            buttons_row.addWidget(decline_btn)
            
            offer_layout.addLayout(buttons_row)
            offer_group.setLayout(offer_layout)
            buttons_layout.addWidget(offer_group)
        
        layout.addLayout(buttons_layout)
        
        # Кнопка закрытия
        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def accept_transfer_offer(self, offer, dialog):
        """Принять предложение о трансфере"""
        self.sign_contract(offer.club, offer.weekly_salary, offer.contract_months)
        dialog.accept()
        self.update_display()
    
    def decline_transfer_offer(self, index):
        """Отклонить предложение о трансфере"""
        if 0 <= index < len(self.transfer_offers):
            club_name = self.transfer_offers[index].club.name
            del self.transfer_offers[index]
            self.add_event(f"❌ Отклонено предложение от {club_name}")
    
    def get_available_clubs(self):
        """Получение списка доступных клубов на основе рейтинга игрока"""
        if not self.player:
            return []
        
        overall = self.player.overall
        reputation = self.player.career_stats['reputation']
        
        # Определяем максимальный доступный tier
        if overall >= 90 and reputation >= 90:
            max_tier = 5
            min_tier = 3
        elif overall >= 85 and reputation >= 80:
            max_tier = 4
            min_tier = 2
        elif overall >= 80 and reputation >= 70:
            max_tier = 4
            min_tier = 2
        elif overall >= 75 and reputation >= 60:
            max_tier = 3
            min_tier = 1
        elif overall >= 70 and reputation >= 50:
            max_tier = 3
            min_tier = 1
        elif overall >= 65 and reputation >= 40:
            max_tier = 2
            min_tier = 0
        else:
            max_tier = 1
            min_tier = 0
        
        # Фильтруем клубы
        available_clubs = []
        for club in self.clubs:
            if min_tier <= club.tier <= max_tier:
                rep_requirement = club.reputation
                if overall >= rep_requirement - 20:
                    available_clubs.append(club)
        
        return available_clubs
    
    def transfer(self):
        """Попытка перейти в другой клуб (активный поиск)"""
        if not self.check_player():
            return
        
        # Проверяем возраст - до 18 нельзя искать самому
        if self.player.age < 18:
            QMessageBox.warning(self, "Внимание", "Вы слишком молоды для самостоятельного поиска клуба! Достигните 18 лет.\n\nНо вы можете получать предложения от клубов.")
            return
        
        # Проверяем, не истек ли контракт
        if self.current_date < self.player.contract['end_date']:
            weeks_left = self.player.contract['end_date'].daysTo(self.current_date) // 7
            reply = QMessageBox.question(self, "Активный контракт", 
                                        f"У вас действующий контракт до {self.player.contract['end_date'].toString('dd.MM.yyyy')} "
                                        f"(осталось {abs(weeks_left)} недель).\n\n"
                                        "Нарушение контракта приведет к штрафу и потере репутации.\n"
                                        "Продолжить поиск клуба?",
                                        QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.No:
                return
            
            # Штраф за нарушение контракта
            self.player.career_stats['reputation'] = max(0, self.player.career_stats['reputation'] - 20)
            self.player.career_stats['salary'] = int(self.player.career_stats['salary'] * 0.7)
            self.add_event("⚠️ Нарушение контракта! Репутация и зарплата снижены")
        
        if self.player.career_stats['energy'] < 20:
            QMessageBox.warning(self, "Внимание", "Недостаточно энергии для переговоров!")
            return
        
        self.player.career_stats['energy'] -= 20
        
        # Получаем доступные клубы
        available_clubs = self.get_available_clubs()
        
        if not available_clubs:
            QMessageBox.information(self, "Трансфер", "Нет доступных клубов для трансфера!")
            return
        
        # Выбираем случайный клуб из доступных
        target_club = random.choice(available_clubs)
        
        # Шанс на трансфер
        base_chance = (self.player.overall + self.player.career_stats['reputation']) / 200
        club_factor = max(0.3, 1 - (target_club.reputation - self.player.overall) / 50)
        transfer_chance = base_chance * club_factor
        
        transfer_chance = max(0.1, min(0.9, transfer_chance))
        
        if random.random() < transfer_chance:
            self.show_contract_offer(target_club)
        else:
            fail_reasons = [
                f"❌ Трансфер в {target_club.name} не состоялся. Клуб не готов платить запрашиваемую сумму.",
                f"❌ {target_club.name} отказал в трансфере. Требуется больше опыта.",
                f"❌ Переговоры с {target_club.name} провалились. Агент запросил слишком высокую комиссию.",
                f"❌ {target_club.name} выбрал другого игрока на вашу позицию."
            ]
            self.add_event(random.choice(fail_reasons))
            self.player.career_stats['reputation'] = max(0, self.player.career_stats['reputation'] - random.randint(1, 3))
        
        self.advance_time()
        self.update_display()
    
    def show_contract_offer(self, club):
        """Показать предложение контракта от клуба"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Предложение контракта")
        dialog.setStyleSheet(self.styleSheet())
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        
        # Информация о клубе
        club_info = QLabel(f"🏢 {club.name}")
        club_info.setStyleSheet("font-size: 16px; color: #FFD700; font-weight: bold;")
        club_info.setAlignment(Qt.AlignCenter)
        layout.addWidget(club_info)
        
        details = QLabel(f"Страна: {club.country}\nЛига: {club.league}\nУровень клуба: {club.tier}")
        details.setWordWrap(True)
        layout.addWidget(details)
        
        # Расчет зарплаты с большим разбросом
        base_salary = 100
        tier_multipliers = {0: 1, 1: 5, 2: 20, 3: 50, 4: 200, 5: 500}
        salary_multiplier = tier_multipliers.get(club.tier, 1)
        
        suggested_salary = int(base_salary * salary_multiplier * (self.player.overall / 50))
        suggested_salary = max(100, min(200000, suggested_salary))
        
        # Выбор длительности контракта
        duration_layout = QHBoxLayout()
        duration_label = QLabel("Длительность контракта:")
        duration_label.setObjectName("title_label")
        duration_layout.addWidget(duration_label)
        
        duration_combo = QComboBox()
        contract_options = [
            ("6 месяцев", 6),
            ("1 год", 12),
            ("1.5 года", 18),
            ("2 года", 24),
            ("2.5 года", 30),
            ("3 года", 36),
            ("3.5 года", 42),
            ("4 года", 48),
            ("4.5 года", 54),
            ("5 лет", 60)
        ]
        
        for option_text, _ in contract_options:
            duration_combo.addItem(option_text)
        
        duration_layout.addWidget(duration_combo)
        layout.addLayout(duration_layout)
        
        # Зарплата
        salary_layout = QHBoxLayout()
        salary_label = QLabel("Зарплата в неделю:")
        salary_label.setObjectName("title_label")
        salary_layout.addWidget(salary_label)
        
        salary_spin = QSpinBox()
        salary_spin.setRange(100, 200000)
        salary_spin.setValue(suggested_salary)
        salary_spin.setSuffix(" $")
        salary_spin.setSingleStep(500)
        salary_layout.addWidget(salary_spin)
        layout.addLayout(salary_layout)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        
        sign_btn = QPushButton("✅ Подписать контракт")
        sign_btn.clicked.connect(lambda: self.sign_contract_from_dialog(club, salary_spin.value(), 
                                                                        contract_options[duration_combo.currentIndex()][1], 
                                                                        dialog))
        
        reject_btn = QPushButton("❌ Отклонить")
        reject_btn.clicked.connect(dialog.reject)
        
        buttons_layout.addWidget(sign_btn)
        buttons_layout.addWidget(reject_btn)
        layout.addLayout(buttons_layout)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def sign_contract_from_dialog(self, club, salary, duration_months, dialog):
        """Подписание контракта из диалога"""
        self.sign_contract(club, salary, duration_months)
        dialog.accept()
        self.update_display()
    
    def show_stats(self):
        """Показать детальную статистику"""
        if not self.check_player():
            return
        
        # Определяем текущий уровень клуба
        tier_names = {0: "Молодежная академия", 1: "Любительский", 2: "Низший дивизион", 
                     3: "Первая лига", 4: "Высшая лига", 5: "Топ-клуб"}
        
        current_tier = tier_names.get(self.player.career_stats['club_tier'], "Неизвестно")
        
        # Информация о контракте - показываем дату окончания и оставшееся время
        weeks_left = self.player.contract['end_date'].daysTo(self.current_date) // 7
        if weeks_left > 0:
            contract_status = f"Действует до {self.player.contract['end_date'].toString('dd.MM.yyyy')} (осталось {abs(weeks_left)} недель)"
        else:
            contract_status = f"ИСТЕК {self.player.contract['end_date'].toString('dd.MM.yyyy')}"
        
        stats_text = f"""
        Детальная статистика игрока {self.player.name}:
        
        Общая информация:
        - Возраст: {self.player.age}
        - Позиция: {self.player.position}
        - Общий рейтинг: {self.player.overall}
        - Клуб: {self.player.career_stats['club']} ({current_tier})
        - Зарплата: ${self.player.career_stats['salary']}/неделя
        - Репутация: {self.player.career_stats['reputation']}/100
        
        Контракт:
        - {contract_status}
        
        Карьерная статистика:
        - Матчи: {self.player.career_stats['matches']}
        - Голы: {self.player.career_stats['goals']}
        - Передачи: {self.player.career_stats['assists']}
        - Г+П за матч: {(self.player.career_stats['goals'] + self.player.career_stats['assists']) / max(1, self.player.career_stats['matches']):.2f}
        
        Юбилеи:
        - Сыграно юбилейных матчей: {sum(1 for m, achieved in self.player.milestones['matches'].items() if achieved)} из {len(self.player.milestones['matches'])}
        - Юбилейных голов: {sum(1 for m, achieved in self.player.milestones['goals'].items() if achieved)} из {len(self.player.milestones['goals'])}
        - Юбилейных передач: {sum(1 for m, achieved in self.player.milestones['assists'].items() if achieved)} из {len(self.player.milestones['assists'])}
        
        Трофеи: {len(self.player.trophies)}
        
        Доступно клубов для трансфера: {len(self.get_available_clubs())}
        Входящих предложений: {len(self.transfer_offers)}
        """
        
        QMessageBox.information(self, "Статистика карьеры", stats_text)
    
    def initUI(self):
        """Инициализация пользовательского интерфейса"""
        self.setWindowTitle('Симулятор карьеры футболиста')
        self.setGeometry(100, 100, 1200, 700)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a2e;
            }
            QLabel {
                color: #FFFFFF;
                font-size: 12px;
                font-weight: bold;
            }
            QLabel#title_label {
                color: #FFD700;
                font-size: 13px;
                font-weight: bold;
            }
            QLabel#value_label {
                color: #FFFFFF;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #16213e;
                color: white;
                border: 2px solid #0f3460;
                border-radius: 5px;
                padding: 8px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0f3460;
                border: 2px solid #FFD700;
            }
            QPushButton:pressed {
                background-color: #1a1a2e;
            }
            QGroupBox {
                color: #FFD700;
                font-size: 14px;
                font-weight: bold;
                border: 2px solid #0f3460;
                border-radius: 8px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #FFD700;
            }
            QProgressBar {
                border: 2px solid #0f3460;
                border-radius: 5px;
                text-align: center;
                color: white;
                background-color: #16213e;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 3px;
            }
            QListWidget {
                background-color: #16213e;
                color: #FFFFFF;
                border: 2px solid #0f3460;
                border-radius: 5px;
            }
            QListWidget::item {
                color: #FFFFFF;
            }
            QListWidget::item:selected {
                background-color: #0f3460;
            }
            QSpinBox, QComboBox, QLineEdit {
                background-color: #16213e;
                color: white;
                border: 2px solid #0f3460;
                border-radius: 3px;
                padding: 5px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background-color: #0f3460;
                border: none;
                border-radius: 2px;
            }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, 1)
        
        center_panel = self.create_center_panel()
        main_layout.addWidget(center_panel, 2)
        
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel, 1)
        
        QTimer.singleShot(100, self.show_create_player_dialog)
    
    def create_left_panel(self):
        """Создание левой панели с информацией об игроке"""
        left_panel = QGroupBox("ИНФОРМАЦИЯ ОБ ИГРОКЕ")
        left_layout = QVBoxLayout()
        
        self.player_name_label = QLabel("Имя: Не создан")
        self.player_name_label.setObjectName("value_label")
        
        self.player_age_label = QLabel("Возраст: -")
        self.player_age_label.setObjectName("value_label")
        
        self.player_position_label = QLabel("Позиция: -")
        self.player_position_label.setObjectName("value_label")
        
        self.player_overall_label = QLabel("Общий рейтинг: -")
        self.player_overall_label.setObjectName("value_label")
        
        self.player_club_label = QLabel("Клуб: -")
        self.player_club_label.setObjectName("value_label")
        
        self.player_salary_label = QLabel("Зарплата: -")
        self.player_salary_label.setObjectName("value_label")
        
        self.player_reputation_label = QLabel("Репутация: -")
        self.player_reputation_label.setObjectName("value_label")
        
        self.player_contract_label = QLabel("Контракт: -")
        self.player_contract_label.setObjectName("value_label")
        
        energy_layout = QHBoxLayout()
        energy_label = QLabel("Энергия:")
        energy_label.setObjectName("title_label")
        energy_layout.addWidget(energy_label)
        
        self.energy_bar = QProgressBar()
        self.energy_bar.setRange(0, 100)
        energy_layout.addWidget(self.energy_bar)
        
        stats_group = QGroupBox("ХАРАКТЕРИСТИКИ")
        stats_layout = QVBoxLayout()
        
        stats_names = {
            'pace': '⚡ Скорость',
            'shooting': '🎯 Удар',
            'passing': '📤 Пас',
            'dribbling': '🔄 Дриблинг',
            'defending': '🛡️ Защита',
            'physical': '💪 Физика',
            'stamina': '❤️ Выносливость'
        }
        
        for stat_key, stat_name in stats_names.items():
            stat_layout = QHBoxLayout()
            
            name_label = QLabel(f"{stat_name}:")
            name_label.setObjectName("title_label")
            stat_layout.addWidget(name_label)
            
            progress = QProgressBar()
            progress.setRange(0, 100)
            setattr(self, f"stat_{stat_key}", progress)
            
            value_label = QLabel("0")
            value_label.setObjectName("value_label")
            value_label.setMinimumWidth(30)
            setattr(self, f"stat_{stat_key}_value", value_label)
            
            stat_layout.addWidget(progress)
            stat_layout.addWidget(value_label)
            stats_layout.addLayout(stat_layout)
        
        stats_group.setLayout(stats_layout)
        
        left_layout.addWidget(self.player_name_label)
        left_layout.addWidget(self.player_age_label)
        left_layout.addWidget(self.player_position_label)
        left_layout.addWidget(self.player_overall_label)
        left_layout.addWidget(self.player_club_label)
        left_layout.addWidget(self.player_salary_label)
        left_layout.addWidget(self.player_reputation_label)
        left_layout.addWidget(self.player_contract_label)
        left_layout.addLayout(energy_layout)
        left_layout.addWidget(stats_group)
        left_layout.addStretch()
        
        left_panel.setLayout(left_layout)
        return left_panel
    
    def create_center_panel(self):
        """Создание центральной панели с календарем и статистикой"""
        center_panel = QGroupBox("КАРЬЕРА И СОБЫТИЯ")
        center_layout = QVBoxLayout()
        
        calendar_group = QGroupBox("Календарь")
        calendar_layout = QHBoxLayout()
        
        self.date_label = QLabel("1 января 2024")
        self.date_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #FFD700;")
        
        self.week_counter_label = QLabel("Неделя 1")
        self.week_counter_label.setStyleSheet("font-size: 14px; color: #FFFFFF;")
        
        calendar_layout.addWidget(self.date_label)
        calendar_layout.addWidget(self.week_counter_label)
        calendar_layout.addStretch()
        calendar_group.setLayout(calendar_layout)
        
        stats_group = QGroupBox("Статистика карьеры")
        stats_layout = QGridLayout()
        
        stats_items = [
            ('matches', ('📊 Матчи:', '0')),
            ('goals', ('⚽ Голы:', '0')),
            ('assists', ('🎯 Передачи:', '0')),
            ('trophies', ('🏆 Трофеи:', '0')),
            ('injury', ('⚠️ Травмы:', 'Нет'))
        ]
        
        for i, (key, (label_text, default_value)) in enumerate(stats_items):
            label = QLabel(label_text)
            label.setObjectName("title_label")
            
            value_label = QLabel(default_value)
            value_label.setObjectName("value_label")
            
            setattr(self, f"career_{key}_label", value_label)
            
            stats_layout.addWidget(label, i, 0)
            stats_layout.addWidget(value_label, i, 1)
        
        stats_group.setLayout(stats_layout)
        
        events_group = QGroupBox("Последние события")
        events_layout = QVBoxLayout()
        
        self.events_list = QListWidget()
        events_layout.addWidget(self.events_list)
        events_group.setLayout(events_layout)
        
        center_layout.addWidget(calendar_group)
        center_layout.addWidget(stats_group)
        center_layout.addWidget(events_group)
        
        center_panel.setLayout(center_layout)
        return center_panel
    
    def create_right_panel(self):
        """Создание правой панели с действиями"""
        right_panel = QGroupBox("ДЕЙСТВИЯ")
        right_layout = QVBoxLayout()
        
        buttons_info = [
            ("🏋️ Тренировка", self.train, "Улучшает характеристики, тратит энергию"),
            ("⚽ Матч", self.play_match, "Сыграть матч, можно забить гол"),
            ("😴 Отдых", self.rest, "Восстановить энергию"),
            ("🔄 Искать клуб", self.transfer, "Активный поиск нового клуба"),
            ("📨 Предложения", self.show_transfer_offers, "Просмотр входящих предложений"),
            ("📊 Статистика", self.show_stats, "Детальная статистика"),
            ("💾 Сохранить", self.save_game, "Сохранить прогресс"),
            ("📂 Загрузить", self.load_game, "Загрузить игру")
        ]
        
        for btn_text, btn_func, tooltip in buttons_info:
            btn = QPushButton(btn_text)
            btn.clicked.connect(btn_func)
            btn.setToolTip(tooltip)
            btn.setMinimumHeight(35)
            right_layout.addWidget(btn)
        
        status_group = QGroupBox("Текущее состояние")
        status_layout = QVBoxLayout()
        
        self.status_label = QLabel("Создайте игрока для начала карьеры")
        self.status_label.setWordWrap(True)
        self.status_label.setObjectName("value_label")
        status_layout.addWidget(self.status_label)
        
        self.offers_label = QLabel("Предложений: 0")
        self.offers_label.setObjectName("value_label")
        status_layout.addWidget(self.offers_label)
        
        status_group.setLayout(status_layout)
        right_layout.addWidget(status_group)
        right_layout.addStretch()
        
        right_panel.setLayout(right_layout)
        return right_panel
    
    def show_create_player_dialog(self):
        """Диалог создания игрока"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Создание игрока")
        dialog.setStyleSheet(self.styleSheet())
        dialog.setModal(True)
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        
        title_label = QLabel("⚽ СОЗДАНИЕ НОВОГО ИГРОКА")
        title_label.setStyleSheet("font-size: 16px; color: #FFD700; font-weight: bold; padding: 10px;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        name_layout = QHBoxLayout()
        name_label = QLabel("Имя игрока:")
        name_label.setObjectName("title_label")
        name_layout.addWidget(name_label)
        
        name_input = QLineEdit()
        name_input.setPlaceholderText("Введите имя")
        name_layout.addWidget(name_input)
        layout.addLayout(name_layout)
        
        pos_layout = QHBoxLayout()
        pos_label = QLabel("Позиция:")
        pos_label.setObjectName("title_label")
        pos_layout.addWidget(pos_label)
        
        position_combo = QComboBox()
        positions = ['CF', 'ST', 'LW', 'RW', 'CAM', 'CM', 'CDM', 'CB', 'LB', 'RB', 'GK']
        position_combo.addItems(positions)
        pos_layout.addWidget(position_combo)
        layout.addLayout(pos_layout)
        
        params_group = QGroupBox("Начальные параметры")
        params_layout = QGridLayout()
        
        age_label = QLabel("Возраст:")
        age_label.setObjectName("title_label")
        params_layout.addWidget(age_label, 0, 0)
        
        age_spin = QSpinBox()
        age_spin.setRange(14, 40)
        age_spin.setValue(14)
        age_spin.setSuffix(" лет")
        params_layout.addWidget(age_spin, 0, 1)
        
        overall_label = QLabel("Начальный рейтинг:")
        overall_label.setObjectName("title_label")
        params_layout.addWidget(overall_label, 1, 0)
        
        overall_spin = QSpinBox()
        overall_spin.setRange(1, 99)
        overall_spin.setValue(1)
        params_layout.addWidget(overall_spin, 1, 1)
        
        params_group.setLayout(params_layout)
        layout.addWidget(params_group)
        
        clubs_info = QLabel(f"📊 В игре доступно {len(self.clubs)} клубов из разных стран")
        clubs_info.setStyleSheet("color: #4CAF50; font-size: 11px; padding: 5px;")
        clubs_info.setAlignment(Qt.AlignCenter)
        layout.addWidget(clubs_info)
        
        buttons_layout = QHBoxLayout()
        create_btn = QPushButton("✅ СОЗДАТЬ")
        create_btn.setMinimumHeight(35)
        create_btn.setStyleSheet("background-color: #4CAF50; color: white;")
        
        cancel_btn = QPushButton("❌ ОТМЕНА")
        cancel_btn.setMinimumHeight(35)
        
        def create_player():
            name = name_input.text().strip()
            if not name:
                QMessageBox.warning(dialog, "Ошибка", "Введите имя игрока!")
                return
            
            self.player = Player(name)
            self.player.age = age_spin.value()
            self.player.overall = overall_spin.value()
            self.player.position = position_combo.currentText()
            
            # Балансировка начальных характеристик
            base_stats = overall_spin.value()
            for stat in self.player.stats:
                self.player.stats[stat] = min(99, max(1, base_stats + random.randint(-5, 5)))
            
            # Устанавливаем дату рождения
            self.player.birth_day = 7
            self.player.birth_month = 12
            self.player.last_birthday_year = self.current_date.year()
            
            # Сбрасываем флаги юбилеев
            self.player.milestones = {
                'matches': {1: False, 5: False, 10: False, 50: False, 100: False, 200: False, 300: False},
                'goals': {1: False, 5: False, 10: False, 50: False, 100: False, 200: False, 300: False},
                'assists': {1: False, 5: False, 10: False, 50: False, 100: False, 200: False, 300: False}
            }
            
            # Всегда начинаем в Беларуси, Казахстане или ФНЛ
            start_countries = ["Беларусь", "Казахстан", "Россия"]
            start_clubs = [c for c in self.clubs if c.country in start_countries and c.tier <= 1]
            
            if start_clubs:
                start_club = random.choice(start_clubs)
                self.player.career_stats['club'] = start_club.name
                self.player.career_stats['club_tier'] = start_club.tier
                self.player.career_stats['salary'] = 100 + random.randint(0, 100)  # Начальная зарплата от 100 до 200
                
                # Начальный контракт на 1 год
                self.player.contract['start_date'] = self.current_date
                self.player.contract['end_date'] = self.current_date.addMonths(12)
                self.player.contract['duration_months'] = 12
                self.player.contract['weekly_salary'] = self.player.career_stats['salary']
                self.player.contract['club'] = start_club.name
            else:
                # Запасной вариант
                self.player.career_stats['club'] = "Молодежная академия"
                self.player.career_stats['club_tier'] = 0
                self.player.career_stats['salary'] = 100
            
            self.update_display()
            self.add_event(f"✨ Игрок {name} создан! Добро пожаловать в мир футбола!")
            self.add_event(f"🏁 Начальный клуб: {self.player.career_stats['club']}")
            dialog.accept()
        
        create_btn.clicked.connect(create_player)
        cancel_btn.clicked.connect(dialog.reject)
        
        buttons_layout.addWidget(create_btn)
        buttons_layout.addWidget(cancel_btn)
        layout.addLayout(buttons_layout)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def train(self):
        """Тренировка игрока - улучшает одну характеристику"""
        if not self.check_player():
            return
        
        if self.player.career_stats['energy'] < 20:
            QMessageBox.warning(self, "Внимание", "Недостаточно энергии для тренировки!")
            return
        
        self.player.career_stats['energy'] -= 20
        
        # Тренировка улучшает одну случайную характеристику на 1-2 очка
        stat = random.choice(list(self.player.stats.keys()))
        if self.player.stats[stat] < 100:
            improvement = random.randint(1, 2)
            self.player.stats[stat] = min(100, self.player.stats[stat] + improvement)
            self.add_event(f"💪 Тренировка успешна! {stat} улучшена на +{improvement}")
        else:
            self.add_event("💪 Тренировка прошла, но характеристика уже максимальна")
        
        self.update_overall()
        self.advance_time()
        self.update_display()
    
    def play_match(self):
        """Сыграть матч"""
        if not self.check_player():
            return
        
        # Проверяем, есть ли у игрока клуб
        if self.player.career_stats['club'] == "Молодежная академия" or self.player.career_stats['club_tier'] == 0:
            QMessageBox.warning(self, "Внимание", "Вы не можете играть матчи без клуба! Сначала найдите клуб.")
            return
        
        if self.player.career_stats['energy'] < 30:
            QMessageBox.warning(self, "Внимание", "Недостаточно энергии для матча!")
            return
        
        if self.player.injured:
            QMessageBox.warning(self, "Внимание", "Игрок травмирован! Невозможно сыграть матч.")
            return
        
        self.player.career_stats['energy'] -= 30
        
        # Сохраняем предыдущие значения для проверки юбилеев
        old_matches = self.player.career_stats['matches']
        old_goals = self.player.career_stats['goals']
        old_assists = self.player.career_stats['assists']
        
        # Результат матча зависит от рейтинга игрока и случайности
        performance = random.randint(50, 100) + self.player.overall
        
        goals = 0
        assists = 0
        
        # Диапазоны с меньшим средним количеством, но возможностью достичь 7
        if performance > 160:  # Экстраординарная игра (очень редко)
            goals = random.randint(4, 7)
            assists = random.randint(2, 5)
            result = "ЛЕГЕНДАРНО! 👑🔥"
        elif performance > 145:  # Феноменальная игра
            goals = random.randint(2, 5)
            assists = random.randint(1, 4)
            result = "ФЕНОМЕНАЛЬНО! 🔥"
        elif performance > 130:  # Отличная игра
            goals = random.randint(1, 3)
            assists = random.randint(0, 2)
            result = "ОТЛИЧНО ⭐"
        elif performance > 115:  # Хорошая игра
            goals = random.randint(0, 2)
            assists = random.randint(0, 2)
            result = "ХОРОШО 👍"
        elif performance > 100:  # Средняя игра
            goals = random.randint(0, 1)
            assists = random.randint(0, 1)
            result = "НОРМАЛЬНО 📊"
        elif performance > 85:  # Ниже среднего
            goals = 0
            assists = random.randint(0, 1)
            result = "ТАК СЕБЕ 📉"
        else:  # Плохая игра
            goals = 0
            assists = 0
            result = "ПЛОХО 👎"
        
        # Ограничиваем максимальные значения
        goals = min(7, goals)
        assists = min(7, assists)
        
        # Обновляем статистику
        self.player.career_stats['matches'] += 1
        self.player.career_stats['goals'] += goals
        self.player.career_stats['assists'] += assists
        
        # Проверяем юбилеи
        self.check_milestones('matches', self.player.career_stats['matches'])
        self.check_milestones('goals', self.player.career_stats['goals'])
        self.check_milestones('assists', self.player.career_stats['assists'])
        
        # Шанс травмы
        if random.random() < 0.05:
            self.player.injured = True
            self.player.injury_weeks = random.randint(1, 4)
            self.add_event(f"⚠️ Травма во время матча! Выбыл на {self.player.injury_weeks} недель")
        
        # Обновляем репутацию
        rep_change = goals * 3 + assists * 2
        self.player.career_stats['reputation'] = min(100, self.player.career_stats['reputation'] + rep_change)
        
        # Добавляем событие
        event_text = f"⚽ Матч сыгран {result} Голы: {goals}, передачи: {assists}"
        self.add_event(event_text)
        
        self.advance_time()
        self.update_display()
    
    def rest(self):
        """Отдых для восстановления энергии"""
        if not self.check_player():
            return
        
        if self.player.injured:
            self.player.injury_weeks -= 1
            if self.player.injury_weeks <= 0:
                self.player.injured = False
                self.add_event("✨ Травма зажила! Игрок снова готов к матчам")
        
        # Восстановление энергии от 30 до 40
        energy_recovery = random.randint(30, 40)
        self.player.career_stats['energy'] = min(100, self.player.career_stats['energy'] + energy_recovery)
        
        self.add_event(f"😴 Отдых восстановил {energy_recovery} энергии")
        self.advance_time()
        self.update_display()
    
    def save_game(self):
        """Сохранение игры"""
        if not self.check_player():
            return
        
        QMessageBox.information(self, "Сохранение", "💾 Игра сохранена (демо-режим)")
        self.add_event("💾 Прогресс сохранен")
    
    def load_game(self):
        """Загрузка игры"""
        QMessageBox.information(self, "Загрузка", "📂 Функция загрузки в разработке")
    
    def update_overall(self):
        """Обновление общего рейтинга на основе характеристик"""
        if self.player:
            self.player.overall = int(sum(self.player.stats.values()) / len(self.player.stats))
    
    def advance_time(self):
        """Продвижение времени (на неделю)"""
        self.weeks_passed += 1
        self.current_date = self.current_date.addDays(7)
        
        # Проверяем день рождения (каждый год после 7 декабря)
        self.check_birthday()
        
        self.check_contract_expiry()
        self.generate_transfer_offers()
    
    def update_display(self):
        """Обновление отображения данных"""
        if not self.player:
            return
        
        self.player_name_label.setText(f"👤 Имя: {self.player.name}")
        self.player_age_label.setText(f"📅 Возраст: {self.player.age}")
        self.player_position_label.setText(f"📍 Позиция: {self.player.position}")
        self.player_overall_label.setText(f"⭐ Общий рейтинг: {self.player.overall}")
        self.player_club_label.setText(f"🏢 Клуб: {self.player.career_stats['club']}")
        self.player_salary_label.setText(f"💰 Зарплата: ${self.player.career_stats['salary']}/неделя")
        self.player_reputation_label.setText(f"📊 Репутация: {self.player.career_stats['reputation']}/100")
        
        # Исправлено отображение контракта - показываем оставшееся время или что истек
        weeks_left = self.player.contract['end_date'].daysTo(self.current_date) // 7
        if weeks_left > 0:
            contract_text = f"📝 Контракт: {weeks_left} нед. до {self.player.contract['end_date'].toString('dd.MM.yy')}"
        else:
            contract_text = f"📝 Контракт: ИСТЕК {self.player.contract['end_date'].toString('dd.MM.yy')}"
        self.player_contract_label.setText(contract_text)
        
        self.energy_bar.setValue(self.player.career_stats['energy'])
        
        for stat_key, stat_value in self.player.stats.items():
            bar = getattr(self, f"stat_{stat_key}")
            bar.setValue(stat_value)
            label = getattr(self, f"stat_{stat_key}_value")
            label.setText(str(stat_value))
        
        self.career_matches_label.setText(f"{self.player.career_stats['matches']}")
        self.career_goals_label.setText(f"{self.player.career_stats['goals']}")
        self.career_assists_label.setText(f"{self.player.career_stats['assists']}")
        self.career_trophies_label.setText(f"{len(self.player.trophies)}")
        
        injury_text = "Да ⚠️" if self.player.injured else "Нет ✅"
        if self.player.injured:
            injury_text += f" (осталось {self.player.injury_weeks} нед.)"
        self.career_injury_label.setText(injury_text)
        
        self.date_label.setText(self.current_date.toString("d MMMM yyyy"))
        self.week_counter_label.setText(f"📆 Неделя {self.weeks_passed}")
        
        if self.player.injured:
            self.status_label.setText(f"⚠️ ТРАВМА! Восстановление: {self.player.injury_weeks} недель")
        else:
            self.status_label.setText(f"✅ Здоров | ⚡ Энергия: {self.player.career_stats['energy']}%")
        
        self.offers_label.setText(f"📨 Предложений: {len(self.transfer_offers)}")
    
    def add_event(self, event_text):
        """Добавление события в список"""
        timestamp = self.current_date.toString("dd.MM.yyyy")
        self.events_list.insertItem(0, f"[{timestamp}] {event_text}")
        
        while self.events_list.count() > 20:
            self.events_list.takeItem(self.events_list.count() - 1)
    
    def check_player(self):
        """Проверка, создан ли игрок"""
        if not self.player:
            QMessageBox.warning(self, "Внимание", "Сначала создайте игрока!")
            self.show_create_player_dialog()
            return False
        return True

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    app.setWindowIcon(QIcon())
    
    window = FootballCareerSimulator()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()