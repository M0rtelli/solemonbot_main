from aiogram import F, Router
from aiogram import types
from aiogram.fsm.context import FSMContext
from typing import Any, Dict

import markup as markup
import app.classes as classes
import app.base as base


router = Router()

@router.message(classes.giveDiscount.userId)
async def process_givediscount_uid(message: types.Message, state: FSMContext):
    
    userId = 0
    userName = ''
    if not message.text.isdigit():
        try:
            userId = base.cursor.execute(f"SELECT userid FROM users WHERE username = '{message.text}' LIMIT 1").fetchone()[0]
            userName += message.text
        except:
            await message.answer(text = "Данного пользователя не существует.\nВозможно ошибка в правильности ввода", reply_markup = markup.adminMenu)
            await state.clear()
            return
    else:
        userId = message.text
        try:
            userName += base.cursor.execute(f"SELECT username FROM users WHERE userid = '{message.text}' LIMIT 1").fetchone()[0]
        except:
            await message.answer(text = "Данного пользователя не существует.\nВозможно ошибка в правильности ввода", reply_markup = markup.adminMenu)
            await state.clear()
            return
    
    # Выдача скидки
    await state.update_data(userId = userId)
    await message.answer(text = "Какую скидку Вы хотите установить? Введите цифру\n\nПример: 15")

    await state.set_state(classes.giveDiscount.discount)

@router.message(classes.giveDiscount.discount)
async def process_givediscount_uid(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        # ошибка, не число
        await message.answer(text = "Вы ввели не число.")
        return    

    data = await state.update_data(discount = message.text)
    await state.clear()
    await giveDiscount_(message = message, data = data)

async def giveDiscount_(message: types.Message, data: Dict[str, Any], positive: bool = True) -> None:
    userId = data["userId"]
    discount = data["discount"]
    # language = data.get("language", "<something unexpected>")
    # Выдача +1 к позициям
    discount_old = base.cursor.execute(f"SELECT discount FROM users WHERE userid = '{userId}' LIMIT 1").fetchone()[0]
    userName = base.cursor.execute(f"SELECT username FROM users WHERE userid = '{userId}' LIMIT 1").fetchone()[0]
        
    base.cursor.execute(f"UPDATE users SET discount = {discount} WHERE userid = {userId}")
    base.conn.commit()

    await message.answer(text = f"<b>Вы успешно выдали {userName} [id: {userId}] скидку </b>\n\n\
Было - {discount_old}%\n\
Стало - {discount}%", parse_mode = "html", reply_markup = markup.adminMenu)