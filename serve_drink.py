#!/usr/bin/env python3

import configparser
import json
import sys
import argparse
import list_drinks

pumps = configparser.ConfigParser()
pumps.read('pumps.ini')

with open('drinks.json', 'r') as f:
    drinks_config = json.load(f)
    drinks = drinks_config['drinks']


def serve_drink(drink_id):
    for i in list_drinks.get_ingredients_by_id(drink_id):
        for key, value in i.items():
            print("Pouring",key,value,"ml") 


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Server drink')
    parser.add_argument('id',
                        type=int, 
                        help='The drink-id to server')

    args = parser.parse_args()
    serve_drink(args.id)
