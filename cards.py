import random


def get_effect(x, ef, message):
    x.effects.append(ef)
    status = CARDS["status"]
    status["top_text"] = message
    x.rooms[-1]["card"] = status


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


path = "assets/"
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
MAGE["agree"] = lambda x: get_effect(x, "blue", "Что-то точно изменилось")
MAGE["disagree"] = lambda x: get_effect(x, "red", "Что-то точно изменилось")
MAGE['actions'] = ["Синий", "Красный"]
MAGE["background"] = (68, 4, 206)
MAGE["border_color"] = (46, 19, 104)
CARDS["mage"] = [MAGE]
CARDS[""]