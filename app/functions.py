from aiogram import types
from main import bot

import config
import markup as markup
import app.base as base
import logging
import random


# ---------------
# --- ФУНКЦИИ ---
# ---------------

async def check_admin(id: int):
    if base.cursor.execute(f"SELECT userid FROM admins WHERE userid = {id}").fetchone():
        return True
    
async def check_change_username(message: types.Message):
    try:
        username_bd = base.cursor.execute(f"SELECT username FROM users WHERE userid = {message.from_user.id}").fetchone()[0]
        if message.from_user.username != None:
            if username_bd != '@' + message.from_user.username:
                base.cursor.execute(f"UPDATE users SET username = '@{message.from_user.username}' WHERE userid = {message.from_user.id}")
                base.conn.commit()
        else:
            base.cursor.execute(f"UPDATE users SET username = '' WHERE userid = {message.from_user.id}")
            base.conn.commit()
    except:
        pass


async def send_message_to_users_handler(
    user_id: int, text: str, disable_notification: bool = False, message: types.Message = False
) -> bool:
    """
    Safe messages sender
    :param user_id:
    :param text:
    :param disable_notification:
    :return:
    """
    try:
        if message.animation != None:
            await message.bot.send_animation(chat_id = user_id,
                caption = message.caption,
                animation = message.animation.file_id,
                disable_notification = False,
                parse_mode = "html")
        elif message.photo != None:
            await message.bot.send_photo(chat_id = user_id,
                caption = message.caption,
                photo = message.photo[-1].file_id,
                disable_notification = False,
                parse_mode = "html")
        else:
            await message.bot.send_message(
                user_id,
                text,
                disable_notification = False,
                parse_mode = "html",
                disable_web_page_preview = True,
                reply_markup=markup.mainMenu
            )

        
    except Exception as exc:
        logging.error(f"Target [ID:{user_id}]: failed. Reason: {exc}")
        return False
    else:
        logging.info(f"Target [ID:{user_id}]: success")
        return True
    return False

async def get_referal_text(message: types.Message, typeRequest: int): # typeRequest: 0 - with text, 1 - only referals 
    referals = ''
    for row in base.cursor.execute(f"SELECT * FROM referals WHERE uid_shared = '{message.from_user.id}'"):
        referals += f"Пользователь {base.cursor.execute(f'SELECT `username` FROM `users` WHERE `userid` = {row[1]}').fetchone()[0]} [ID: <a href=\"tg://user?id={row[1]}\">{row[1]}</a>] - Статус: <b>{'активен' if int(row[3]) != 0 else 'не активен'}</b>\n"
        
    if typeRequest == 0:
        text = "<b>Реферальная система</b> - за каждую покупку твоего реферала ты получишь 5% скидки на следующую <b>СВОЮ</b> покупку\n\n\
Твоя реферальная ссылка: \n<code>{link}</code>\n\n\
<b>Список твоих рефералов:</b>\n\n{referals}\
".format(link  = f"https://t.me/{config.bot_nickname}?start={message.from_user.id}", referals = f"{referals}")
        
    elif typeRequest == 1:
        text = "\n\n{referals}\
".format(referals = f"{referals}")
    else:
        text = f"<b>Ошибка!</b>\nОтчет об ошибке уже был отправлен разработчику.\n\nCode: typeRequest error\nUser: @{message.from_user.username}"
        await message.bot.send_message(chat_id = 654148701, text = text, parse_mode = "html")
    return text

async def getProfileText(message: types.Message):
    userId = message.from_user.id
    topPosition = 0
    countMarketAds = 0
    numbersContest = ""
    alltext = f"<b>Профиль @{message.from_user.username} [ID: <a href=\"tg://user?id={userId}\">{userId}</a>]</b>\n\n"
    for row in base.cursor.execute(f"SELECT userid FROM users ORDER BY position_month DESC;"):
        topPosition += 1
        if int(row[0]) == int(userId):
            break

    try:
        for row in base.cursor.execute(f"SELECT id FROM marketplace WHERE uid = {userId};"):
            countMarketAds += 1
    except:
        pass        
    
    try:
        for row in base.cursor.execute(f'SELECT number_contest FROM contest_info WHERE uid = {message.from_user.id}'):
            numbersContest += f"{str(row[0])}; "
    except:
        pass        

    for row in base.cursor.execute(f"SELECT * FROM users WHERE userid = '{message.from_user.id}' LIMIT 1;"):
            '''
                0 - id
                1 - username
                2 - userid
                3 - discount
                4 - position_all 
                5 - position_month
                6 - temp_discount
                7 - top_discount
            '''
            _, username, _, discount, position_all, position_month, temp_discount, top_discount = row

            alltext += f"<code>Ваша основная скидка:</code><b> {discount}</b>\n"
            alltext += f"<code>Дополнительные скидки:</code><b> { f'{top_discount}% (до конца месяца)' if int(top_discount) > 0 else ''}\
{f', {temp_discount}% (одноразовая)' if int(temp_discount) > 0 and (top_discount) > 0 else f'{temp_discount}% (одноразовая)' if int(temp_discount) > 0 else 'отсутствуют' if int(temp_discount) <= 0 and int(top_discount) <= 0 else '' }</b>\n"
            alltext += f"<code>Всего покупок:</code><b> {position_all} шт., {position_month} из которых в этом месяце</b>\n"
            alltext += f"<code>Место в топе:</code><b> {topPosition}</b>\n"
            alltext += f"<code>Количество объявлений на барахолке:</code><b> {countMarketAds}</b>\n"
            alltext += f"<code>Номерки еженедельного розыгрыша:</code><b> {numbersContest if numbersContest != '' else 'отсутствуют'}</b>\n"
            alltext += f"<code>Рефералы:</code> {await get_referal_text(message, 1)}"
            
    return alltext


async def doContest():
    
    selectAnswer = [
        [
            types.InlineKeyboardButton(text="Да", callback_data = f"contest_yes"),
            types.InlineKeyboardButton(text="Нет", callback_data = f"contest_no")
        ]    
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard = selectAnswer)
    await bot.send_message(654148701, "Пришло время еженедельного розыгрыша. Все пользователи внесены в базу?", parse_mode='html', reply_markup = keyboard)

async def makeContestResults():
    allUsers = []
    try:
        for row in base.cursor.execute("SELECT * FROM contest_info WHERE winner = 0;"):
            allUsers.insert(len(allUsers), [row[1], row[2]])
            
    except:
        await bot.send_message(654148701, f"Ошибка! Пустая бд")
        return
    
    random.shuffle(allUsers)
    randomUser = random.choice(allUsers)
    randomUserUsername = base.cursor.execute(f'SELECT username FROM users WHERE userid = {randomUser[0]};').fetchone()[0]
    
    selectAnswer = [
        [
            types.InlineKeyboardButton(text="Да", callback_data = f"contestResult_yes"),
            types.InlineKeyboardButton(text="Нет", callback_data = f"contestResult_no")
        ]    
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard = selectAnswer)



    base.cursor.execute(f'DELETE FROM contest_info;')
    base.conn.commit()

    base.cursor.execute(f"INSERT INTO contest_info (uid, number_contest, winner) VALUES ({randomUser[0]}, {randomUser[1]}, 1);")
    base.conn.commit()        

    await bot.send_message(654148701, f"Победитель конкурса - { randomUserUsername if randomUserUsername != '' else 'no username'} [ID: <a href='tg://user?id={randomUser[0]}'>{randomUser[0]}</a>] с номерком <b>№{randomUser[1]}</b>\n\n\
Начать рассылку по всем пользователям?", 
parse_mode= 'html', reply_markup = keyboard)
    

