import asyncio

from database.db import PostgresBase


class BuildLimit(PostgresBase):

    async def insert_limit_level_one(self):

        await self.execute_query(
            """
            INSERT INTO table_limits (level) 
            VALUES ($1)
            """, (1, ))

    async def insert_limit_level_ten(self):

        await self.execute_query(
            """
            INSERT INTO table_limits (
            level,
            gold_mines,
            stone_mines,
            homes,
            ranches,
            storage,
            villages,
            count_storage) 
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8);
            """, (10, 5, 6, 10, 3, 4, 22, 100))

    async def insert_limit_level_twenty(self):
        await self.execute_query(
            """
            INSERT INTO table_limits (
            level,
            gold_mines,
            stone_mines,
            homes,
            ranches,
            storage,
            villages,
            count_storage) 
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8);
            """, (20, 10, 10, 20, 6, 8, 50, 700))

    async def insert_limit_level_thirty(self):
        await self.execute_query(
            """
            INSERT INTO table_limits (
            level,
            gold_mines,
            stone_mines,
            homes,
            ranches,
            storage,
            villages,
            count_storage) 
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8);
            """, (30, 10, 10, 49, 6, 8, 100, 1000))

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
