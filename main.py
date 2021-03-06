import asyncio
import config
import logging
from aiogram import Bot, Dispatcher, executor
from subs_postgres import subscriptions
# from subs import subscribers

loop = asyncio.get_event_loop()
#задаем уровень логов
logging.basicConfig(level=logging.INFO)

#initialization of bot
bot = Bot(token=config.API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot,loop= loop)

#initializing db
db = subscriptions('subscriptions')
#db = subscribers('subsdb.db')
async def scheduled(wait_for):
    from exrate import get_dollar
    while True:
        await asyncio.sleep(wait_for)
        subscribtions = db.get_subscriptions()
        for s in subscribtions:
            await bot.send_message(s[1],
                               f"Курс доллара к рублю {get_dollar()}\nУдачного дня☺")

#execute polling
if __name__=='__main__':
    from handlers import dp,send_to_admin
    dp.loop.create_task(scheduled(300))
    executor.start_polling(dp,skip_updates=True)#,on_startup=send_to_admin)
print("Hello world!")