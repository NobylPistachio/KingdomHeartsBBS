import json
import logging
from pprint import pprint

logging.basicConfig(level=logging.INFO)

BBS_MELDING_GUIDE:dict = json.load(open("BBS_MELDING_GUIDE.json"))

CRYSTALS = ["Shimmering","Fleeting","Pulsing","Wellspring","Soothing","Hungry","Abounding"]

#Sort the melding guide by character
def by_character(character:str) -> dict:
    if character == "Any" or not character:
        return BBS_MELDING_GUIDE
    else:
        guide = {}
        for table_name, table in BBS_MELDING_GUIDE.items():
            if table_name == "Crystal Melding Outcomes":
                guide[table_name] = table
                continue
            guide[table_name] = []
            for meld in table:
                if meld["Used By"][character]:
                    guide[table_name].append(meld)
        return guide
    
def by_command_goal(command:str,guide) -> list:
    result_guide = []
    for table_name, table in guide.items():
        if table_name != "Crystal Melding Outcomes":
            for meld in table:
                if meld["Command"] == command:
                    result_guide.append(meld)
    return result_guide

def by_command_ingredient(command:str,guide) -> list:
    result_guide = []
    for table_name, table in guide.items():
        if table_name != "Crystal Melding Outcomes":
            for meld in table:
                if meld["1st Ingredient"] == command or meld["2nd Ingredient"] == command:
                    result_guide.append(meld)
    return result_guide

def get_unique_commands(guide) -> list:
    all_commands = []
    for table_name, table in guide.items():
        if table_name != "Crystal Melding Outcomes":
            for meld in table:
                if meld['Command'] not in all_commands:
                    all_commands.append(meld['Command'])
    all_commands.sort()
    return all_commands

def get_other_ingredient(command:str,list_of_melds) -> list:
    result = ['']
    for meld in list_of_melds:
        if meld["1st Ingredient"] == command:
            if meld['2nd Ingredient'] not in result:
                result.append(meld['2nd Ingredient'])
        if meld["2nd Ingredient"] == command:
            if meld['1st Ingredient'] not in result:
                result.append(meld['1st Ingredient'])
    return result

def get_unique_ingredients(guide) -> list:
    all_commands = ['']
    for table_name, table in guide.items():
        if table_name != "Crystal Melding Outcomes":
            for meld in table:
                if meld['1st Ingredient'] not in all_commands:
                    all_commands.append(meld['1st Ingredient'])
                if meld['2nd Ingredient'] not in all_commands:
                    all_commands.append(meld['2nd Ingredient'])
    all_commands.sort()
    return all_commands

def get_meld(command1:str,command2:str):
    for table_name, table in BBS_MELDING_GUIDE.items():
        if table_name != "Crystal Melding Outcomes":
            for meld in table:
                if meld['1st Ingredient'] == command1 and meld['2nd Ingredient'] == command2:
                    return meld['Command']
                elif meld['1st Ingredient'] == command2 and meld['2nd Ingredient'] == command1:
                    return meld['Command']
    logging.debug("No meld found for %s and %s",command1,command2)
    return None

def get_type(command1:str,command2:str) -> str:
    for table_name, table in BBS_MELDING_GUIDE.items():
        if table_name != "Crystal Melding Outcomes":
            for meld in table:
                if meld['1st Ingredient'] == command1 and meld['2nd Ingredient'] == command2:
                    return meld['Type']
                elif meld['1st Ingredient'] == command2 and meld['2nd Ingredient'] == command1:
                    return meld['Type']
    logging.debug("No meld found for %s and %s",command1,command2)
    return None

def get_ability(crystal,meld_type) -> str:
        
    if not crystal or not meld_type:
        return ""
    return BBS_MELDING_GUIDE["Crystal Melding Outcomes"][f'Type {meld_type}'][crystal]
    
