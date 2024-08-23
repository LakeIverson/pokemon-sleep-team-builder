import sys
import click
import os
import sqlite3

DB_FILE = 'sleep.db'

def getDB():
    if not os.path.exists(DB_FILE):
        print('Error in getDB: {0} does not exist.'.format(DB_FILE))
        sys.exit(1)
    con = sqlite3.connect(DB_FILE)
    con.execute('PRAGMA foreign_keys = ON')
    return con

@click.group()
def cli():
    pass

@click.command()
def addPokemon():
    with getDB() as con:
        cur = con.cursor()
        pokedex_num, name, typing, ability, ingredient1, ingredient2, ingredient3 = None, None, None, None, None, None, None

        while True:
            pokedex_num = input("What is the pokedex number for the new pokemon? ")
            if not pokedex_num.isnumeric():
                print("Pokedex number must be a number.")
            else:
                break   
        int(pokedex_num)

        name = input("What is the pokemon name? ")
        name.lower()

        cur.execute("SELECT pokedex_num, name FROM pokemon WHERE pokedex_num = ? AND name LIKE ?", (pokedex_num, name))
        row = cur.fetchone()
        if row is not None:
            print('{0}: {1} is already a pokemon in the database. Quitting.'.format(pokedex_num, name))
            return

        while True:
            typing = input("What is the type of the pokemon? ")
            typing.lower()
        
            cur.execute("SELECT type FROM berries WHERE type = ?", (typing,))
            row = cur.fetchone()
            if row is None:
                print('{0} is not a valid pokemon type. Please try again. If this type is a new type, first run the command "addberry". You can press Ctrl+D to abort.'.format(typing))
            else:
                break

        while True:
            print("What is the ability of the pokemon?")
            print("Please note that for 'Charge Strength S', 'Charge Strength M' and 'Dream Shard Magnet S'")
            print("that due to the way the abilities have different functions but the same name, they are")
            print("in the database as 'Charge Strength S (Set Value)' for if it's always a set value, and")
            print("'Charge Strength S (Value Range)' if it's from a range x-y. So write these exactly this")
            print("way.")
            ability = input("")
        
            cur.execute("SELECT id FROM abilities WHERE name LIKE ?", (ability,))
            row = cur.fetchone()
            if row is None:
                print('{0} is not a valid ability. Please try again.'.format(ability))
            else:
                ability = row[0]
                ability = int(ability)
                break

        i = 1
        valid_ingredients = ['leek', 'mushroom', 'egg', 'potato', 'apple', 'herb', 'sausage', 'milk', 'honey', 'oil', 'ginger,' 'tomato', 'cacao', 'tail', 'soybeans', 'corn']
        while True:
            print('What is ingredient {0} of the pokemon?'.format(i))
            print('options: leek, mushroom, egg, potato, apple, herb, sausage, milk')
            print('         honey, oil, ginger, tomato, cacao, tail, soybeans, corn')
            ingredient = input('')
            ingredient.lower()

            if ingredient not in valid_ingredients:
                print('{0} is not a valid ingredient. Please try again.'.format(ingredient))
                continue
            if i == 1:
                ingredient1 = ingredient
                i = 2
            elif i == 2:
                ingredient2 = ingredient
                i = 3
            elif i == 3:
                ingredient3 = ingredient
                break;
        
        cur.execute("SELECT name FROM abilities WHERE id = ?", (ability,))
        ability_name = cur.fetchone()[0]
        while True:
            print('{0}: {1}, the {2} type with the ability {3}. Finds ingredients {4}, {5} and {6}.'.format(pokedex_num, name, typing, ability_name, ingredient1, ingredient2, ingredient3))
            confirmation = input("Is this pokemon okay to add to the database? (y/n) ")
            if confirmation.lower() == "y":
                cur.execute("INSERT INTO pokemon (pokedex_num, name, type, ability, ingredient_1, ingredient_2, ingredient_3) VALUES (?, ?, ?, ?, ?, ?, ?)", (pokedex_num, name, typing, ability, ingredient1, ingredient2, ingredient3))
                data = open("data.txt", "r")
                datalines = data.readlines()
                data.close()
                newdata = open("data.txt", "w")
                pokemon = False
                written = False
                for line in datalines:
                    if "pokemon" in line:
                        pokemon = True
                        newdata.write(line)
                        continue
                    if not pokemon:
                        newdata.write(line)
                        continue
                    if "close" in line:
                        pokemon = False
                        newdata.write(line)
                        continue
                    n = ""
                    n_found = False
                    for char in line:
                        if not n_found and char != " ":
                            n += char
                        else:
                            n_found = True
                    if int(pokedex_num) <= int(n):
                        if not written:
                            newdata.write('{0} "{1}" {2} {3} {4} {5} {6}\n'.format(pokedex_num, name, typing, ability, ingredient1, ingredient2, ingredient3))
                            written = True
                    newdata.write(line)
                newdata.close()
                break
            elif confirmation.lower() == "n":
                return

@click.command()
def addAbility():
    with getDB() as con:
        cur = con.cursor()
        name, max_level = None, None
        name = input("What is the name of the ability? ")
        while True:
            max_level = input("What is the max level of the new ability? ")
            max_level = int(max_level)
            if max_level < 1:
                print("Level must be 1 or greater. Please try again.")
            else:
                break
        while True:
            print('{0}, Max Level: {1}.'.format(name, max_level))
            confirmation = input("Is this ability okay to add to the database? (y/n) ")
            if confirmation.lower() == "y":
                cur.execute("INSERT INTO abilities (name, max_level) VALUES (?, ?)", (name, max_level))
                data = open("data.txt", "r")
                datalines = data.readlines()
                data.close()
                newdata = open("data.txt", "w")
                ability = False
                written = False
                for line in datalines:
                    if line[0] == "#":
                        newdata.write(line)
                        continue
                    if "abilities" in line:
                        ability = True
                        newdata.write(line)
                        continue
                    if not ability:
                        newdata.write(line)
                        continue
                    if "close" in line and ability:
                        ability = False
                        newdata.write('"{0}" {1}\n'.format(name, max_level))
                        newdata.write(line)
                        continue
                    newdata.write(line)
                newdata.close()
                break
            elif confirmation.lower() == "n":
                return

@click.command()
def addSubSkill():
    with getDB() as con:
        cur = con.cursor()
        name = None
        name = input("What is the name of the SubSkill? ")
        while True:
            print('{0}.'.format(name))
            confirmation = input("Is this SubSkill okay to add to the database? (y/n) ")
            if confirmation.lower() == "y":
                cur.execute("INSERT INTO subskills (name) VALUES (?)", (name,))
                data = open("data.txt", "r")
                datalines = data.readlines()
                data.close()
                newdata = open("data.txt", "w")
                subskill = False
                written = False
                for line in datalines:
                    if line[0] == "#":
                        newdata.write(line)
                        continue
                    if "subskills" in line:
                        subskill = True
                        newdata.write(line)
                        continue
                    if not subskill:
                        newdata.write(line)
                        continue
                    if "close" in line and subskill:
                        subskill = False
                        newdata.write('"{0}"\n'.format(name))
                        newdata.write(line)
                        continue
                    newdata.write(line)
                newdata.close()
                break
            elif confirmation.lower() == "n":
                return

@click.command()
def addDish():
    with getDB() as con:
        cur = con.cursor()
        dish_type, name, base_strength = None, None, None
        ingredients = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        while True:
            dish_type = input("What is the type of dish? Options: curry, salad, dessert. ")
            if dish_type.lower() not in ["curry", "salad", "dessert"]:
                print("Please choose one of curry, salad or dessert. Please try again.")
            else:
                break
        name = input("What is the name of the dish? ")
        while True:
            base_strength = input("What is the base strength of the dish? ")
            base_strength = int(base_strength)
            if base_strength < 0:
                print("Base strength cannot be less than 0. Please try again.")
            else:
                break
        choices = ["leek", "mushroom", "egg", "potato", "apple", "herb", "sausage", "milk", "honey", "oil", "ginger", "tomato", "cacao", "tail", "soybeans", "corn", "confirm-recipe", "confirm recipe", "confirm", "c"]
        while True:
            print("Add an ingredient?")
            print("Options: leek, mushroom, egg, potato, apple, herb, sausage, milk")
            print("         honey, oil, ginger, tomato, cacao, tail, soybeans, corn")
            print("         confirm-recipe (c).")
            ingredient = input("")
            if ingredient.lower() not in choices:
                print("Choose one of the options listed. Please try again.")
            elif ingredient == "confirm-recipe" or ingredient == "confirm reciple" or ingredient == "confirm" or ingredient == "c":
                break
            else:
                while True:
                    value = input("How many? ")
                    value = int(value)
                    if value < 0:
                        print("Cannot have less than 0 ingredient. Please try again.")
                    else:
                        i = choices.index(ingredient)
                        ingredients[i] = value;
                        break
        ingredient_text = ""
        for i in range(len(ingredients)):
            if ingredients[i] > 0:
                ingredient_text += '{0}: {1}, '.format(choices[i], ingredients[i])
        if ingredient_text == "":
            ingredient_text = "no ingredients."
        else:
            ingredient_text = ingredient_text[0:-2]
        while True:
            print('{0} - {1} with Base Strength of {2}. Made with "{3}"'.format(dish_type, name, base_strength, ingredient_text))
            confirmation = input("Is this Dish okay to add to the database? (y/n) ")
            if confirmation.lower() == "y":
                cur.execute("INSERT INTO recipes (dish_type, name, base_strength, leek, mushroom, egg, potato, apple, herb, sausage, milk, honey, oil, ginger, tomato, cacao, tail, soybeans, corn) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (dish_type, name, base_strength, ingredients[0], ingredients[1], ingredients[2], ingredients[3], ingredients[4], ingredients[5], ingredients[6], ingredients[7], ingredients[8], ingredients[9], ingredients[10], ingredients[11], ingredients[12], ingredients[13], ingredients[14], ingredients[15]))
                data = open("data.txt", "r")
                datalines = data.readlines()
                data.close()
                newdata = open("data.txt", "w")
                dish = False
                written = False
                dtype = False
                for line in datalines:
                    if line[0] == "#":
                        newdata.write(line)
                        continue
                    if "recipes" in line:
                        dish = True
                        newdata.write(line)
                        continue
                    if not dish:
                        newdata.write(line)
                        continue
                    if "close" in line:
                        dish = False
                        newdata.write(line)
                        continue
                    if dish:
                        if dish_type in line:
                            dtype = True
                            newdata.write(line)
                            continue
                    if dish and dtype and not written:
                        dtype = False
                        if dish_type not in line:
                            newdata.write('{0} "{1}" {2} {3} {4} {5} {6} {7} {8} {9} {10} {11} {12} {13} {14} {15} {16} {17} {18}\n'.format(dish_type, name, base_strength, ingredients[0], ingredients[1], ingredients[2], ingredients[3], ingredients[4], ingredients[5], ingredients[6], ingredients[7], ingredients[8], ingredients[9], ingredients[10], ingredients[11], ingredients[12], ingredients[13], ingredients[14], ingredients[15]))
                        newdata.write(line)
                        continue
                    newdata.write(line)
                newdata.close()
                break
            elif confirmation.lower() == "n":
                return
    
@click.command()
def addNature():
    with getDB() as con:
        cur = con.cursor()
        name = None
        name = input("What is the name of the Nature? ")
        while True:
            print('{0}.'.format(name))
            confirmation = input("Is this Nature okay to add to the database? (y/n) ")
            if confirmation.lower() == "y":
                cur.execute("INSERT INTO natures (name) VALUES (?)", (name,))
                data = open("data.txt", "r")
                datalines = data.readlines()
                data.close()
                newdata = open("data.txt", "w")
                nature = False
                written = False
                for line in datalines:
                    if line[0] == "#":
                        newdata.write(line)
                        continue
                    if "natures" in line:
                        nature = True
                        newdata.write(line)
                        continue
                    if not nature:
                        newdata.write(line)
                        continue
                    if "close" in line and nature:
                        nature = False
                        newdata.write('"{0}"\n'.format(name))
                        newdata.write(line)
                        continue
                    newdata.write(line)
                newdata.close()
                break
            elif confirmation.lower() == "n":
                return

@click.command()
def addBerry():
    with getDB() as con:
        cur = con.cursor()
        name, btype = None, None
        name = input("What is the name of the Berry? ")
        btype = input("What is the type of the Berry? ")
        while True:
            print('{0} for {1} types.'.format(name, btype))
            confirmation = input("Is this Berry okay to add to the database? (y/n) ")
            if confirmation.lower() == "y":
                cur.execute("INSERT INTO berries (berry, type) VALUES (?, ?)", (name, btype))
                data = open("data.txt", "r")
                datalines = data.readlines()
                data.close()
                newdata = open("data.txt", "w")
                berry = False
                written = False
                for line in datalines:
                    if line[0] == "#":
                        newdata.write(line)
                        continue
                    if "berries" in line:
                        berry = True
                        newdata.write(line)
                        continue
                    if not berry:
                        newdata.write(line)
                        continue
                    if "close" in line and berry:
                        berry = False
                        newdata.write('{0} {1}\n'.format(name, btype))
                        newdata.write(line)
                        continue
                    newdata.write(line)
                newdata.close()
                break
            elif confirmation.lower() == "n":
                return

cli.add_command(addPokemon)
cli.add_command(addAbility)
cli.add_command(addSubSkill)
cli.add_command(addDish)
cli.add_command(addNature)
cli.add_command(addBerry)

cli()

def main():
    return 0

main()
