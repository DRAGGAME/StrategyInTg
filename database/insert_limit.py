import asyncio

from database.db import PostgresBase


class BuildLimit(PostgresBase):

    async def insert_limit(self, level: int,

                            gold_mines_one: int,
                            gold_mines_two: int,
                            gold_mines_three: int,
                            gold_mines_four: int,
                            gold_mines_five: int,

                            stone_mines_one: int,
                            stone_mines_two: int,
                            stone_mines_three: int,
                            stone_mines_four: int,
                            stone_mines_five: int,

                            homes_one: int,
                            homes_two: int,
                            homes_three: int,
                            homes_four: int,
                            homes_five: int,

                            ranches_one: int,
                            ranches_too: int,
                            ranches_three: int,
                            ranches_four: int,
                            ranches_five: int,

                            barracks_one: int,
                            barracks_two: int,
                            barracks_three: int,
                            barracks_four: int,
                            barracks_five: int,
                            
                            storage: int,
                            villages: int,
                            count_storage: int

    ):

        await self.execute_query(
            """
            INSERT INTO table_limits (
                                Level,
                                
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
                                
                                homes_one,
                                homes_two,
                                homes_three,
                                homes_four,
                                homes_five,

                                ranches_one,
                                ranches_two,
                                ranches_three,
                                ranches_four,
                                ranches_five,
                                
                                barracks_one,
                                barracks_two,
                                barracks_three,
                                barracks_four,
                                barracks_five,

                                storage,
                                villagers,
                                count_storage)
                                
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22, $23, $24);
            """, (level,
                  gold_mines_one, gold_mines_two, gold_mines_three, gold_mines_four, gold_mines_five,
                  stone_mines_one, stone_mines_two, stone_mines_three, stone_mines_four, stone_mines_five,
                  homes_one, homes_two, homes_three, homes_four, homes_five,
                  ranches_one, ranches_too, ranches_three, ranches_four, ranches_five,
                  barracks_one, barracks_two, barracks_three, barracks_four, barracks_five,
                  storage, villages, count_storage))

    async def insert_limit_level_one(self):

        await self.execute_query(
            """
            INSERT INTO table_limits (level) 
            VALUES ($1)
            """, (1, ))

    async def insert_limit_level_ten(self):
        await self.insert_limit(
            10,
            3, 1, 0, 0, 0,
            4, 2, 0, 0, 0,
            10, 10, 0, 0, 0,
            6, 3, 0, 0, 0,
            1, 30, 200
        )

    async def insert_limit_level_twenty(self):
        await self.insert_limit(20,
                                4, 2, 1, 0, 0,
                                5, 2, 1, 0, 0,
                                20, 10, 0, 0, 0,
                                6, 2, 1, 0, 0,
                                1, 50, 500)

    async def insert_limit_level_thirty(self):
        await self.insert_limit(30,
                                4, 2, 1, 1, 0,
                                3, 4, 1, 0, 0,
                                10, 20, 0, 0, 0,
                                6, 2, 3, 0, 0,
                                1, 50, 1000)

if __name__ == '__main__':
    async def create_limits():
        db = BuildLimit()
        await db.connect()
        await db.create_table_limits()
        count = await db.execute_query('''SELECT id FROM table_limits''')
        len_count = len(count)
        if len_count == 1:
            await db.insert_limit_level_ten()
            await db.insert_limit_level_twenty()
            await db.insert_limit_level_thirty()
        elif len_count == 2:
            await db.insert_limit_level_twenty()
            await db.insert_limit_level_thirty()

        elif count == 3:
            await db.insert_limit_level_thirty()
        else:
            await db.insert_limit_level_one()
            await db.insert_limit_level_ten()
            await db.insert_limit_level_twenty()
            await db.insert_limit_level_thirty()
        await db.connect_close()


    asyncio.run(create_limits())
