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
@click.argument('dish_type')
@click.argument('berry_1')
@click.argument('berry_2')
@click.argument('berry_3')
def getBestTeam(dish_type, berry_1, berry_2, berry_3):
    with getDB() as con:
        cur = con.cursor()
        cur.execute("""
            WITH dishes AS (
                SELECT name, base_strength AS strength
                FROM recipes
                WHERE dish_type LIKE ?
                GROUP BY base_strength, name
            )
            SELECT
                ((d.strength / 1000.0) * r.leek) AS leek,
                ((d.strength / 1000.0) * r.mushroom) AS mushroom,
                ((d.strength / 1000.0) * r.egg) AS egg,
                ((d.strength / 1000.0) * r.potato) AS potato,
                ((d.strength / 1000.0) * r.apple) AS apple,
                ((d.strength / 1000.0) * r.herb) AS herb,
                ((d.strength / 1000.0) * r.sausage) AS sausage,
                ((d.strength / 1000.0) * r.milk) AS milk,
                ((d.strength / 1000.0) * r.honey) AS honey,
                ((d.strength / 1000.0) * r.oil) AS oil,
                ((d.strength / 1000.0) * r.ginger) AS ginger,
                ((d.strength / 1000.0) * r.tomato) AS tomato,
                ((d.strength / 1000.0) * r.cacao) AS cacao,
                ((d.strength / 1000.0) * r.tail) AS tail,
                ((d.strength / 1000.0) * r.soybeans) AS soybeans,
                ((d.strength / 1000.0) * r.corn) AS corn
            FROM dishes AS d
            JOIN recipes AS r ON
                d.name = r.name
            ORDER BY r.base_strength DESC, d.name ASC;
            """, (dish_type,))
        ingredient_scores = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        rows = cur.fetchall()
        for row in rows:
            ingredient_scores[0] += row[0]
            ingredient_scores[1] += row[1]
            ingredient_scores[2] += row[2]
            ingredient_scores[3] += row[3]
            ingredient_scores[4] += row[4]
            ingredient_scores[5] += row[5]
            ingredient_scores[6] += row[6]
            ingredient_scores[7] += row[7]
            ingredient_scores[8] += row[8]
            ingredient_scores[9] += row[9]
            ingredient_scores[10] += row[10]
            ingredient_scores[11] += row[11]
            ingredient_scores[12] += row[12]
            ingredient_scores[13] += row[13]
            ingredient_scores[14] += row[14]
            ingredient_scores[15] += row[15]
        cur.execute("SELECT type FROM berries WHERE berry LIKE ? OR berry LIKE ? OR berry LIKE ?", (berry_1, berry_2, berry_3))
        berry_types = cur.fetchone()
        cur.execute("SELECT * FROM helpers")
        helpers = cur.fetchall()
        helper_scores = []
        choices = ["leek", "mushroom", "egg", "potato", "apple", "herb", "sausage", "milk", "honey", "oil", "ginger", "tomato", "cacao", "tail", "soybeans", "corn"]
        for row in helpers:
            score = 0
            cur.execute("SELECT type FROM pokemon WHERE pokedex_num = ?", (row[1],))
            typing = cur.fetchone()[0]
            if typing in berry_types:
                score += 500
            i = choices.index(row[5].lower())
            score += ingredient_scores[i]
            i = choices.index(row[6].lower())
            score += ingredient_scores[i]
            i = choices.index(row[7].lower())
            score += ingredient_scores[i]
            helper_scores.append((score, row[2], row[3], row[4]))

        helper_scores.sort(reverse = True)
        j = 0
        for i in range(len(helper_scores)):
            j += 1
            pokemon = helper_scores[i]
            s = ""
            if pokemon[2] == 1:
                s = "*"
            print('{0}{1} Lv. {2}'.format(pokemon[1], s, pokemon[3]))
            if j == 5:
                break

    con.close()

cli.add_command(getBestTeam)

cli()

def main():
    return 0

main()
