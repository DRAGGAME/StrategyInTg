import asyncio
import logging
import asyncpg
from config import HOST, PASSWORD, DATABASE, USER

# logging.basicConfig(level=logging.INFO)

pg_host = HOST
pg_user = USER
pg_password = PASSWORD
pg_database = DATABASE

class PostgresBase:

    def __init__(self):
        """Инициализация начальных переменных"""
        self.pool = None

    async def connect(self) -> None:
        try:
            self.pool = await asyncpg.create_pool(
                host=pg_host,
                user=pg_user,
                password=pg_password,
                database=pg_database,
                min_size=1,
                max_size=10000
            )
        except asyncpg.PostgresError as e:
            raise f"Ошибка подключения к базе данных: {e}"

    async def connect_close(self) -> None:
        try:
            if self.pool:
                await self.pool.close()
        except asyncpg.PostgresError as e:
            raise f"Ошибка закрытия подключения к базе данных: {e}"

    async def execute_query(self, query: str, params=None) -> tuple:
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                if params:
                    return await connection.fetch(query, *params)
                return await connection.fetch(query)

    async def create_user_data(self):
        """
        Начальные таблицы с правильными связями.
        """
        # Таблица user_data с правильным именованием полей и типом первичного ключа
        await self.execute_query(
        '''
        CREATE TABLE IF NOT EXISTS user_and_villagers_data (
        Id SERIAL PRIMARY KEY,
        user_id TEXT UNIQUE NOT NULL,
        First_name TEXT NOT NULL,
        Village_name TEXT NOT NULL,
        Level INTEGER DEFAULT 1,
        Message_id TEXT NOT NULL,
        Gold INTEGER DEFAULT 50,
        Stone INTEGER DEFAULT 60,
        Food INTEGER DEFAULT 40,
        Villagers INTEGER DEFAULT 13,
        Villagers_busy INTEGER DEFAULT 5,
        count_new_villagers INTEGER DEFAULT 0,  
        Storages INTEGER DEFAULT 1
        );
        '''
        )


    async def create_table_limits(self):
        await self.execute_query(f"""CREATE TABLE IF NOT EXISTS table_limits (
                                Id SERIAL PRIMARY KEY,
                                Level INTEGER NOT NULL,
                                
                                gold_mines_one INTEGER DEFAULT 2,
                                gold_mines_two INTEGER DEFAULT 0,
                                gold_mines_three INTEGER DEFAULT 0,
                                gold_mines_four INTEGER DEFAULT 0,
                                gold_mines_five INTEGER DEFAULT 0,
                                
                                stone_mines_one INTEGER DEFAULT 4,
                                stone_mines_two INTEGER DEFAULT 0,
                                stone_mines_three INTEGER DEFAULT 0,
                                stone_mines_four INTEGER DEFAULT 0,
                                stone_mines_five INTEGER DEFAULT 0,
                                
                                homes_one INTEGER DEFAULT 10,
                                homes_two INTEGER DEFAULT 0,
                                homes_three INTEGER DEFAULT 0,
                                homes_four INTEGER DEFAULT 0,
                                homes_five INTEGER DEFAULT 0,

                                ranches_one INTEGER DEFAULT 3,
                                ranches_two INTEGER DEFAULT 0,
                                ranches_three INTEGER DEFAULT 0,
                                ranches_four INTEGER DEFAULT 0,
                                ranches_five INTEGER DEFAULT 0,
                                
                                storage INTEGER DEFAULT 3,
                                villagers INTEGER DEFAULT 20,
                                count_storage INTEGER DEFAULT 100);
                                """)

    async def create_table_limit_const(self):
        await self.execute_query("""CREATE TABLE IF NOT EXISTS about_constructions
                                (
                                Id SERIAL PRIMARY KEY,
                                type_construction TEXT NOT NULL,
                                tier INTEGER NOT NULL, 
                                limit_stone INTEGER DEFAULT 18,
                                limit_gold INTEGER DEFAULT 6,
                                limit_village INTEGER DEFAULT 0,
                                limit_food INTEGER DEFAULT 0,
                                production INTEGER DEFAULT 0
                                );
                                """)

    async def insert_default(self, user_id: int, first_name: str, village_name: str, message_id: int) -> None:
        message_id = str(message_id)
        user_id = str(user_id)
        await self.execute_query(
        """
        INSERT INTO user_and_villagers_data (user_id, first_name, village_name, message_id) 
        VALUES ($1, $2, $3, $4)
        """, (user_id, first_name, village_name, message_id))

        await self.execute_query('''INSERT INTO stone_mines_table (user_id) VALUES ($1)''', (user_id, ))
        await self.execute_query('''INSERT INTO gold_mines_table (user_id) VALUES ($1)''', (user_id, ))
        await self.execute_query('''INSERT INTO ranches_table (user_id) VALUES ($1)''', (user_id, ))
        await self.execute_query('''INSERT INTO homes_table (user_id) VALUES ($1)''', (user_id, ))

    async def update_user_data(self, count_stone: int, count_gold: int, count_villages: int, count_village_busy: int,
                               count_mine: int,count_food: int,
                               type_build: str, this_tier: str, last_tier: str, user_id: int):
        user_id = str(user_id)
        await self.execute_query('''
            UPDATE user_and_villagers_data
            SET stone = $1,
                gold = $2,
                villagers = $3,
                villagers_busy = $4,
                food = $5
            WHERE user_id = $6;
        ''', (count_stone, count_gold, count_villages, count_village_busy, count_food, user_id))

        if last_tier:

            # Обновляем {type_build}_table (например, mine_table)
            await self.execute_query(f'''
                UPDATE {type_build}_table
                SET ({type_build}_{last_tier}, {type_build}_{this_tier}) = ($1, $2) 
                WHERE user_id = $3;
            ''', (count_mine-1, count_mine, user_id))
        else:
            # Обновляем {type_build}_table (например, mine_table)
            await self.execute_query(f'''
                UPDATE {type_build}_table
                SET {type_build}_{this_tier} = $1
                WHERE user_id = $2;
            ''', (count_mine, user_id))

if __name__ == "__main__":
    async def dav():
        db = PostgresBase()
        await db.connect()

        # await db.insert_default(12, 'Тест', 'Есс')
        await db.connect_close()

    asyncio.run(dav())

