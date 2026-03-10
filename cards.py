import random
from json import dump, loads


def figth(x, power):
    n = random.randint(0, x.power + power)
    if n >= 0 and n <= x.power:
        change_p(x, power=10)
        another_one(x)
    else:
        change_p(x, power=-1000)


def claim_for_POP(x, money):
    if change_p(x, money=money):
        status = CARDS["status"].copy()
        status["top_text"] = "Налог Уплачен, народ вас любит"
        status["texture"] = path + "items/scaled_x9/square_141_x5.png"
        status["text"] = "-20 денег"
        open_card(x, status)
        print(x.cnt)


def change_p(x, karma=0, money=0, power=0, atr=0):
    x.karma += karma
    x.money += money
    x.power += power
    x.atractive += atr
    status = CARDS["status"].copy()
    status["text"] = "СМЕРТЬ"
    status["agree"] = lambda x: exit_func(x)
    status["disagree"] = lambda x: exit_func(x)
    f = 0
    if x.karma > 100:
        status["top_text"] = "Народ настолько вас любил, что убил"
        f = 1
    elif x.karma < 0:
        status["top_text"] = "Народ ненавидит вас, он убил вас"
        f = 1
    elif x.money > 100:
        status["top_text"] = "Денги фраера сгубили"
        f = 1
    elif x.money < 0:
        status["top_text"] = "ВЫ УМЕРЛИ ОТ БЕДНОСТИ"
        f = 1
    elif x.atractive < 0:
        status["top_text"] = "Вас перепутали с гоблином"
        f = 1
    elif x.atractive > 100:
        status["top_text"] = "Вы были слишком красивы для мира сего"
        f = 1
    elif power < 0:
        status["top_text"] = "Недостаток силы"
        f = 1
    if f:
        status["text"] = f"СЧЕТ: {x.cnt}"
        mx = 0
        try:
            with open("data/conf.json", "r") as f:
                mx = loads(f)[0]
        except Exception:
            pass
        if mx < x.cnt:
            status["text"] = f"ЛУЧШИЙ СЧЕТ: {x.cnt}"
            with open("data/conf.json", "w") as f:
                dump([x.cnt], f)
        open_card(x, status)
        return False
    return True


path = "assets/"


def open_card(x, card):
    x.rooms[-1]["card"] = card.copy()


def ANTI_POP_FUNC(x):
    x.rooms[-1]["card"]["top_text"] = "Ну пожалуйста..."
    x.rooms[-1]["card"]["agree"] = lambda x: another_one(x)


def pet(x):
    x.rooms[-1]["card"]["top_text"] = "Он, хочет еще..."
    if "dogged" not in x.effects:
        x.effects.append("dogged")
        x.karma += 5
        if x.karma > 300:
            x.karma = 300


def another_one(x):
    maybe = []
    maybe.extend(CARDS["just_a_dogs"])
    maybe.extend(CARDS["mage"])
    maybe.append(CARDS["pop"])
    maybe.append(CARDS["thief"])
    maybe.append(CARDS["lost_money"])
    maybe.append(CARDS["merchant"])
    maybe.append(CARDS["pilgrim"])
    maybe.append(CARDS["artifact"])
    maybe.append(CARDS["altar"])
    if x.cnt == 19:
        x.level += 1
        status = CARDS["status"].copy()
        status["top_text"] = "ВЫ ПЕРЕШЛИ НА НОВЫЙ УРОВЕНЬ"
        open_card(x, status)
    else:
        x.rooms[-1]["card"] = random.choice(maybe).copy()
    x.cnt += 1


def mage_func(x, color):
    if color == "blue":
        if change_p(x, atr=15):
            status = CARDS["status"].copy()
            status["top_text"] = "Ваше лицо стало привлекательнее"
            open_card(x, status)
    if color == "red":
        if change_p(x, power=15):
            status = CARDS["status"].copy()
            status["top_text"] = "Вас переполняет мощь"
            status["texture"] = path + "items/scaled_x9/square_19_x5.png"
            open_card(x, status)
    if color == "yellow":
        if change_p(x, money=15):
            status = CARDS["status"].copy()
            status["top_text"] = "Кошелек тяжелеет"
            status["texture"] = path + "items/scaled_x9/square_141_x5.png"
            open_card(x, status)
    if color == "green":
        if change_p(x, karma=15):
            status = CARDS["status"].copy()
            status["top_text"] = "Народ доволен"
            open_card(x, status)


example = {
    "border_color": (255, 255, 255),
    "background": (100, 100, 100),
    "text": "Пьяный Эльф",
    "text_color": (255, 255, 0),
    "texture": "assets/rogues/scaled_x9/square_1_x5.png",
    "scale": 2.0,
    "actions": ["ДА", "Нет"],
    "agree": lambda x: another_one(x),
    "disagree": lambda x: another_one(x),
    "top_text": "BEBEBE",
}
CARDS = {}
STATUS_CARD = example.copy()
STATUS_CARD["actions"] = ["ЧТО?", "ЧТО?"]
STATUS_CARD["texture"] = path + "items/scaled_x9/square_131_x5.png"
STATUS_CARD["top_text"] = "НАЧАЛО ИГРЫ..."
STATUS_CARD["text"] = "ВНИМАНИЕ"
STATUS_CARD["background"] = (61, 1, 29)
STATUS_CARD["border_color"] = (45, 0, 21)
CARDS["status"] = STATUS_CARD
DOG_1 = dict(
    zip(
        list(example.keys()),
        [
            (152, 31, 0),
            (183, 162, 16),
            "СОБАКА",
            (0, 0, 0),
            path + "animals/scaled_x9/square_20_x5.png",
            1.5,
            ["Погладить", "Уйти"],
            pet,
            another_one,
            "Он хочет, чтобы его погладили...",
        ],
    )
)
DOG_2 = DOG_1.copy()
DOG_2["texture"] = path + "animals/scaled_x9/square_21_x5.png"
CARDS["just_a_dogs"] = [DOG_1, DOG_2]
MAGE = example.copy()
MAGE["texture"] = path + "rogues/scaled_x9/square_24_x5.png"
MAGE["text"] = "КРУТОЙ МАГ"
MAGE["top_text"] = "синий или красный?"
MAGE["agree"] = lambda x: mage_func(x, "blue")
MAGE["disagree"] = lambda x: mage_func(x, "red")
MAGE["actions"] = ["Синий", "Красный"]
MAGE["background"] = (68, 4, 206)
MAGE["border_color"] = (46, 19, 104)
MAGE_2 = MAGE.copy()
MAGE_2["top_text"] = "желтый или зеленый"
MAGE_2["actions"] = ["Желтый", "Зеленый"]
MAGE_2["agree"] = lambda x: mage_func(x, "yellow")
MAGE_2["disagree"] = lambda x: mage_func(x, "green")
CARDS["mage"] = [MAGE, MAGE_2]
POP = example.copy()
POP["texture"] = path + "rogues/scaled_x9/square_11_x5.png"
POP["text"] = "Священник"
POP["top_text"] = "Налог на церковь?"
POP["actions"] = ["НЕТ", "Ладно(20)"]
POP["disagree"] = lambda x: claim_for_POP(x, -20)
POP["agree"] = lambda x: open_card(x, CARDS["antipop"])
CARDS["pop"] = POP
ANTI_POP = example.copy()
ANTI_POP["text"] = "Анти священник"
ANTI_POP["top_text"] = "может тогда в мою?"
ANTI_POP["actions"] = ["НЕЕЕЕТ", "Ладно(20)"]
ANTI_POP["disagree"] = lambda x: claim_for_POP(x, -20)
ANTI_POP["agree"] = lambda x: ANTI_POP_FUNC(x)
ANTI_POP["texture"] = path + "rogues/scaled_x9/square_15_x5.png"
CARDS["antipop"] = ANTI_POP


def exit_func(x):
    x.reset()


THIEF = example.copy()
THIEF["text"] = "Разбойник"
THIEF["top_text"] = "Ты будешь легкой добычей)"
THIEF["texture"] = path + "rogues/scaled_x9/square_3_x5.png"
THIEF["actions"] = ["Бежать", "Сражаться"]
THIEF["disagree"] = lambda x: figth(x, 80)
CARDS["thief"] = THIEF
LOST_MONEY = example.copy()
LOST_MONEY["text"] = "чьи-то денги"
LOST_MONEY["top_text"] = "Что упало, то пропало, так ведь?"
LOST_MONEY["texture"] = path + "items/scaled_x9/square_142_x5.png"
LOST_MONEY["actions"] = ["Уйти", "Взять"]
LOST_MONEY["disagree"] = lambda x: bring_lost_money(x)


def bring_lost_money(x):
    if change_p(x, karma=-10, money=20):
        status = CARDS["status"].copy()
        status["top_text"] = "Вам очень стыдно"
        status["text"] = "+20 денег"
        open_card(x, status)


CARDS["lost_money"] = LOST_MONEY
MERCHANT = example.copy()
MERCHANT["text"] = "Странствующий торговец"
MERCHANT["top_text"] = "У меня есть зелье красоты! Всего за 10 монет."
MERCHANT["texture"] = path + "rogues/scaled_x9/square_39_x5.png"
MERCHANT["actions"] = ["Купить за 10", "Пройти мимо"]
MERCHANT["background"] = (210, 180, 100)
MERCHANT["border_color"] = (160, 140, 80)


def merchant_buy(x):
    if change_p(x, money=-10, atr=25):
        status = CARDS["status"].copy()
        status["top_text"] = "Вы стали заметно симпатичнее!"
        status["texture"] = path + "items/scaled_x9/square_121_x5.png"
        open_card(x, status)


MERCHANT["agree"] = merchant_buy
MERCHANT["disagree"] = another_one
CARDS["merchant"] = MERCHANT
PILGRIM = example.copy()
PILGRIM["text"] = "Заблудившийся паломник"
PILGRIM["top_text"] = "Я потерял дорогу... Не могли бы вы дать мне пару монет?"
PILGRIM["texture"] = path + "rogues/scaled_x9/square_38_x5.png"
PILGRIM["actions"] = ["Помочь (5)", "Отказать"]
PILGRIM["background"] = (120, 160, 200)
PILGRIM["border_color"] = (80, 120, 160)


def pilgrim_help(x):
    if change_p(x, money=-5, karma=15):
        status = CARDS["status"].copy()
        status["top_text"] = "Паломник благодарит вас. Народ уважает доброту."
        status["texture"] = path + "items/scaled_x9/square_140_x5.png"
        open_card(x, status)


def pilgrim_refuse(x):
    change_p(x, karma=-5)
    another_one(x)


PILGRIM["agree"] = pilgrim_help
PILGRIM["disagree"] = pilgrim_refuse
CARDS["pilgrim"] = PILGRIM
ARTIFACT = example.copy()
ARTIFACT["text"] = "Древний артефакт"
ARTIFACT["top_text"] = (
    "Вы нашли светящийся камень. Он пульсирует энергией... Активировать?"
)
ARTIFACT["texture"] = path + "items/scaled_x9/square_97_x5.png"
ARTIFACT["actions"] = ["Активировать", "Оставить"]
ARTIFACT["background"] = (80, 60, 100)
ARTIFACT["border_color"] = (120, 90, 150)


def artifact_activate(x):
    if random.choice([True, False]):
        if change_p(x, power=30):
            status = CARDS["status"].copy()
            status["top_text"] = "Артефакт наделил вас невероятной силой!"
            status["texture"] = path + "items/scaled_x9/square_97_x5.png"
            open_card(x, status)
    else:
        if change_p(x, karma=-20):
            status = CARDS["status"].copy()
            status["top_text"] = (
                "Странная энергия испортила вашу ауру. Народ насторожен."
            )
            status["texture"] = path + "items/scaled_x9/square_97_x5.png"
            open_card(x, status)


def artifact_leave(x):
    status = CARDS["status"].copy()
    status["top_text"] = "Вы решили не рисковать. Артефакт остался нетронутым."
    status["text"] = "Ничего не произошло"
    open_card(x, status)


ARTIFACT["agree"] = artifact_activate
ARTIFACT["disagree"] = artifact_leave
CARDS["artifact"] = ARTIFACT
ALTAR = example.copy()
ALTAR["text"] = "Алтарь искупления"
ALTAR["top_text"] = "Древний камень впитывает энергию. И не знает, что дает"
ALTAR["texture"] = path + "items/scaled_x9/square_105_x5.png"
ALTAR["actions"] = ["Активировать", "Уйти"]
ALTAR["background"] = (100, 80, 120)
ALTAR["border_color"] = (140, 110, 160)


def altar_sacrifice(x):
    if x.power < 20:
        status = CARDS["status"].copy()
        status["top_text"] = "У вас недостаточно силы для жертвоприношения."
        status["text"] = "Попробуйте позже"
        open_card(x, status)
        return

    if change_p(x, power=-20, karma=30):
        status = CARDS["status"].copy()
        status["top_text"] = "Народ благодарит вас за жертву! Ваша мудрость признана."
        status["texture"] = path + "items/scaled_x9/square_106_x5.png"
        status["text"] = "+30 кармы, -20 силы"
        open_card(x, status)


def altar_leave(x):
    status = CARDS["status"].copy()
    status["top_text"] = "Вы решили не жертвовать силой."
    status["text"] = "Ничего не произошло"
    open_card(x, status)


ALTAR["agree"] = altar_sacrifice
ALTAR["disagree"] = altar_leave
CARDS["altar"] = ALTAR
