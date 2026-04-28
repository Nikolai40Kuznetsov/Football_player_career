import sys
import random
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Player:
    """Класс игрока (футболиста)"""
    def __init__(self, name, nationality):
        self.name = name
        self.nationality = nationality
        self.age = 14
        self.overall = 1
        self.position = "CF"
        self.money = 10000
        self.has_contract = False
        self.years_in_club = 0  # Количество лет в текущем клубе
        
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
            'yellow_cards': 0,
            'red_cards': 0,
            'clean_sheets': 0,
            'salary': 0,
            'club': 'Свободный агент',
            'reputation': 1,
            'energy': 100,
            'club_tier': 0,
            'club_satisfaction': 50
        }
        
        # Контракт
        self.contract = {
            'start_date': QDate(2024, 1, 1),
            'end_date': QDate(2024, 1, 1),
            'duration_months': 0,
            'weekly_salary': 0,
            'signing_bonus': 0,
            'loyalty_bonus': 0,  # Бонус за лояльность при переподписании
            'salary_increase_pct': 0,  # Процент повышения зарплаты за год
            'club': 'Свободный агент',
            'bonuses': {
                'goal_bonus': 0,
                'assist_bonus': 0,
                'match_bonus': 0,
                'clean_sheet_bonus': 0
            }
        }
        
        # Карьерная статистика
        self.career_history = []
        
        # Трофеи и достижения
        self.trophies = []
        self.injured = False
        self.injury_weeks = 0
        self.weeks_without_match = 0
        
        # Сборная
        self.national_caps = 0
        self.national_goals = 0
        self.national_assists = 0
        self.in_national_team = False
        self.national_trophies = []
        
        # Дата рождения
        self.birth_day = 7
        self.birth_month = 12
        self.last_birthday_year = 2024
        
        # Флаги для юбилейных сообщений
        self.milestones = {
            'matches': {1: False, 5: False, 10: False, 50: False, 100: False, 200: False, 300: False},
            'goals': {1: False, 5: False, 10: False, 50: False, 100: False, 200: False, 300: False},
            'assists': {1: False, 5: False, 10: False, 50: False, 100: False, 200: False, 300: False},
            'national_caps': {1: False, 5: False, 10: False, 25: False, 50: False, 100: False}
        }

class Club:
    """Класс для представления клуба"""
    def __init__(self, name, country, tier, league, reputation, is_amateur=False):
        self.name = name
        self.country = country
        self.tier = tier
        self.league = league
        self.reputation = reputation
        self.is_amateur = is_amateur  # Любительский клуб
        
        # Турнирная таблица
        self.league_position = 1
        self.league_points = 0
        self.league_matches = 0
        self.league_wins = 0
        self.league_draws = 0
        self.league_losses = 0
        self.league_goals_for = 0
        self.league_goals_against = 0
        
        # Статистика в еврокубках
        self.champions_league = False
        self.europa_league = False
        self.conference_league = False
        self.europe_progress = 0
        
        # Статистика в кубке
        self.cup_progress = 0

class TransferOffer:
    """Класс для предложения о трансфере"""
    def __init__(self, club, weekly_salary, contract_months, signing_bonus, loyalty_bonus, salary_increase_pct, bonuses):
        self.club = club
        self.weekly_salary = weekly_salary
        self.contract_months = contract_months
        self.signing_bonus = signing_bonus
        self.loyalty_bonus = loyalty_bonus
        self.salary_increase_pct = salary_increase_pct
        self.bonuses = bonuses
        self.date_received = QDate.currentDate()

class NationalTeamCallDialog(QDialog):
    """Диалог вызова в сборную"""
    def __init__(self, tournament_name, parent=None):
        super().__init__(parent)
        self.tournament_name = tournament_name
        self.accepted = False
        self.setWindowTitle("Вызов в сборную")
        self.setMinimumSize(400, 300)
        self.setStyleSheet(parent.styleSheet() if parent else "")
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        title = QLabel(f"🇺🇳 ВЫЗОВ В СБОРНУЮ!")
        title.setStyleSheet("font-size: 18px; color: #FFD700; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        info = QLabel(f"Вы получили вызов в национальную сборную для участия в {self.tournament_name}!\n\n"
                     f"Это отличная возможность проявить себя на международной арене.\n\n"
                     f"Участие в турнире может повысить вашу репутацию,\n"
                     f"но потребует времени и энергии.")
        info.setWordWrap(True)
        info.setAlignment(Qt.AlignCenter)
        info.setStyleSheet("font-size: 12px; color: #FFFFFF;")
        layout.addWidget(info)
        
        buttons_layout = QHBoxLayout()
        
        accept_btn = QPushButton("✅ Принять вызов")
        accept_btn.clicked.connect(self.accept_call)
        
        decline_btn = QPushButton("❌ Отказаться")
        decline_btn.clicked.connect(self.reject)
        
        buttons_layout.addWidget(accept_btn)
        buttons_layout.addWidget(decline_btn)
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
    
    def accept_call(self):
        self.accepted = True
        self.accept()

class NationalTeamDialog(QDialog):
    """Диалог статистики в сборной"""
    def __init__(self, player, parent=None):
        super().__init__(parent)
        self.player = player
        self.setWindowTitle(f"Сборная {player.nationality}")
        self.setMinimumSize(500, 400)
        self.setStyleSheet(parent.styleSheet() if parent else "")
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        title = QLabel(f"🇺🇳 СБОРНАЯ {self.player.nationality.upper()}")
        title.setStyleSheet("font-size: 18px; color: #FFD700; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        stats_group = QGroupBox("Статистика в сборной")
        stats_layout = QVBoxLayout()
        
        stats_layout.addWidget(QLabel(f"📊 Матчи: {self.player.national_caps}"))
        stats_layout.addWidget(QLabel(f"⚽ Голы: {self.player.national_goals}"))
        stats_layout.addWidget(QLabel(f"🎯 Передачи: {self.player.national_assists}"))
        stats_layout.addWidget(QLabel(f"📈 Г+П за матч: {(self.player.national_goals + self.player.national_assists) / max(1, self.player.national_caps):.2f}"))
        
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        if self.player.national_trophies:
            trophies_group = QGroupBox("Трофеи со сборной")
            trophies_layout = QVBoxLayout()
            for trophy in self.player.national_trophies:
                trophies_layout.addWidget(QLabel(f"🏆 {trophy}"))
            trophies_group.setLayout(trophies_layout)
            layout.addWidget(trophies_group)
        
        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)

class ContractExtensionDialog(QDialog):
    """Диалог продления контракта"""
    def __init__(self, club, current_salary, current_bonuses, player, is_club_initiated, parent=None):
        super().__init__(parent)
        self.club = club
        self.current_salary = current_salary
        self.current_bonuses = current_bonuses.copy()
        self.player = player
        self.is_club_initiated = is_club_initiated
        self.final_salary = current_salary
        self.final_bonuses = current_bonuses.copy()
        self.final_duration = 12
        self.final_signing_bonus = 0
        self.final_loyalty_bonus = 0
        self.final_salary_increase_pct = 0
        self.extension_success = False
        
        self.setWindowTitle(f"Продление контракта с {club.name}")
        self.setMinimumWidth(600)
        self.setStyleSheet(parent.styleSheet() if parent else "")
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        if self.is_club_initiated:
            title = QLabel(f"🏢 КЛУБ ПРЕДЛАГАЕТ ПРОДЛИТЬ КОНТРАКТ")
            title.setStyleSheet("font-size: 16px; color: #FFD700; font-weight: bold;")
        else:
            title = QLabel(f"🤝 ЗАПРОС НА ПРОДЛЕНИЕ КОНТРАКТА")
            title.setStyleSheet("font-size: 16px; color: #FFD700; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        club_info = QLabel(f"🏢 {self.club.name} ({self.club.country}, {self.club.league})")
        club_info.setStyleSheet("font-size: 14px; color: #FFFFFF;")
        club_info.setAlignment(Qt.AlignCenter)
        layout.addWidget(club_info)
        
        satisfaction = QLabel(f"📊 Удовлетворенность клуба: {self.player.career_stats['club_satisfaction']}/100")
        satisfaction.setStyleSheet("color: #FFD700;")
        satisfaction.setAlignment(Qt.AlignCenter)
        layout.addWidget(satisfaction)
        
        player_rating = QLabel(f"⭐ Ваш рейтинг: {self.player.overall} | Репутация: {self.player.career_stats['reputation']}")
        player_rating.setStyleSheet("color: #FFD700;")
        player_rating.setAlignment(Qt.AlignCenter)
        layout.addWidget(player_rating)
        
        current_group = QGroupBox("Текущие условия")
        current_layout = QVBoxLayout()
        current_layout.addWidget(QLabel(f"💰 Текущая зарплата: ${self.current_salary}/неделя"))
        current_layout.addWidget(QLabel(f"📈 Повышение зарплаты: {self.player.contract['salary_increase_pct']}% в год"))
        current_layout.addWidget(QLabel(f"🎯 Бонус за гол: ${self.current_bonuses['goal_bonus']}"))
        current_layout.addWidget(QLabel(f"🎯 Бонус за передачу: ${self.current_bonuses['assist_bonus']}"))
        current_layout.addWidget(QLabel(f"📊 Бонус за матч: ${self.current_bonuses['match_bonus']}"))
        current_group.setLayout(current_layout)
        layout.addWidget(current_group)
        
        offer_group = QGroupBox("Предложение клуба")
        offer_layout = QVBoxLayout()
        
        suggested_salary = int(self.current_salary * random.uniform(1.05, 1.25))
        self.salary_spin = QSpinBox()
        self.salary_spin.setRange(int(suggested_salary * 0.8), int(suggested_salary * 1.2))
        self.salary_spin.setValue(suggested_salary)
        self.salary_spin.setSuffix(" $/неделя")
        self.salary_spin.setSingleStep(500)
        offer_layout.addWidget(QLabel("💰 Предлагаемая зарплата:"))
        offer_layout.addWidget(self.salary_spin)
        
        # Повышение зарплаты за год
        offer_layout.addWidget(QLabel("📈 Повышение зарплаты (от 1% до 20% в год):"))
        self.increase_pct_spin = QDoubleSpinBox()
        self.increase_pct_spin.setRange(1, 20)
        self.increase_pct_spin.setValue(random.randint(1, 20))
        self.increase_pct_spin.setSuffix(" %")
        self.increase_pct_spin.setSingleStep(0.5)
        offer_layout.addWidget(self.increase_pct_spin)
        
        offer_layout.addWidget(QLabel("🎯 Бонусы:"))
        bonus_layout = QGridLayout()
        
        bonus_layout.addWidget(QLabel("⚽ За гол:"), 0, 0)
        self.goal_bonus_spin = QSpinBox()
        self.goal_bonus_spin.setRange(int(self.current_salary * 0.02), int(self.current_salary * 0.1))
        self.goal_bonus_spin.setValue(self.current_bonuses['goal_bonus'])
        self.goal_bonus_spin.setSuffix(" $")
        bonus_layout.addWidget(self.goal_bonus_spin, 0, 1)
        
        bonus_layout.addWidget(QLabel("🎯 За передачу:"), 1, 0)
        self.assist_bonus_spin = QSpinBox()
        self.assist_bonus_spin.setRange(int(self.current_salary * 0.02), int(self.current_salary * 0.1))
        self.assist_bonus_spin.setValue(self.current_bonuses['assist_bonus'])
        self.assist_bonus_spin.setSuffix(" $")
        bonus_layout.addWidget(self.assist_bonus_spin, 1, 1)
        
        bonus_layout.addWidget(QLabel("📊 За матч:"), 2, 0)
        self.match_bonus_spin = QSpinBox()
        self.match_bonus_spin.setRange(int(self.current_salary * 0.02), int(self.current_salary * 0.1))
        self.match_bonus_spin.setValue(self.current_bonuses['match_bonus'])
        self.match_bonus_spin.setSuffix(" $")
        bonus_layout.addWidget(self.match_bonus_spin, 2, 1)
        
        offer_layout.addLayout(bonus_layout)
        
        # Бонус за лояльность
        offer_layout.addWidget(QLabel("💎 Бонус за лояльность (от 0.5 до 3 зарплат):"))
        self.loyalty_bonus_spin = QSpinBox()
        min_bonus = int(self.current_salary * 0.5)
        max_bonus = int(self.current_salary * 3)
        self.loyalty_bonus_spin.setRange(min_bonus, max_bonus)
        self.loyalty_bonus_spin.setValue(random.randint(min_bonus, max_bonus))
        self.loyalty_bonus_spin.setSuffix(" $")
        self.loyalty_bonus_spin.setSingleStep(500)
        offer_layout.addWidget(self.loyalty_bonus_spin)
        
        # Подъемные
        offer_layout.addWidget(QLabel("💵 Подъемные:"))
        self.signing_bonus_spin = QSpinBox()
        min_signing = int(self.current_salary * 1)
        max_signing = int(self.current_salary * 6)
        self.signing_bonus_spin.setRange(min_signing, max_signing)
        self.signing_bonus_spin.setValue(random.randint(min_signing, max_signing))
        self.signing_bonus_spin.setSuffix(" $")
        self.signing_bonus_spin.setSingleStep(1000)
        offer_layout.addWidget(self.signing_bonus_spin)
        
        offer_layout.addWidget(QLabel("📅 Длительность:"))
        self.duration_combo = QComboBox()
        contract_options = [
            ("6 месяцев", 6), ("1 год", 12), ("1.5 года", 18), ("2 года", 24),
            ("2.5 года", 30), ("3 года", 36), ("3.5 года", 42), ("4 года", 48),
            ("4.5 года", 54), ("5 лет", 60)
        ]
        for option_text, _ in contract_options:
            self.duration_combo.addItem(option_text)
        offer_layout.addWidget(self.duration_combo)
        
        offer_group.setLayout(offer_layout)
        layout.addWidget(offer_group)
        
        self.success_label = QLabel("⚖️ Шанс на успех: 50%")
        self.success_label.setAlignment(Qt.AlignCenter)
        self.success_label.setStyleSheet("color: #FFD700; font-size: 12px;")
        layout.addWidget(self.success_label)
        
        buttons_layout = QHBoxLayout()
        
        accept_btn = QPushButton("✅ Принять продление")
        accept_btn.clicked.connect(self.accept_extension)
        
        reject_btn = QPushButton("❌ Отказаться")
        reject_btn.clicked.connect(self.reject)
        
        buttons_layout.addWidget(accept_btn)
        buttons_layout.addWidget(reject_btn)
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
        
        def update_chance():
            base_chance = 0.6 + (self.player.overall / 200) + (self.player.career_stats['reputation'] / 200)
            base_chance = min(0.95, base_chance)
            
            salary_ratio = self.salary_spin.value() / self.current_salary
            if salary_ratio <= 1.0:
                salary_factor = 1.0 + (1.0 - salary_ratio) * 0.3
            else:
                salary_factor = 1.0 - (salary_ratio - 1.0) * 0.6
            
            chance = base_chance * salary_factor
            chance = max(0.1, min(0.95, chance))
            
            self.success_label.setText(f"⚖️ Шанс на успех: {int(chance * 100)}%")
            self.negotiation_chance = chance
        
        self.salary_spin.valueChanged.connect(update_chance)
        update_chance()
    
    def accept_extension(self):
        if random.random() < self.negotiation_chance:
            self.final_salary = self.salary_spin.value()
            self.final_bonuses = {
                'goal_bonus': self.goal_bonus_spin.value(),
                'assist_bonus': self.assist_bonus_spin.value(),
                'match_bonus': self.match_bonus_spin.value(),
                'clean_sheet_bonus': self.current_bonuses['clean_sheet_bonus']
            }
            self.final_duration = [6, 12, 18, 24, 30, 36, 42, 48, 54, 60][self.duration_combo.currentIndex()]
            self.final_signing_bonus = self.signing_bonus_spin.value()
            self.final_loyalty_bonus = self.loyalty_bonus_spin.value()
            self.final_salary_increase_pct = self.increase_pct_spin.value()
            self.extension_success = True
            self.accept()
        else:
            QMessageBox.warning(self, "Переговоры провалены", 
                              "Клуб не согласился на ваши условия.")

class CareerHistoryDialog(QDialog):
    """Диалог с историей карьеры"""
    def __init__(self, player, parent=None):
        super().__init__(parent)
        self.player = player
        self.setWindowTitle("История карьеры")
        self.setMinimumSize(600, 400)
        self.setStyleSheet(parent.styleSheet() if parent else "")
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        title = QLabel("📜 ИСТОРИЯ КАРЬЕРЫ")
        title.setStyleSheet("font-size: 16px; color: #FFD700; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(7)
        self.history_table.setHorizontalHeaderLabels(["Клуб", "Страна", "Пришел", "Ушел", "Матчи", "Голы", "Передачи"])
        self.history_table.horizontalHeader().setStretchLastSection(True)
        
        self.update_history()
        
        layout.addWidget(self.history_table)
        
        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)
    
    def update_history(self):
        history = self.player.career_history
        self.history_table.setRowCount(len(history))
        
        for i, entry in enumerate(history):
            self.history_table.setItem(i, 0, QTableWidgetItem(entry['club']))
            self.history_table.setItem(i, 1, QTableWidgetItem(entry.get('country', 'Неизвестно')))
            self.history_table.setItem(i, 2, QTableWidgetItem(entry['start'].toString("dd.MM.yyyy")))
            self.history_table.setItem(i, 3, QTableWidgetItem(entry['end'].toString("dd.MM.yyyy")))
            self.history_table.setItem(i, 4, QTableWidgetItem(str(entry['matches'])))
            self.history_table.setItem(i, 5, QTableWidgetItem(str(entry['goals'])))
            self.history_table.setItem(i, 6, QTableWidgetItem(str(entry['assists'])))

class TrophiesDialog(QDialog):
    """Диалог с трофеями"""
    def __init__(self, player, parent=None):
        super().__init__(parent)
        self.player = player
        self.setWindowTitle("Трофеи и достижения")
        self.setMinimumSize(500, 400)
        self.setStyleSheet(parent.styleSheet() if parent else "")
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        title = QLabel("🏆 ТРОФЕИ И ДОСТИЖЕНИЯ")
        title.setStyleSheet("font-size: 16px; color: #FFD700; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        tabs = QTabWidget()
        
        club_trophies = QWidget()
        club_layout = QVBoxLayout(club_trophies)
        if not [t for t in self.player.trophies if 'Сборная' not in t['name']]:
            no_trophies = QLabel("Пока нет выигранных клубных трофеев")
            no_trophies.setStyleSheet("color: #FFFFFF; font-size: 14px; padding: 20px;")
            no_trophies.setAlignment(Qt.AlignCenter)
            club_layout.addWidget(no_trophies)
        else:
            trophies_table = QTableWidget()
            trophies_table.setColumnCount(4)
            trophies_table.setHorizontalHeaderLabels(["Трофей", "Клуб", "Дата", "Сезон"])
            trophies_table.horizontalHeader().setStretchLastSection(True)
            
            club_trophies_list = [t for t in self.player.trophies if 'Сборная' not in t['name']]
            trophies_table.setRowCount(len(club_trophies_list))
            
            for i, trophy in enumerate(club_trophies_list):
                trophies_table.setItem(i, 0, QTableWidgetItem(trophy['name']))
                trophies_table.setItem(i, 1, QTableWidgetItem(trophy['club']))
                trophies_table.setItem(i, 2, QTableWidgetItem(trophy['date'].toString("dd.MM.yyyy")))
                trophies_table.setItem(i, 3, QTableWidgetItem(trophy['season']))
            
            club_layout.addWidget(trophies_table)
        
        tabs.addTab(club_trophies, "Клубные трофеи")
        
        national_trophies = QWidget()
        national_layout = QVBoxLayout(national_trophies)
        if not self.player.national_trophies:
            no_trophies = QLabel("Пока нет трофеев со сборной")
            no_trophies.setStyleSheet("color: #FFFFFF; font-size: 14px; padding: 20px;")
            no_trophies.setAlignment(Qt.AlignCenter)
            national_layout.addWidget(no_trophies)
        else:
            national_table = QTableWidget()
            national_table.setColumnCount(3)
            national_table.setHorizontalHeaderLabels(["Турнир", "Дата", "Сезон"])
            national_table.horizontalHeader().setStretchLastSection(True)
            
            national_table.setRowCount(len(self.player.national_trophies))
            for i, trophy in enumerate(self.player.national_trophies):
                national_table.setItem(i, 0, QTableWidgetItem(trophy['name']))
                national_table.setItem(i, 1, QTableWidgetItem(trophy['date'].toString("dd.MM.yyyy")))
                national_table.setItem(i, 2, QTableWidgetItem(trophy['season']))
            
            national_layout.addWidget(national_table)
        
        tabs.addTab(national_trophies, "Трофеи со сборной")
        layout.addWidget(tabs)
        
        stats_group = QGroupBox("Статистика трофеев")
        stats_layout = QVBoxLayout()
        
        club_trophies_list = [t for t in self.player.trophies if 'Сборная' not in t['name']]
        league_titles = sum(1 for t in club_trophies_list if "Чемпион" in t['name'] and "Лиги" in t['name'])
        cup_titles = sum(1 for t in club_trophies_list if "Кубок" in t['name'])
        champions_league = sum(1 for t in club_trophies_list if "Лига Чемпионов" in t['name'])
        europa_league = sum(1 for t in club_trophies_list if "Лига Европы" in t['name'])
        conference_league = sum(1 for t in club_trophies_list if "Лига Конференций" in t['name'])
        
        stats_layout.addWidget(QLabel(f"🏆 Чемпионства в лиге: {league_titles}"))
        stats_layout.addWidget(QLabel(f"🏆 Кубковые победы: {cup_titles}"))
        stats_layout.addWidget(QLabel(f"🌟 Победы в Лиге Чемпионов: {champions_league}"))
        stats_layout.addWidget(QLabel(f"🌟 Победы в Лиге Европы: {europa_league}"))
        stats_layout.addWidget(QLabel(f"🌟 Победы в Лиге Конференций: {conference_league}"))
        stats_layout.addWidget(QLabel(f"🇺🇳 Трофеи со сборной: {len(self.player.national_trophies)}"))
        stats_layout.addWidget(QLabel(f"📊 Всего трофеев: {len(self.player.trophies) + len(self.player.national_trophies)}"))
        
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)

class ClubInfoDialog(QDialog):
    """Диалог с информацией о клубе"""
    def __init__(self, club, player, parent=None):
        super().__init__(parent)
        self.club = club
        self.player = player
        self.setWindowTitle(f"Информация о клубе {club.name}")
        self.setMinimumSize(500, 400)
        self.setStyleSheet(parent.styleSheet() if parent else "")
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        title = QLabel(f"🏢 {self.club.name}")
        title.setStyleSheet("font-size: 18px; color: #FFD700; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        info_group = QGroupBox("Основная информация")
        info_layout = QGridLayout()
        
        info_layout.addWidget(QLabel(f"🌍 Страна:"), 0, 0)
        info_layout.addWidget(QLabel(f"{self.club.country}"), 0, 1)
        
        info_layout.addWidget(QLabel(f"📊 Лига:"), 1, 0)
        info_layout.addWidget(QLabel(f"{self.club.league}"), 1, 1)
        
        info_layout.addWidget(QLabel(f"📈 Уровень клуба:"), 2, 0)
        if self.club.is_amateur:
            info_layout.addWidget(QLabel(f"Любительский клуб"), 2, 1)
        else:
            tier_names = {0: "Любительский", 1: "Низший дивизион", 2: "Первая лига", 
                         3: "Высшая лига", 4: "Топ-клуб", 5: "Суперклуб"}
            info_layout.addWidget(QLabel(f"{tier_names.get(self.club.tier, 'Неизвестно')}"), 2, 1)
        
        info_layout.addWidget(QLabel(f"⭐ Репутация:"), 3, 0)
        info_layout.addWidget(QLabel(f"{self.club.reputation}/100"), 3, 1)
        
        info_layout.addWidget(QLabel(f"📊 Удовлетворенность игроком:"), 4, 0)
        info_layout.addWidget(QLabel(f"{self.player.career_stats['club_satisfaction']}/100"), 4, 1)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        league_group = QGroupBox("Турнирная таблица")
        league_layout = QGridLayout()
        
        league_layout.addWidget(QLabel(f"🏆 Позиция в лиге:"), 0, 0)
        league_layout.addWidget(QLabel(f"{self.club.league_position}-е место"), 0, 1)
        
        league_layout.addWidget(QLabel(f"⚽ Очки:"), 1, 0)
        league_layout.addWidget(QLabel(f"{self.club.league_points}"), 1, 1)
        
        league_layout.addWidget(QLabel(f"📊 Матчи:"), 2, 0)
        league_layout.addWidget(QLabel(f"{self.club.league_matches}"), 2, 1)
        
        league_layout.addWidget(QLabel(f"✅ Победы:"), 3, 0)
        league_layout.addWidget(QLabel(f"{self.club.league_wins}"), 3, 1)
        
        league_layout.addWidget(QLabel(f"🤝 Ничьи:"), 4, 0)
        league_layout.addWidget(QLabel(f"{self.club.league_draws}"), 4, 1)
        
        league_layout.addWidget(QLabel(f"❌ Поражения:"), 5, 0)
        league_layout.addWidget(QLabel(f"{self.club.league_losses}"), 5, 1)
        
        league_layout.addWidget(QLabel(f"⚽ Голы:"), 6, 0)
        league_layout.addWidget(QLabel(f"{self.club.league_goals_for}:{self.club.league_goals_against}"), 6, 1)
        
        league_group.setLayout(league_layout)
        layout.addWidget(league_group)
        
        if not self.club.is_amateur:
            europe_group = QGroupBox("Еврокубки")
            europe_layout = QVBoxLayout()
            
            europe_status = []
            if self.club.champions_league:
                europe_status.append("Лига Чемпионов")
            if self.club.europa_league:
                europe_status.append("Лига Европы")
            if self.club.conference_league:
                europe_status.append("Лига Конференций")
            
            if europe_status:
                europe_layout.addWidget(QLabel("Участвует в: " + ", ".join(europe_status)))
                europe_progress_names = {0: "Не участвует", 1: "Групповой этап", 2: "1/16 финала", 
                                        3: "1/8 финала", 4: "1/4 финала", 5: "1/2 финала", 
                                        6: "Финалист", 7: "Победитель"}
                europe_layout.addWidget(QLabel(f"Прогресс: {europe_progress_names.get(self.club.europe_progress, 'Неизвестно')}"))
            else:
                europe_layout.addWidget(QLabel("Не участвует в еврокубках"))
            
            europe_group.setLayout(europe_layout)
            layout.addWidget(europe_group)
            
            cup_group = QGroupBox("Национальный кубок")
            cup_layout = QVBoxLayout()
            
            cup_progress_names = {0: "Вылет", 1: "1/64 финала", 2: "1/32 финала", 3: "1/16 финала",
                                 4: "1/8 финала", 5: "1/4 финала", 6: "1/2 финала", 
                                 7: "Финалист", 8: "Победитель"}
            cup_layout.addWidget(QLabel(f"Прогресс: {cup_progress_names.get(self.club.cup_progress, 'Неизвестно')}"))
            
            cup_group.setLayout(cup_layout)
            layout.addWidget(cup_group)
        
        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)

class NegotiationDialog(QDialog):
    """Диалог переговоров с клубом"""
    def __init__(self, club, initial_salary, initial_bonuses, player, is_renewal=False, parent=None):
        super().__init__(parent)
        self.club = club
        self.initial_salary = initial_salary
        self.initial_bonuses = initial_bonuses.copy()
        self.player = player
        self.is_renewal = is_renewal  # Переподписание контракта с тем же клубом
        self.final_salary = initial_salary
        self.final_bonuses = initial_bonuses.copy()
        self.final_duration = 12
        self.final_signing_bonus = 0
        self.final_loyalty_bonus = 0
        self.final_salary_increase_pct = 0
        self.negotiation_success = False
        
        self.setWindowTitle(f"Переговоры с {club.name}")
        self.setMinimumWidth(600)
        self.setStyleSheet(parent.styleSheet() if parent else "")
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        title = QLabel("🤝 ПЕРЕГОВОРЫ О КОНТРАКТЕ")
        title.setStyleSheet("font-size: 16px; color: #FFD700; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        club_info = QLabel(f"🏢 {self.club.name} ({self.club.country}, {self.club.league})")
        club_info.setStyleSheet("font-size: 14px; color: #FFFFFF;")
        club_info.setAlignment(Qt.AlignCenter)
        layout.addWidget(club_info)
        
        player_rating = QLabel(f"⭐ Ваш рейтинг: {self.player.overall} | Репутация: {self.player.career_stats['reputation']}")
        player_rating.setStyleSheet("color: #FFD700;")
        player_rating.setAlignment(Qt.AlignCenter)
        layout.addWidget(player_rating)
        
        salary_group = QGroupBox("💰 Зарплата (в неделю)")
        salary_layout = QVBoxLayout()
        
        salary_label = QLabel(f"Предложение клуба: ${self.initial_salary}")
        salary_label.setStyleSheet("color: #4CAF50; font-size: 12px;")
        salary_layout.addWidget(salary_label)
        
        salary_slider_layout = QHBoxLayout()
        salary_slider = QSlider(Qt.Horizontal)
        salary_slider.setRange(int(self.initial_salary * 0.5), int(self.initial_salary * 1.5))
        salary_slider.setValue(self.initial_salary)
        salary_slider.setTickInterval(100)
        salary_slider.setTickPosition(QSlider.TicksBelow)
        salary_slider_layout.addWidget(salary_slider)
        
        salary_value = QSpinBox()
        salary_value.setRange(int(self.initial_salary * 0.5), int(self.initial_salary * 1.5))
        salary_value.setValue(self.initial_salary)
        salary_value.setSuffix(" $")
        salary_slider_layout.addWidget(salary_value)
        
        salary_slider.valueChanged.connect(salary_value.setValue)
        salary_value.valueChanged.connect(salary_slider.setValue)
        
        salary_layout.addLayout(salary_slider_layout)
        salary_group.setLayout(salary_layout)
        layout.addWidget(salary_group)
        
        # Повышение зарплаты за год
        increase_group = QGroupBox("📈 Повышение зарплаты за год")
        increase_layout = QHBoxLayout()
        
        self.increase_pct_spin = QDoubleSpinBox()
        self.increase_pct_spin.setRange(1, 20)
        self.increase_pct_spin.setValue(random.randint(1, 20))
        self.increase_pct_spin.setSuffix(" %")
        self.increase_pct_spin.setSingleStep(0.5)
        increase_layout.addWidget(self.increase_pct_spin)
        
        increase_group.setLayout(increase_layout)
        layout.addWidget(increase_group)
        
        bonuses_group = QGroupBox("🎯 Бонусы (от 2% до 10% от зарплаты)")
        bonuses_layout = QGridLayout()
        
        bonuses_layout.addWidget(QLabel("⚽ За гол:"), 0, 0)
        goal_bonus_spin = QSpinBox()
        goal_bonus_spin.setRange(int(self.initial_salary * 0.02), int(self.initial_salary * 0.1))
        goal_bonus_spin.setValue(self.initial_bonuses['goal_bonus'])
        goal_bonus_spin.setSuffix(" $")
        goal_bonus_spin.setSingleStep(50)
        bonuses_layout.addWidget(goal_bonus_spin, 0, 1)
        
        bonuses_layout.addWidget(QLabel("🎯 За передачу:"), 1, 0)
        assist_bonus_spin = QSpinBox()
        assist_bonus_spin.setRange(int(self.initial_salary * 0.02), int(self.initial_salary * 0.1))
        assist_bonus_spin.setValue(self.initial_bonuses['assist_bonus'])
        assist_bonus_spin.setSuffix(" $")
        assist_bonus_spin.setSingleStep(50)
        bonuses_layout.addWidget(assist_bonus_spin, 1, 1)
        
        bonuses_layout.addWidget(QLabel("📊 За матч:"), 2, 0)
        match_bonus_spin = QSpinBox()
        match_bonus_spin.setRange(int(self.initial_salary * 0.02), int(self.initial_salary * 0.1))
        match_bonus_spin.setValue(self.initial_bonuses['match_bonus'])
        match_bonus_spin.setSuffix(" $")
        match_bonus_spin.setSingleStep(25)
        bonuses_layout.addWidget(match_bonus_spin, 2, 1)
        
        bonuses_layout.addWidget(QLabel("🧤 За сухой матч:"), 3, 0)
        clean_sheet_spin = QSpinBox()
        clean_sheet_spin.setRange(int(self.initial_salary * 0.02), int(self.initial_salary * 0.1))
        clean_sheet_spin.setValue(self.initial_bonuses['clean_sheet_bonus'])
        clean_sheet_spin.setSuffix(" $")
        clean_sheet_spin.setSingleStep(50)
        bonuses_layout.addWidget(clean_sheet_spin, 3, 1)
        
        bonuses_group.setLayout(bonuses_layout)
        layout.addWidget(bonuses_group)
        
        # Бонус за лояльность (только при переподписании)
        if self.is_renewal:
            loyalty_group = QGroupBox("💎 Бонус за лояльность (от 0.5 до 3 зарплат)")
            loyalty_layout = QHBoxLayout()
            
            self.loyalty_bonus_spin = QSpinBox()
            min_bonus = int(self.initial_salary * 0.5)
            max_bonus = int(self.initial_salary * 3)
            self.loyalty_bonus_spin.setRange(min_bonus, max_bonus)
            self.loyalty_bonus_spin.setValue(random.randint(min_bonus, max_bonus))
            self.loyalty_bonus_spin.setSuffix(" $")
            self.loyalty_bonus_spin.setSingleStep(500)
            loyalty_layout.addWidget(self.loyalty_bonus_spin)
            
            loyalty_group.setLayout(loyalty_layout)
            layout.addWidget(loyalty_group)
        
        signing_group = QGroupBox("💵 Подъемные (от 1 до 6 зарплат)")
        signing_layout = QHBoxLayout()
        
        signing_bonus_spin = QSpinBox()
        min_signing = int(self.initial_salary * 1)
        max_signing = int(self.initial_salary * 6)
        signing_bonus_spin.setRange(min_signing, max_signing)
        signing_bonus_spin.setValue(random.randint(min_signing, max_signing))
        signing_bonus_spin.setSuffix(" $")
        signing_bonus_spin.setSingleStep(1000)
        signing_layout.addWidget(signing_bonus_spin)
        
        signing_group.setLayout(signing_layout)
        layout.addWidget(signing_group)
        
        duration_group = QGroupBox("📅 Длительность контракта")
        duration_layout = QHBoxLayout()
        
        duration_combo = QComboBox()
        contract_options = [
            ("6 месяцев", 6), ("1 год", 12), ("1.5 года", 18), ("2 года", 24),
            ("2.5 года", 30), ("3 года", 36), ("3.5 года", 42), ("4 года", 48),
            ("4.5 года", 54), ("5 лет", 60)
        ]
        
        for option_text, _ in contract_options:
            duration_combo.addItem(option_text)
        
        duration_layout.addWidget(duration_combo)
        duration_group.setLayout(duration_layout)
        layout.addWidget(duration_group)
        
        self.success_label = QLabel("⚖️ Шанс на успех: 50%")
        self.success_label.setAlignment(Qt.AlignCenter)
        self.success_label.setStyleSheet("color: #FFD700; font-size: 12px;")
        layout.addWidget(self.success_label)
        
        def update_success_chance():
            base_chance = 0.5 + (self.player.overall / 200) + (self.player.career_stats['reputation'] / 200)
            base_chance = min(0.9, base_chance)
            
            salary_ratio = salary_value.value() / self.initial_salary
            
            if salary_ratio <= 1.0:
                salary_factor = 1.0 + (1.0 - salary_ratio) * 0.5
            else:
                salary_factor = 1.0 - (salary_ratio - 1.0) * 0.8
            
            bonus_diff = 0
            bonus_count = 0
            
            if self.initial_bonuses['goal_bonus'] > 0:
                goal_ratio = goal_bonus_spin.value() / self.initial_bonuses['goal_bonus']
                if goal_ratio <= 1.0:
                    bonus_diff += (1.0 - goal_ratio) * 0.3
                else:
                    bonus_diff -= (goal_ratio - 1.0) * 0.5
                bonus_count += 1
            
            if self.initial_bonuses['assist_bonus'] > 0:
                assist_ratio = assist_bonus_spin.value() / self.initial_bonuses['assist_bonus']
                if assist_ratio <= 1.0:
                    bonus_diff += (1.0 - assist_ratio) * 0.3
                else:
                    bonus_diff -= (assist_ratio - 1.0) * 0.5
                bonus_count += 1
            
            if self.initial_bonuses['match_bonus'] > 0:
                match_ratio = match_bonus_spin.value() / self.initial_bonuses['match_bonus']
                if match_ratio <= 1.0:
                    bonus_diff += (1.0 - match_ratio) * 0.2
                else:
                    bonus_diff -= (match_ratio - 1.0) * 0.4
                bonus_count += 1
            
            bonus_factor = 1.0 + (bonus_diff / max(1, bonus_count))
            
            signing_ratio = signing_bonus_spin.value() / self.initial_salary
            if signing_ratio <= 3:
                signing_factor = 1.0 + (3 - signing_ratio) * 0.1
            else:
                signing_factor = 1.0 - (signing_ratio - 3) * 0.15
            
            # Фактор лояльности (при переподписании)
            loyalty_factor = 1.0
            if self.is_renewal:
                loyalty_ratio = self.loyalty_bonus_spin.value() / self.initial_salary
                if loyalty_ratio <= 2:
                    loyalty_factor = 1.0 + (2 - loyalty_ratio) * 0.1
                else:
                    loyalty_factor = 1.0 - (loyalty_ratio - 2) * 0.15
            
            duration_value = contract_options[duration_combo.currentIndex()][1]
            if duration_value >= 36:
                duration_factor = 0.95
            elif duration_value <= 12:
                duration_factor = 1.05
            else:
                duration_factor = 1.0
            
            chance = base_chance * salary_factor * bonus_factor * signing_factor * loyalty_factor * duration_factor
            chance = max(0.1, min(0.95, chance))
            
            self.success_label.setText(f"⚖️ Шанс на успех: {int(chance * 100)}%")
            self.negotiation_chance = chance
        
        salary_value.valueChanged.connect(update_success_chance)
        goal_bonus_spin.valueChanged.connect(update_success_chance)
        assist_bonus_spin.valueChanged.connect(update_success_chance)
        match_bonus_spin.valueChanged.connect(update_success_chance)
        clean_sheet_spin.valueChanged.connect(update_success_chance)
        signing_bonus_spin.valueChanged.connect(update_success_chance)
        if self.is_renewal:
            self.loyalty_bonus_spin.valueChanged.connect(update_success_chance)
        duration_combo.currentIndexChanged.connect(update_success_chance)
        
        update_success_chance()
        
        buttons_layout = QHBoxLayout()
        
        negotiate_btn = QPushButton("🤝 Начать переговоры")
        
        if self.is_renewal:
            negotiate_btn.clicked.connect(lambda: self.finish_negotiation(
                salary_value.value(),
                goal_bonus_spin.value(),
                assist_bonus_spin.value(),
                match_bonus_spin.value(),
                clean_sheet_spin.value(),
                signing_bonus_spin.value(),
                self.loyalty_bonus_spin.value(),
                self.increase_pct_spin.value(),
                contract_options[duration_combo.currentIndex()][1]
            ))
        else:
            negotiate_btn.clicked.connect(lambda: self.finish_negotiation(
                salary_value.value(),
                goal_bonus_spin.value(),
                assist_bonus_spin.value(),
                match_bonus_spin.value(),
                clean_sheet_spin.value(),
                signing_bonus_spin.value(),
                0,
                self.increase_pct_spin.value(),
                contract_options[duration_combo.currentIndex()][1]
            ))
        
        reject_btn = QPushButton("❌ Отказаться")
        reject_btn.clicked.connect(self.reject)
        
        buttons_layout.addWidget(negotiate_btn)
        buttons_layout.addWidget(reject_btn)
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
    
    def finish_negotiation(self, salary, goal_bonus, assist_bonus, match_bonus, clean_sheet_bonus, signing_bonus, loyalty_bonus, increase_pct, duration):
        if random.random() < self.negotiation_chance:
            self.final_salary = salary
            self.final_bonuses = {
                'goal_bonus': goal_bonus,
                'assist_bonus': assist_bonus,
                'match_bonus': match_bonus,
                'clean_sheet_bonus': clean_sheet_bonus
            }
            self.final_duration = duration
            self.final_signing_bonus = signing_bonus
            self.final_loyalty_bonus = loyalty_bonus
            self.final_salary_increase_pct = increase_pct
            self.negotiation_success = True
            self.accept()
        else:
            QMessageBox.warning(self, "Переговоры провалены", 
                              "Клуб не согласился на ваши условия. Попробуйте снова с другими параметрами.")

class FootballCareerSimulator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.player = None
        self.current_date = QDate(2024, 1, 1)
        self.weeks_passed = 0
        self.transfer_offers = []
        self.clubs = []
        self.current_season = "2024"
        self.season_start_date = QDate(2024, 8, 1)
        self.in_national_tournament = False
        self.national_tournament_name = ""
        self.init_clubs()
        self.initUI()
        
    def init_clubs(self):
        """Инициализация базы клубов"""
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
            Club("Академия Пушкаша", "Венгрия", 3, "НБ I", 65),
            Club("Шериф", "Молдова", 3, "Дивизия Националь", 65),
        ]
        
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
        
        # Любительские клубы
        amateur_clubs = [
            Club("Локомотив-Любители", "Россия", 0, "Любительская лига", 30, True),
            Club("Динамо-Любители", "Россия", 0, "Любительская лига", 28, True),
            Club("Спартак-Любители", "Россия", 0, "Любительская лига", 29, True),
            Club("Академия Футбола", "Россия", 0, "Любительская лига", 25, True),
            Club("ФК Любитель", "Россия", 0, "Любительская лига", 22, True),
            Club("Старт", "Россия", 0, "Любительская лига", 24, True),
            Club("Торпедо-Любители", "Россия", 0, "Любительская лига", 26, True),
            Club("Зенит-Любители", "Россия", 0, "Любительская лига", 27, True),
        ]
        
        kosovo_clubs = [
            Club("Дрита", "Косово", 2, "Суперлига Косово", 46),
            Club("Приштина", "Косово", 2, "Суперлига Косово", 45),
        ]
        
        russian_clubs = [
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
        
        self.clubs.extend(top_clubs)
        self.clubs.extend(strong_clubs)
        self.clubs.extend(championship_clubs)
        self.clubs.extend(segunda_clubs)
        self.clubs.extend(zweite_bundesliga_clubs)
        self.clubs.extend(serie_b_clubs)
        self.clubs.extend(medium_european_clubs)
        self.clubs.extend(weak_european_clubs)
        self.clubs.extend(amateur_clubs)
        self.clubs.extend(kosovo_clubs)
        self.clubs.extend(russian_clubs)
        self.clubs.extend(south_america)
        self.clubs.extend(north_america)
        self.clubs.extend(asia)
        self.clubs.extend(africa)
        
        self.init_league_tables()
    
    def init_league_tables(self):
        for club in self.clubs:
            clubs_in_league = len([c for c in self.clubs if c.league == club.league])
            club.league_position = random.randint(1, clubs_in_league)
            club.league_matches = random.randint(10, 30)
            club.league_wins = random.randint(3, club.league_matches - 3)
            club.league_draws = random.randint(1, 8)
            club.league_losses = club.league_matches - club.league_wins - club.league_draws
            club.league_points = club.league_wins * 3 + club.league_draws
            club.league_goals_for = random.randint(20, 60)
            club.league_goals_against = random.randint(15, 50)
            
            # Любительские клубы не участвуют в еврокубках и кубках
            if not club.is_amateur:
                if club.tier >= 4 and random.random() < 0.7:
                    club.champions_league = True
                    club.europe_progress = random.randint(1, 6)
                elif club.tier >= 3 and random.random() < 0.5:
                    club.europa_league = True
                    club.europe_progress = random.randint(1, 6)
                elif club.tier >= 2 and random.random() < 0.3:
                    club.conference_league = True
                    club.europe_progress = random.randint(1, 6)
                
                club.cup_progress = random.randint(0, 8)
    
    def check_trophy_day(self):
        """Проверка - 25 мая, день вручения трофеев"""
        if self.current_date.day() == 25 and self.current_date.month() == 5:
            if self.player and self.player.has_contract and not self.player.contract['club'].is_amateur:
                player_club = None
                for club in self.clubs:
                    if club.name == self.player.career_stats['club']:
                        player_club = club
                        break
                
                if player_club:
                    # Проверка чемпионства в лиге
                    if player_club.league_position == 1:
                        self.win_trophy(f"Чемпион {player_club.league}")
                    
                    # Проверка кубка
                    if player_club.cup_progress == 8:
                        self.win_trophy(f"Кубок {player_club.country}")
                    
                    # Проверка еврокубков
                    if player_club.europe_progress == 7:
                        if player_club.champions_league:
                            self.win_trophy("Лига Чемпионов")
                        elif player_club.europa_league:
                            self.win_trophy("Лига Европы")
                        elif player_club.conference_league:
                            self.win_trophy("Лига Конференций")
    
    def update_satisfaction(self, match_played=False, goals=0, assists=0, clean_sheet=False, yellow_cards=0, red_cards=0):
        if not self.player or not self.player.has_contract:
            return
        
        satisfaction = self.player.career_stats['club_satisfaction']
        
        if match_played:
            satisfaction += 1
            satisfaction += goals * 2
            satisfaction += assists * 2
            if clean_sheet and self.player.position in ['GK', 'CB', 'LB', 'RB', 'CDM']:
                satisfaction += 3
            
            satisfaction -= yellow_cards * 3
            satisfaction -= red_cards * 10
        else:
            if not self.player.injured and self.player.career_stats['matches'] == 0:
                self.player.weeks_without_match += 1
                if self.player.weeks_without_match >= 4:
                    satisfaction -= 5
            else:
                self.player.weeks_without_match = 0
        
        satisfaction = max(0, min(100, satisfaction))
        self.player.career_stats['club_satisfaction'] = satisfaction
    
    def check_contract_extension_opportunity(self):
        if not self.player or not self.player.has_contract:
            return
        
        months_left = self.player.contract['end_date'].daysTo(self.current_date) // 30
        satisfaction = self.player.career_stats['club_satisfaction']
        
        if satisfaction < 60:
            return
        
        if months_left <= 0.25:
            if random.random() < 0.5:
                self.offer_contract_extension()
        elif months_left <= 6:
            if random.random() < 0.33:
                self.offer_contract_extension()
        elif months_left <= 12:
            if random.random() < 0.2:
                self.offer_contract_extension()
        elif months_left <= 24:
            if random.random() < 0.1:
                self.offer_contract_extension()
    
    def offer_contract_extension(self):
        player_club = None
        for club in self.clubs:
            if club.name == self.player.career_stats['club']:
                player_club = club
                break
        
        if not player_club:
            return
        
        self.add_event(f"📨 Клуб {player_club.name} предлагает продлить контракт!")
        
        dialog = ContractExtensionDialog(
            player_club,
            self.player.career_stats['salary'],
            self.player.contract['bonuses'],
            self.player,
            True,
            self
        )
        
        if dialog.exec_() == QDialog.Accepted and dialog.extension_success:
            self.sign_contract(
                player_club,
                dialog.final_salary,
                dialog.final_duration,
                dialog.final_signing_bonus,
                dialog.final_loyalty_bonus,
                dialog.final_salary_increase_pct,
                dialog.final_bonuses,
                True
            )
            self.add_event(f"✅ Контракт с {player_club.name} продлен до {self.player.contract['end_date'].toString('dd.MM.yyyy')}")
            self.update_display()
    
    def check_national_team_call(self):
        if not self.player or not self.player.has_contract:
            return
        
        if self.player.age < 18 or self.player.career_stats['reputation'] < 50:
            return
        
        if self.weeks_passed % 16 != 0:
            return
        
        year = self.current_date.year()
        tournaments = []
        
        if year % 4 == 2:
            tournaments.append("Чемпионат Мира")
        
        if self.player.nationality in ["Испания", "Англия", "Италия", "Германия", "Франция", "Португалия", "Нидерланды", "Бельгия"]:
            if year % 4 == 0:
                tournaments.append("Чемпионат Европы")
        elif self.player.nationality in ["Бразилия", "Аргентина", "Уругвай", "Колумбия", "Чили"]:
            if year % 4 == 1:
                tournaments.append("Кубок Америки")
        elif self.player.nationality in ["Египет", "Марокко", "ЮАР", "Тунис", "Алжир"]:
            if year % 2 == 1:
                tournaments.append("Кубок Африки")
        
        if tournaments and random.random() < 0.3:
            tournament = random.choice(tournaments)
            self.call_to_national_team(tournament)
    
    def call_to_national_team(self, tournament_name):
        dialog = NationalTeamCallDialog(tournament_name, self)
        
        if dialog.exec_() == QDialog.Accepted and dialog.accepted:
            self.in_national_tournament = True
            self.national_tournament_name = tournament_name
            self.add_event(f"🇺🇳 Вы вызваны в сборную {self.player.nationality} для участия в {tournament_name}!")
            self.play_national_tournament(tournament_name)
    
    def play_national_tournament(self, tournament_name):
        matches = random.randint(3, 7)
        goals = 0
        assists = 0
        yellow_cards = 0
        red_cards = 0
        wins = 0
        
        for _ in range(matches):
            performance = random.randint(50, 100) + self.player.overall
            
            if performance > 150:
                match_goals = random.randint(1, 3)
                match_assists = random.randint(0, 2)
            elif performance > 120:
                match_goals = random.randint(0, 2)
                match_assists = random.randint(0, 1)
            else:
                match_goals = random.randint(0, 1)
                match_assists = 0
            
            goals += match_goals
            assists += match_assists
            
            if random.random() < 0.1:
                yellow_cards += 1
            if random.random() < 0.02:
                red_cards += 1
            
            if match_goals > random.randint(0, 2):
                wins += 1
        
        self.player.national_caps += matches
        self.player.national_goals += goals
        self.player.national_assists += assists
        self.player.career_stats['reputation'] = min(100, self.player.career_stats['reputation'] + 5)
        
        self.add_event(f"🇺🇳 Статистика на {tournament_name}: {matches} матчей, {goals} голов, {assists} передач")
        
        if yellow_cards > 0:
            self.add_event(f"🟨 Желтые карточки: {yellow_cards}")
        if red_cards > 0:
            self.add_event(f"🟥 Красные карточки: {red_cards}")
        
        if wins >= matches - 1 or random.random() < 0.3:
            trophy_name = tournament_name
            self.player.national_trophies.append({
                'name': trophy_name,
                'date': self.current_date,
                'season': self.get_current_season()
            })
            self.add_event(f"🏆 ВЫ ВЫИГРАЛИ {tournament_name} СО СБОРНОЙ {self.player.nationality}! Великое достижение!")
            
            bonus = 10000
            self.player.money += bonus
            self.add_event(f"💰 Премия за победу в турнире: +${bonus}")
        
        self.in_national_tournament = False
    
    def show_national_team_stats(self):
        if not self.check_player():
            return
        
        dialog = NationalTeamDialog(self.player, self)
        dialog.exec_()
    
    def update_league_tables(self):
        if not self.player or not self.player.has_contract:
            return
        
        player_club = None
        for club in self.clubs:
            if club.name == self.player.career_stats['club']:
                player_club = club
                break
        
        if not player_club:
            return
        
        if random.random() < 0.3:
            change = random.randint(-2, 2)
            player_club.league_position = max(1, min(20, player_club.league_position + change))
    
    def update_european_competitions(self):
        if not self.player or not self.player.has_contract:
            return
        
        player_club = None
        for club in self.clubs:
            if club.name == self.player.career_stats['club']:
                player_club = club
                break
        
        if not player_club or player_club.is_amateur:
            return
        
        if (player_club.champions_league or player_club.europa_league or player_club.conference_league) and player_club.europe_progress > 0:
            if player_club.europe_progress < 7 and random.random() < 0.2:
                player_club.europe_progress += 1
    
    def update_cup_competition(self):
        if not self.player or not self.player.has_contract:
            return
        
        player_club = None
        for club in self.clubs:
            if club.name == self.player.career_stats['club']:
                player_club = club
                break
        
        if not player_club or player_club.is_amateur:
            return
        
        if player_club.cup_progress > 0 and player_club.cup_progress < 8 and random.random() < 0.25:
            player_club.cup_progress += 1
    
    def win_trophy(self, trophy_name):
        if not self.player:
            return
        
        season = self.get_current_season()
        trophy = {
            'name': trophy_name,
            'club': self.player.career_stats['club'],
            'date': self.current_date,
            'season': season
        }
        self.player.trophies.append(trophy)
        self.add_event(f"🏆 ВЫ ВЫИГРАЛИ {trophy_name}! Поздравляем с трофеем!")
        
        bonus = 5000 * (self.player.career_stats['club_tier'] + 1)
        self.player.money += bonus
        self.add_event(f"💰 Премия за победу: +${bonus}")
    
    def get_current_season(self):
        year = self.current_date.year()
        if self.current_date >= QDate(year, 8, 1):
            return f"{year}-{year+1}"
        else:
            return f"{year-1}-{year}"
    
    def apply_age_penalty(self):
        if not self.player or self.player.age < 33:
            return
        
        penalties = {
            33: 1, 34: 2, 35: 3, 36: 4, 37: 5, 38: 6, 39: 7
        }
        
        penalty = penalties.get(self.player.age, 0)
        if penalty > 0:
            old_overall = self.player.overall
            for stat in self.player.stats:
                self.player.stats[stat] = max(1, self.player.stats[stat] - penalty)
            self.update_overall()
            self.add_event(f"📉 Возрастной спад: рейтинг упал на {penalty} (был {old_overall}, стал {self.player.overall})")
    
    def generate_bonuses(self, club_tier, salary):
        bonuses = {}
        
        min_bonus = int(salary * 0.02)
        max_bonus = int(salary * 0.1)
        
        bonuses['goal_bonus'] = random.randint(min_bonus, max_bonus)
        bonuses['assist_bonus'] = random.randint(min_bonus, max_bonus)
        bonuses['match_bonus'] = random.randint(min_bonus, max_bonus)
        bonuses['clean_sheet_bonus'] = random.randint(min_bonus, max_bonus)
        
        return bonuses
    
    def sign_contract(self, club, salary, duration_months, signing_bonus, loyalty_bonus, salary_increase_pct, bonuses=None, is_renewal=False):
        if not self.player:
            return False
        
        if self.player.has_contract and self.player.career_stats['club'] != "Свободный агент":
            for entry in self.player.career_history:
                if entry['club'] == self.player.career_stats['club'] and entry['end'].isNull():
                    entry['end'] = self.current_date
                    entry['matches'] = self.player.career_stats['matches'] - entry.get('start_matches', 0)
                    entry['goals'] = self.player.career_stats['goals'] - entry.get('start_goals', 0)
                    entry['assists'] = self.player.career_stats['assists'] - entry.get('start_assists', 0)
        
        # Обновляем годы в клубе
        if is_renewal:
            self.player.years_in_club += 1
        else:
            self.player.years_in_club = 0
        
        new_entry = {
            'club': club.name,
            'country': club.country,
            'start': self.current_date,
            'end': QDate(),
            'start_matches': self.player.career_stats['matches'],
            'start_goals': self.player.career_stats['goals'],
            'start_assists': self.player.career_stats['assists'],
            'matches': 0,
            'goals': 0,
            'assists': 0
        }
        self.player.career_history.append(new_entry)
        
        old_club = self.player.career_stats['club']
        old_tier = self.player.career_stats['club_tier']
        
        self.player.career_stats['club'] = club.name
        self.player.career_stats['club_tier'] = club.tier if not club.is_amateur else 0
        self.player.career_stats['salary'] = salary
        self.player.has_contract = True
        self.player.career_stats['club_satisfaction'] = 50
        
        self.player.contract['start_date'] = self.current_date
        self.player.contract['end_date'] = self.current_date.addMonths(duration_months)
        self.player.contract['duration_months'] = duration_months
        self.player.contract['weekly_salary'] = salary
        self.player.contract['signing_bonus'] = signing_bonus
        self.player.contract['loyalty_bonus'] = loyalty_bonus
        self.player.contract['salary_increase_pct'] = salary_increase_pct
        self.player.contract['club'] = club.name
        
        self.player.money += signing_bonus
        if loyalty_bonus > 0:
            self.player.money += loyalty_bonus
            self.add_event(f"💎 Бонус за лояльность: +${loyalty_bonus}")
        
        if bonuses:
            self.player.contract['bonuses'] = bonuses
        else:
            self.player.contract['bonuses'] = self.generate_bonuses(club.tier, salary)
        
        tier_names = {0: "Любительский", 1: "Низший дивизион", 2: "Первая лига", 
                     3: "Высшая лига", 4: "Топ-клуб", 5: "Суперклуб"}
        
        old_tier_name = tier_names.get(old_tier, "Неизвестно")
        new_tier_name = "Любительский клуб" if club.is_amateur else tier_names.get(club.tier, "Неизвестно")
        
        contract_text = f"📝 ПОДПИСАН КОНТРАКТ! {old_club} ({old_tier_name}) → {club.name} ({new_tier_name}, {club.country})"
        self.add_event(contract_text)
        self.add_event(f"💰 Зарплата: ${salary}/неделя | Срок: {duration_months} месяцев")
        self.add_event(f"📈 Повышение зарплаты: {salary_increase_pct}% в год")
        self.add_event(f"💵 Подъемные: +${signing_bonus}")
        
        bonuses_text = f"🎯 Бонусы: ${self.player.contract['bonuses']['goal_bonus']}/гол, ${self.player.contract['bonuses']['assist_bonus']}/пас, ${self.player.contract['bonuses']['match_bonus']}/матч"
        self.add_event(bonuses_text)
        
        self.transfer_offers = []
        
        return True
    
    def apply_salary_increase(self):
        """Применение повышения зарплаты за год в клубе"""
        if not self.player or not self.player.has_contract:
            return
        
        if self.player.years_in_club > 0:
            increase = self.player.contract['salary_increase_pct'] / 100
            new_salary = int(self.player.career_stats['salary'] * (1 + increase))
            self.player.career_stats['salary'] = new_salary
            self.player.contract['weekly_salary'] = new_salary
            self.add_event(f"📈 Повышение зарплаты за год в клубе: +{self.player.contract['salary_increase_pct']}% (теперь ${new_salary}/неделя)")
    
    def request_contract_extension(self):
        if not self.check_player():
            return
        
        if not self.player.has_contract:
            QMessageBox.warning(self, "Внимание", "У вас нет активного контракта для продления!")
            return
        
        player_club = None
        for club in self.clubs:
            if club.name == self.player.career_stats['club']:
                player_club = club
                break
        
        if not player_club:
            return
        
        if random.random() < 0.7:
            dialog = ContractExtensionDialog(
                player_club,
                self.player.career_stats['salary'],
                self.player.contract['bonuses'],
                self.player,
                False,
                self
            )
            
            if dialog.exec_() == QDialog.Accepted and dialog.extension_success:
                self.sign_contract(
                    player_club,
                    dialog.final_salary,
                    dialog.final_duration,
                    dialog.final_signing_bonus,
                    dialog.final_loyalty_bonus,
                    dialog.final_salary_increase_pct,
                    dialog.final_bonuses,
                    True
                )
                self.add_event(f"✅ Контракт с {player_club.name} продлен до {self.player.contract['end_date'].toString('dd.MM.yyyy')}")
                self.update_display()
        else:
            QMessageBox.information(self, "Отказ", "Клуб отказался обсуждать продление контракта.")
    
    def process_weekly_expenses(self):
        if not self.player:
            return
        
        if self.player.age < 18:
            return
        
        if self.player.has_contract and self.player.career_stats['club'] != "Свободный агент":
            current_club = None
            for club in self.clubs:
                if club.name == self.player.career_stats['club']:
                    current_club = club
                    break
            
            country_costs = {
                "Швейцария": 200, "Норвегия": 188, "Дания": 175, "Исландия": 175,
                "Великобритания": 150, "Англия": 150, "Франция": 138, "Германия": 138,
                "Нидерланды": 138, "Бельгия": 125, "Австрия": 125, "Ирландия": 125,
                "Финляндия": 125, "Швеция": 125, "Италия": 113, "Испания": 113,
                "США": 150, "Канада": 138, "Япония": 125, "Южная Корея": 100,
                "Китай": 88, "Россия": 75, "Украина": 63, "Беларусь": 38,
                "Казахстан": 38, "Азербайджан": 38, "Грузия": 38, "Армения": 30,
                "Турция": 75, "Саудовская Аравия": 100, "ОАЭ": 113, "Катар": 113,
                "Бразилия": 75, "Аргентина": 63, "Мексика": 75, "Египет": 38,
                "Марокко": 38, "ЮАР": 50,
            }
            
            base_cost = 50
            if current_club and current_club.country in country_costs:
                base_cost = country_costs[current_club.country]
            
            if self.player.career_stats['club_tier'] >= 4:
                base_cost += 50
            elif self.player.career_stats['club_tier'] >= 2:
                base_cost += 25
        else:
            base_cost = 30
        
        expenses = base_cost
        
        if random.random() < 0.1:
            unexpected_expenses = [
                ("💊 Лечение зубов", random.randint(125, 500)),
                ("🚗 Ремонт автомобиля", random.randint(75, 375)),
                ("🏥 Медицинская страховка", random.randint(100, 300)),
                ("📱 Новый телефон", random.randint(125, 250)),
                ("👔 Покупка одежды", random.randint(50, 200)),
                ("🎁 Подарок родственникам", random.randint(25, 125)),
                ("🏠 Ремонт в квартире", random.randint(125, 750)),
                ("📚 Курсы/обучение", random.randint(75, 250)),
                ("✈️ Поездка домой", random.randint(100, 375)),
                ("💻 Новый компьютер", random.randint(200, 500)),
            ]
            
            expense_name, expense_amount = random.choice(unexpected_expenses)
            expenses += expense_amount
            self.add_event(f"💰 Непредвиденные расходы: {expense_name} -${expense_amount}")
        
        self.player.money -= expenses
        
        if self.player.money <= 0:
            self.add_event(f"💔 БАНКРОТСТВО! Деньги закончились (-${abs(self.player.money)})")
            self.game_over()
            return
        
        status = " (свободный агент)" if not self.player.has_contract else ""
        self.add_event(f"💸 Еженедельные расходы{status}: -${expenses} (${self.player.money} осталось)")
    
    def receive_salary(self):
        if not self.player or not self.player.has_contract:
            return
        
        salary = self.player.career_stats['salary']
        self.player.money += salary
        self.add_event(f"💰 Получена зарплата: +${salary}")
    
    def pay_bonus(self, bonus_type, amount):
        if not self.player or not self.player.has_contract:
            return
        
        bonus = self.player.contract['bonuses'].get(bonus_type, 0) * amount
        if bonus > 0:
            self.player.money += bonus
            bonus_names = {
                'goal_bonus': 'за голы',
                'assist_bonus': 'за передачи',
                'match_bonus': 'за матчи',
                'clean_sheet_bonus': 'за сухие матчи'
            }
            self.add_event(f"💰 Бонус {bonus_names.get(bonus_type, '')}: +${bonus}")
    
    def check_retirement(self):
        if not self.player:
            return False
        
        if self.player.age >= 40:
            reply = QMessageBox.question(self, "👴 ЗАВЕРШЕНИЕ КАРЬЕРЫ", 
                                        f"Вам исполнилось 40 лет! Пришло время завершить карьеру.\n\n"
                                        f"Итоговая статистика карьеры:\n"
                                        f"📊 Сыграно недель: {self.weeks_passed}\n"
                                        f"⚽ Матчей: {self.player.career_stats['matches']}\n"
                                        f"🎯 Голов: {self.player.career_stats['goals']}\n"
                                        f"📤 Передач: {self.player.career_stats['assists']}\n"
                                        f"🟨 Желтых карточек: {self.player.career_stats['yellow_cards']}\n"
                                        f"🟥 Красных карточек: {self.player.career_stats['red_cards']}\n"
                                        f"🇺🇳 Матчей за сборную: {self.player.national_caps}\n"
                                        f"🇺🇳 Голов за сборную: {self.player.national_goals}\n"
                                        f"💰 Итоговый капитал: ${self.player.money}\n"
                                        f"🏆 Трофеев: {len(self.player.trophies)}\n"
                                        f"📜 Клубов в истории: {len(self.player.career_history)}\n\n"
                                        f"Начать новую игру?",
                                        QMessageBox.Yes | QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                self.player = None
                self.current_date = QDate(2024, 1, 1)
                self.weeks_passed = 0
                self.transfer_offers = []
                self.show_create_player_dialog()
            else:
                self.close()
            return True
        return False
    
    def game_over(self):
        reply = QMessageBox.question(self, "💔 ИГРА ОКОНЧЕНА", 
                                    f"Вы обанкротились! Денег больше нет.\n\n"
                                    f"Статистика карьеры:\n"
                                    f"📊 Сыграно недель: {self.weeks_passed}\n"
                                    f"⚽ Матчей: {self.player.career_stats['matches']}\n"
                                    f"🎯 Голов: {self.player.career_stats['goals']}\n"
                                    f"📤 Передач: {self.player.career_stats['assists']}\n\n"
                                    f"Начать новую игру?",
                                    QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.player = None
            self.current_date = QDate(2024, 1, 1)
            self.weeks_passed = 0
            self.transfer_offers = []
            self.show_create_player_dialog()
        else:
            self.close()
    
    def show_career_history(self):
        if not self.check_player():
            return
        
        dialog = CareerHistoryDialog(self.player, self)
        dialog.exec_()
    
    def show_trophies(self):
        if not self.check_player():
            return
        
        dialog = TrophiesDialog(self.player, self)
        dialog.exec_()
    
    def show_club_info(self):
        if not self.check_player() or not self.player.has_contract:
            QMessageBox.warning(self, "Внимание", "У вас нет контракта с клубом!")
            return
        
        player_club = None
        for club in self.clubs:
            if club.name == self.player.career_stats['club']:
                player_club = club
                break
        
        if player_club:
            dialog = ClubInfoDialog(player_club, self.player, self)
            dialog.exec_()
    
    def check_contract_expiry(self):
        if not self.player or not self.player.has_contract:
            return
        
        if self.current_date >= self.player.contract['end_date']:
            self.player.has_contract = False
            self.player.career_stats['club'] = 'Свободный агент'
            self.player.career_stats['salary'] = 0
            self.player.career_stats['club_tier'] = 0
            self.add_event("⚠️ Контракт истек! Вы стали свободным агентом")
    
    def check_birthday(self):
        if not self.player:
            return
        
        current_year = self.current_date.year()
        birthday_this_year = QDate(current_year, self.player.birth_month, self.player.birth_day)
        
        if self.current_date >= birthday_this_year and self.player.last_birthday_year < current_year:
            self.player.age += 1
            self.player.last_birthday_year = current_year
            
            # Применяем повышение зарплаты за год в клубе
            if self.player.has_contract:
                self.apply_salary_increase()
            
            birthday_gift = random.randint(500, 2000)
            self.player.money += birthday_gift
            self.add_event(f"🎉🎂 С ДНЕМ РОЖДЕНИЯ! {self.player.name} исполнилось {self.player.age} лет! Получен подарок ${birthday_gift}! 🎂🎉")
            
            if self.player.age == 18:
                self.add_event("🎉 ТЕПЕРЬ ВЫ СОВЕРШЕННОЛЕТНИЙ! У вас появятся расходы")
            
            self.apply_age_penalty()
            self.check_retirement()
    
    def check_milestones(self, stat_type, current_value):
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
                if milestone >= 100:
                    message = "⭐ " + message + " ⭐"
                self.add_event(message)
                
                if self.player.has_contract:
                    bonus = milestone * 50
                    self.player.money += bonus
                    self.add_event(f"💰 Премия за достижение: +${bonus}")
    
    def generate_transfer_offers(self):
        if not self.player:
            return
        
        if random.random() < 0.05:
            available_clubs = self.get_available_clubs()
            
            if available_clubs:
                if self.player.has_contract:
                    available_clubs = [c for c in available_clubs if c.name != self.player.career_stats['club']]
                
                if available_clubs:
                    num_offers = random.randint(1, 2)
                    for _ in range(min(num_offers, len(available_clubs))):
                        club = random.choice(available_clubs)
                        available_clubs.remove(club)
                        
                        # Для любительских клубов базовая зарплата минимальная
                        if club.is_amateur:
                            salary = 50
                        else:
                            base_salary = 100
                            tier_multipliers = {0: 1, 1: 5, 2: 20, 3: 50, 4: 200, 5: 500}
                            salary_multiplier = tier_multipliers.get(club.tier, 1)
                            salary = int(base_salary * salary_multiplier * (self.player.overall / 50) * random.uniform(0.7, 1.5))
                            salary = max(50, min(500000, salary))
                        
                        contract_options = [6, 12, 18, 24, 30, 36, 42, 48, 54, 60]
                        contract_months = random.choice(contract_options)
                        
                        signing_bonus = int(salary * random.randint(1, 6))
                        loyalty_bonus = 0
                        salary_increase_pct = random.randint(1, 20)
                        bonuses = self.generate_bonuses(club.tier, salary)
                        
                        offer = TransferOffer(club, salary, contract_months, signing_bonus, loyalty_bonus, salary_increase_pct, bonuses)
                        self.transfer_offers.append(offer)
                        
                        club_type = " (Любительский)" if club.is_amateur else ""
                        self.add_event(f"📨 Поступило предложение от {club.name}{club_type}! Зарплата: ${salary}/неделя, подъемные: ${signing_bonus}, контракт: {contract_months} мес.")
    
    def show_transfer_offers(self):
        if not self.player:
            return
        
        if not self.transfer_offers:
            QMessageBox.information(self, "Предложения", "Нет входящих предложений о трансфере.")
            return
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Входящие предложения")
        dialog.setStyleSheet(self.styleSheet())
        dialog.setMinimumWidth(600)
        dialog.setMinimumHeight(500)
        
        layout = QVBoxLayout()
        
        title = QLabel(f"📨 Предложения для {self.player.name}")
        title.setStyleSheet("font-size: 14px; color: #FFD700; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        reject_all_btn = QPushButton("❌ Отказать всем")
        reject_all_btn.clicked.connect(lambda: self.decline_all_offers(dialog))
        reject_all_btn.setStyleSheet("background-color: #8B0000; color: white;")
        layout.addWidget(reject_all_btn)
        
        offers_list = QListWidget()
        offers_list.setMinimumHeight(150)
        
        for i, offer in enumerate(self.transfer_offers):
            club_type = " (Любительский)" if offer.club.is_amateur else ""
            item_text = f"{offer.club.name}{club_type} ({offer.club.country}, {offer.club.league})"
            offers_list.addItem(item_text)
        
        layout.addWidget(offers_list)
        
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        for i, offer in enumerate(self.transfer_offers):
            offer_group = QGroupBox(f"Предложение от {offer.club.name}")
            offer_layout = QVBoxLayout()
            
            info_label = QLabel(f"🏢 Страна: {offer.club.country}\n"
                               f"📊 Лига: {offer.club.league}\n"
                               f"📈 Уровень клуба: {'Любительский' if offer.club.is_amateur else offer.club.tier}\n"
                               f"💰 Зарплата: ${offer.weekly_salary}/неделя\n"
                               f"💵 Подъемные: ${offer.signing_bonus}\n"
                               f"📈 Повышение зарплаты: {offer.salary_increase_pct}% в год\n"
                               f"📅 Контракт: {offer.contract_months} месяцев\n\n"
                               f"🎯 Бонусы:\n"
                               f"   ⚽ Гол: ${offer.bonuses['goal_bonus']}\n"
                               f"   🎯 Передача: ${offer.bonuses['assist_bonus']}\n"
                               f"   📊 Матч: ${offer.bonuses['match_bonus']}\n"
                               f"   🧤 Сухой матч: ${offer.bonuses['clean_sheet_bonus']}")
            info_label.setWordWrap(True)
            info_label.setStyleSheet("font-size: 11px; color: #000000; background-color: #FFFFFF; padding: 5px; border-radius: 3px;")
            offer_layout.addWidget(info_label)
            
            buttons_row = QHBoxLayout()
            
            negotiate_btn = QPushButton("🤝 Вести переговоры")
            negotiate_btn.clicked.connect(lambda checked, o=offer: self.negotiate_transfer(o, dialog))
            
            accept_btn = QPushButton("✅ Принять (без переговоров)")
            accept_btn.clicked.connect(lambda checked, o=offer: self.accept_transfer_offer(o, dialog))
            
            decline_btn = QPushButton("❌ Отклонить")
            decline_btn.clicked.connect(lambda checked, idx=i: self.decline_transfer_offer(idx))
            
            buttons_row.addWidget(negotiate_btn)
            buttons_row.addWidget(accept_btn)
            buttons_row.addWidget(decline_btn)
            
            offer_layout.addLayout(buttons_row)
            offer_group.setLayout(offer_layout)
            scroll_layout.addWidget(offer_group)
        
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)
        
        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def decline_all_offers(self, dialog):
        reply = QMessageBox.question(self, "Подтверждение", 
                                    f"Вы уверены, что хотите отклонить все {len(self.transfer_offers)} предложений?",
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.add_event(f"❌ Отклонены все {len(self.transfer_offers)} предложений")
            self.transfer_offers = []
            dialog.accept()
    
    def negotiate_transfer(self, offer, parent_dialog):
        is_renewal = (offer.club.name == self.player.career_stats['club'])
        
        negotiate_dialog = NegotiationDialog(
            offer.club, 
            offer.weekly_salary, 
            offer.bonuses,
            self.player,
            is_renewal,
            self
        )
        
        if negotiate_dialog.exec_() == QDialog.Accepted and negotiate_dialog.negotiation_success:
            self.sign_contract(
                offer.club,
                negotiate_dialog.final_salary,
                negotiate_dialog.final_duration,
                negotiate_dialog.final_signing_bonus,
                negotiate_dialog.final_loyalty_bonus,
                negotiate_dialog.final_salary_increase_pct,
                negotiate_dialog.final_bonuses,
                is_renewal
            )
            parent_dialog.accept()
            self.update_display()
    
    def accept_transfer_offer(self, offer, dialog):
        is_renewal = (offer.club.name == self.player.career_stats['club'])
        self.sign_contract(offer.club, offer.weekly_salary, offer.contract_months, offer.signing_bonus, offer.loyalty_bonus, offer.salary_increase_pct, offer.bonuses, is_renewal)
        dialog.accept()
        self.update_display()
    
    def decline_transfer_offer(self, index):
        if 0 <= index < len(self.transfer_offers):
            club_name = self.transfer_offers[index].club.name
            del self.transfer_offers[index]
            self.add_event(f"❌ Отклонено предложение от {club_name}")
    
    def get_available_clubs(self):
        if not self.player:
            return []
        
        overall = self.player.overall
        reputation = self.player.career_stats['reputation']
        available_clubs = []
        
        # Любительские клубы доступны всем с 18 лет
        if self.player.age >= 18:
            for club in self.clubs:
                if club.is_amateur:
                    available_clubs.append(club)
        
        # Профессиональные клубы по рейтингу
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
        
        for club in self.clubs:
            if not club.is_amateur and min_tier <= club.tier <= max_tier:
                rep_requirement = club.reputation
                if overall >= rep_requirement - 20:
                    available_clubs.append(club)
        
        return available_clubs
    
    def transfer(self):
        if not self.check_player():
            return
        
        if self.player.age < 18:
            QMessageBox.warning(self, "Внимание", "Вы слишком молоды для самостоятельного поиска клуба! Достигните 18 лет.\n\nНо вы можете получать предложения от клубов.")
            return
        
        if self.player.has_contract and self.current_date < self.player.contract['end_date']:
            weeks_left = self.player.contract['end_date'].daysTo(self.current_date) // 7
            reply = QMessageBox.question(self, "Активный контракт", 
                                        f"У вас действующий контракт до {self.player.contract['end_date'].toString('dd.MM.yyyy')} "
                                        f"(осталось {abs(weeks_left)} недель).\n\n"
                                        "Нарушение контракта приведет к штрафу и потере репутации.\n"
                                        "Продолжить поиск клуба?",
                                        QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.No:
                return
            
            self.player.career_stats['reputation'] = max(0, self.player.career_stats['reputation'] - 20)
            self.player.career_stats['salary'] = int(self.player.career_stats['salary'] * 0.7)
            fine = int(self.player.money * 0.1)
            self.player.money -= fine
            self.add_event(f"⚠️ Нарушение контракта! Репутация снижена, штраф -${fine}")
        
        if self.player.career_stats['energy'] < 20:
            QMessageBox.warning(self, "Внимание", "Недостаточно энергии для переговоров!")
            return
        
        self.player.career_stats['energy'] -= 20
        
        available_clubs = self.get_available_clubs()
        
        if not available_clubs:
            QMessageBox.information(self, "Трансфер", "Нет доступных клубов для трансфера!")
            return
        
        target_club = random.choice(available_clubs)
        
        # Любительские клубы берут всех
        if target_club.is_amateur:
            self.show_contract_offer(target_club)
        else:
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
        if club.is_amateur:
            salary = 50
        else:
            salary = self.calculate_salary(club)
        
        initial_bonuses = self.generate_bonuses(club.tier, salary)
        is_renewal = (club.name == self.player.career_stats['club'])
        
        negotiate_dialog = NegotiationDialog(
            club,
            salary,
            initial_bonuses,
            self.player,
            is_renewal,
            self
        )
        
        if negotiate_dialog.exec_() == QDialog.Accepted and negotiate_dialog.negotiation_success:
            self.sign_contract(
                club,
                negotiate_dialog.final_salary,
                negotiate_dialog.final_duration,
                negotiate_dialog.final_signing_bonus,
                negotiate_dialog.final_loyalty_bonus,
                negotiate_dialog.final_salary_increase_pct,
                negotiate_dialog.final_bonuses,
                is_renewal
            )
            self.update_display()
    
    def calculate_salary(self, club):
        if club.is_amateur:
            return 50
        
        base_salary = 100
        tier_multipliers = {0: 1, 1: 5, 2: 20, 3: 50, 4: 200, 5: 500}
        salary_multiplier = tier_multipliers.get(club.tier, 1)
        
        salary = int(base_salary * salary_multiplier * (self.player.overall / 50) * random.uniform(0.7, 1.5))
        salary = max(50, min(500000, salary))
        
        return salary
    
    def get_position_multipliers(self, position):
        position_stats = {
            'CF': {'goals': (0.6, 1.0), 'assists': (0.2, 0.5)},
            'ST': {'goals': (0.5, 0.9), 'assists': (0.2, 0.5)},
            'LW': {'goals': (0.4, 0.7), 'assists': (0.3, 0.6)},
            'RW': {'goals': (0.4, 0.7), 'assists': (0.3, 0.6)},
            'CAM': {'goals': (0.2, 0.5), 'assists': (0.4, 0.8)},
            'CM': {'goals': (0.1, 0.3), 'assists': (0.3, 0.6)},
            'CDM': {'goals': (0.05, 0.15), 'assists': (0.15, 0.4)},
            'CB': {'goals': (0.02, 0.08), 'assists': (0.02, 0.08)},
            'LB': {'goals': (0.03, 0.1), 'assists': (0.05, 0.2)},
            'RB': {'goals': (0.03, 0.1), 'assists': (0.05, 0.2)},
            'GK': {'goals': (0, 0.005), 'assists': (0, 0.005)}
        }
        return position_stats.get(position, {'goals': (0.15, 0.4), 'assists': (0.15, 0.4)})
    
    def show_stats(self):
        if not self.check_player():
            return
        
        tier_names = {0: "Свободный агент", 1: "Низший дивизион", 2: "Первая лига", 
                     3: "Высшая лига", 4: "Топ-клуб", 5: "Суперклуб"}
        
        current_tier = tier_names.get(self.player.career_stats['club_tier'], "Неизвестно")
        
        if self.player.has_contract:
            weeks_left = self.player.contract['end_date'].daysTo(self.current_date) // 7
            if weeks_left > 0:
                contract_status = f"Действует до {self.player.contract['end_date'].toString('dd.MM.yyyy')} (осталось {abs(weeks_left)} недель)"
            else:
                contract_status = f"ИСТЕК {self.player.contract['end_date'].toString('dd.MM.yyyy')}"
            
            bonuses_info = (f"⚽ Бонус за гол: ${self.player.contract['bonuses']['goal_bonus']}\n"
                           f"🎯 Бонус за передачу: ${self.player.contract['bonuses']['assist_bonus']}\n"
                           f"📊 Бонус за матч: ${self.player.contract['bonuses']['match_bonus']}\n"
                           f"🧤 Бонус за сухой матч: ${self.player.contract['bonuses']['clean_sheet_bonus']}")
        else:
            contract_status = "НЕТ КОНТРАКТА (свободный агент)"
            bonuses_info = "Нет бонусов (нет контракта)"
        
        earned_bonuses = ""
        if self.player.has_contract and self.player.career_stats['matches'] > 0:
            earned_bonuses = (f"\n\nЗаработано бонусов:\n"
                             f"💰 За матчи: ${self.player.career_stats['matches'] * self.player.contract['bonuses']['match_bonus']}\n"
                             f"💰 За голы: ${self.player.career_stats['goals'] * self.player.contract['bonuses']['goal_bonus']}\n"
                             f"💰 За передачи: ${self.player.career_stats['assists'] * self.player.contract['bonuses']['assist_bonus']}")
        
        goals_per_match = self.player.career_stats['goals'] / max(1, self.player.career_stats['matches'])
        assists_per_match = self.player.career_stats['assists'] / max(1, self.player.career_stats['matches'])
        
        stats_text = f"""
        Детальная статистика игрока {self.player.name}:
        
        Финансы:
        - 💰 Баланс: ${self.player.money}
        
        Общая информация:
        - 🏳️ Национальность: {self.player.nationality}
        - Возраст: {self.player.age} {'(нет расходов до 18)' if self.player.age < 18 else ''}
        - Позиция: {self.player.position}
        - Общий рейтинг: {self.player.overall}
        - Клуб: {self.player.career_stats['club']} ({current_tier})
        - Зарплата: ${self.player.career_stats['salary'] if self.player.has_contract else 0}/неделя
        - Повышение зарплаты: {self.player.contract['salary_increase_pct'] if self.player.has_contract else 0}% в год
        - Лет в клубе: {self.player.years_in_club}
        - Репутация: {self.player.career_stats['reputation']}/100
        - Удовлетворенность клуба: {self.player.career_stats['club_satisfaction']}/100
        - Статус: {'✅ Есть контракт' if self.player.has_contract else '⚠️ Свободный агент'}
        
        Контракт:
        - {contract_status}
        - 💵 Подъемные при подписании: ${self.player.contract['signing_bonus'] if self.player.has_contract else 0}
        - 💎 Бонус за лояльность: ${self.player.contract['loyalty_bonus'] if self.player.has_contract else 0}
        
        Бонусы по контракту:
        {bonuses_info}
        {earned_bonuses}
        
        Карьерная статистика:
        - Матчи: {self.player.career_stats['matches']}
        - Голы: {self.player.career_stats['goals']} (в среднем {goals_per_match:.2f} за матч)
        - Передачи: {self.player.career_stats['assists']} (в среднем {assists_per_match:.2f} за матч)
        - Желтые карточки: {self.player.career_stats['yellow_cards']}
        - Красные карточки: {self.player.career_stats['red_cards']}
        - Сухие матчи: {self.player.career_stats['clean_sheets']}
        - Г+П за матч: {(self.player.career_stats['goals'] + self.player.career_stats['assists']) / max(1, self.player.career_stats['matches']):.2f}
        
        Сборная {self.player.nationality}:
        - 🇺🇳 Матчи: {self.player.national_caps}
        - ⚽ Голы: {self.player.national_goals}
        - 🎯 Передачи: {self.player.national_assists}
        - 📈 Г+П за матч: {(self.player.national_goals + self.player.national_assists) / max(1, self.player.national_caps):.2f}
        - 🏆 Трофеи: {len(self.player.national_trophies)}
        
        Юбилеи:
        - Сыграно юбилейных матчей: {sum(1 for m, achieved in self.player.milestones['matches'].items() if achieved)} из {len(self.player.milestones['matches'])}
        - Юбилейных голов: {sum(1 for m, achieved in self.player.milestones['goals'].items() if achieved)} из {len(self.player.milestones['goals'])}
        - Юбилейных передач: {sum(1 for m, achieved in self.player.milestones['assists'].items() if achieved)} из {len(self.player.milestones['assists'])}
        
        Трофеи: {len(self.player.trophies)} клубных + {len(self.player.national_trophies)} со сборной
        Клубы в истории: {len(self.player.career_history)}
        
        Доступно клубов для трансфера: {len(self.get_available_clubs())}
        Входящих предложений: {len(self.transfer_offers)}
        """
        
        QMessageBox.information(self, "Статистика карьеры", stats_text)
    
    def initUI(self):
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
            QTableWidget {
                background-color: #16213e;
                color: white;
                border: 2px solid #0f3460;
                border-radius: 5px;
            }
            QTableWidget::item {
                color: white;
            }
            QHeaderView::section {
                background-color: #0f3460;
                color: white;
                padding: 5px;
                border: 1px solid #1a1a2e;
            }
            QSlider::groove:horizontal {
                height: 6px;
                background: #16213e;
                border: 1px solid #0f3460;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #FFD700;
                border: 1px solid #0f3460;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
            QSlider::sub-page:horizontal {
                background: #4CAF50;
                border: 1px solid #0f3460;
                border-radius: 3px;
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
        left_panel = QGroupBox("ИНФОРМАЦИЯ ОБ ИГРОКЕ")
        left_layout = QVBoxLayout()
        
        self.player_name_label = QLabel("Имя: Не создан")
        self.player_name_label.setObjectName("value_label")
        
        self.player_nationality_label = QLabel("🏳️ Национальность: -")
        self.player_nationality_label.setObjectName("value_label")
        
        self.player_age_label = QLabel("📅 Возраст: -")
        self.player_age_label.setObjectName("value_label")
        
        self.player_position_label = QLabel("📍 Позиция: -")
        self.player_position_label.setObjectName("value_label")
        
        self.player_overall_label = QLabel("⭐ Общий рейтинг: -")
        self.player_overall_label.setObjectName("value_label")
        
        self.player_club_label = QLabel("🏢 Клуб: -")
        self.player_club_label.setObjectName("value_label")
        
        self.player_money_label = QLabel("💰 Деньги: $0")
        self.player_money_label.setStyleSheet("color: #4CAF50; font-size: 14px; font-weight: bold;")
        
        self.player_salary_label = QLabel("💰 Зарплата: -")
        self.player_salary_label.setObjectName("value_label")
        
        self.player_increase_label = QLabel("📈 Повышение: -")
        self.player_increase_label.setObjectName("value_label")
        
        self.player_years_label = QLabel("📅 Лет в клубе: -")
        self.player_years_label.setObjectName("value_label")
        
        self.player_reputation_label = QLabel("📊 Репутация: -")
        self.player_reputation_label.setObjectName("value_label")
        
        self.player_satisfaction_label = QLabel("😊 Удовлетворенность клуба: -")
        self.player_satisfaction_label.setObjectName("value_label")
        
        self.player_contract_label = QLabel("📝 Контракт: -")
        self.player_contract_label.setObjectName("value_label")
        
        self.bonuses_label = QLabel("🎯 Бонусы: нет контракта")
        self.bonuses_label.setObjectName("value_label")
        self.bonuses_label.setWordWrap(True)
        
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
        left_layout.addWidget(self.player_nationality_label)
        left_layout.addWidget(self.player_age_label)
        left_layout.addWidget(self.player_position_label)
        left_layout.addWidget(self.player_overall_label)
        left_layout.addWidget(self.player_club_label)
        left_layout.addWidget(self.player_money_label)
        left_layout.addWidget(self.player_salary_label)
        left_layout.addWidget(self.player_increase_label)
        left_layout.addWidget(self.player_years_label)
        left_layout.addWidget(self.player_reputation_label)
        left_layout.addWidget(self.player_satisfaction_label)
        left_layout.addWidget(self.player_contract_label)
        left_layout.addWidget(self.bonuses_label)
        left_layout.addLayout(energy_layout)
        left_layout.addWidget(stats_group)
        left_layout.addStretch()
        
        left_panel.setLayout(left_layout)
        return left_panel
    
    def create_center_panel(self):
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
            ('yellow_cards', ('🟨 ЖК:', '0')),
            ('red_cards', ('🟥 КК:', '0')),
            ('trophies', ('🏆 Трофеи:', '0')),
            ('injury', ('⚠️ Травмы:', 'Нет')),
            ('history', ('📜 Клубов в истории:', '0'))
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
        right_panel = QGroupBox("ДЕЙСТВИЯ")
        right_layout = QVBoxLayout()
        
        buttons_info = [
            ("🏋️ Тренировка", self.train, "Улучшает характеристики, тратит энергию"),
            ("⚽ Матч", self.play_match, "Сыграть матч, можно забить гол"),
            ("😴 Отдых", self.rest, "Восстановить энергию"),
            ("🔄 Искать клуб", self.transfer, "Активный поиск нового клуба"),
            ("📨 Предложения", self.show_transfer_offers, "Просмотр входящих предложений"),
            ("📝 Продлить контракт", self.request_contract_extension, "Попросить клуб о продлении"),
            ("📜 История карьеры", self.show_career_history, "История клубов"),
            ("🏆 Трофеи", self.show_trophies, "Выигранные трофеи"),
            ("🏢 Информация о клубе", self.show_club_info, "Турнирная таблица и еврокубки"),
            ("🇺🇳 Сборная", self.show_national_team_stats, "Статистика в национальной сборной"),
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
        dialog = QDialog(self)
        dialog.setWindowTitle("Создание игрока")
        dialog.setStyleSheet(self.styleSheet())
        dialog.setModal(True)
        dialog.setMinimumWidth(450)
        
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
        
        nationality_layout = QHBoxLayout()
        nationality_label = QLabel("Национальность:")
        nationality_label.setObjectName("title_label")
        nationality_layout.addWidget(nationality_label)
        
        nationality_combo = QComboBox()
        nationalities = [
            "Россия", "Беларусь", "Казахстан", "Украина", "Испания", "Англия", 
            "Италия", "Германия", "Франция", "Нидерланды", "Португалия", "Бельгия",
            "Бразилия", "Аргентина", "Уругвай", "США", "Япония", "Египет", "Марокко"
        ]
        nationality_combo.addItems(nationalities)
        nationality_layout.addWidget(nationality_combo)
        layout.addLayout(nationality_layout)
        
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
        age_spin.setRange(14, 39)
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
        
        money_label = QLabel("Начальные деньги:")
        money_label.setObjectName("title_label")
        params_layout.addWidget(money_label, 2, 0)
        
        money_spin = QSpinBox()
        money_spin.setRange(0, 1000000)
        money_spin.setValue(10000)
        money_spin.setSuffix(" $")
        money_spin.setSingleStep(1000)
        params_layout.addWidget(money_spin, 2, 1)
        
        params_group.setLayout(params_layout)
        layout.addWidget(params_group)
        
        info_label = QLabel("ℹ️ До 18 лет нет расходов. Игра заканчивается в 40 лет.\n"
                           "С 33 лет рейтинг начинает падать.\n"
                           "Вызовы в сборную возможны с 18 лет при репутации > 50.\n"
                           "Любительские клубы доступны всем с 18 лет, но не дают трофеев.")
        info_label.setStyleSheet("color: #FFD700; font-size: 11px; padding: 5px;")
        info_label.setWordWrap(True)
        info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_label)
        
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
            
            nationality = nationality_combo.currentText()
            self.player = Player(name, nationality)
            self.player.age = age_spin.value()
            self.player.overall = overall_spin.value()
            self.player.position = position_combo.currentText()
            self.player.money = money_spin.value()
            self.player.has_contract = False
            self.player.career_stats['club'] = 'Свободный агент'
            self.player.career_stats['salary'] = 0
            self.player.career_stats['club_tier'] = 0
            self.player.career_stats['club_satisfaction'] = 50
            self.player.years_in_club = 0
            
            base_stats = overall_spin.value()
            for stat in self.player.stats:
                self.player.stats[stat] = min(99, max(1, base_stats + random.randint(-5, 5)))
            
            self.player.birth_day = 7
            self.player.birth_month = 12
            self.player.last_birthday_year = self.current_date.year()
            
            self.player.milestones = {
                'matches': {1: False, 5: False, 10: False, 50: False, 100: False, 200: False, 300: False},
                'goals': {1: False, 5: False, 10: False, 50: False, 100: False, 200: False, 300: False},
                'assists': {1: False, 5: False, 10: False, 50: False, 100: False, 200: False, 300: False},
                'national_caps': {1: False, 5: False, 10: False, 25: False, 50: False, 100: False}
            }
            
            self.update_display()
            self.add_event(f"✨ Игрок {name} создан! Добро пожаловать в мир футбола!")
            self.add_event(f"🏳️ Национальность: {nationality}")
            self.add_event(f"🏁 Статус: Свободный агент")
            self.add_event(f"💰 Начальный капитал: ${self.player.money}")
            if self.player.age < 18:
                self.add_event(f"📅 До 18 лет нет расходов")
            dialog.accept()
        
        create_btn.clicked.connect(create_player)
        cancel_btn.clicked.connect(dialog.reject)
        
        buttons_layout.addWidget(create_btn)
        buttons_layout.addWidget(cancel_btn)
        layout.addLayout(buttons_layout)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def train(self):
        if not self.check_player():
            return
        
        if self.player.career_stats['energy'] < 20:
            QMessageBox.warning(self, "Внимание", "Недостаточно энергии для тренировки!")
            return
        
        self.player.career_stats['energy'] -= 20
        
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
        if not self.check_player():
            return
        
        if not self.player.has_contract or self.player.career_stats['club'] == "Свободный агент":
            QMessageBox.warning(self, "Внимание", "Вы не можете играть матчи без контракта! Сначала подпишите контракт с клубом.")
            return
        
        if self.player.career_stats['energy'] < 30:
            QMessageBox.warning(self, "Внимание", "Недостаточно энергии для матча!")
            return
        
        if self.player.injured:
            QMessageBox.warning(self, "Внимание", "Игрок травмирован! Невозможно сыграть матч.")
            return
        
        self.player.career_stats['energy'] -= 30
        
        multipliers = self.get_position_multipliers(self.player.position)
        performance = random.randint(50, 100) + self.player.overall
        
        goals = 0
        assists = 0
        yellow_cards = 0
        red_cards = 0
        
        if performance > 175:
            goals = random.randint(4, 7)
            assists = random.randint(2, 5)
            result = "ЛЕГЕНДАРНО! 👑🔥"
        elif performance > 160:
            goals = random.randint(2, 5)
            assists = random.randint(1, 4)
            result = "ФЕНОМЕНАЛЬНО! 🔥"
        elif performance > 145:
            goals = random.randint(1, 3)
            assists = random.randint(0, 2)
            result = "ОТЛИЧНО ⭐"
        elif performance > 125:
            goals = random.randint(0, 2)
            assists = random.randint(0, 2)
            result = "ХОРОШО 👍"
        elif performance > 105:
            goals = random.randint(0, 1)
            assists = random.randint(0, 1)
            result = "НОРМАЛЬНО 📊"
        elif performance > 90:
            goals = 0
            assists = random.randint(0, 1)
            result = "ТАК СЕБЕ 📉"
        else:
            goals = 0
            assists = 0
            result = "ПЛОХО 👎"
        
        goals = min(7, max(0, int(goals * multipliers['goals'][0] + random.random() * (multipliers['goals'][1] - multipliers['goals'][0]))))
        assists = min(7, max(0, int(assists * multipliers['assists'][0] + random.random() * (multipliers['assists'][1] - multipliers['assists'][0]))))
        
        if random.random() < 0.15:
            yellow_cards = random.randint(1, 2)
            if random.random() < 0.2 and yellow_cards == 2:
                red_cards = 1
                yellow_cards = 0
            self.player.career_stats['yellow_cards'] += yellow_cards
            self.player.career_stats['red_cards'] += red_cards
            if yellow_cards > 0:
                self.add_event(f"🟨 Получена желтая карточка! (всего: {self.player.career_stats['yellow_cards']})")
            if red_cards > 0:
                self.add_event(f"🟥 КРАСНАЯ КАРТОЧКА! Удаление с поля! (всего: {self.player.career_stats['red_cards']})")
        
        team_goals = goals + random.randint(0, 3)
        opponent_goals = random.randint(0, team_goals - 1) if team_goals > 0 else random.randint(0, 2)
        match_score = f"{team_goals}:{opponent_goals}"
        
        clean_sheet = False
        if self.player.position in ['GK', 'CB', 'LB', 'RB', 'CDM'] and opponent_goals == 0:
            clean_sheet = True
            self.player.career_stats['clean_sheets'] += 1
            self.add_event(f"🧤 СУХОЙ МАТЧ! (всего: {self.player.career_stats['clean_sheets']})")
        
        self.player.career_stats['matches'] += 1
        self.player.career_stats['goals'] += goals
        self.player.career_stats['assists'] += assists
        
        player_club = None
        for club in self.clubs:
            if club.name == self.player.career_stats['club']:
                player_club = club
                break
        
        if player_club:
            player_club.league_matches += 1
            player_club.league_goals_for += team_goals
            player_club.league_goals_against += opponent_goals
            
            if team_goals > opponent_goals:
                player_club.league_wins += 1
                player_club.league_points += 3
            elif team_goals == opponent_goals:
                player_club.league_draws += 1
                player_club.league_points += 1
            else:
                player_club.league_losses += 1
            
            if team_goals > opponent_goals and random.random() < 0.3:
                player_club.league_position = max(1, player_club.league_position - random.randint(1, 2))
            elif team_goals < opponent_goals and random.random() < 0.2:
                player_club.league_position = min(20, player_club.league_position + random.randint(1, 2))
        
        self.pay_bonus('goal_bonus', goals)
        self.pay_bonus('assist_bonus', assists)
        self.pay_bonus('match_bonus', 1)
        if clean_sheet:
            self.pay_bonus('clean_sheet_bonus', 1)
        
        self.update_satisfaction(True, goals, assists, clean_sheet, yellow_cards, red_cards)
        
        self.check_milestones('matches', self.player.career_stats['matches'])
        self.check_milestones('goals', self.player.career_stats['goals'])
        self.check_milestones('assists', self.player.career_stats['assists'])
        
        if random.random() < 0.05 and red_cards == 0:
            self.player.injured = True
            self.player.injury_weeks = random.randint(1, 4)
            self.add_event(f"⚠️ Травма во время матча! Выбыл на {self.player.injury_weeks} недель")
        
        rep_change = goals * 3 + assists * 2 - yellow_cards - red_cards * 5
        self.player.career_stats['reputation'] = min(100, max(0, self.player.career_stats['reputation'] + rep_change))
        
        event_text = f"⚽ Матч сыгран {result} Счет: {match_score} | Ваш вклад: Голы: {goals}, передачи: {assists}"
        self.add_event(event_text)
        
        self.advance_time()
        self.update_display()
    
    def rest(self):
        if not self.check_player():
            return
        
        if self.player.injured:
            self.player.injury_weeks -= 1
            if self.player.injury_weeks <= 0:
                self.player.injured = False
                self.add_event("✨ Травма зажила! Игрок снова готов к матчам")
        
        energy_recovery = random.randint(30, 40)
        self.player.career_stats['energy'] = min(100, self.player.career_stats['energy'] + energy_recovery)
        
        self.add_event(f"😴 Отдых восстановил {energy_recovery} энергии")
        self.advance_time()
        self.update_display()
    
    def save_game(self):
        if not self.check_player():
            return
        
        QMessageBox.information(self, "Сохранение", "💾 Игра сохранена (демо-режим)")
        self.add_event("💾 Прогресс сохранен")
    
    def load_game(self):
        QMessageBox.information(self, "Загрузка", "📂 Функция загрузки в разработке")
    
    def update_overall(self):
        if self.player:
            self.player.overall = int(sum(self.player.stats.values()) / len(self.player.stats))
    
    def advance_time(self):
        self.weeks_passed += 1
        self.current_date = self.current_date.addDays(7)
        
        self.process_weekly_expenses()
        
        if self.weeks_passed % 4 == 0:
            self.receive_salary()
            self.update_european_competitions()
            self.update_cup_competition()
        
        self.check_birthday()
        self.check_contract_expiry()
        self.check_contract_extension_opportunity()
        self.check_national_team_call()
        self.generate_transfer_offers()
        self.check_trophy_day()
        
        self.update_league_tables()
        
        if self.player and self.player.money <= 0:
            self.game_over()
    
    def update_display(self):
        if not self.player:
            return
        
        self.player_name_label.setText(f"👤 Имя: {self.player.name}")
        self.player_nationality_label.setText(f"🏳️ Национальность: {self.player.nationality}")
        self.player_age_label.setText(f"📅 Возраст: {self.player.age}" + (" (нет расходов)" if self.player.age < 18 else ""))
        self.player_position_label.setText(f"📍 Позиция: {self.player.position}")
        self.player_overall_label.setText(f"⭐ Общий рейтинг: {self.player.overall}")
        self.player_club_label.setText(f"🏢 Клуб: {self.player.career_stats['club']}")
        self.player_money_label.setText(f"💰 Деньги: ${self.player.money}")
        self.player_salary_label.setText(f"💰 Зарплата: ${self.player.career_stats['salary'] if self.player.has_contract else 0}/неделя")
        self.player_increase_label.setText(f"📈 Повышение: {self.player.contract['salary_increase_pct'] if self.player.has_contract else 0}% в год")
        self.player_years_label.setText(f"📅 Лет в клубе: {self.player.years_in_club}")
        self.player_reputation_label.setText(f"📊 Репутация: {self.player.career_stats['reputation']}/100")
        self.player_satisfaction_label.setText(f"😊 Удовлетворенность клуба: {self.player.career_stats['club_satisfaction']}/100")
        
        if self.player.has_contract:
            weeks_left = self.player.contract['end_date'].daysTo(self.current_date) // 7
            if weeks_left > 0:
                contract_text = f"📝 Контракт: {weeks_left} нед. до {self.player.contract['end_date'].toString('dd.MM.yy')}"
            else:
                contract_text = f"📝 Контракт: ИСТЕК {self.player.contract['end_date'].toString('dd.MM.yy')}"
            
            bonuses_text = (f"🎯 Бонусы: ⚽${self.player.contract['bonuses']['goal_bonus']} "
                           f"🎯${self.player.contract['bonuses']['assist_bonus']} "
                           f"📊${self.player.contract['bonuses']['match_bonus']}")
        else:
            contract_text = "📝 Контракт: НЕТ (свободный агент)"
            bonuses_text = "🎯 Бонусы: нет контракта"
        
        self.player_contract_label.setText(contract_text)
        self.bonuses_label.setText(bonuses_text)
        
        self.energy_bar.setValue(self.player.career_stats['energy'])
        
        for stat_key, stat_value in self.player.stats.items():
            bar = getattr(self, f"stat_{stat_key}")
            bar.setValue(stat_value)
            label = getattr(self, f"stat_{stat_key}_value")
            label.setText(str(stat_value))
        
        self.career_matches_label.setText(f"{self.player.career_stats['matches']}")
        self.career_goals_label.setText(f"{self.player.career_stats['goals']}")
        self.career_assists_label.setText(f"{self.player.career_stats['assists']}")
        self.career_yellow_cards_label.setText(f"{self.player.career_stats['yellow_cards']}")
        self.career_red_cards_label.setText(f"{self.player.career_stats['red_cards']}")
        self.career_trophies_label.setText(f"{len(self.player.trophies)}")
        self.career_history_label.setText(f"{len(self.player.career_history)}")
        
        injury_text = "Да ⚠️" if self.player.injured else "Нет ✅"
        if self.player.injured:
            injury_text += f" (осталось {self.player.injury_weeks} нед.)"
        self.career_injury_label.setText(injury_text)
        
        self.date_label.setText(self.current_date.toString("d MMMM yyyy"))
        self.week_counter_label.setText(f"📆 Неделя {self.weeks_passed} | Сезон {self.get_current_season()}")
        
        if self.player.injured:
            self.status_label.setText(f"⚠️ ТРАВМА! Восстановление: {self.player.injury_weeks} недель")
        else:
            status = f"✅ Здоров | ⚡ Энергия: {self.player.career_stats['energy']}%"
            if not self.player.has_contract:
                status += " | ⚠️ Свободный агент"
            if self.player.age < 18:
                status += " | 📅 Нет расходов"
            self.status_label.setText(status)
        
        self.offers_label.setText(f"📨 Предложений: {len(self.transfer_offers)}")
    
    def add_event(self, event_text):
        timestamp = self.current_date.toString("dd.MM.yyyy")
        self.events_list.insertItem(0, f"[{timestamp}] {event_text}")
        
        while self.events_list.count() > 20:
            self.events_list.takeItem(self.events_list.count() - 1)
    
    def check_player(self):
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
