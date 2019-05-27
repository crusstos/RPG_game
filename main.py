import random
import os

class personage:
    xp_for_lvlup = 100
    max_level = 100

    def __init__(self, name):
        self.name = name
        self._set_stats()
        print("Hello, {}!\n".format(self.name))

    # Приватный метод задающий статы
    def _set_stats(self, hp = 100, attack = 10, level = 1, xp = 0):
        self.hp = hp
        self.attack = attack
        self.level = level
        self.xp = xp

    def get_hp(self):
        return self.hp

    # Функция атаки
    def __sub__(self, enemy):
        self.hp -= enemy.attack
        print("{} attacked {} for {} damage!".format(enemy.name, self.name, enemy.attack))
        return None

    # Вывод статистики
    def __str__(self):
        return "{} has {} hp, {} damage and level {} ({} experience)!".format(self.name, self.hp, self.attack, self.level, self. xp)

    # Условия поражения
    def defeated(self):
        if self.hp <= 0:
            return True
        else:
            return False

class npc(personage):
    def __init__(self, hero_level, name = None):
        if name == None:
            self.name = "Monster"
        else:
            self.name = name
        self._set_stats(hero_level)
        print("Here we go again...")

    def _set_stats(self, hero_level):
        self.hp = hero_level * 100
        self.attack = hero_level * 10
        self.level = hero_level
        self.xp_for_kill = random.randint(hero_level * 10, hero_level * 35)

    def super_attack(self, chance = None, damage = None):
        if chance == None:
            chance = self.level
        if damage == None:
            damage = self.attack * random.randint(2, 4)

        is_super = random.randint(1, personage.max_level)
        if chance >= is_super:
            return damage
        else:
            return None

    def __str__(self):
        return "{} has {} hp, {} damage and level {}!".format(self.name, self.hp, self.attack, self.level)

    def __sub__(self, enemy):
        turns = enemy.stun_attack()
        if turns == None:
            self.hp -= enemy.attack
            print("\n{} attacked {} for {} damage!".format(enemy.name, self.name, enemy.attack))
            return 0
        else:
            self.hp -= enemy.attack
            print("\n{} attacked {} for {} damage and stunned for {} turn!".format(enemy.name, self.name, enemy.attack, turns))
            return turns

    def die(self, hero_):
        hero_ + self.xp_for_kill
        hero_.win()

class hero(personage):
    def __init__(self, name):
        personage.__init__(self, name)
        self.max_hp = self.hp

    def levelup(self):
        if self.xp >= self.xp_for_lvlup:
            self.xp -= self.xp_for_lvlup
            self.level += 1
            self.attack += 10
            self.max_hp += 20
            self.hp = self.max_hp
            print("{} is now level {}!".format(self.name, self.level))
            print(self.__str__())
            return False
        return True

    def respawn(self):
        name = self.name
        os.system('cls' if os.name == 'nt' else 'clear')
        self.__init__(name)

    def stun_attack(self, chance = None, turns = None):
        if chance == None:
            chance = self.level // 5 + 10
        if turns == None:
            turns = self.level // 10 + 1

        is_stun = random.randint(1, personage.max_level)
        if chance >= is_stun:
            return turns
        else:
            return None

    def __sub__(self, enemy):
        damage = enemy.super_attack()
        if damage == None:
            self.hp -= enemy.attack
            print("\n{} attacked {} for {} damage!".format(enemy.name, self.name, enemy.attack))
        else:
            self.hp -= damage
            print("\n{} attacked {} for {} critical damage!".format(enemy.name, self.name, damage))

    def __add__(self, xp):
        self.xp += xp
        self.levelup()

    def get_level(self):
        return self.level

    def win(self):
        is_needed_resp = self.levelup()
        if is_needed_resp:
            hp_ = self.max_hp
            attack_ = self.attack
            level_ = self.level
            xp_ = self.xp
            self._set_stats(hp_, attack_, level_, xp_)


if __name__ == "__main__":
    name = input("Enter your name please: ")
    HERO = hero(name)
    ENEMY = []

    stun = 0
    game = True

    died = False
    # Главный цикл игры
    while game:
        enemy_couner = -1
        while not died:
            ENEMY.append(npc(HERO.get_level()))
            enemy_couner += 1


            while ENEMY[enemy_couner].get_hp() > 0 and HERO.get_hp() > 0:
                command = input("\nEnter 'attack' to hit an enemy or 'info' to see your stats for now.\n")
                while command != 'attack' and command != 'info':
                    command = input("\nWrong input! Enter 'attack' to hit an enemy or 'info' to see your stats for now.\n")

                if command == 'info':
                    print("Enemy:")
                    print(ENEMY[enemy_couner])
                    print("You:")
                    print(HERO)
                    continue

                if command == 'attack':
                    result = ENEMY[enemy_couner] - HERO
                    if result > 0 or stun > 0:
                        stun += result
                        stun -= 1
                        continue
                HERO - ENEMY[enemy_couner]

            if enemy_couner == 0 and ENEMY[enemy_couner].defeated():
                ENEMY[enemy_couner].die(HERO)
                print("\nCongratulations! You killed 1 boss!")
            elif ENEMY[enemy_couner].defeated():
                ENEMY[enemy_couner].die(HERO)
                print("\nCongratulations! You killed {} bosses!".format(enemy_couner + 1))
            elif HERO.defeated():
                print("\nYou died, but that was a nice battle! You killed {} bosses so far!".format(enemy_couner))
                quit = input("\nDo you want to quit? Enter 'yes' to quit or 'no' to restart the game!\n")
                while quit != 'yes' and quit != 'no':
                    quit = input("\nDo you want to quit? Enter 'yes' to quit or 'no' to restart the game!\n")
                if quit == 'yes':
                    game = False
                    died = True
                else:
                    HERO.respawn()
                    deid = True
            else:
                print("\n\nSomething went wrong...")
