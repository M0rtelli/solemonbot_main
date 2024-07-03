from aiogram import F, Router
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

import markup as markup
import app.classes as classes
import app.base as base
import app.functions as function
import texts as texts

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

@router.message(F.text.lower() == "правила")
async def button_top(message: types.Message):
    if message.from_user.id == message.chat.id:
        await function.check_change_username(message)

        photo = types.FSInputFile("src/img/rules_photo.jpg")
        await message.answer_photo(photo = photo, caption = texts.rules_discount, parse_mode="html", reply_markup = markup.backToMainMenu)

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
        await message.answer(text = await function.get_referal_text(message), parse_mode = "html", reply_markup = types.ReplyKeyboardMarkup(
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
