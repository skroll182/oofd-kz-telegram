from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from oofd_kz_telegram.handlers import (
    handle_add_ticket,
    handle_add_ticket_by_qr,
    handle_qr_photo,
    handle_start,
)
from oofd_kz_telegram.settings import Settings
from oofd_kz_telegram.states import States


def build_dispatcher():
    bot = Bot(token=Settings.api_token)
    dispatcher = Dispatcher(bot, storage=MemoryStorage())
    dispatcher.register_message_handler(handle_start, commands=["start"])
    dispatcher.register_message_handler(
        handle_add_ticket, Text("Добавить чек"), state=States.choice
    )
    dispatcher.register_message_handler(
        handle_add_ticket_by_qr, Text("Добавить по QR коду"), state=States.add_ticket
    )
    dispatcher.register_message_handler(
        handle_qr_photo, content_types=["photo"], state=States.add_ticket_by_qr
    )
    return dispatcher
