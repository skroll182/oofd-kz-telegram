from aiogram.dispatcher.filters.state import State, StatesGroup


class States(StatesGroup):
    choice = State()
    list_tickets = State()
    add_ticket = State()
    add_ticket_by_qr = State()
    add_ticket_by_parameters = State()
