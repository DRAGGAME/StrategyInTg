import asyncio

from database.db import PostgresBase


class ResourcesForConstruct(PostgresBase):

    async def create_table(self):
        await self.execute_query("""CREATE TABLE IF NOT EXISTS limit_for_construction 
                                (
                                Id SERIAL PRIMARY KEY,
                                type_construction TEXT,
                                limit_stone INTEGER DEFAULT 18,
                                limit_gold INTEGER DEFAULT 6,
                                limit_village INTEGER DEFAULT 0,
                                limit_food INTEGER DEFAULT 0
                                );
                                """)

    async def limit_resources_for_construct(self):
        await self.execute_query("""INSERT INTO limit_for_construction (type_construction, limit_stone, limit_gold, limit_village)
         VALUES ($1, $2, $3, $4);""", ('gold_mines', 27, 5, 2))

        await self.execute_query("""INSERT INTO limit_for_construction (type_construction, limit_stone, limit_gold, limit_village)
         VALUES ($1, $2, $3, $4);""", ('stone_mines', 31, 12, 3))

        await self.execute_query("""INSERT INTO limit_for_construction (type_construction, limit_stone, limit_gold, limit_village, limit_food)
         VALUES ($1, $2, $3, $4, $5);""", ('ranches', 20, 6, 5, 6))

        await self.execute_query("""INSERT INTO limit_for_construction (type_construction, limit_stone, limit_gold)
         VALUES ($1, $2, $3);""", ('homes', 37, 20))


if __name__ == "__main__":

    db = ResourcesForConstruct()

    async def create_limits():
        await db.connect()
        await db.create_table()
        await db.limit_resources_for_construct()
        await db.connect_close()

    asyncio.run(create_limits())
