from aiogram import F, Router
from aiogram import types
from aiogram.fsm.context import FSMContext
from typing import Any, Dict

import markup as markup
import app.classes as classes
import app.base as base

router = Router()

@router.message(classes.giveSell.userId)
async def process_givesell(message: types.Message, state: FSMContext):
    await state.update_data(userId = message.text)
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
            
    position = base.cursor.execute(f"SELECT position_all FROM users WHERE userid = '{userId}' LIMIT 1").fetchone()[0]
    await state.update_data(userId = userId)
    await message.answer(text = f"Какое количество купленных позиций вы хотите установить (всего, т.е. покупки за месяц не изменятся)?\nСейчас (всего): {position}\n\nПример: 15")
    await state.set_state(classes.giveSell.countSell)



@router.message(classes.giveSell.countSell)
async def process_givesell_uid(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer(text = "Вы ввели не число.")
        return    

    data = await state.update_data(countSell = message.text)
    await state.clear()
    await giveSell_(message = message, data = data)

async def giveSell_(message: types.Message, data: Dict[str, Any], positive: bool = True) -> None:
    userId = data["userId"]
    countSell = data["countSell"]

    countSell_old = base.cursor.execute(f"SELECT position_all FROM users WHERE userid = '{userId}' LIMIT 1").fetchone()[0]
    userName = base.cursor.execute(f"SELECT username FROM users WHERE userid = '{userId}' LIMIT 1").fetchone()[0]
        
    base.cursor.execute(f"UPDATE users SET position_all = {countSell} WHERE userid = {userId}")
    base.conn.commit()

    if userName == '@' or userName == '':
        await message.answer(text = f'<b>Вы успешно выдали <code>username не указан</code> [id: <a href="tg://user?id={userId}">{userId}</a>] скидку </b>\n\n\
Было - {countSell_old} шт.\n\
Стало - {countSell} шт.', parse_mode = "html", reply_markup = markup.adminMenu)
    else:
        await message.answer(text = f"<b>Вы успешно выдали {userName} [id: {userId}] скидку </b>\n\n\
Было - {countSell_old} шт.\n\
Стало - {countSell} шт.", parse_mode = "html", reply_markup = markup.adminMenu)