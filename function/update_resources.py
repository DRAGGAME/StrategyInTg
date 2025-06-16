import asyncio


from database.db import PostgresBase

level_string = {
    1: 'one',
    2: 'two',
    3: 'three',
    4: 'four',
    5: 'five'

}

async def update_res(sqlbase: PostgresBase, type_build: str, tier: int, user_id: int) -> (str, int):
    last_tier = ''
    if tier-1 == 0:
        upgrade = False
        this_tier = level_string.get(int(tier))

    else:
        upgrade = True
        this_tier = level_string.get(int(tier))
        last_tier = level_string.get(int(tier-1))

    all_about_resources = await sqlbase.execute_query(f"""SELECT stone, gold, Villagers, Villagers_busy, food, level, 
                                                                {f'{type_build}_{last_tier}, ' if upgrade else ''}
                                                                {type_build}_{this_tier},
                                                                {type_build}_one,
                                                                {type_build}_two,
                                                                {type_build}_three,
                                                                {type_build}_four,
                                                                {type_build}_five
                                                                FROM user_and_villagers_data JOIN {type_build}_table 
                                                                ON {type_build}_table.user_id=user_and_villagers_data.user_id  
                                                                WHERE user_and_villagers_data.user_id = $1 AND {type_build}_table.user_id = $1;""",
                                                      (str(user_id), ))

    count_for_level = await sqlbase.execute_query(f"""SELECT count(*) FROM table_limits;""")

    this_level = all_about_resources[0][5]
    if this_level < 10:
        level = 1
    else:
        level = min((this_level // 10) * 10, count_for_level[0][0] * 10)

    limits_for_construction = await sqlbase.execute_query("""SELECT limit_stone, limit_gold, limit_village, limit_food FROM about_constructions
     WHERE type_construction = $1;""", (f'{type_build}_{this_tier}', ))
    print(level)
    limits = await sqlbase.execute_query(f'''SELECT 
                                                {type_build}_one, 
                                                {type_build}_two,
                                                {type_build}_three,
                                                {type_build}_four, 
                                                {type_build}_five,
                                                {type_build}_{this_tier}
                                                FROM table_limits WHERE level = $1''',
                                         (level,))


    limit_stone = limits_for_construction[0][0]
    limit_gold = limits_for_construction[0][1]
    limit_village = limits_for_construction[0][2]
    limit_food = limits_for_construction[0][3]

    count_stone = all_about_resources[0][0]
    count_gold = all_about_resources[0][1]
    count_village = all_about_resources[0][2]
    count_village_busy = all_about_resources[0][3]
    count_food = all_about_resources[0][4]
    count_build = all_about_resources[0][-1] + all_about_resources[0][-2] + all_about_resources[0][-3] + all_about_resources[0][-4] + all_about_resources[0][-5]
    about_count_build = all_about_resources[0][-6]
    about_last_count_build = all_about_resources[0][-7]

    first_count_stone = count_stone - limit_stone
    first_count_gold = count_gold - limit_gold
    first_count_village = count_village - limit_village
    first_count_village_busy = limit_village + count_village_busy
    first_count_food = count_food - limit_food
    first_count = count_build
    resources_info = [this_level, first_count_gold, first_count_stone, first_count_food, first_count_village, first_count_village_busy, first_count_village+first_count_village_busy]
    for num, resource in enumerate(resources_info):
        if resource < 0:
            resources_info[num] = 0


    if about_last_count_build == 0:
        return 'about_last_count_error', first_count, resources_info

    elif about_count_build + 1 > limits[0][-1]:
        return 'about_count_error', first_count, resources_info

    elif first_count + 1 > limits[0][0] + limits[0][1] + limits[0][2] + limits[0][3] + limits[0][4]:

        return 'count_error', first_count, resources_info

    elif first_count_village < 0:

        return 'village_error', first_count, resources_info

    elif first_count_stone < 0:

        return 'stone_error', first_count, resources_info

    elif first_count_gold < 0:

        return 'gold_error', first_count, resources_info

    elif first_count_food < 0:

        return 'food_error', first_count, resources_info

    else:
        about_count_build += 1

        await sqlbase.update_user_data(first_count_stone, first_count_gold, first_count_village, first_count_village_busy,
                                             about_count_build, first_count_food, type_build, this_tier, last_tier, user_id)
        return 'not_error', about_count_build, resources_info

if __name__ == '__main__':
    async def test():
        sq = PostgresBase()
        await sq.connect()
        await sq.connect_close()
    asyncio.run(test())
