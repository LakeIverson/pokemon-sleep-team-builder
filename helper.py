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
def addHelper():
    with getDB() as con:
        cur = con.cursor()

        # Get the pokedex_num from the user.
        pokedex_num = None
        pokemon_name = None
        while True:
            # Prompt user for either dex number or pokemon name.
            pokemon = input("What is the pokedex number of your helper? You can also submit the name of the pokemon. ")
            # Check if the input is a pokedex number or a pokemon's name.
            if pokemon.isnumeric():
                # Verify that the pokedex num is in the database.
                cur.execute("SELECT name FROM pokemon WHERE pokedex_num = (?)", (pokemon,)) 
                row = cur.fetchone()
                if row is not None:
                    # Pokedex number in database.
                    pokedex_num = pokemon
                    pokemon_name = row[0]
                    break
                print('{0} is not the Pokedex number for any Pokemon in Pokemon Sleep. Please try again.'.format(pokemon))
            else:
                # Verify that the pokemon is in the database.
                cur.execute("SELECT pokedex_num FROM pokemon WHERE name LIKE (?)", (pokemon,))
                row = cur.fetchone()
                if row is not None:
                    # Pokemon in database.
                    pokedex_num = int(row[0])
                    pokemon_name = pokemon.lower()
                    break
                print('{0} is not a Pokemon in Pokemon Sleep. Please try again.'.format(pokemon))

        # Get the pokemon shininess.
        shiny = None
        while True:
            s = input('Is you pokemon shiny? y/n. ')
            if s.lower() == 'y':
                shiny = True
                break
            elif s.lower() == 'n':
                shiny = False
                break
            else:
                print("Please answer only y or n.")
        
        # Get the pokemon level.
        level = None
        while True:
            # Prompt the user for the level.
            l = input('What level is {0}? '.format(pokemon_name))
            l = int(l)
            if l < 1 or l > 100:
                print('{0} is not a valid level. Levels can only be between 1 and 100. Please try again.'.format(l))
            else:
                level = l
                break

        # Get the ingredients.
        ingredients = [None, None, None]
        row = cur.execute("SELECT ingredient_1, ingredient_2, ingredient_3 FROM pokemon WHERE pokedex_num = (?)", (pokedex_num,))
        options = row.fetchone()
        i = 1
        while True:
            # Prompt the user for the ingredients
            ing = input('What is Ingredient #{0}? options: {1}, {2}, {3} '.format(i, options[0], options[1], options[2]))
            if ing.lower() not in options:
                print('{0} is not an ingredient {1} can have. Please try again.'.format(ing, pokemon_name))
            else:
                # Ingredient exists.
                ingredients[i - 1] = ing.lower()
                i += 1
            if i > 3:
                break

        # Get the subskills.
        subskills = [None, None, None, None, None]
        s = 1
        levels = [10, 25, 50, 75, 100]
        while True:
            # Prompt the user for the skills
            skill = input('What is subskill {0}? (Level {1} skill) '.format(s, levels[s- 1]))
            cur.execute("SELECT id FROM subskills WHERE name LIKE (?)", (skill,))
            row = cur.fetchone()
            if row is not None:
                # Skill in database.
                # Enforcing unique skills.
                if row[0] in subskills:
                    print('{0} already listed. You can only have 1 of each subskill. If this is a mistake, Ctrl+D to abort.'.format(skill))
                else:
                    subskills[s - 1] = int(row[0])
                    s += 1
            else:
                print('{0} is not a valid subskill. Please try again.'.format(skill))
            if s > 5:
                break
                
        # Get the nature.
        nature = None
        while True:
            # Prompt the user for the nature
            nat = input('What is the pokemon nature? ')
            cur.execute("SELECT id FROM natures WHERE name LIKE (?)", (nat,))
            row = cur.fetchone()
            if row is not None:
                # Nature in database.
                nature = int(row[0])
                break
            print('{0} is not a valid nature. Please try again.'.format(nat))

        # Insert pokemon
        cur.execute("INSERT INTO helpers (pokedex, pokemon, shiny, level, subskill_1, subskill_2, subskill_3, subskill_4, subskill_5, nature, ingredient_1, ingredient_2, ingredient_3) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (pokedex_num, pokemon_name, shiny, level, subskills[0], subskills[1], subskills[2], subskills[3], subskills[4], nature, ingredients[0], ingredients[1], ingredients[2]))
        rowid = cur.lastrowid
        con.commit();
        cur.execute("SELECT name FROM pokemon WHERE pokedex_num = (?)", (pokedex_num,))
        pokemon = cur.fetchone()[0]
        print('{0} inserted into database with id: {1}'.format(pokemon, rowid))
    con.close()

@click.command()
@click.argument('command')
@click.argument('helper_id')
def updateHelper(command, helper_id):
    with getDB() as con:
        cur = con.cursor()
        key = None
        value = None
        if command == "level":
            cur.execute("SELECT level FROM helpers WHERE id = (?)", (helper_id,))
            level = cur.fetchone()[0]
            while True:
                value = input('What is the new value for level? Current level: {0}. '.format(level))
                value = int(value)
                if value < 1 or value > 100:
                    print('{0} is not a valid level. Levels can only be between 1 and 100. Please try again.'.format(value))
                else:
                    break
            cur.execute("UPDATE helpers SET level = ? WHERE id = ?", (value, helper_id))
            rowid = cur.lastrowid
            print('{0}: Updated level with {1}'.format(rowid, value))
            con.commit()
        elif command == "ingredient1":
            cur.execute("SELECT pokedex, ingredient_1 FROM helpers WHERE id = (?)", (helper_id,))
            row = cur.fetchone()
            (pokedex_num, ing1) = row
            row = cur.execute("SELECT ingredient_1, ingredient_2, ingredient_3 FROM pokemon WHERE pokedex_num = (?)", (pokedex_num,))
            options = row.fetchone()
            while True:
                value = input('What is the new ingredient for ingredient 1? Current ingredient: {0}. Options: {1}, {2}, {3}. '.format(ing1, options[0], options[1], options[2]))
                if value.lower() not in options:
                    print('{0} is not in options. Please try again.'.format(value))
                else:
                    break
            cur.execute("UPDATE helpers SET ingredient_1 = ? WHERE id = ?", (value, helper_id))
            rowid = cur.lastrowid
            print('{0}: Updated ingredient_1 with {1}'.format(rowid, value))
            con.commit()
        elif command == "ingredient2":
            cur.execute("SELECT pokedex, ingredient_2 FROM helpers WHERE id = (?)", (helper_id,))
            row = cur.fetchone()
            (pokedex_num, ing2) = row
            row = cur.execute("SELECT ingredient_1, ingredient_2, ingredient_3 FROM pokemon WHERE pokedex_num = (?)", (pokedex_num,))
            options = row.fetchone()
            while True:
                value = input('What is the new ingredient for ingredient 2? Current ingredient: {0}. Options: {1}, {2}, {3}. '.format(ing2, options[0], options[1], options[2]))
                if value.lower() not in options:
                    print('{0} is not in options. Please try again.'.format(value))
                else:
                    break
            cur.execute("UPDATE helpers SET ingredient_2 = ? WHERE id = ?", (value, helper_id))
            rowid = cur.lastrowid
            print('{0}: Updated ingredient_2 with {1}'.format(rowid, value))
            con.commit()
        elif command == "ingredient3":
            cur.execute("SELECT pokedex, ingredient_3 FROM helpers WHERE id = (?)", (helper_id,))
            row = cur.fetchone()
            (pokedex_num, ing3) = row
            row = cur.execute("SELECT ingredient_1, ingredient_2, ingredient_3 FROM pokemon WHERE pokedex_num = (?)", (pokedex_num,))
            options = row.fetchone()
            while True:
                value = input('What is the new ingredient for ingredient 3? Current ingredient: {0}. Options: {1}, {2}, {3}. '.format(ing3, options[0], options[1], options[2]))
                if value.lower() not in options:
                    print('{0} is not in options. Please try again.'.format(value))
                else:
                    break
            cur.execute("UPDATE helpers SET ingredient_3 = ? WHERE id = ?", (value, helper_id))
            rowid = cur.lastrowid
            print('{0}: Updated ingredient_3 with {1}'.format(rowid, value))
            con.commit()
        elif command == "skill1":
            cur.execute("SELECT subskill_1 FROM helpers WHERE id = (?)", (helper_id,))
            skill1 = cur.fetchone()[0]
            cur.execute("SELECT name FROM subskills WHERE id = (?)", (skill1,))
            skill1 = cur.fetchone()[0]
            row = cur.execute("SELECT subskill_2, subskill_3, subskill_4, subskill_5 FROM helpers WHERE id = (?)", (helper_id,))
            skills = row.fetchone()
            while True:
                value = input('What is the new subskill for subskill 1? Current skill: {0}. (This is the Lv. 10 Skill). '.format(skill1))
                cur.execute("SELECT id FROM subskills WHERE name LIKE (?)", (value,))
                row = cur.fetchone()
                if row is not None:
                    if row[0] in skills:
                        confirmation = input('{0} already listed. You can only have 1 of each subskill. If you wish to replace anyways, type `confirm`. '.format(value))
                        if confirmation.lower() == "confirm":
                            value = row[0]
                            break
                    else:
                        value = row[0]
                        break
                else:
                    print('{0} is not a valid subskill. Please try again.'.format(value))
            cur.execute("UPDATE helpers SET subskill_1 = ? WHERE id = ?", (value, helper_id))
            rowid = cur.lastrowid
            print('{0}: Updated subskill_1 with {1}'.format(rowid, value))
            con.commit()
        elif command == "skill2":
            cur.execute("SELECT subskill_2 FROM helpers WHERE id = (?)", (helper_id,))
            skill2 = cur.fetchone()[0]
            cur.execute("SELECT name FROM subskills WHERE id = (?)", (skill2,))
            skill2 = cur.fetchone()[0]
            row = cur.execute("SELECT subskill_1, subskill_3, subskill_4, subskill_5 FROM helpers WHERE id = (?)", (helper_id,))
            skills = row.fetchone()
            while True:
                value = input('What is the new subskill for subskill 2? Current skill: {0}. (This is the Lv. 25 Skill). '.format(skill2))
                cur.execute("SELECT id FROM subskills WHERE name LIKE (?)", (value,))
                row = cur.fetchone()
                if row is not None:
                    if row[0] in skills:
                        confirmation = input('{0} already listed. You can only have 1 of each subskill. If you wish to replace anyways, type `confirm`. '.format(value))
                        if confirmation.lower() == "confirm":
                            value = row[0]
                            break
                    else:
                        value = row[0]
                        break
                else:
                    print('{0} is not a valid subskill. Please try again.'.format(value))
            cur.execute("UPDATE helpers SET subskill_2 = ? WHERE id = ?", (value, helper_id))
            rowid = cur.lastrowid
            print('{0}: Updated subskill_2 with {1}'.format(rowid, value))
            con.commit()
        elif command == "skill3":
            cur.execute("SELECT subskill_3 FROM helpers WHERE id = (?)", (helper_id,))
            skill3 = cur.fetchone()[0]
            cur.execute("SELECT name FROM subskills WHERE id = (?)", (skill3,))
            skill3 = cur.fetchone()[0]
            row = cur.execute("SELECT subskill_1, subskill_2, subskill_4, subskill_5 FROM helpers WHERE id = (?)", (helper_id,))
            skills = row.fetchone()
            while True:
                value = input('What is the new subskill for subskill 3? Current skill: {0}. (This is the Lv. 50 Skill). '.format(skill3))
                cur.execute("SELECT id FROM subskills WHERE name LIKE (?)", (value,))
                row = cur.fetchone()
                if row is not None:
                    if row[0] in skills:
                        confirmation = input('{0} already listed. You can only have 1 of each subskill. If you wish to replace anyways, type `confirm`. '.format(value))
                        if confirmation.lower() == "confirm":
                            value = row[0]
                            break
                    else:
                        value = row[0]
                        break
                else:
                    print('{0} is not a valid subskill. Please try again.'.format(value))
            cur.execute("UPDATE helpers SET subskill_3 = ? WHERE id = ?", (value, helper_id))
            rowid = cur.lastrowid
            print('{0}: Updated subskill_3 with {1}'.format(rowid, value))
            con.commit()
        elif command == "skill4":
            cur.execute("SELECT subskill_4 FROM helpers WHERE id = (?)", (helper_id,))
            skill4 = cur.fetchone()[0]
            cur.execute("SELECT name FROM subskills WHERE id = (?)", (skill4,))
            skill4 = cur.fetchone()[0]
            row = cur.execute("SELECT subskill_1, subskill_2, subskill_3, subskill_5 FROM helpers WHERE id = (?)", (helper_id,))
            skills = row.fetchone()
            while True:
                value = input('What is the new subskill for subskill 4? Current skill: {0}. (This is the Lv. 75 Skill). '.format(skill4))
                cur.execute("SELECT id FROM subskills WHERE name LIKE (?)", (value,))
                row = cur.fetchone()
                if row is not None:
                    if row[0] in skills:
                        confirmation = input('{0} already listed. You can only have 1 of each subskill. If you wish to replace anyways, type `confirm`. '.format(value))
                        if confirmation.lower() == "confirm":
                            value = row[0]
                            break
                    else:
                        value = row[0]
                        break
                else:
                    print('{0} is not a valid subskill. Please try again.'.format(value))
            cur.execute("UPDATE helpers SET subskill_4 = ? WHERE id = ?", (value, helper_id))
            rowid = cur.lastrowid
            print('{0}: Updated subskill_4 with {1}'.format(rowid, value))
            con.commit()
        elif command == "skill5":
            cur.execute("SELECT subskill_5 FROM helpers WHERE id = (?)", (helper_id,))
            skill5 = cur.fetchone()[0]
            cur.execute("SELECT name FROM subskills WHERE id = (?)", (skill5,))
            skill5 = cur.fetchone()[0]
            row = cur.execute("SELECT subskill_1, subskill_2, subskill_3, subskill_4 FROM helpers WHERE id = (?)", (helper_id,))
            skills = row.fetchone()
            while True:
                value = input('What is the new subskill for subskill 5? Current skill: {0}. (This is the Lv. 100 Skill). '.format(skill5))
                cur.execute("SELECT id FROM subskills WHERE name LIKE (?)", (value,))
                row = cur.fetchone()
                if row is not None:
                    if row[0] in skills:
                        confirmation = input('{0} already listed. You can only have 1 of each subskill. If you wish to replace anyways, type `confirm`. '.format(value))
                        if confirmation.lower() == "confirm":
                            value = row[0]
                            break
                    else:
                        value = row[0]
                        break
                else:
                    print('{0} is not a valid subskill. Please try again.'.format(value))
            cur.execute("UPDATE helpers SET subskill_5 = ? WHERE id = ?", (value, helper_id))
            rowid = cur.lastrowid
            print('{0}: Updated subskill_5 with {1}'.format(rowid, value))
            con.commit()
        elif command == "nature":
            cur.execute("SELECT nature FROM helpers WHERE id = (?)", (helper_id,))
            nature = cur.fetchone()[0]
            cur.execute("SELECT name FROM natures WHERE id = (?)", (nature,))
            nature = cur.fetchone()[0]
            while True:
                value = input('What is the new nature? Current nature: {0}. '.format(nature))
                cur.execute("SELECT id FROM natures WHERE name LIKE (?)", (value,))
                row = cur.fetchone()
                if row is not None:
                    value = int(row[0])
                    break
                else:
                    print('{0} is not a valid nature. Please try again.'.format(nat))
            cur.execute("UPDATE helpers SET nature = ? WHERE id = ?", (value, helper_id))
            rowid = cur.lastrowid
            print('{0}: Updated nature with {1}'.format(rowid, value))
            con.commit()
        else:
            print('Unrecognized command: {0}.'.format(command))
            print('options: level, ingredient1, ingredient2, ingredient3, skill1, skill2, skill3, skill4, skill5, nature')
    con.close()

@click.command()
def listHelpers():
    with getDB() as con:
        cur = con.cursor()
        cur.execute("SELECT id, pokemon, shiny, level FROM helpers")
        for row in cur.fetchall():
            (helperid, pokemon, shiny, level) = row
            s = ""
            if shiny:
                s = '*'
            print('{0}: Lv.{1} {2} {3}'.format(helperid, level, pokemon, s))
    con.close()
    
@click.command()
@click.argument('helper_id')
def removeHelper(helper_id):
    with getDB() as con:
        cur = con.cursor()
        cur.execute("SELECT pokemon FROM helpers WHERE id = (?)", (helper_id,))
        pokemon = cur.fetchone()[0]
        confirmation = input('Are you sure you want to remove {0}? You cannot undo this action. y/n. '.format(pokemon))
        if confirmation.lower() == "y":
            cur.execute("DELETE FROM helpers WHERE id = ?", (helper_id,))

        con.commit()
    con.close()

cli.add_command(addHelper)
cli.add_command(updateHelper)
cli.add_command(listHelpers)
cli.add_command(removeHelper)

cli()

def main():
    return 0

main()

