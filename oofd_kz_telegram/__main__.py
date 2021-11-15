from aiogram import executor
from oofd_kz_telegram.bot import build_dispatcher

if __name__ == "__main__":
    executor.start_polling(build_dispatcher(), skip_updates=True)
