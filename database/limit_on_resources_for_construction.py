import asyncio

from database.db import PostgresBase


class ResourcesForConstruct(PostgresBase):

    async def limit_resources_for_construct(self):

        await self.execute_query("""INSERT INTO limit_for_construction (type_construction, tier, limit_stone, limit_gold, limit_village)
         VALUES ($1, $2, $3, $4, $5);""", ('gold_mines', 1, 27, 5, 2))

        await self.execute_query("""INSERT INTO limit_for_construction (type_construction, tier, limit_stone, limit_gold, limit_village)
         VALUES ($1, $2, $3, $4, $5);""", ('stone_mines', 1, 31, 12, 3))

        await self.execute_query("""INSERT INTO limit_for_construction (type_construction, tier, limit_stone, limit_gold, limit_village, limit_food)
         VALUES ($1, $2, $3, $4, $5, $6);""", ('ranches', 1, 20, 6, 5, 6))

        await self.execute_query("""INSERT INTO limit_for_construction (type_construction, tier, limit_stone, limit_gold)
         VALUES ($1, $2, $3, $4);""", ('homes', 1, 37, 20))

        #
        # await self.execute_query("""INSERT INTO limit_for_construction (type_construction, tier, limit_stone, limit_gold, limit_village)
        #  VALUES ($1, $2, $3, $4);""", ('gold_mines', 2, 27, 5, 2))
        #
        # await self.execute_query("""INSERT INTO limit_for_construction (type_construction, tier, limit_stone, limit_gold, limit_village)
        #  VALUES ($1, $2, $3, $4);""", ('stone_mines', 2, 27, 5, 2))
        #
        # await self.execute_query("""INSERT INTO limit_for_construction (type_construction, tier, limit_stone, limit_gold, limit_village, limit_food)
        #  VALUES ($1, $2, $3, $4, $5);""", ('ranches', 2, 20, 6, 5, 6))
        #
        # await self.execute_query("""INSERT INTO limit_for_construction (type_construction, tier, limit_stone, limit_gold, limit_village)
        #  VALUES ($1, $2, $3, $4);""", ('homes', 2, 27, 5, 2))

if __name__ == "__main__":

    db = ResourcesForConstruct()

    async def create_limits():
        await db.connect()

        await db.limit_resources_for_construct()
        await db.connect_close()

    asyncio.run(create_limits())
