# Опис клавіш керування персонажем:
key_switch_camera = "c"  # перемикання камери (закріплена за героєм чи вільна)
key_switch_mode = "z"  # режим проходження крізь перешкоди (активується/деактивується)

# Клавіші для переміщення персонажа:
key_forward = "w"  # крок вперед (у напрямку камери)
key_back = "s"  # крок назад
key_left = "a"  # крок вліво (відносно камери)
key_right = "d"  # крок вправо
key_up = "e"  # крок вгору
key_down = "q"  # крок вниз

# Клавіші для повороту камери:
key_turn_left = "n"  # поворот камери вліво
key_turn_right = "m"  # поворот камери вправо

# Клавіші для будівництва та руйнування блоків:
key_build = "b"  # побудувати блок перед собою
key_destroy = "v"  # зруйнувати блок перед собою

# Клавіші для збереження і завантаження карти:
key_savemap = 'k' # збереження карти
key_loadmap = 'l' # завантаження карти

class Hero:
    def __init__(self, pos, land):
        # Ініціалізує персонажа на карті
        self.land = land  # карта, на якій знаходиться герой
        self.mode = True  # режим проходження крізь об'єкти
        self.hero = loader.loadModel("smiley")  # завантаження моделі персонажа
        self.hero.setColor(1, 0.5, 0)  # встановлює колір героя
        self.hero.setScale(0.3)  # масштабує героя
        self.hero.setH(180)  # встановлює напрямок героя
        self.hero.setPos(pos)  # розміщує героя в заданій позиції
        self.hero.reparentTo(render)  # додає героя до сцени
        self.cameraBind()  # встановлює прив'язку камери до героя
        self.accept_events()  # прив'язує обробники подій

    def changeMode(self):
        """Перемикає режим проходження крізь об'єкти"""
        self.mode = not self.mode

    def cameraBind(self):
        """Прив'язує камеру до героя"""
        base.disableMouse()
        base.camera.setH(180)  # встановлює напрямок камери
        base.camera.reparentTo(self.hero)  # прив'язує камеру до героя
        base.camera.setPos(0, 0, 1.5)  # позиціонує камеру
        self.cameraOn = True

    def cameraUp(self):
        """Від'єднує камеру від героя для вільного перегляду"""
        pos = self.hero.getPos()
        base.mouseInterfaceNode.setPos(-pos[0], -pos[1], -pos[2] - 3)  # позиціонує камеру для огляду
        base.camera.reparentTo(render)
        base.enableMouse()
        self.cameraOn = False

    def changeView(self):
        """Перемикає вид камери (прив'язана або вільна)"""
        if self.cameraOn:
            self.cameraUp()
        else:
            self.cameraBind()

    def turn_left(self):
        """Повертає героя вліво"""
        self.hero.setH((self.hero.getH() + 5) % 360)

    def turn_right(self):
        """Повертає героя вправо"""
        self.hero.setH((self.hero.getH() - 5) % 360)

    def look_at(self, angle):
        """Повертає координати, в які переміститься персонаж при кроці у вказаному напрямку"""
        x_from = round(self.hero.getX())
        y_from = round(self.hero.getY())
        z_from = round(self.hero.getZ())
        dx, dy = self.check_dir(angle)  # визначає зміни координат залежно від кута
        x_to = x_from + dx
        y_to = y_from + dy
        return x_to, y_to, z_from

    def just_move(self, angle):
        """Переміщається до нової позиції незалежно від об'єктів"""
        pos = self.look_at(angle)
        self.hero.setPos(pos)

    def move_to(self, angle):
        """Рух у зазначеному напрямку з урахуванням режиму проходження крізь об'єкти"""
        if self.mode:
            self.just_move(angle)
        else:
            self.try_move(angle)

    def check_dir(self, angle):
        """повертає заокруглені зміни координат X, Y,
        відповідні переміщенню у бік кута angle.
        Координата Y зменшується, якщо персонаж дивиться на кут 0,
        та збільшується, якщо дивиться на кут 180.
        Координата X збільшується, якщо персонаж дивиться на кут 90,
        та зменшується, якщо дивиться на кут 270.
            кут 0 (від 0 до 20) -> Y - 1
            кут 45 (від 25 до 65) -> X + 1, Y - 1
            кут 90 (від 70 до 110) -> X + 1
            від 115 до 155 -> X + 1, Y + 1
            від 160 до 200 -> Y + 1
            від 205 до 245 -> X - 1, Y + 1
            від 250 до 290 -> X - 1
            від 290 до 335 -> X - 1, Y - 1
            від 340 -> Y - 1
        """
        if angle >= 0 and angle <= 20:
            return (0, -1)
        elif angle <= 65:
            return (1, -1)
        elif angle <= 110:
            return (1, 0)
        elif angle <= 155:
            return (1, 1)
        elif angle <= 200:
            return (0, 1)
        elif angle <= 245:
            return (-1, 1)
        elif angle <= 290:
            return (-1, 0)
        elif angle <= 335:
            return (-1, -1)
        else:
            return (0, -1)

    def back(self):
        """Рух назад"""
        angle = (self.hero.getH() + 180) % 360
        self.move_to(angle)

    def forward(self):
        """Рух вперед"""
        angle = self.hero.getH() % 360
        self.move_to(angle)

    def left(self):
        """Рух вліво"""
        angle = (self.hero.getH() + 90) % 360
        self.move_to(angle)

    def right(self):
        """Рух вправо"""
        angle = (self.hero.getH() + 270) % 360
        self.move_to(angle)



    def try_move(self, angle):
        """Переміщується, якщо позиція вільна, інакше підіймається"""
        pos = self.look_at(angle)
        if self.land.isEmpty(pos):  # перевірка, чи позиція вільна
            pos = self.land.findHighestEmpty(pos)  # знаходить найвищу вільну позицію
            self.hero.setPos(pos)
        else:
            pos = pos[0], pos[1], pos[2] + 1
            if self.land.isEmpty(pos):  # піднімається, якщо можливо
                self.hero.setPos(pos)

    def up(self):
        """Піднімається на один рівень (у режимі проходження крізь об'єкти)"""
        if self.mode:
            self.hero.setZ(self.hero.getZ() + 1)

    def down(self):
        """Опускається на один рівень (у режимі проходження крізь об'єкти)"""
        if self.mode and self.hero.getZ() > 1:
            self.hero.setZ(self.hero.getZ() - 1)

    def build(self):
        """Будує блок перед собою"""
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.addBlock(pos)
        else:
            self.land.buildBlock(pos)

    def destroy(self):
        """Руйнує блок перед собою"""
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.delBlock(pos)
        else:
            self.land.delBlockFrom(pos)

    def accept_events(self):
        """Задає події для клавіш керування персонажем"""
        base.accept(key_turn_left, self.turn_left)
        base.accept(key_turn_left + "-repeat", self.turn_left)
        base.accept(key_turn_right, self.turn_right)
        base.accept(key_turn_right + "-repeat", self.turn_right)
        base.accept(key_forward, self.forward)
        base.accept(key_forward + "-repeat", self.forward)
        base.accept(key_back, self.back)
        base.accept(key_back + "-repeat", self.back)
        base.accept(key_left, self.left)
        base.accept(key_left + "-repeat", self.left)
        base.accept(key_right, self.right)
        base.accept(key_right + "-repeat", self.right)
        base.accept(key_switch_camera, self.changeView)
        base.accept(key_switch_mode, self.changeMode)
        base.accept(key_up, self.up)
        base.accept(key_up + "-repeat", self.up)
        base.accept(key_down, self.down)
        base.accept(key_down + "-repeat", self.down)
        base.accept(key_build, self.build)
        base.accept(key_destroy, self.destroy)
        base.accept(key_savemap, self.land.saveMap)
        base.accept(key_loadmap, self.land.loadMap)
