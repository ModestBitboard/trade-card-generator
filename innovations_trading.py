#! /usr/bin/env python3

# Imports
import os
import json
from re import sub
from colorama import Fore, Style
import cards
from Ids import *

doInfo = True
namespace = "create_innovations"


# Str Types
def snake_case(msg):
    return '_'.join(
        sub('([A-Z][a-z]+)', r' \1',
            sub('([A-Z]+)', r' \1',
                msg.replace('-', ' ')
                .replace("'", "").replace("!", "")
                )).split()).lower()


def info(msg):
    if doInfo:
        print(Fore.CYAN + msg + Style.RESET_ALL)


def update(msg):
    print(Fore.GREEN + msg + Style.RESET_ALL)


def alert(msg):
    print(Fore.YELLOW + msg + Style.RESET_ALL)


# Variables

PROFESSIONS = dict()

STONECUTTING = {
    "type": MC("stonecutting"),
    "ingredient": {
        "item": str
    },
    "result": str,
    "count": int,
    "nbt": str
}

TRADING = {
  "type": CI("mechanical_trading"),
  "ingredients": [
    {
      "item": str,
      "count": int
    }
  ],
  "output": {
    "item": str,
    "count": int
  }
}

G = CI("gold_coin")
S = CI("silver_coin")


# Config/Helper Functions
def set_info(state: bool):
    global doInfo
    doInfo = state


def set_namespace(name: str):
    global namespace
    namespace = name


def CN(object_id: str):
    return namespace + ":" + object_id


# Functions
def trade_card(
        item_name: str = "Garbage",
        item_id: str = CI("garbage"),
        item_amount: int = 1,
        money_amount: int = 1,
        money_id: str = S,
        color_1: hex = 0xEB8034,
        color_2: hex = 0x404040
):
    """
    Generates trade card recipes into the "Build" folder.

    :param item_name: The name displayed on the card
    :param item_id: The id of the item outputted
    :param item_amount: The amount of the item outputted
    :param money_amount: The amount of money inputted
    :param money_id: The id for the item used as money
    :param color_1: The color on top of the card
    :param color_2: The color on the bottom of the card
    """

    trading_name = snake_case(item_name)+"_trading"
    stonecutting_name = "trade_card_"+snake_case(item_name)

    nbt = {
        "recipeIds": [CN("trading/"+trading_name)],
        "NamedAfter": item_name,
        "CardColor1": "%x" % color_1,
        "CardColor2": "%x" % color_2
    }

    stonecutting_recipe = STONECUTTING

    stonecutting_recipe["ingredient"]["item"] = CI("blank_trade_card")
    stonecutting_recipe["result"] = CI("trade_card")
    stonecutting_recipe["nbt"] = str(nbt)
    stonecutting_recipe["count"] = 1

    with open(f"{os.path.dirname(__file__)}/Build/stonecutting/{stonecutting_name}.json", "w") as f:
        json.dump(stonecutting_recipe, f, indent=2)

    info(f"Generated file stonecutting/{stonecutting_name}.json")

    trading_recipe = TRADING

    trading_recipe["ingredients"][0]["item"] = money_id
    trading_recipe["ingredients"][0]["count"] = money_amount
    trading_recipe["output"]["item"] = item_id
    trading_recipe["output"]["count"] = item_amount

    with open(f"{os.path.dirname(__file__)}/Build/mechanical_trading/{trading_name}.json", "w") as f:
        json.dump(trading_recipe, f, indent=2)

    info(f"Generated file mechanical_trading/{trading_name}.json")

    update(f"Registered Trade Card for \"{item_name}\"")


def profession_recipe(
        profession: str = "Garbage Collector",
        recipe_name: str = "garbage",
        item_id: str = CI("garbage"),
        item_amount: int = 1,
        money_id: str = S,
        money_amount: int = 1
):
    """
    Generates recipes for profession card trading into the "Build" folder.

    :param profession: The name of the profession
    :param recipe_name: The name of the recipe
    :param item_id: The input ingredient id
    :param item_amount: The amount of the input ingredient
    :param money_id: The id for the item used as money
    :param money_amount: The amount of money outputted
    """

    global PROFESSIONS

    if profession not in PROFESSIONS.values():
        PROFESSIONS[snake_case(profession)] = list()

    trading_name = "%s_%s_trading" % (snake_case(recipe_name), snake_case(profession))

    trading_recipe = TRADING

    trading_recipe["ingredients"][0]["item"] = item_id
    trading_recipe["ingredients"][0]["count"] = item_amount
    trading_recipe["output"]["item"] = money_id
    trading_recipe["output"]["count"] = money_amount

    with open(f"{os.path.dirname(__file__)}/Build/mechanical_trading/{trading_name}.json", "w") as f:
        json.dump(trading_recipe, f, indent=2)

    PROFESSIONS[snake_case(profession)].append(CN("trading/"+trading_name))
    info(f"Generated file mechanical_trading/{trading_name}.json")


def profession_card(
        profession: str = "Garbage Collector",
        color_1: hex = 0xEB8034,
        color_2: hex = 0x404040
):
    """
    Generates profession card recipes into the "Build" folder.
    Register Profession trades before registering professions,
    otherwise the card won't load those recipes.

    :param profession: The name of the profession
    :param color_1: The color on top of the card
    :param color_2: The color on the bottom of the card
    """

    stonecutting_name = "profession_card_" + snake_case(profession)

    nbt = {
        "recipeIds": PROFESSIONS[snake_case(profession)],
        "NamedAfter": profession,
        "CardColor1": "%x" % color_1,
        "CardColor2": "%x" % color_2
    }

    stonecutting_recipe = STONECUTTING

    stonecutting_recipe["ingredient"]["item"] = CI("blank_profession_card")
    stonecutting_recipe["result"] = CI("profession_card")
    stonecutting_recipe["nbt"] = str(nbt)
    stonecutting_recipe["count"] = 1

    with open(f"{os.path.dirname(__file__)}/Build/stonecutting/{stonecutting_name}.json", "w") as f:
        json.dump(stonecutting_recipe, f, indent=2)

    info(f"Generated file stonecutting/{stonecutting_name}.json")
    update(f"Registered Trade Card for \"{profession}\"")
