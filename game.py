from direct.showbase.ShowBase import ShowBase  # імпортує базовий клас для створення гри
from mapmanager import Mapmanager  # імпортує клас для керування картою
from hero import Hero  # імпортує клас героя

class Game(ShowBase):
    def __init__(self):
        # Ініціалізація базового класу для запуску графічного інтерфейсу гри
        ShowBase.__init__(self)
        
        # Створення об'єкта карти та завантаження карти з файлу "land.txt"
        self.land = Mapmanager()
        x, y = self.land.loadLand("land.txt")  # завантажує карту та повертає її розміри
        
        # Створення об'єкта героя на основі завантаженої карти та позиціонування в центрі
        self.hero = Hero((x // 2, y // 2, 2), self.land)  # розміщує героя в центрі карти

        # Встановлення поля зору камери на 90 градусів для ширшого огляду
        base.camLens.setFov(90)

# Створення та запуск гри
game = Game()
game.run()
