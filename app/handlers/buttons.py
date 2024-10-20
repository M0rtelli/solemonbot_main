from aiogram import F, Router
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest 

import markup as markup
import app.classes as classes
import app.base as base
import app.functions as function
import texts as texts
import app.localdata.load as localdata
import asyncio

router = Router()


@router.message(F.text.lower() == "топ 🔝")
async def button_top(message: types.Message):
    if message.from_user.id == message.chat.id:
        await function.check_change_username(message)
        counter = 0
        text = texts.top
        for row in base.cursor.execute("SELECT username, position_month, userid FROM users ORDER BY position_month DESC LIMIT 5"):
            counter += 1 
            for i in row[0]:
                if i == "@":
                    text += f"№{counter} | {row[0]} - <code>{row[1]} позиций 🙉</code>\n"
                    break
            else: 
                text += f'№{counter} | username не указан (userid: <a href="tg://user?id={row[2]}">{row[2]}</a>) - {row[1]} позиций 🙉\n'
        await message.answer(text = text, parse_mode="html")

@router.message(F.text.lower() == "моя скидочка 💸")
async def button_top(message: types.Message):
    if message.from_user.id == message.chat.id:
        await function.check_change_username(message)

        discount = base.cursor.execute(f"SELECT discount FROM users WHERE userid = '{message.from_user.id}' LIMIT 1").fetchone()[0]
        position = base.cursor.execute(f"SELECT position_all FROM users WHERE userid = '{message.from_user.id}' LIMIT 1").fetchone()[0]
        temp_discount = base.cursor.execute(f"SELECT temp_discount FROM users WHERE userid = \'{message.from_user.id}\' LIMIT 1").fetchone()[0]
        top_discount = base.cursor.execute(f"SELECT top_discount FROM users WHERE userid = \'{message.from_user.id}\' LIMIT 1").fetchone()[0]
        
        await message.answer(text = f"💰 - Ваша скидка *{discount}%*\n\
🤘 - Количество кулпенных позиций - *{position} шт.*\n\n\
{f'У Вас действует скидка {top_discount}% на этот месяц (не складывается с основной скидкой)!' if int(top_discount) > 0 else ''}\n\n\
{f'У Вас действует временная скидка {temp_discount}%!' if int(temp_discount) > 0 else ''}", parse_mode="Markdown")
        
@router.message(F.text.lower() == "мой профиль")
async def button_top(message: types.Message):
    if message.from_user.id == message.chat.id:
        await function.check_change_username(message)

        await message.answer(text = await function.getProfileText(message), parse_mode = "html")
        
@router.message(F.text.lower() == "еженедельный розыгрыш")
async def button_top(message: types.Message):
    if message.from_user.id == message.chat.id:
        await function.check_change_username(message)

        for row in base.cursor.execute('SELECT * FROM contest_info WHERE winner = 1 LIMIT 1;'):
            _, winner_uid, number_contest, _ = row

        last_winner = base.cursor.execute(f'SELECT username FROM users WHERE userid = {winner_uid} LIMIT 1;').fetchone()[0]
        await message.answer(text = f"<b>ПРАВИЛА ЕЖЕНЕДЕЛЬНЫХ РОЗЫГРЫШЕЙ:</b>\n\n\
<code>1. Покупаешь любую позицию в течение недели, помимо добавленного балла <i>(который идет за каждую покупку и прокачивает твою постоянную скидку)</i>, тебе еще присваивается номерок.</code>\n\n\
<code>2. В воскресенье, ровно в 00:00 бот автоматически выбирает выигрышный номерочек и ты на халяву получаешь баночку жижи!</code>\n\n\
Чем больше позиций ты приобрел в течение недели, тем больше у тебя будет номерков, соответсвенно, шансов выиграть. \n\n\
<b>Это не сон, розыгрыши будут проходить каждую неделю, дерзайте!!</b>\n\n\
Последний победитель: { last_winner if last_winner != '' else 'no username'} \
[ID: <a href=\"tg://user?id={winner_uid}\">{winner_uid}</a>] с номерком <b>№{number_contest}</b>", parse_mode = "html")
        

@router.message(F.text.lower() == "правила")
async def button_top(message: types.Message):
    if message.from_user.id == message.chat.id:
        await function.check_change_username(message)

        photo = types.FSInputFile("src/img/rules_photo.jpg")
        await message.answer_photo(photo = photo, caption = texts.rules_discount, parse_mode="html", reply_markup = markup.backToMainMenu)

        builder = InlineKeyboardBuilder()
        builder.row(types.InlineKeyboardButton(
            text="Барахолка", url="tg://resolve?domain=BobruiskVape")
        )
        builder.row(types.InlineKeyboardButton(
            text="Solemon",
            url="https://t.me/+Y9vf31LCNRc2NTYy")
        )
        builder.row(types.InlineKeyboardButton(
            text="Pepsi",
            url="tg://resolve?domain=PepsiColaVape")
        )
        await message.answer(text = "<b>Наши ссылки:</b>", reply_markup = builder.as_markup(), parse_mode = "html")

@router.message(F.text.lower() == "support/help")
async def button_top(message: types.Message):
    if message.from_user.id == message.chat.id:
        await function.check_change_username(message)

        photo = types.FSInputFile("src/img/support_photo.jpg")
        await message.answer_photo(photo = photo, caption = texts.support, parse_mode="html", reply_markup = markup.backToMainMenu)

@router.message(F.text.lower() == "назад в меню")
async def button_top(message: types.Message):
    if message.from_user.id == message.chat.id:
        await function.check_change_username(message)

        await message.answer(text = "Выберите пункт меню:", reply_markup = markup.mainMenu)

@router.message(F.text.lower() == "о нас")
async def button_top(message: types.Message):
    if message.from_user.id == message.chat.id:
        await function.check_change_username(message)
        

@router.message(F.text.lower() == "скупка устройств 🛍")
async def button_top(message: types.Message, state: FSMContext):
    if message.from_user.id == message.chat.id:
        await function.check_change_username(message)
        await state.set_state(classes.sellPod.namePod)
        await message.answer(text = "Введите название вашего устройства:\n\nПример: <code>Smoant Pasito 2</code>", parse_mode = "html", reply_markup = types.ReplyKeyboardMarkup(
                    keyboard=[
                        [
                            types.KeyboardButton(text="Отмена")
                        ]
                    ],
                    resize_keyboard=True,
                ),
            )
    
@router.message(F.text.lower() == "барахолка")
async def button_top(message: types.Message, state: FSMContext):
    if message.from_user.id == message.chat.id:
        await function.check_change_username(message)
        await state.set_state(classes.toMarketPlace.chooseMenu)
        await message.answer(text = "Выберите действие ниже", parse_mode = "html", reply_markup = types.ReplyKeyboardMarkup(
                    keyboard=[
                        [
                            types.KeyboardButton(text="Посмотреть объявления"),
                            types.KeyboardButton(text="Мои объявления"),
                            types.KeyboardButton(text="Назад")
                        ]
                    ],
                    resize_keyboard=True,
                ),
            )

        
@router.message(F.text.lower() == "реферальная система")
async def button_top(message: types.Message, state: FSMContext):
    if message.from_user.id == message.chat.id:
        await function.check_change_username(message)
        await message.answer(text = await function.get_referal_text(message, 0), parse_mode = "html", reply_markup = types.ReplyKeyboardMarkup(
                    keyboard=[
                        [
                            types.KeyboardButton(text="Назад в меню")
                        ]
                    ],
                    resize_keyboard=True,
                ),
            )

    # ----- ADMIN BUTTONS ---------

@router.message(F.text.lower() == "информация о юзере")
async def button_top(message: types.Message, state: FSMContext):
    if await function.check_admin(message.from_user.id):
        await state.set_state(classes.selectUser.userId)
        await message.answer(text = "Введите username или userid пользователя:\n\nПример: <code>@solemxn</code>", parse_mode = "html", reply_markup = types.ReplyKeyboardMarkup(
                keyboard=[
                    [
                        types.KeyboardButton(text="/отмена")
                    ]
                ],
                resize_keyboard=True,
            ),
        )

@router.message(F.text.lower() == "выдать продажу")
async def button_top(message: types.Message, state: FSMContext):
    if await function.check_admin(message.from_user.id):
        await state.set_state(classes.giveSell.userId)
        await message.answer(text = "Введите username или userid пользователя:\n\nПример: <code>@solemxn</code>", parse_mode = "html", reply_markup = types.ReplyKeyboardMarkup(
                keyboard=[
                    [
                        types.KeyboardButton(text="/отмена")
                    ]
                ],
                resize_keyboard=True,
            ),
        )

@router.message(F.text.lower() == "выдать скидку")
async def button_top(message: types.Message, state: FSMContext):
    if await function.check_admin(message.from_user.id):
        await state.set_state(classes.giveDiscount.userId)
        await message.answer(text = "Введите username или userid пользователя:\n\nПример: <code>@solemxn</code>", parse_mode = "html",reply_markup = types.ReplyKeyboardMarkup(
                keyboard=[
                    [
                        types.KeyboardButton(text="/отмена")
                    ]
                ],
                resize_keyboard=True,
            ),
        )

@router.message(F.text.lower() == "моя статистика")
async def button_top(message: types.Message, state: FSMContext):
    if await function.check_admin(message.from_user.id):
        # TODO
        allUsers = base.cursor.execute("SELECT id FROM users ORDER BY id DESC LIMIT 1;").fetchone()[0]

        allPosition = 0
        for row in base.cursor.execute("SELECT position_all FROM users ORDER BY position_all DESC"):
            allPosition += row[0]
            if row[0] == 0:
                break

        monthPosition = 0
        for row in base.cursor.execute("SELECT position_month FROM users ORDER BY position_month DESC"):
            monthPosition += row[0]
            if row[0] == 0:
                break

        await message.answer(text = f"<b>Общая статистика</b>\n\n\
Количество юзеров: <code>{allUsers}</code>\n\
Количество продаж (всего): <code>{allPosition}</code>\n\
Количество продаж (за месяц): <code>{monthPosition}</code>\n\
\n\
Мои продажи: <code>в разработке</code>\
"
, parse_mode = "html")


@router.callback_query(F.data.startswith("contest_"))
async def callbacks_num(callback: types.CallbackQuery):
    action = callback.data.split("_")[1]

    if action == "yes":

        await callback.message.edit_text(text = "Событие успешно запущено!", reply_markup = None)
        await function.makeContestResults()
    else:
        await callback.message.edit_text(text = "Внесите покупки пользователей в базу и введите /startcontest", reply_markup = None)

    await callback.answer()

@router.callback_query(F.data.startswith("contestResult_"))
async def callbacks_num(callback: types.CallbackQuery):
    action = callback.data.split("_")[1]

    if action == "yes":
        
        winnerUid = base.cursor.execute("SELECT uid FROM contest_info WHERE winner = 1 LIMIT 1;").fetchone()[0]
        winnerNumberContest = base.cursor.execute("SELECT number_contest FROM contest_info WHERE winner = 1 LIMIT 1;").fetchone()[0]
        winnerUsername = base.cursor.execute(f"SELECT username FROM users WHERE userid = {winnerUid} LIMIT 1;").fetchone()[0]

        await callback.message.edit_text(text = "Начинаем рассылку! Не используйте бота, пока рассылка не окончится.", reply_markup = None)
        text = f"<b>ИТОГИ ЕЖЕНЕДЕЛЬНОГО РОЗЫГРЫША:</b>\n\n\
Новый победитель: { winnerUsername if winnerUsername != '' else 'no username'} [ID: <a href='tg://user?id={winnerUid}'>{winnerUid}</a>]\n\
Номер билета: <b>№{winnerNumberContest}</b>\n\n\
Поздравим в <a href='https://t.me/+aLy-EyGvM-AzZTU6'>чатике!</a>"
        
        count = 0
        count_all = 0
        try:
            for row in range(len(localdata.localUsers)):
                
                if await function.send_message_to_users_handler( int( localdata.localUsers[row]["userid"] ) , text, False, callback.message):
                # print(f'user - {localdata.localUsers[row]["userid"]}')
                    count += 1
                count_all += 1
                # 20 messages per second (Limit: 30 messages per second)
                await asyncio.sleep(.05)
        finally:
            await callback.message.answer(f"{count} из {count_all} сообщений успешно отправлено.")

    else:
        await callback.message.edit_text(text = "Рассылка отменена!", reply_markup = None)

    await callback.answer()
