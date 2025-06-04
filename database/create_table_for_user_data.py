from database.db import PostgresBase


class TableForVillage(PostgresBase):

    async def create_table_stone_mines(self):
        await self.execute_query('''
                                CREATE TABLE IF NOT EXISTS stone_mines_table(
                                user_id TEXT UNIQUE NOT NULL,
                                stone_mines_one INTEGER DEFAULT 1, 
                                stone_mines_too INTEGER DEFAULT 0, 
                                stone_mines_three INTEGER DEFAULT 0, 
                                stone_mines_four INTEGER DEFAULT 0, 
                                stone_mines_five INTEGER DEFAULT 0, 
                                FOREIGN KEY (user_id)  REFERENCES user_and_villagers_data (user_id)
                                );''')

    async def create_table_gold_mines(self):
        await self.execute_query('''
                                CREATE TABLE IF NOT EXISTS gold_mines_table(
                                user_id TEXT UNIQUE NOT NULL,
                                stone_gold_one INTEGER DEFAULT 1, 
                                stone_gold_too INTEGER DEFAULT 0, 
                                stone_gold_three INTEGER DEFAULT 0, 
                                stone_gold_four INTEGER DEFAULT 0 ,
                                stone_gold_five INTEGER DEFAULT 0, 
                                FOREIGN KEY (user_id)  REFERENCES user_and_villagers_data (user_id)
                                );''')

    async def create_table_ranches(self):
        await self.execute_query('''
                                CREATE TABLE IF NOT EXISTS ranches_table(
                                user_id TEXT UNIQUE NOT NULL,
                                ranches_one INTEGER DEFAULT 1, 
                                ranches_too INTEGER DEFAULT 0, 
                                ranches_three INTEGER DEFAULT 0, 
                                ranches_four INTEGER DEFAULT 0 ,
                                ranches_five INTEGER DEFAULT 0, 
                                FOREIGN KEY (user_id)  REFERENCES user_and_villagers_data (user_id)
                                );''')

    async def create_table_home(self):
        await self.execute_query('''
                                CREATE TABLE IF NOT EXISTS homes_table (
                                user_id TEXT UNIQUE NOT NULL,
                                homes_one INTEGER DEFAULT 1, 
                                homes_too INTEGER DEFAULT 0, 
                                homes_three INTEGER DEFAULT 0, 
                                homes_four INTEGER DEFAULT 0 ,
                                homes_five INTEGER DEFAULT 0, 
                                FOREIGN KEY (user_id)  REFERENCES user_and_villagers_data (user_id)
                                );''')

    async def crate_group_table_data(self):

        await self.create_user_data()
        await self.create_table_stone_mines()
        await self.create_table_ranches()
        await self.create_table_home()
