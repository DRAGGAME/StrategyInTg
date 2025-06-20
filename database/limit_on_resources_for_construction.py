import asyncio

from database.db import PostgresBase


class ResourcesForConstruct(PostgresBase):

    async def query_for_insert(self, type_build: str, tier: int, count_stone: int, count_gold: int, count_village: int, count_food: int, production: int):
        await self.execute_query("""INSERT INTO about_constructions (type_construction, tier, limit_stone, limit_gold, limit_village, limit_food, production)
         VALUES ($1, $2, $3, $4, $5, $6, $7);""", (type_build, tier, count_stone, count_gold, count_village, count_food, production))

    async def limit_resources_for_construct(self):

        await self.query_for_insert('gold_mines_one', 1, 27, 5, 2, 0, 1)
        await self.query_for_insert('gold_mines_two', 2, 54, 10, 3, 0, 2)
        await self.query_for_insert('gold_mines_three', 3, 54, 15, 2, 10, 5)
        await self.query_for_insert('gold_mines_four', 4, 100, 40, 10, 30, 7)
        await self.query_for_insert('gold_mines_five', 5, 400, 100, 100, 60, 16)

        await self.query_for_insert('stone_mines_one', 1, 31, 12, 3, 0, 4)
        await self.query_for_insert('stone_mines_two', 2, 43, 16, 5, 0, 9)
        await self.query_for_insert('stone_mines_three', 3, 54, 15, 2, 10, 16)
        await self.query_for_insert('stone_mines_four', 4, 100, 40, 10, 30, 18)
        await self.query_for_insert('stone_mines_five', 5, 400, 100, 100, 60, 20)

        await self.query_for_insert('ranches_one', 1, 24, 18, 3, 3, 6)
        await self.query_for_insert('ranches_two', 2, 39, 22, 3, 20, 10)
        await self.query_for_insert('ranches_three', 3, 54, 15, 2, 10, 14)
        await self.query_for_insert('ranches_four', 4, 100, 40, 10, 30, 17)
        await self.query_for_insert('ranches_five', 5, 400, 100, 100, 60, 30)

        await self.query_for_insert('homes_one', 1, 31, 12, 0, 0, 0)
        await self.query_for_insert('homes_two', 2, 43, 16, 0, 0, 0)
        await self.query_for_insert('homes_three', 3, 54, 15, 0, 10, 0)
        await self.query_for_insert('homes_four', 4, 100, 40, 0, 20, 0)
        await self.query_for_insert('homes_five', 5, 400, 100, 0, 40, 0)

        await self.query_for_insert('barracks_one', 1, 60, 10, 0, 20, 0)
        await self.query_for_insert('barracks_one', 2, 400, 100, 0, 40, 0)
        await self.query_for_insert('barracks_one', 3, 400, 100, 0, 40, 0)
        await self.query_for_insert('barracks_one', 4, 400, 100, 0, 40, 0)
        await self.query_for_insert('barracks_one', 5, 400, 100, 0, 40, 0)
    

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
