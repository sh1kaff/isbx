from aiogram.fsm.state import StatesGroup, State


class CrackState(StatesGroup):
    """Cracking state"""
    working = State()
