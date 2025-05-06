from aiogram import Router
from aiogram.types import Message, BufferedInputFile
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.chat_action import ChatActionSender

import asyncio

from src.bot.states import CrackState
from src.cracker.hash_cracker import crack_hash_with_mp
from src.cracker.crack_time import get_crack_stats
from src.cracker.utils import visual_crack_stats, card_is_luhn_correct


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
    args = message.text.split(" ", maxsplit=4)[1:]
    if len(args) != 4:
        await message.answer("Right command: `/crack hash_alg target_hash bin_code last_digits`")
        return

    hash_alg, target_hash, bin_code, last_digits = args

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
            hash_alg,
        )

    if crack_result is None:
        await message.answer("Sorry, no result :(")
        await state.set_state(CrackState.working)
        return

    await message.answer(f"Cracked! Result: {crack_result}")

    await state.clear()


@router.message(
    StateFilter(None),
    Command("crack_time"),
)
async def cmd_crack_time(
    message: Message,
    state: FSMContext,
):
    args = message.text.split(" ", maxsplit=4)[1:]
    if len(args) != 4:
        await message.answer("Right command: `/crack_time hash_alg target_hash bin_code last_digits`")
        return

    hash_alg, target_hash, bin_code, last_digits = args

    if len(bin_code) != 6:
        await message.answer("Bin = 6 digits")
        return

    if len(last_digits) != 4:
        await message.answer("last_digits = 4 digits")
    
    await state.set_state(CrackState.working)

    await message.answer("Processing...")
    
    async with ChatActionSender.choose_sticker(bot=message.bot, chat_id=message.chat.id):
        crack_time_stats = []
        cores_stats = []
        for stat in get_crack_stats(target_hash, last_digits, bin_code, hash_alg):
            crack_time_stats.append(stat["crack_time"])
            cores_stats.append(stat["cores"])
        
        print("crack time:", crack_time_stats)
        print("cores:", cores_stats)

        buffer = await asyncio.to_thread(
            visual_crack_stats,
            cores_stats,
            crack_time_stats,
        )

        await message.answer_photo(
            photo=BufferedInputFile(file=buffer.getvalue(), filename="stats.jpg"),
            caption=f"Stats for {hash_alg} hash:"
        )

    await state.clear()


@router.message(
    StateFilter(None),
    Command("luhn"),
)
async def cmd_luhn(
    message: Message,
):
    args = message.text.split(" ", maxsplit=1)
    if len(args) != 2:
        await message.answer("Right command: `/luhn card`")
        return

    card = args[-1]

    correct = card_is_luhn_correct(card)

    await message.answer(
        f"Card {card} is {'' if correct else 'not'} correct."
    )
