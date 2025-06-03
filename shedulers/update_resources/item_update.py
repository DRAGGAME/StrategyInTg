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
        all_about_resources = await sqlbase_for_stone.execute_query("""SELECT stone, gold, food, stone_mines, gold_mines,
                                                                    ranches, storages, level, villagers
                                                                    FROM user_and_villagers_data WHERE user_id = $1""",
                                                            (user_id, ))
        count_for_level = await sqlbase_for_stone.execute_query("""SELECT count(*) FROM table_limits;""")
        level = int(all_about_resources[0][-2])
        for multiplication in range(count_for_level[0][0] + 1, 1, -1):

            if level >= multiplication * 10 and count_for_level[0][0] >= multiplication:
                level = multiplication * 10
                break
            elif level < 10:
                level = 1
                break


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
        count_stone_mines = all_about_resources[0][3]
        count_gold_mines = all_about_resources[0][4]
        count_food_ranches = all_about_resources[0][5]
        count_storage = all_about_resources[0][6]

        print(f'Количество камня: {count_stone}\n'
              f'Количество золота: {count_gold}\n'
              f'Количество еды: {count_food}\n'
              f'Количество каменных шахт: {count_stone_mines}\n'
              f'Количество золотых шахт: {count_gold_mines}\n'
              f'Количество ферм: {count_food_ranches}')

        if count_storage != 0:
            limit = count_storage*limit_count_storage # Высчитываем лимит хранилища
            print(f'Лимит хранилища - {limit}')

            first_count_stone = 4 * count_stone_mines + count_stone
            first_count_gold = 2 * count_gold_mines + count_gold
            first_count_food = 2 * count_food_ranches + count_food

            print(f'Количество камня для добавления - {1 * count_stone_mines}. Всего: {1 * count_stone_mines+count_stone}')
            print(f'Количество золота для добавления - {2 * count_gold_mines}. Всего: {1 * count_gold_mines+count_gold}')
            print(f'Количество еды для добавления - {1 * count_food_ranches}. Всего: {1 * count_food_ranches+count_food}')

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

            await bot.send_message(user_id=user_id, text='У вас отсутствуют хранилища. Склады переполнены')

    except Exception as e:
        logging.error(f'Задача не работает. Ошибка: {e}')
        item_schedulers.remove_job(job_id=f'farm{user_id}')

    await sqlbase_for_stone.connect_close()



