import sys
import os
import sqlite3

DB_FILE = "sleep.db"

def populate():
    data = open("data.txt", "r")
    current = ""
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    for line in data.readlines():
        line.strip()
        if line[0] == "#":
            continue
        if current == "abilities":
            if "close" in line:
                current = ""
                continue
            values = ["", ""]
            i = 0
            quotes = False
            for char in line:
                if char == ' ' and quotes == False:
                    i += 1
                elif char == '"':
                    quotes = not quotes
                else:
                    values[i] += char
            for i in range(len(values)):
                values[i] = values[i].strip()
            cur.execute("INSERT INTO abilities (name, max_level) VALUES (?, ?)", tuple(values))
            con.commit()
            print('INSERT: abilities(name, max_level) = {0}, {1}'.format(values[0], values[1])) 

        if current == "subskills":
            if "close" in line:
                current = ""
                continue
            values = [""]
            i = 0
            quotes = False
            for char in line:
                if char == ' ' and quotes == False:
                    i += 1
                elif char == '"':
                    quotes = not quotes
                else:
                    values[i] += char
            for i in range(len(values)):
                values[i] = values[i].strip()
            cur.execute("INSERT INTO subskills (name) VALUES (?)", tuple(values))
            con.commit()
            print('INSERT: subskills(name) = {0}'.format(values[0])) 

        if current == "natures":
            if "close" in line:
                current = ""
                continue
            values = [""]
            i = 0
            quotes = False
            for char in line:
                if char == ' ' and quotes == False:
                    i += 1
                elif char == '"':
                    quotes = not quotes
                else:
                    values[i] += char
            for i in range(len(values)):
                values[i] = values[i].strip()
            cur.execute("INSERT INTO natures (name) VALUES (?)", tuple(values))
            con.commit()
            print('INSERT: natures(name) = {0}'.format(values[0])) 

        if current == "pokemon":
            if "close" in line:
                current = ""
                continue
            values = ["", "", "", "", "", "", ""]
            i = 0
            quotes = False
            for char in line:
                if char == ' ' and quotes == False:
                    i += 1
                elif char == '"':
                    quotes = not quotes
                else:
                    values[i] += char
            for i in range(len(values)):
                values[i] = values[i].strip()
            values[1] = values[1].lower()
            cur.execute("INSERT INTO pokemon (pokedex_num, name, type, ability, ingredient_1, ingredient_2, ingredient_3) VALUES (?, ?, ?, ?, ?, ?, ?)", tuple(values))
            con.commit()
            print('INSERT: pokemon(pokedex_num, name, type, ability, ingredient_1, ingredient_2, ingredient_3) = {0}, {1}, {2}, {3}, {4}, {5}, {6}'.format(values[0], values[1], values[2], values[3], values[4], values[5], values[6])) 

        if current == "recipes":
            if "close" in line:
                current = ""
                continue
            values = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
            i = 0
            quotes = False
            for char in line:
                if char == ' ' and quotes == False:
                    i += 1
                elif char == '"':
                    quotes = not quotes
                else:
                    values[i] += char
            for i in range(len(values)):
                values[i] = values[i].strip()
            cur.execute("INSERT INTO recipes (dish_type, name, base_strength, leek, mushroom, egg, potato, apple, herb, sausage, milk, honey, oil, ginger, tomato, cacao, tail, soybeans, corn) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", tuple(values))
            con.commit()
            print('INSERT: recipes(dish_type, name, base_strength, leek, mushroom, egg, potato, apple, herb, sausage, milk, honey, oil, ginger, tomato, cacao, tail, soybeans, corn) = {0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15}, {16}, {17}, {18}'.format(values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7], values[8], values[9], values[10], values[11], values[12], values[13], values[14], values[15], values[16], values[17], values[18])) 

        if current == "berries":
            if "close" in line:
                current = ""
                continue
            values = ["", ""]
            i = 0
            quotes = False
            for char in line:
                if char == ' ' and quotes == False:
                    i += 1
                elif char == '"':
                    quotes = not quotes
                else:
                    values[i] += char
            for i in range(len(values)):
                values[i] = values[i].strip()
            cur.execute("INSERT INTO berries (berry, type) VALUES (?, ?)", tuple(values))
            con.commit()
            print('INSERT: berries(berry, type) = {0}'.format(values[0], values[1])) 

        if current == "":
            if "abilities" in line:
                current = "abilities"
            if "subskills" in line:
                current = "subskills"
            if "natures" in line:
                current = "natures"
            if "pokemon" in line:
                current = "pokemon"
            if "recipes" in line:
                current = "recipes"
            if "berries" in line:
                current = "berries"
            continue
    data.close()
    con.close()
    return

populate()
