import asyncio
from time import time

from discord.ext import tasks

from app.utils import get_last_q_hour, QUARTER_HOUR


class UpdateSalariesTask:

    def __init__(self, manager):
        self.manager = manager

    async def setup(self):
        print((get_last_q_hour() + QUARTER_HOUR) - time())
        await asyncio.sleep((get_last_q_hour() + QUARTER_HOUR) - time())
        self.update_salaries.start()

    @tasks.loop(minutes=QUARTER_HOUR // 60)
    async def update_salaries(self):
        print('Updating salaries...')
        await self.manager.update_salaries()
