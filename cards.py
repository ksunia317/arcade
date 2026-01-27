import random


def change_p(x, karma=0, money=0, power=0, atr=0):
    x.karma += karma
    x.money += money
    x.power += power
    x.atractive += atr


path = "assets/"


def open_card(x, card):
    x.rooms[-1]["card"] = card.copy()


def pet(x):
    x.rooms[-1]["card"]["top_text"] = "Он, хочет еще..."
    if "dogged" not in x.effects:
        x.effects.append("dogged")
        x.karma += 5
        if (x.karma > 300):
            x.karma = 300


def another_one(x):
    maybe = []
    maybe.extend(CARDS["just_a_dogs"])
    if ("blue" not in x.effects and "red" not in x.effects):
        maybe.extend(CARDS["mage"])
    x.rooms[-1]['card'] = random.choice(maybe).copy()
    x.cnt += 1


def mage_func(x, color):
    if color == "blue":
        change_p(x, atr=15)
        status = CARDS["status"].copy()
        status["top_text"] = "Ваше лицо стало привлекательнее"
        open_card(x, status)
    if color == "red":
        change_p(x, power=15)
        status = CARDS["status"].copy()
        status["top_text"] = "Вас переполняет мощь"
        status["texture"] = path + "items/scaled_x9/square_19_x5.png"
        open_card(x, status)
    if color == "yellow":
        change_p(x, money=15)
        status = CARDS["status"].copy()
        status["top_text"] = "Кошелек тяжелеет"
        status["texture"] = path + "items/scaled_x9/square_141_x5.png"
        open_card(x, status)
    if color == "green":
        change_p(x, karma=15)
        status = CARDS["status"].copy()
        status["top_text"] = "Народ доволен"
        open_card(x, status)


example = {"border_color": (255, 255, 255),
           "background": (100, 100, 100),
           "text": "Пьяный Эльф",
           "text_color": (255, 255, 0),
           "texture": "assets/rogues/scaled_x9/square_1_x5.png",
           "scale": 2.0,
           "actions": ["ДА", "Нет"],
           "agree": lambda x: another_one(x),
           "disagree": lambda x: another_one(x),
           "top_text": "BEBEBE"}
CARDS = {}
STATUS_CARD = example.copy()
STATUS_CARD["actions"] = ["ЧТО?", "ЧТО?"]
STATUS_CARD["texture"] = path + "items/scaled_x9/square_131_x5.png"
STATUS_CARD["top_text"] = "НАЧАЛО ИГРЫ..."
STATUS_CARD["text"] = "ВНИМАНИЕ"
STATUS_CARD["background"] = (61, 1, 29)
STATUS_CARD["border_color"] = (45, 0, 21)
CARDS["status"] = STATUS_CARD
DOG_1 = dict(zip(list(example.keys()), [(152, 31, 0),
                                        (183, 162, 16),
                                        "СОБАКА",
                                        (0, 0, 0),
                                        path + "animals/scaled_x9/square_20_x5.png",
                                        1.5,
                                        ["Погладить", "Уйти"],
                                        pet,
                                        another_one,
                                        "Он хочет, чтобы его погладили..."]))
DOG_2 = DOG_1.copy()
DOG_2["texture"] = path + "animals/scaled_x9/square_21_x5.png"
CARDS["just_a_dogs"] = [DOG_1, DOG_2]
MAGE = example.copy()
MAGE["texture"] = path + "rogues/scaled_x9/square_24_x5.png"
MAGE["text"] = "КРУТОЙ МАГ"
MAGE["top_text"] = "синий или красный?"
MAGE["agree"] = lambda x: mage_func(x, "blue")
MAGE["disagree"] = lambda x: mage_func(x, "red")
MAGE['actions'] = ["Синий", "Красный"]
MAGE["background"] = (68, 4, 206)
MAGE["border_color"] = (46, 19, 104)
MAGE_2 = MAGE.copy()
MAGE_2["top_text"] = "желтый или зеленый"
MAGE_2["actions"] = ["Желтый", "Зеленый"]
MAGE_2["agree"] = lambda x: mage_func(x, "yellow")
MAGE_2["disagree"] = lambda x: mage_func(x, "green")
CARDS["mage"] = [MAGE, MAGE_2]