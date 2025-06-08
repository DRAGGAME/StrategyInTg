import logging
from config import bot
from database.db import PostgresBase
from shedulers.update_resources.scheduler_object import item_schedulers


async def item_update(user_id: int):
    """Обработчик для пополнения всех ресурсов"""
    sqlbase_for_stone = PostgresBase()
    await sqlbase_for_stone.connect()

    try:
        user_id = str(user_id)

        production = await sqlbase_for_stone.execute_query("""SELECT production FROM about_constructions ORDER BY id ASC""")

        all_about_resources = await sqlbase_for_stone.execute_query("""SELECT stone, gold, food, 
        
                                                                        gold_mines_one,
                                                                        gold_mines_two,
                                                                        gold_mines_three,
                                                                        gold_mines_four,
                                                                        gold_mines_five,
                                                                             
                                                                        stone_mines_one,
                                                                        stone_mines_two,
                                                                        stone_mines_three,
                                                                        stone_mines_four,
                                                                        stone_mines_five,
                                                                        
                                                                        ranches_one,
                                                                        ranches_two,
                                                                        ranches_three,
                                                                        ranches_four,
                                                                        ranches_five,
                                                                        
                                                                        storages, level, villagers
                                                                        
                                                                        FROM user_and_villagers_data
                                                                        
                                                                        INNER JOIN gold_mines_table ON user_and_villagers_data.user_id = gold_mines_table.user_id
                                                                        INNER JOIN stone_mines_table ON user_and_villagers_data.user_id = stone_mines_table.user_id
                                                                        INNER JOIN ranches_table ON user_and_villagers_data.user_id = ranches_table.user_id
                                                                        
                                                                        WHERE user_and_villagers_data.user_id = $1 AND 
                                                                        gold_mines_table.user_id = $1 AND 
                                                                        stone_mines_table.user_id = $1 AND 
                                                                         ranches_table.user_id = $1""",
                                                            (user_id, ))

        level = int(all_about_resources[0][-2])

        count_for_level = await sqlbase_for_stone.execute_query("""SELECT count(*) FROM table_limits;""")
        if level < 10:
            level = 1
        else:
            level = min((level // 10) * 10, count_for_level[0][0] * 10)
        limit = await sqlbase_for_stone.execute_query("""SELECT count_storage FROM table_limits 
                                                                WHERE level = $1""",
                                                                (level, ))
        if limit:
            pass
        else:
            return

        limit_count_storage = limit[0][0]

        count_stone = all_about_resources[0][0]
        count_gold = all_about_resources[0][1]
        count_food = all_about_resources[0][2]
        count_storage = all_about_resources[0][-3]

        print(f'Количество камня: {count_stone}\n'
              f'Количество золота: {count_gold}\n'
              f'Количество еды: {count_food}')

        if count_storage != 0:
            limit = count_storage*limit_count_storage # Высчитываем лимит хранилища
            print(f'Лимит хранилища - {limit}')

            first_count_gold = (all_about_resources[0][-18]*production[0][0] + all_about_resources[0][-17]*production[1][0] +
                                all_about_resources[0][-16]*production[2][0] + all_about_resources[0][-15]*production[3][0] +
                                all_about_resources[0][-14]*production[4][0]) + count_gold

            first_count_stone = (all_about_resources[0][-13]*production[5][0] + all_about_resources[0][-12]*production[6][0] +
                                all_about_resources[0][-11]*production[7][0] + all_about_resources[0][-10]*production[8][0] +
                                all_about_resources[0][-9]*production[9][0]) + count_stone

            first_count_food = (all_about_resources[0][-8]*production[10][0] + all_about_resources[0][-7]*production[11][0] +
                                all_about_resources[0][-6]*production[12][0] + all_about_resources[0][-5]*production[13][0] +
                                all_about_resources[0][-4]*production[14][0]) + count_food

            print(f'Всего: {first_count_gold}')
            print(f'Всего: {first_count_stone}')
            print(f'Всего: {first_count_food}')

            if first_count_stone > limit:
                first_count_stone = limit
                logging.info('Хранилище камня переполненно.')
            if first_count_gold > limit:
                first_count_gold = limit
                logging.info('Хранилище золота переполненно.')
            if first_count_food > limit:
                first_count_food = limit
                logging.info('Хранилище еды переполненно.')

            await sqlbase_for_stone.execute_query("""UPDATE user_and_villagers_data
                                                    SET (stone, gold, food) = ($1, $2, $3)
                                                    WHERE user_id = $4""",
                                                  (first_count_stone, first_count_gold, first_count_food, user_id))
            logging.info('Хранилища пополнены')
        else:
            logging.info('Хранилища не существует')

            logging.info('У вас отсутствуют хранилища. Склады переполнены')
        await sqlbase_for_stone.connect_close()

    except Exception as e:
        logging.error(f'Задача не работает. Ошибка: {e}')
        item_schedulers.remove_job(job_id=f'farm{user_id}')
    finally:
        pass



