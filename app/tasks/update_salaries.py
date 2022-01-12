import asyncio
from time import time

from app.utils import get_last_q_hour, QUARTER_HOUR


class UpdateSalariesTask:

    def __init__(self, manager):
        self.manager = manager

    async def update_salaries(self):
        print('Updating salaries...')
        await self.manager.update_salaries()
