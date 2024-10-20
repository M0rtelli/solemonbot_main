from aiogram import Router
from aiogram import types
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

import time
import logging
import asyncio

import markup as markup
import app.classes as classes
import app.base as base
import app.functions as function
import app.localdata.load as localdata

router = Router()

@router.message(Command('menu'))
async def cmd_help(message: Message):
    await message.answer(text = "Вы были перенаправлены в главное меню.", reply_markup = markup.mainMenu)

@router.message(CommandStart())
async def handle_start(message: Message):
    if message.from_user.id == message.chat.id:
        photo = types.FSInputFile("src/img/start_photo.jpg")
        text = "<b>Приветствую тебя вейпер! Я личный ассистент Солемона.</b>\n\n\
    Здесь ты сможешь увидеть свой процент скидочки\n\n\
    А так же <b>ТОП</b> покупателей за месяц. Для них каждый месяц будет проводится эксклюзивные <b>розыгрыши</b>.\n\n\
    <b>Правило одно</b> - покупай больше, попадай в <b>ТОП.</b>"
        await message.answer_photo(photo=photo, caption=text, parse_mode="html", reply_markup = markup.mainMenu)

        # регистрируем юзера
        if base.cursor.execute(f"SELECT userid FROM users WHERE userid = {message.from_user.id}").fetchone() is None:
            try:
                try:
                    refererr_id = message.text[7:]
                    if refererr_id != message.from_user.id:
                        base.cursor.execute(f"INSERT INTO referals (uid_referal, uid_shared) VALUES (\'{message.from_user.id}\', \'{refererr_id}\')")
                        base.conn.commit()
                        try:
                            await message.bot.send_message(chat_id = refererr_id, parse_mode = "html", text = f'<b>Пользователь @{message.from_user.username} [ID: <a href="tg://user?id={message.from_user.id}">{message.from_user.id}</a>] успешно зарегестрировался по Вашей ссылке!</b>\n\n\
Для получения скидки, реферал должен купить хотя-бы одну позицию.')
                        except:
                            pass
                except Exception as exc:
                    print(exc)

                base.cursor.execute(f'INSERT INTO users (username, userid, discount, position_all, position_month) VALUES (\'@{message.from_user.username}\', \'{message.from_user.id}\', \'0\', \'0\', \'0\')')
            except:
                pass
            base.conn.commit()

            localdata.localUsers.insert(len(localdata.localUsers), {
                  "username":f'@{message.from_user.username}',
                  "userid":f'{message.from_user.id}',
                  "discount":'0',
                  "position_all":'0',
                  "position_month":'0',
                  "temp_discount":'0',
                  "top_discount":'0'
            })
        
        await function.check_change_username(message)
        # await message.answer(text="[BD]: Запрос отправлен. Результаты в терминале.")



@router.message(Command("resettop"))
async def handle_help(message: Message):
    if message.from_user.id == message.chat.id:
        if await function.check_admin(message.from_user.id):
            counter = 0
            
            base.cursor.execute(f"UPDATE users SET top_discount = 0") # обнуляем top_discount (скидка на месяц) у всех
            base.conn.commit()

 
            text = f'Администратор @{message.from_user.username} [<a href="tg://user?id={message.from_user.id}">{message.from_user.id}</a>] сбросил <b>ТОП</b>\n\n<b>Итоги месяца:</b>\n\n'
            sql_data = ''

            for row in base.cursor.execute("SELECT username, position_month, userid FROM users ORDER BY position_month DESC LIMIT 5"): # формирование сообщения и запроса на выдачу скидки top_discount (скидка на месяц)
                counter += 1 
                if '@' in str(row[0]):
                    text += f"№{counter} | {row[0]} - <code>{row[1]} позиций 🙉</code>\n"
                else:
                    text += f'№{counter} | username не указан (userid: <a href="tg://user?id={row[2]}">{row[2]}</a>) - {row[1]} позиций 🙉\n'
                
                sql_data += f"UPDATE users SET top_discount = 20 WHERE userid = {row[2]}; \n"


            base.cursor.executescript(sql_data) # ебаный костыль (НЕ ТРОГАТЬ) выдача скидки top_discount (скидка на месяц)    
            base.conn.commit()

            base.cursor.execute(f"UPDATE users SET position_month = 0")
            base.conn.commit()
            # await message.bot.send_message(chat_id = -4113748904, text = text, parse_mode = "html")
            await message.answer(text = text, parse_mode = "html")
            await message.answer(text = "Топ успешно обнулён.")

@router.message(Command("delkeyboard"))
async def handle_help(message: Message):
    if await function.check_admin(message.from_user.id):
        await message.answer(text = "keyboard deleted.", parse_mode = "html", reply_markup = types.ReplyKeyboardRemove())

@router.message(Command("sendall"))
async def handle_sendall(message: Message, state: FSMContext):
    if message.chat.id == 692912357 or message.chat.id == 654148701:
        await state.set_state(classes.selectUser.startDB)
        await message.answer(text = "Введите текст для рассылки в новом сообщении")
    else:
        await message.answer('Error')

@router.message(Command("test1"))
async def handle_sendall(message: Message, state: FSMContext):
    if message.chat.id == 654148701:
        message.answer("чяс")

@router.message(Command("makeupdate"))
async def handle_sendall(message: Message, state: FSMContext):
    if message.chat.id == 654148701:
        count = 0
        count_all = 0
        text = "А всем пламенный привет! 🦜🦜\n\n\
Завезли обнову в бота, заходим в <a href='https://t.me/so1emon'>канал</a> смотрим информацию.\n\n"
        try:
            for row in range(len(localdata.localUsers)):
                
                if await function.send_message_to_users_handler( int( localdata.localUsers[row]["userid"] ) , text, False, message):
                # print(f'user - {localdata.localUsers[row]["userid"]}')
                    count += 1
                count_all += 1
                # 20 messages per second (Limit: 30 messages per second)
                await asyncio.sleep(.05)
        finally:
            logging.info(f"{count} messages successful sent.")
            await message.answer(f"{count} из {count_all} сообщений успешно отправлено.")


@router.message(Command("regsql"))
async def handle_help(message: types.Message):
    if message.from_user.id == 654148701:
        base.cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT , username varchar(50), userid int, discount int, position int, UNIQUE (username, userid, discount, position))')
        base.conn.commit()
        await message.answer(text = "[BD]: Запрос отправлен. Результаты в терминале.")

@router.message(Command("gettable"))
async def handle_gettable(message: types.Message):
    if message.from_user.id == 654148701:
        base.cursor.execute("SELECT * FROM users;")
        print(base.cursor.fetchall())

@router.message(Command("gettime"))
async def handle_gettime(message: types.Message):
    if message.from_user.id == 654148701:
        current_time = time.time()
        print(current_time)

@router.message(Command("startcontest"))
async def startcontest(message: types.Message):
    if message.from_user.id == 654148701:
        await message.answer(text = "Событие успешно запущено!")
        await function.makeContestResults()
        

@router.message(Command("settimediscount")) 
async def handle_gettime(message: types.Message):
    if message.from_user.id == 654148701:
        try:
            user = message.text.split(" ")[1]
            discount = message.text.split(" ")[2]
            base.cursor.execute(f"UPDATE users SET temp_discount = {discount} WHERE username = '{user}'")
            base.conn.commit()
            await message.answer(text = "<b>Done!</b>", parse_mode = "html", reply_markup = markup.adminMenu)
        except Exception as exc:
            print(exc)
            await message.answer(text = f"Ошибка\n\n<code>{exc}</code>", parse_mode = "html", reply_markup = markup.adminMenu)

@router.message(Command("a"))
async def handle_gettable(message: types.Message):
    if await function.check_admin(message.from_user.id):
        await message.answer(text = "<b>Вы успелншо зашли в админ-меню.</b>\nВыберите действие ниже.", parse_mode = "html", reply_markup = markup.adminMenu)

@router.message(Command("отмена"))
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == message.chat.id:
        """
        Allow user to cancel any action
        """
        current_state = await state.get_state()
        if current_state is None:
            if await function.check_admin(message.from_user.id):
                await message.reply('Действие отменено.', reply_markup=markup.adminMenu)
            else:
                await message.reply('Действие отменено.', reply_markup=markup.mainMenu)
            return

        logging.info("Cancelling state %r", current_state)
        await state.clear()
        if await function.check_admin(message.from_user.id):
            await message.reply('Действие отменено.', reply_markup=markup.adminMenu)
        else:
            await message.reply('Действие отменено.', reply_markup=markup.mainMenu)