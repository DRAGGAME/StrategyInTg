from aiohttp import streamer

from database.db import PostgresBase

async def update_res(sqlbase: PostgresBase, type_build: str, user_id: int):
    limits = await sqlbase.execute_query("""SELECT limit_stone, limit_gold, limit_village, limit_food FROM limit_for_construction
     WHERE type_construction = $1;""", (type_build, ))

    all_about_resources = await sqlbase.execute_query(f"""SELECT stone, gold, Villagers, Villagers_busy, food, {type_build}
                                                                FROM user_and_villagers_data WHERE user_id = $1""",
                                                                (str(user_id), ))

    limit_stone = limits[0][0]
    limit_gold = limits[0][1]
    limit_village = limits[0][2]
    limit_food = limits[0][3]

    count_stone = all_about_resources[0][0]
    count_gold = all_about_resources[0][1]
    count_village = all_about_resources[0][2]
    count_village_busy = all_about_resources[0][3]
    count_food = all_about_resources[0][4]
    count_gold_mines = all_about_resources[0][5]

    first_count_stone = count_stone - limit_stone
    first_count_gold = count_gold - limit_gold
    first_count_village = count_village - limit_village
    first_count_village_busy = limit_village + count_village_busy
    first_count_food = count_food - limit_food
    first_count_gold_mines = count_gold_mines + 1

    if first_count_village < 0:

        return 'village_error', first_count_gold_mines

    elif first_count_stone < 0:

        return 'stone_error', first_count_gold_mines

    elif first_count_gold < 0:

        return 'gold_error', first_count_gold_mines

    else:
        await sqlbase.update_user_data(first_count_stone, first_count_gold, first_count_village, first_count_village_busy,
                                             first_count_gold_mines, first_count_food, type_build, user_id)
        return 'not_error', first_count_gold_mines