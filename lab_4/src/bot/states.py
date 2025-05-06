from aiogram.fsm.state import StatesGroup, State


class CrackState(StatesGroup):
    working = State()
