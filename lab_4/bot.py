from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio

import logging

from src.bot.handlers import router

from src.config_reader import config


async def main():
    logging.basicConfig(
        level=logging.INFO  
    )

    bot = Bot(
        token=config.api_token.get_secret_value()
    )

    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Exit bot.")
