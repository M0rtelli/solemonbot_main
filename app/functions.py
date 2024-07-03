from aiogram import types

import config
import markup as markup
import app.base as base
import logging



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
                disable_web_page_preview = True
            )

        
    except Exception as exc:
        print(exc)
        logging.error(f"Target [ID:{user_id}]: failed")
        return False
    else:
        logging.info(f"Target [ID:{user_id}]: success")
        return True
    return False

async def get_referal_text(message: types.Message):
    referals = ''
    for row in base.cursor.execute(f"SELECT * FROM referals WHERE uid_shared = '{message.from_user.id}'"):
        referals += f"Пользователь {base.cursor.execute(f'SELECT `username` FROM `users` WHERE `userid` = {row[1]}').fetchone()[0]} [ID: <a href=\"tg://user?id={row[1]}\">{row[1]}</a>] - Статус: <b>{'активен' if int(row[3]) != 0 else 'не активен'}</b>\n"
        
    text = "<b>Реферальная система</b> - за каждую покупку твоего реферала ты получишь 5% скидки на следующую <b>СВОЮ</b> покупку\n\n\
Твоя реферальная ссылка: \n<code>{link}</code>\n\n\
<b>Список твоих рефералов:</b>\n\n{referals}\
".format(link  = f"https://t.me/{config.bot_nickname}?start={message.from_user.id}", referals = f"{referals}")
    return text
