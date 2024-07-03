from aiogram import F, Router
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest 

import logging
import asyncio

import markup as markup
import app.classes as classes
import app.base as base
import app.functions as function
import app.localdata.load as localdata
from contextlib import suppress

router = Router()

@router.message(classes.selectUser.startDB)
async def sellAdMessage(message: types.Message, state: FSMContext):
    count = 0
    count_all = 0
    try:
        for row in range(len(localdata.localUsers)):
            
            if await function.send_message_to_users_handler( int( localdata.localUsers[row]["userid"] ) , message.text, False, message):
            # print(f'user - {localdata.localUsers[row]["userid"]}')
                count += 1
            count_all += 1
            # 20 messages per second (Limit: 30 messages per second)
            await asyncio.sleep(.05)
    finally:
        logging.info(f"{count} messages successful sent.")
        await message.answer(f"{count} из {count_all} сообщений успешно отправлено.")
        await state.clear()

@router.message(classes.selectUser.userId)
async def process_userinfo(message: types.Message, state: FSMContext):
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
        
    # Выдача инфы о пользователе
    
    position_all = base.cursor.execute(f"SELECT position_all FROM users WHERE userid = '{userId}' LIMIT 1").fetchone()[0]
    position_month = base.cursor.execute(f"SELECT position_month FROM users WHERE userid = '{userId}' LIMIT 1").fetchone()[0]

    temp_discount = base.cursor.execute(f"SELECT temp_discount FROM users WHERE userid = \'{userId}\' LIMIT 1").fetchone()[0]
    top_discount = base.cursor.execute(f"SELECT top_discount FROM users WHERE userid = \'{userId}\' LIMIT 1").fetchone()[0]

    discount = base.cursor.execute(f"SELECT discount FROM users WHERE userid = '{userId}' LIMIT 1").fetchone()[0]
    changePosition = [
        [
            types.InlineKeyboardButton(text="-1", callback_data = f"num_decr_{userId}"),
            types.InlineKeyboardButton(text="+1", callback_data = f"num_incr_{userId}")
        ]    
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard = changePosition)
    nl = '\n'
    text = f"<b>Информация о пользователе {userName} [id: {userId}]</b>\n\n\
Количество покупок (всего): {position_all}\n\
Количество покупок (за месяц): {position_month}\n\
Получаемая скидка: {discount}\n\
{f'{nl}<code>Действует скидка {top_discount}% на этот месяц (не складывается с основной скидкой)!</code>{nl}' if int(top_discount) > 0 else ''}\
{f'{nl}<code>Действует временная скидка {temp_discount}%!</code>{nl}' if int(temp_discount) > 0 else ''}\
\n<i>Ниже можно нажать на '+1' или '-1' для изменения количества покупок ЗА МЕСЯЦ</i>"
    await message.answer(text = text, parse_mode = "html", reply_markup = keyboard)
    msg = await message.answer(text = "Вы перешли в <b>меню-администратора</b>.", parse_mode = "html", reply_markup = markup.adminMenu)
    # await bot.delete_message(chat_id = msg.chat.id, message_id = int(msg.message_id))
    # await msg.edit_reply_markup(reply_markup = keyboard)

    await state.clear()

@router.callback_query(F.data.startswith("num_"))
async def callbacks_num(callback: types.CallbackQuery):
    with suppress(TelegramBadRequest):
        action = callback.data.split("_")[1]
        userId = callback.data.split("_")[2]
        changePosition = [
            [
                types.InlineKeyboardButton(text="-1", callback_data = f"num_decr_{userId}"),
                types.InlineKeyboardButton(text="+1", callback_data = f"num_incr_{userId}")
            ]    
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard = changePosition)

        userName = ''
        try:
            userName += base.cursor.execute(f"SELECT username FROM users WHERE userid = '{userId}' LIMIT 1").fetchone()[0]
        except:
            await callback.message.answer(text = "Данного пользователя не существует.\nВозможно ошибка в правильности ввода", reply_markup = markup.adminMenu)
            await callback.answer()
            return
            
        # Выдача инфы о пользователе
        
        position_all = base.cursor.execute(f"SELECT position_all FROM users WHERE userid = '{userId}' LIMIT 1").fetchone()[0]
        position_month = base.cursor.execute(f"SELECT position_month FROM users WHERE userid = '{userId}' LIMIT 1").fetchone()[0]
        discount = base.cursor.execute(f"SELECT discount FROM users WHERE userid = '{userId}' LIMIT 1").fetchone()[0]
        temp_discount = base.cursor.execute(f"SELECT temp_discount FROM users WHERE userid = \'{userId}\' LIMIT 1").fetchone()[0]
        top_discount = base.cursor.execute(f"SELECT top_discount FROM users WHERE userid = \'{userId}\' LIMIT 1").fetchone()[0]

        if action == "incr": # выдача +1 покупки
            try:
                position_all += 1
                position_month += 1
                base.cursor.execute(f"UPDATE users SET position_all = position_all + 1 WHERE userid = {userId}")
                base.conn.commit()
                base.cursor.execute(f"UPDATE users SET position_month = position_month + 1 WHERE userid = {userId}")
                try:
                    await callback.bot.send_message(chat_id = userId, text = f"<b>@{callback.from_user.username} выдал Вам +1 покупку</b>\n\n\
Благодарим Вас за покупку!", parse_mode = "html")
                except:
                    pass
            except:
                pass

            # check referal
            try:
                if int(base.cursor.execute(f"SELECT active FROM referals WHERE uid_referal = '{userId}'").fetchone()[0]) == 0:
                    base.cursor.execute(f"UPDATE referals SET active = 1 WHERE uid_referal = '{userId}'")
                    base.conn.commit()
                    uid = int(base.cursor.execute(f'SELECT uid_shared FROM referals WHERE uid_referal = \'{userId}\'').fetchone()[0])
                    if int(base.cursor.execute(f"SELECT temp_discount FROM users WHERE userid = '{uid}'").fetchone()[0]) < 26:
                        
                        base.cursor.execute(f"UPDATE users SET temp_discount = temp_discount + 5 WHERE userid = {uid}")
                        base.conn.commit()
                        try:
                            await callback.bot.send_message(chat_id = uid, text = f"<b>Ваш реферал {userName} [ID: <a href=\"tg://user?id={userId}\">{userId}</a>] совершил покупку, тем самым став активным.</b>\n\
    Вам начислено 5% скидки на следующую покупку!", parse_mode = "html")
                        except:
                            pass
                    else:
                        try:
                            await callback.bot.send_message(chat_id = uid, text = f"ПРЕДУПРЕЖДЕНИЕ!\n\n<b>Ваш реферал {userName} [ID: <a href=\"tg://user?id={userId}\">{userId}</a>] совершил покупку, тем самым став активным.</b>\n\
    Временная скидка не может превышать 30%", parse_mode = "html")
                        except:
                            pass
            except:
                pass
                
            # check temp discount 
            if int(base.cursor.execute(f"SELECT temp_discount FROM users WHERE userid = \'{userId}\'").fetchone()[0]) > 0:
                base.cursor.execute(f"UPDATE users SET temp_discount = 0 WHERE userid = {userId}")
                base.conn.commit()
                try:
                    await callback.bot.send_message(chat_id = userId, text = f"<b>Ваша временная скидка была потрачена!</b>", parse_mode = "html")
                except:
                    pass

            

        elif action == "decr": # выдача -1 покупки
            position_all -= 1
            position_month -= 1
            base.cursor.execute(f"UPDATE users SET position_all = position_all - 1 WHERE userid = {userId}")
            base.conn.commit()
            base.cursor.execute(f"UPDATE users SET position_month = position_month - 1 WHERE userid = {userId}")
            await callback.bot.send_message(chat_id = userId, text = f"<b>@{callback.from_user.username} выдал Вам -1 покупку</b>", parse_mode = "html")
        
        base.conn.commit()

        # check all position and give main discount
        if position_all == 10:
            discount = 5
            base.cursor.execute(f"UPDATE users SET discount = {discount} WHERE userid = {userId}")
            base.conn.commit()
        if position_all == 20:
            discount = 10
            base.cursor.execute(f"UPDATE users SET discount = {discount} WHERE userid = {userId}")
            base.conn.commit()
        if position_all == 30:
            discount = 15
            base.cursor.execute(f"UPDATE users SET discount = {discount} WHERE userid = {userId}")
            base.conn.commit()
                        
        nl = '\n'

        await callback.message.edit_text(text = f"<b>Информация о пользователе {userName} [id: {userId}]</b>\n\n\
Количество покупок (всего): {position_all}\n\
Количество покупок (за месяц): {position_month}\n\
Получаемая скидка: {discount}\n\
{f'{nl}<code>Действует скидка {top_discount}% на этот месяц (не складывается с основной скидкой)!</code>{nl}' if int(top_discount) > 0 else ''}\n\
{f'<code>Действует временная скидка {temp_discount}%!</code>{nl}' if int(temp_discount) > 0 else ''}\n\
<i>Ниже можно нажать на '+1' или '-1' для изменения количества покупок ЗА МЕСЯЦ</i>", parse_mode = "html", reply_markup = keyboard)

        await callback.answer()