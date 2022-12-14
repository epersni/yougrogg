#!/usr/bin/env python3

import configparser
import json
import sys
import argparse

pumps = configparser.ConfigParser()
pumps.read('pumps.ini')

with open('drinks.json', 'r') as f:
    drinks_config = json.load(f)
    drinks = drinks_config['drinks']


def get_ingredients_by_id(id):
    for drink in drinks:
        if drink['id'] == id:
            return drink['ingredients']


def get_pump_by_ingredient(ingredient_value):
    for each_section in pumps.sections():
        for (each_key, each_val) in pumps.items(each_section):
            if each_key == "value" and each_val == ingredient_value:
                return each_section
    return None


def is_drink_available(drink_id):
    for i in get_ingredients_by_id(drink_id):
        for name, _ in i.items():
            if get_pump_by_ingredient(name) is None:
                return False
    return True


def get_all_drinks():
    result = []
    for drink in drinks:
        result.append(drink)
    return result


def get_available_drinks():
    result = []
    for drink in drinks:
        if is_drink_available(drink['id']):
            result.append(drink)
    return result


def get_non_alcholic_drinks():
    result = []
    for drink in drinks:
        if is_drink_available(drink['id']) and drink['non-alcoholic']:
            result.append(drink)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get drinks (returns JSON)')
    parser.add_argument('-a', '--all',
                        dest='all',
                        action='store_true',
                        help='List only non-alcholic drinks')
    parser.add_argument('-n', '--non-alcoholic',
                        dest='nonalcoholic',
                        action='store_true',
                        help='List only non-alcholic drinks')

    args = parser.parse_args()
    if args.all:
        print(json.dumps(get_all_drinks()))
    elif args.nonalcoholic:
        print(json.dumps(get_non_alcholic_drinks()))
    else:
        print(json.dumps(get_available_drinks()))

