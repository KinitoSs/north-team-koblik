import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers import choosing
from aiogram.fsm.storage.memory import MemoryStorage

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    bot = Bot(token="6505008426:AAE5hepCucaxOPj9iMt7Sr99JV4-lY-klt0")
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(choosing.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())