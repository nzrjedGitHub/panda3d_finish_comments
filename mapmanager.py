import pickle

class Mapmanager:
    """Керування картою"""

    def __init__(self):
        # Ініціалізує модель блоків та їх текстури
        self.model = "block"  # модель кубика лежить у файлі block.egg
        self.texture = "block.png"  # використовуються такі текстури
        self.colors = [
            (0.2, 0.2, 0.35, 1),   # темно-синій
            (0.2, 0.5, 0.2, 1),    # зелений
            (0.7, 0.2, 0.2, 1),    # червоний
            (0.5, 0.3, 0.0, 1),    # коричневий
        ]  # rgba
        self.startNew()  # створює нову карту

    def startNew(self):
        """Створює основу для нової карти, додаючи кореневий вузол для блоків"""
        self.land = render.attachNewNode("Land")  # кореневий вузол для блоків карти

    def getColor(self, z):
        """Повертає колір залежно від висоти блоку"""
        if z < len(self.colors):
            return self.colors[z]
        else:
            return self.colors[len(self.colors) - 1]

    def addBlock(self, position):
        """Створює та додає блок на карту"""
        self.block = loader.loadModel(self.model)  # завантажує 3D-модель блоку
        self.block.setTexture(loader.loadTexture(self.texture))  # встановлює текстуру
        self.block.setPos(position)  # встановлює позицію
        self.color = self.getColor(int(position[2]))  # визначає колір на основі висоти
        self.block.setColor(self.color)  # застосовує колір
        self.block.setTag("at", str(position))  # встановлює тег з позицією блоку
        self.block.reparentTo(self.land)  # прив’язує блок до кореневого вузла карти

    def clear(self):
        """Очищає карту, видаляючи всі блоки"""
        self.land.removeNode()  # видаляє кореневий вузол
        self.startNew()  # створює новий кореневий вузол

    def saveMap(self):
        """Зберігає позиції всіх блоків у файл"""
        blocks = self.land.getChildren()  # отримує всі блоки
        with open("my_map.dat", "wb") as fout:
            pickle.dump(len(blocks), fout)  # записує кількість блоків
            for block in blocks:
                x, y, z = block.getPos()  # отримує позицію кожного блоку
                pos = (int(x), int(y), int(z))
                pickle.dump(pos, fout)  # зберігає позицію

    def loadMap(self):
        """Завантажує карту з файлу, створюючи блоки у збережених позиціях"""
        self.clear()  # очищає поточну карту
        with open("my_map.dat", "rb") as fin:
            length = pickle.load(fin)  # зчитує кількість блоків
            for i in range(length):
                pos = pickle.load(fin)  # зчитує позицію кожного блоку
                self.addBlock(pos)  # створює блок у зчитаній позиції

    def loadLand(self, filename):
        """Завантажує карту з текстового файлу та створює блоки на основі висоти"""
        self.clear()
        with open(filename) as file:
            y = 0  # координата y збільшується для кожного рядка
            for line in file:
                x = 0  # координата x збільшується для кожного значення у рядку
                line = line.split(" ")
                for z in line:
                    for z0 in range(int(z) + 1):  # створює блоки до зазначеної висоти
                        block = self.addBlock((x, y, z0))
                    x += 1
                y += 1
        return x, y

    def findBlocks(self, pos):
        """Знаходить всі блоки на певній позиції"""
        return self.land.findAllMatches("=at=" + str(pos))

    def isEmpty(self, pos):
        """Перевіряє, чи є позиція вільною від блоків"""
        blocks = self.findBlocks(pos)
        return not blocks

    def findHighestEmpty(self, pos):
        """Знаходить найвищу вільну позицію для блоку"""
        x, y, z = pos
        z = 1
        while not self.isEmpty((x, y, z)):  # збільшує z, доки позиція не буде вільною
            z += 1
        return (x, y, z)

    def buildBlock(self, pos):
        """Ставить новий блок над найвищим існуючим блоком на цій позиції"""
        x, y, z = pos
        new = self.findHighestEmpty(pos)
        if new[2] <= z + 1:  # додає блок, якщо позиція відповідає рівню або нижче
            self.addBlock(new)

    def delBlock(self, position):
        """Видаляє всі блоки на зазначеній позиції"""
        blocks = self.findBlocks(position)
        for block in blocks:
            block.removeNode()  # видаляє вузли блоків з кореневого вузла

    def delBlockFrom(self, position):
        """Видаляє блок з найвищої заповненої позиції на зазначеній координаті"""
        x, y, z = self.findHighestEmpty(position)
        pos = x, y, z - 1  # визначає позицію найвищого існуючого блоку
        for block in self.findBlocks(pos):
            block.removeNode()  # видаляє знайдений блок
