import logging
import pathlib
from tempfile import NamedTemporaryFile

from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from oofd_kz_parser.exceptions import QRNotFoundException
from oofd_kz_parser.parser import parse_from_qr
from oofd_kz_telegram.states import States
from PIL import Image

logger = logging.getLogger()


async def handle_start(message: Message):
    reply_keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True).add(
        KeyboardButton("Добавить чек")
    )
    await message.bot.send_message(
        chat_id=message.chat.id,
        text=f"Выбери действие",
        reply_markup=reply_keyboard,
    )

    await States.choice.set()


async def handle_add_ticket(message: Message):
    chat_id = message.chat.id
    await message.bot.send_message(
        chat_id=chat_id,
        text="Каким способом добавить чек?",
        reply_markup=(
            ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2).add(
                KeyboardButton("Добавить по QR коду"),
            )
        ),
    )
    await States.add_ticket.set()


async def handle_add_ticket_by_qr(message: Message):
    chat_id = message.chat.id

    await message.bot.send_message(chat_id=chat_id, text="Отправь фото QR кода с чека")

    await States.add_ticket_by_qr.set()


async def handle_qr_photo(message: Message):
    photo_file_name = pathlib.Path(NamedTemporaryFile(suffix=".jpg").name)
    await message.photo[-1].download(destination_file=photo_file_name)
    img = Image.open(photo_file_name)
    try:
        ticket = parse_from_qr(img)
        ticket_text = ticket.json(indent=2)
        message_chunks = [
            ticket_text[i * 4096 : (i * 4096) + 4096] for i in range(round(len(ticket_text) / 4096))
        ]
        for message_chunk in message_chunks:
            await message.bot.send_message(chat_id=message.chat.id, text=message_chunk)
        await handle_start(message)
    except QRNotFoundException:
        await message.bot.send_message(chat_id=message.chat.id, text="Не удалось распознать QR код")
        await handle_add_ticket_by_qr(message)
    finally:
        photo_file_name.unlink()
