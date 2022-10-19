#! /usr/bin/env python3

# Imports
import os
import json
from re import sub
from colorama import Fore, Style
import cards
from Ids import *

doInfo = True


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

PROFESSIONS = {}

STONECUTTING = {
    "type": MC("stonecutting"),
    "ingredient": {
        "item": str()
    },
    "result": str(),
    "count": int(),
    "nbt": str()
}

TRADING = {
  "type": CI("mechanical_trading"),
  "ingredients": [
    {
      "item": str(),
      "count": int()
    }
  ],
  "output": {
    "item": str(),
    "count": int()
  }
}

G = CI("gold_coin")
S = CI("silver_coin")


# Functions
def trade_card(item_name="Garbage", item_id=CI("garbage"), item_amount=1, money_amount=1, money_type=S, color_1=0xEB8034, color_2=0x404040):
    """Generates profession card recipes into the "Build" folder."""

    trading_name = snake_case(item_name)+"_trading"
    stonecutting_name = "trade_card_"+snake_case(item_name)

    nbt = {
        "recipeIds": [CI("trading/"+trading_name)],
        "NamedAfter": item_name,
        "CardColor1": "%x" % color_1,
        "CardColor2": "%x" % color_2
    }

    stonecutting_recipe = STONECUTTING

    stonecutting_recipe["ingredient"]["item"] = CI("blank_trade_card")
    stonecutting_recipe["result"] = CI("trade_card")
    stonecutting_recipe["nbt"] = str(nbt)
    stonecutting_recipe["count"] = 1

    with open(f"{os.path.dirname(__file__)}\\Build\\stonecutting\\{stonecutting_name}.json", "w") as f:
        json.dump(stonecutting_recipe, f, indent=2)

    info(f"Generated file stonecutting/{stonecutting_name}.json")

    trading_recipe = TRADING

    trading_recipe["ingredients"][0]["item"] = money_type
    trading_recipe["ingredients"][0]["count"] = money_amount
    trading_recipe["output"]["item"] = item_id
    trading_recipe["output"]["count"] = item_amount

    with open(f"{os.path.dirname(__file__)}\\Build\\mechanical_trading\\{trading_name}.json", "w") as f:
        json.dump(trading_recipe, f, indent=2)

    info(f"Generated file mechanical_trading/{trading_name}.json")

    update(f"Registered Trade Card for \"{item_name}\"")


# def exchange_card(money_types=(S, G), color_1=0xEB8034, color_2=0x404040):
#     pass

def profession_recipe(profession="Garbage Collector", input="", input_amount=1, output="", output_amount=1):
    """
    Generates recipes for profession card

    :param profession: The name of the profession
    :param input: The input ingredient
    :param input_amount: The amount of the input ingredient
    :param output: The output ingredient
    :param output_amount: The amount of the output ingredient
    """

    global PROFESSIONS

    if not isinstance(PROFESSIONS[snake_case(profession)], list):
        PROFESSIONS[snake_case(profession)] = list()

    PROFESSIONS[snake_case(profession)].append()


def profession_card(profession="Garbage Collector", color_1=0xEB8034, color_2=0x404040):
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

    with open(f"{os.path.dirname(__file__)}\\Build\\stonecutting\\{stonecutting_name}.json", "w") as f:
        json.dump(stonecutting_recipe, f, indent=2)

    info(f"Generated file stonecutting/{stonecutting_name}.json")
    update(f"Registered Trade Card for \"{profession}\"")


if __name__ == '__main__':
    trade_card()
