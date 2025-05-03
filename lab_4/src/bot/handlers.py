from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.chat_action import ChatActionSender

import asyncio

from src.bot.states import CrackState
from src.cracker.hash_cracker import crack_hash_with_mp
from src.cracker.algorithm import card_is_correct


router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Select command: ...")


@router.message(
    StateFilter(None),
    Command("crack"),
)
async def cmd_crack(
    message: Message,
    state: FSMContext,
):
    args = message.text.split(" ", maxsplit=3)[1:]
    if len(args) != 3:
        await message.answer("Right command: `/crack target_hash bin_code last_digits`")
        return

    target_hash, bin_code, last_digits = args

    if len(bin_code) != 6:
        await message.answer("Bin = 6 digits")
        return

    if len(last_digits) != 4:
        await message.answer("last_digits = 4 digits")
    
    await state.set_state(CrackState.working)
    
    async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
        crack_result = await asyncio.to_thread(
            crack_hash_with_mp,
            target_hash,
            last_digits,
            bin_code,
        )

    if crack_result is None:
        await message.answer("Sorry, no result :(")
        return

    await message.answer(f"Cracked! Result: {crack_result}")

    await state.clear()


@router.message(
    StateFilter(None),
    Command("luhn"),
)
async def cmd_luhn(
    message: Message,
    state: FSMContext,
):
    args = message.text.split(" ", maxsplit=1)
    if len(args) != 2:
        await message.answer("Right command: `/luhn card`")
        return

    card = args[-1]

    correct = card_is_correct(card)

    await message.answer(
        f"Card {card} is {'' if correct else 'not'} correct."
    )
