from aiogram import F, Router
from aiogram import types
from aiogram.fsm.context import FSMContext

import math

import markup as markup
import app.classes as classes
import app.base as base
import app.localdata.load as localdata
import app.functions as function

router = Router()
pageListAllAd = 0
current_ad_id = 0

@router.message(classes.toMarketPlace.chooseMenu)
async def button_chooseMenu(message: types.Message, state: FSMContext):
    if message.text and message.text.lower() == 'посмотреть объявления':
        await state.set_state(classes.toMarketPlace.selectTypeViewAd)
        await message.answer(text = "Выберите тип просмотра", reply_markup = types.ReplyKeyboardMarkup(
                    keyboard=[
                            [
                                types.KeyboardButton(text="Поиск по диапозону цен")
                            ],
                            [
                                types.KeyboardButton(text="Пролистывание")
                            ],
                            [
                                types.KeyboardButton(text="Все объявления")
                            ],
                            [
                                types.KeyboardButton(text="Назад")
                            ]
                        ],
                    resize_keyboard=True,
                ),
                )

    elif message.text and message.text.lower() == 'мои объявления':
        await state.set_state(classes.toMarketPlace.chooseMyAd)
        # await message.answer(text = "В разработке", reply_markup = markup.mainMenu)
        allText = '<b>Ваши объявления: </b>\n\n'
        count = 0
        keyboard = [[types.KeyboardButton(text = f"Назад")]]
        for row in base.cursor.execute(f"SELECT * FROM marketplace WHERE uid = {message.from_user.id}"):
            count += 1
            allText += f'<b>#{count} </b>| {row[2]} | {row[4]} BYN\n'
            keyboard.insert(count, [types.KeyboardButton(text = f"#{count}")]) 
        allText += "\n<i>Выберите номер объявления ниже, для редактирования</i>"
        keyboard.insert(count + 1, [types.KeyboardButton(text = "Добавить объявление")])
        await message.answer(text = allText, parse_mode = "html", reply_markup = types.ReplyKeyboardMarkup(
                    keyboard=keyboard,
                    resize_keyboard=True
                )
            )
        

    elif message.text and message.text.lower() == 'назад':
        await message.answer(text = "Вы вернулись в главное меню", reply_markup = markup.mainMenu)
        await state.clear()


@router.message(classes.toMarketPlace.selectTypeViewAd)
async def button_selectview(message: types.Message, state: FSMContext):
    if message.text and message.text.lower() == 'назад':
        await state.clear()
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

    if message.text and message.text.lower() == 'поиск по диапозону цен':
        await state.set_state(classes.toMarketPlace.TypeViewAd_minprice)
        await message.answer(text = "Выберите минимальную цену.\n\nПример: <code>30</code>", reply_markup = types.ReplyKeyboardMarkup(
                    keyboard=[
                        [
                            types.KeyboardButton(text = "Отмена")
                        ]
                    ],
                    resize_keyboard=True,
                ), parse_mode = "html")
        
    if message.text and message.text.lower() == 'пролистывание':
        try:
            await state.set_state(classes.toMarketPlace.TypeViewAd_list)
            row = base.cursor.execute(f"SELECT * FROM marketplace ORDER BY id ASC LIMIT 1").fetchone()
            await state.update_data(TypeViewAd_list_item = row[0])
            if str(row[5]) == '0': 
                await message.answer(text = f'<b>{row[2]}</b>\n\nСостояние: <code>{row[3]}</code>\nЦена: <code>{row[4]}</code>\nКомментарий: <code>{row[6]}</code>\n\n\
    Продавец: {base.cursor.execute(f"SELECT `username` FROM `users` WHERE `userid` = {row[1]}").fetchone()[0]} [ID: <a href="tg://user?id={row[1]}">{row[1]}</a>]', parse_mode = "html", reply_markup = types.ReplyKeyboardMarkup(
                                keyboard=[
                                    [
                                        types.KeyboardButton(text="Отмена"),
                                        types.KeyboardButton(text="Далее")
                                    ]
                                ],
                                resize_keyboard=True,
                            ),
                        )
            else:
                await message.answer_photo(photo = row[5],caption = f'<b>{row[2]}</b>\n\nСостояние: <code>{row[3]}</code>\nЦена: <code>{row[4]}</code>\nКомментарий: <code>{row[6]}</code>\n\n\
    Продавец: {base.cursor.execute(f"SELECT `username` FROM `users` WHERE `userid` = {row[1]}").fetchone()[0]} [ID: <a href="tg://user?id={row[1]}">{row[1]}</a>]', parse_mode = "html", reply_markup = types.ReplyKeyboardMarkup(
                                keyboard=[
                                    [
                                        types.KeyboardButton(text="Отмена"),
                                        types.KeyboardButton(text="Далее")
                                    ]
                                ],
                                resize_keyboard=True,
                            ),
                        )
        except:
            await state.clear()
            await state.set_state(classes.toMarketPlace.selectTypeViewAd)
            await message.answer(text = "Ничего не найдено", reply_markup = types.ReplyKeyboardMarkup(
                        keyboard=[
                                [
                                    types.KeyboardButton(text="Поиск по диапозону цен")
                                ],
                                [
                                    types.KeyboardButton(text="Пролистывание")
                                ],
                                [
                                    types.KeyboardButton(text="Все объявления")
                                ],
                                [
                                    types.KeyboardButton(text="Назад")
                                ]
                            ],
                        resize_keyboard=True,
                    ),
                )
        
    if message.text and message.text.lower() == 'все объявления':
        await state.set_state(classes.toMarketPlace.TypeViewAd_all_item)

        if len(localdata.localMarketPlaceAllAd) == 0:
            await state.clear()
            await state.set_state(classes.toMarketPlace.selectTypeViewAd)
            await message.answer(text = "Ничего не найдено", reply_markup = types.ReplyKeyboardMarkup(
                        keyboard=[
                                [
                                    types.KeyboardButton(text="Поиск по диапозону цен")
                                ],
                                [
                                    types.KeyboardButton(text="Пролистывание")
                                ],
                                [
                                    types.KeyboardButton(text="Все объявления")
                                ],
                                [
                                    types.KeyboardButton(text="Назад")
                                ]
                            ],
                        resize_keyboard=True,
                    ),
                )
            return

        allText = '<b>Объявления: </b>\n\n'
        A = []
        countInPage = 0

        A.insert(len(A), [types.KeyboardButton(text = f"<"), types.KeyboardButton(text = f">")])

        print(len(localdata.localMarketPlaceAllAd))

        for row in range(10):
            if (row + ( pageListAllAd * 10 )) < len(localdata.localMarketPlaceAllAd):
                countInPage += 1
                allText += f'#{(row + 1) + ( pageListAllAd * 10 )} | {localdata.localMarketPlaceAllAd[row + ( pageListAllAd * 10 )]["name"]} | {localdata.localMarketPlaceAllAd[row + ( pageListAllAd * 10 )]["price"]} BYN\n'
            
        pair = 0
        for i in range(countInPage):
            if countInPage % 2 != 0:
                A.insert(len(A), [types.KeyboardButton(text = f"#{(i + 1) + ( pageListAllAd * 10 )}")])
            else:
                pair += 1
                A.insert(len(A), [types.KeyboardButton(text = f"#{(i + pair) + ( pageListAllAd * 10 )}"), 
                                  types.KeyboardButton(text = f"#{(i + pair + 1) + ( pageListAllAd * 10 )}")])
                if pair == (countInPage/2):
                    break

        A.insert(len(A), [types.KeyboardButton(text = f"Отмена")])
                
        await message.answer(text = allText, parse_mode = 'html', reply_markup = types.ReplyKeyboardMarkup(
                        keyboard = A,
                        resize_keyboard = True
                    )
                ) 


        
@router.message(classes.toMarketPlace.TypeViewAd_all_item)
async def button_viewlist(message: types.Message, state: FSMContext):
    global pageListAllAd
    

    if message.text and message.text.lower() == '<' or message.text and message.text.lower() == '>':
        if message.text and message.text.lower() == '<':
            if pageListAllAd != 0:
                pageListAllAd -= 1
            else:
                await message.answer(text = "Вы находитесь на первой странице")
                return
        if message.text and message.text.lower() == '>':
            if pageListAllAd != int(str(len(localdata.localMarketPlaceAllAd))[:1]):
                pageListAllAd += 1
            else:
                await message.answer(text = "Вы находитесь на последней странице")
                return

        
        await state.set_state(classes.toMarketPlace.TypeViewAd_all_item)

        if len(localdata.localMarketPlaceAllAd) == 0:
            await state.clear()
            await state.set_state(classes.toMarketPlace.selectTypeViewAd)
            await message.answer(text = "Ничего не найдено", reply_markup = types.ReplyKeyboardMarkup(
                        keyboard=[
                                [
                                    types.KeyboardButton(text="Поиск по диапозону цен")
                                ],
                                [
                                    types.KeyboardButton(text="Пролистывание")
                                ],
                                [
                                    types.KeyboardButton(text="Все объявления")
                                ],
                                [
                                    types.KeyboardButton(text="Назад")
                                ]
                            ],
                        resize_keyboard=True,
                    ),
                )
            return

        allText = '<b>Объявления: </b>\n\n'
        A = []
        countInPage = 0

        A.insert(len(A), [types.KeyboardButton(text = f"<"), types.KeyboardButton(text = f">")])

        for row in range(10):
            if (row + ( pageListAllAd * 10 )) < len(localdata.localMarketPlaceAllAd):
                countInPage += 1
                allText += f'#{(row + 1) + ( pageListAllAd * 10 )} | {localdata.localMarketPlaceAllAd[row + ( pageListAllAd * 10 )]["name"]} | {localdata.localMarketPlaceAllAd[row + ( pageListAllAd * 10 )]["price"]} BYN\n'
                
        pair = 0
        for i in range(countInPage):
            if countInPage % 2 != 0:
                A.insert(len(A), [types.KeyboardButton(text = f"#{(i + 1) + ( pageListAllAd * 10 )}")])
            else:
                pair += 1
                A.insert(len(A), [types.KeyboardButton(text = f"#{(i + pair) + ( pageListAllAd * 10 )}"), 
                                types.KeyboardButton(text = f"#{(i + pair + 1) + ( pageListAllAd * 10 )}")])
                if pair == (countInPage/2):
                    break

        A.insert(len(A), [types.KeyboardButton(text = f"Отмена")])
                    
        await message.answer(text = allText, parse_mode = 'html', reply_markup = types.ReplyKeyboardMarkup(
                        keyboard = A,
                        resize_keyboard = True
                    )
                ) 
            

    if message.text and message.text.lower() == 'отмена':
        await state.clear()
        await state.set_state(classes.toMarketPlace.selectTypeViewAd)
        await message.answer(text = "Выберите тип просмотра", reply_markup = types.ReplyKeyboardMarkup(
                    keyboard=[
                            [
                                types.KeyboardButton(text="Поиск по диапозону цен")
                            ],
                            [
                                types.KeyboardButton(text="Пролистывание")
                            ],
                            [
                                types.KeyboardButton(text="Все объявления")
                            ],
                            [
                                types.KeyboardButton(text="Назад")
                            ]
                        ],
                    resize_keyboard=True,
                ),
            )
    
    if message.text and str(message.text.lower())[0] == '#':
        try:
            chooseAd = int(str(message.text.lower()).replace("#", "", 1))
            count = 0
            for row in base.cursor.execute(f"SELECT * FROM marketplace"):
                count += 1
                if count == chooseAd:
                    global current_ad_id
                    current_ad_id = row[0]
                    print(f"current id ad - {current_ad_id}")
                    if str(row[5]) == '0': 
                        if await function.check_admin(message.from_user.id):
                            await message.answer(text = f'<b>{row[2]}</b>\n\nСостояние: <code>{row[3]}</code>\nЦена: <code>{row[4]}</code>\nКомментарий: <code>{row[6]}</code>\n\n\
Продавец: {base.cursor.execute(f"SELECT username FROM users WHERE userid = {row[1]}").fetchone()[0]} [ID: <a href="tg://user?id={row[1]}">{row[1]}</a>]', parse_mode = "html", reply_markup = types.ReplyKeyboardMarkup(
                                keyboard=[
                                    [
                                        types.KeyboardButton(text="Назад"),
                                        types.KeyboardButton(text="Удалить объявление")
                                    ]
                                ],
                                resize_keyboard=True,
                            ),
                        )
                    else:
                        await message.answer_photo(photo = row[5], caption = f'<b>{row[2]}</b>\n\nСостояние: <code>{row[3]}</code>\nЦена: <code>{row[4]}</code>\nКомментарий: <code>{row[6]}</code>\n\n\
Продавец: {base.cursor.execute(f"SELECT username FROM users WHERE userid = {row[1]}").fetchone()[0]} [ID: <a href="tg://user?id={row[1]}">{row[1]}</a>]', parse_mode = "html", reply_markup = types.ReplyKeyboardMarkup(
                            keyboard=[
                                [
                                    types.KeyboardButton(text="Назад")
                                ]
                            ],
                            resize_keyboard=True,
                        ),
                    )
                    break
                    
                        

        except Exception as exc:
            print(exc)
            await state.clear()
            await state.set_state(classes.toMarketPlace.selectTypeViewAd)
            await message.answer(text = "Ошибка! Обратитесь в <b>Support/Help</b>\n\nПеренаправляем Вас назад.", reply_markup = types.ReplyKeyboardMarkup(
                        keyboard=[
                                [
                                    types.KeyboardButton(text="Поиск по диапозону цен")
                                ],
                                [
                                    types.KeyboardButton(text="Пролистывание")
                                ],
                                [
                                    types.KeyboardButton(text="Все объявления")
                                ],
                                [
                                    types.KeyboardButton(text="Назад")
                                ]
                            ],
                        resize_keyboard=True,
                    ),
                )
            
    if message.text and message.text.lower() == 'удалить объявление': # админ удаляет объяву
        await message.answer(text = "<b>Вы уверены, что хотите удалить данное объявление?</b>", reply_markup = types.ReplyKeyboardMarkup(
                        keyboard=[
                                [
                                    types.KeyboardButton(text="Да, уверен"),
                                    types.KeyboardButton(text="Отмена")
                                ]
                            ],
                        resize_keyboard=True,
                    ),)
        await state.clear()
        await state.set_state(classes.toMarketPlace.confirmDeleteAd)
        await state.update_data(chooseMyAd = current_ad_id)
    
    if message.text and message.text.lower() == 'назад':
        await state.set_state(classes.toMarketPlace.TypeViewAd_all_item)

        if len(localdata.localMarketPlaceAllAd) == 0:
            await state.clear()
            await state.set_state(classes.toMarketPlace.selectTypeViewAd)
            await message.answer(text = "Ничего не найдено", reply_markup = types.ReplyKeyboardMarkup(
                        keyboard=[
                                [
                                    types.KeyboardButton(text="Поиск по диапозону цен")
                                ],
                                [
                                    types.KeyboardButton(text="Пролистывание")
                                ],
                                [
                                    types.KeyboardButton(text="Все объявления")
                                ],
                                [
                                    types.KeyboardButton(text="Назад")
                                ]
                            ],
                        resize_keyboard=True,
                    ),
                )
            return

        allText = '<b>Объявления: </b>\n\n'
        A = []
        countInPage = 0

        A.insert(len(A), [types.KeyboardButton(text = f"<"), types.KeyboardButton(text = f">")])

        for row in range(10):
            if (row + ( pageListAllAd * 10 )) < len(localdata.localMarketPlaceAllAd):
                countInPage += 1

                # TODO не показывает последнее объявление
                allText += f'#{(row + 1) + ( pageListAllAd * 10 )} | {localdata.localMarketPlaceAllAd[row + ( pageListAllAd * 10 )]["name"]} | {localdata.localMarketPlaceAllAd[row + ( pageListAllAd * 10 )]["price"]} BYN\n'
            
        pair = 0
        for i in range(countInPage):
            if countInPage % 2 != 0:
                A.insert(len(A), [types.KeyboardButton(text = f"#{(i + 1) + ( pageListAllAd * 10 )}")])
            else:
                pair += 1
                A.insert(len(A), [types.KeyboardButton(text = f"#{(i + pair) + ( pageListAllAd * 10 )}"), 
                                  types.KeyboardButton(text = f"#{(i + pair + 1) + ( pageListAllAd * 10 )}")])
                if pair == (countInPage/2):
                    break

        A.insert(len(A), [types.KeyboardButton(text = f"Отмена")])
                
        await message.answer(text = allText, parse_mode = 'html', reply_markup = types.ReplyKeyboardMarkup(
                        keyboard = A,
                        resize_keyboard = True
                    )
                ) 

@router.message(classes.toMarketPlace.TypeViewAd_list)
async def button_viewlist(message: types.Message, state: FSMContext):
    if message.text and message.text.lower() == 'отмена':
        await state.clear()
        await state.set_state(classes.toMarketPlace.selectTypeViewAd)
        await message.answer(text = "Выберите тип просмотра", reply_markup = types.ReplyKeyboardMarkup(
                    keyboard=[
                            [
                                types.KeyboardButton(text="Поиск по диапозону цен")
                            ],
                            [
                                types.KeyboardButton(text="Пролистывание")
                            ],
                            [
                                types.KeyboardButton(text="Все объявления")
                            ],
                            [
                                types.KeyboardButton(text="Назад")
                            ]
                        ],
                    resize_keyboard=True,
                ),
            )
    if message.text and message.text.lower() == 'далее':
        data = await state.get_data()
        previous_id = data["TypeViewAd_list_item"]

        await state.clear()

        await state.set_state(classes.toMarketPlace.TypeViewAd_list)
        try:
            row = base.cursor.execute(f"SELECT * FROM marketplace WHERE id > {previous_id} ORDER BY id ASC LIMIT 1").fetchone()
            await state.update_data(TypeViewAd_list_item = row[0])
            if str(row[5]) == '0': 
                await message.answer(text = f'<b>{row[2]}</b>\n\nСостояние: <code>{row[3]}</code>\nЦена: <code>{row[4]}</code>\nКомментарий: <code>{row[6]}</code>\n\n\
Продавец: {base.cursor.execute(f"SELECT `username` FROM `users` WHERE `userid` = {row[1]}").fetchone()[0]} [ID: <a href="tg://user?id={row[1]}">{row[1]}</a>]', parse_mode = "html", reply_markup = types.ReplyKeyboardMarkup(
                                keyboard=[
                                    [
                                        types.KeyboardButton(text="Отмена"),
                                        types.KeyboardButton(text="Далее")
                                    ]
                                ],
                                resize_keyboard=True,
                            ),
                        )
            else:
                await message.answer_photo(photo = row[5], caption = f'<b>{row[2]}</b>\n\nСостояние: <code>{row[3]}</code>\nЦена: <code>{row[4]}</code>\nКомментарий: <code>{row[6]}</code>\n\n\
Продавец: {base.cursor.execute(f"SELECT `username` FROM `users` WHERE `userid` = {row[1]}").fetchone()[0]} [ID: <a href="tg://user?id={row[1]}">{row[1]}</a>]', parse_mode = "html", reply_markup = types.ReplyKeyboardMarkup(
                                keyboard=[
                                    [
                                        types.KeyboardButton(text="Отмена"),
                                        types.KeyboardButton(text="Далее")
                                    ]
                                ],
                                resize_keyboard=True,
                            ),
                        )
        except:
            await state.clear()
            await state.set_state(classes.toMarketPlace.selectTypeViewAd)
            await message.answer(text = "Вы долистали до конца", reply_markup = types.ReplyKeyboardMarkup(
                        keyboard=[
                                [
                                    types.KeyboardButton(text="Поиск по диапозону цен")
                                ],
                                [
                                    types.KeyboardButton(text="Пролистывание")
                                ],
                                [
                                    types.KeyboardButton(text="Все объявления")
                                ],
                                [
                                    types.KeyboardButton(text="Назад")
                                ]
                            ],
                        resize_keyboard=True,
                    ),
                )
        
@router.message(classes.toMarketPlace.TypeViewAd_minprice)
async def button_selectview(message: types.Message, state: FSMContext):
    if message.text and message.text.lower() == 'отмена':
        await state.clear()
        await state.set_state(classes.toMarketPlace.selectTypeViewAd)
        await message.answer(text = "Выберите тип просмотра", reply_markup = types.ReplyKeyboardMarkup(
                    keyboard=[
                            [
                                types.KeyboardButton(text="Поиск по диапозону цен")
                            ],
                            [
                                types.KeyboardButton(text="Пролистывание")
                            ],
                            [
                                types.KeyboardButton(text="Все объявления")
                            ],
                            [
                                types.KeyboardButton(text="Назад")
                            ]
                        ],
                    resize_keyboard=True,
                ),
            )
    else:
        try:
            await state.update_data(TypeViewAd_minprice = int(message.text))
            await state.set_state(classes.toMarketPlace.TypeViewAd_maxprice)
            await message.answer(text = "Выберите максимальную цену.\n\nПример: <code>50</code>", reply_markup = types.ReplyKeyboardMarkup(
                    keyboard=[
                        [
                            types.KeyboardButton(text = "Отмена")
                        ]
                    ],
                    resize_keyboard=True,
                ), parse_mode = "html")
            #base.cursor.execute("SELECT * FROM marketplace WHERE price ")
        except:
            await state.clear()
            await state.set_state(classes.toMarketPlace.TypeViewAd_minprice)
            await message.answer(text = "Ошибка! Введите числовое значение\n\nПример: <code>30</code>", parse_mode = "html", reply_markup = types.ReplyKeyboardMarkup(
                            keyboard=[
                                [
                                    types.KeyboardButton(text="Отмена")
                                ]
                            ],
                            resize_keyboard=True,
                        ),
                    )
            
@router.message(classes.toMarketPlace.TypeViewAd_maxprice)
async def button_selectview(message: types.Message, state: FSMContext):
    func_used = False
    if message.text and message.text.lower() == 'назад':
        try:
            func_used = True
            data = await state.get_data()
            max_price = data["TypeViewAd_price_view_max"]
            min_price = data["TypeViewAd_price_view_min"]
            await state.clear()
            await state.set_state(classes.toMarketPlace.TypeViewAd_price_view)
            await state.update_data(TypeViewAd_maxprice = max_price)
            await state.update_data(TypeViewAd_minprice = min_price)
            count = 0
            allText = '<b>Объявления: </b>\n\n'

            for row in base.cursor.execute(f"SELECT * FROM marketplace WHERE price >= {min_price} AND price <= {max_price}"):
                count += 1
                allText += f'#{count} | {row[2]} | {row[4]} BYN\n'

            if count == 0:
                await state.clear()
                await state.set_state(classes.toMarketPlace.selectTypeViewAd)
                await message.answer(text = "Ничего не найдено", reply_markup = types.ReplyKeyboardMarkup(
                            keyboard=[
                                    [
                                        types.KeyboardButton(text="Поиск по диапозону цен")
                                    ],
                                    [
                                        types.KeyboardButton(text="Пролистывание")
                                    ],
                                    [
                                        types.KeyboardButton(text="Все объявления")
                                    ],
                                    [
                                        types.KeyboardButton(text="Назад")
                                    ]
                                ],
                            resize_keyboard=True,
                        ),
                    )
                return

            # матрицу создаем
            matrix = int(math.sqrt(count))
            A = [ [0]*int(count/matrix) for i in range(matrix) ]
                    
                    # если нечетное число
            if count % matrix != 0:
                    for i in range(count % matrix):
                        A.insert(len(A), [0])


            # заполняем матрицу
            c_count_x = 0
            c_count_y = 0
            c_count = 0
            for row in base.cursor.execute(f"SELECT * FROM marketplace WHERE price >= {min_price} AND price <= {max_price}"):
                c_count += 1
                A[c_count_x][c_count_y] = types.KeyboardButton(text = f"#{c_count}")
                c_count_y += 1
                if c_count_y == len(A[c_count_x]):
                    c_count_x += 1
                    c_count_y = 0
            A.insert(len(A), [types.KeyboardButton(text = f"Отмена")])


            await message.answer(text = allText, parse_mode = 'html', reply_markup = types.ReplyKeyboardMarkup(
                        keyboard = A,
                        resize_keyboard = True
                    )
                )
        except:
            await state.clear()
            await state.set_state(classes.toMarketPlace.TypeViewAd_maxprice)
            await message.answer(text = "Ошибка! Введите числовое значение\n\nПример: <code>30</code>", parse_mode = "html", reply_markup = types.ReplyKeyboardMarkup(
                            keyboard=[
                                [
                                    types.KeyboardButton(text="Отмена")
                                ]
                            ],
                            resize_keyboard=True,
                        ),
                    )
    if message.text and message.text.lower() == 'отмена':
        await state.clear()
        await state.set_state(classes.toMarketPlace.selectTypeViewAd)
        await message.answer(text = "Выберите тип просмотра", reply_markup = types.ReplyKeyboardMarkup(
                    keyboard=[
                            [
                                types.KeyboardButton(text="Поиск по диапозону цен")
                            ],
                            [
                                types.KeyboardButton(text="Пролистывание")
                            ],
                            [
                                types.KeyboardButton(text="Все объявления")
                            ],
                            [
                                types.KeyboardButton(text="Назад")
                            ]
                        ],
                    resize_keyboard=True,
                ),
            )
    elif func_used == False:
        try:
            await state.update_data(TypeViewAd_maxprice = int(message.text))
            await state.set_state(classes.toMarketPlace.TypeViewAd_price_view)
            data = await state.get_data()
            max_price = data["TypeViewAd_maxprice"]
            min_price = data["TypeViewAd_minprice"]
            count = 0
            allText = '<b>Объявления: </b>\n\n'

            for row in base.cursor.execute(f"SELECT * FROM marketplace WHERE price >= {min_price} AND price <= {max_price}"):
                count += 1
                allText += f'#{count} | {row[2]} | {row[4]} BYN\n'
            if count == 0:
                await state.clear()
                await state.set_state(classes.toMarketPlace.selectTypeViewAd)
                await message.answer(text = "Ничего не найдено", reply_markup = types.ReplyKeyboardMarkup(
                            keyboard=[
                                    [
                                        types.KeyboardButton(text="Поиск по диапозону цен")
                                    ],
                                    [
                                        types.KeyboardButton(text="Пролистывание")
                                    ],
                                    [
                                        types.KeyboardButton(text="Все объявления")
                                    ],
                                    [
                                        types.KeyboardButton(text="Назад")
                                    ]
                                ],
                            resize_keyboard=True,
                        ),
                    )
                return

            # матрицу создаем
            matrix = int(math.sqrt(count))
            A = [ [0]*int(count/matrix) for i in range(matrix) ]
                    
                    # если нечетное число
            if count % matrix != 0:
                    for i in range(count % matrix):
                        A.insert(len(A), [0])

            # заполняем матрицу
            c_count_x = 0
            c_count_y = 0
            c_count = 0
            for row in base.cursor.execute(f"SELECT * FROM marketplace WHERE price >= {min_price} AND price <= {max_price}"):
                c_count += 1
                A[c_count_x][c_count_y] = types.KeyboardButton(text = f"#{c_count}")
                c_count_y += 1
                if c_count_y == len(A[c_count_x]):
                    c_count_x += 1
                    c_count_y = 0
            A.insert(len(A), [types.KeyboardButton(text = f"Отмена")])


            await message.answer(text = allText, parse_mode = 'html', reply_markup = types.ReplyKeyboardMarkup(
                            keyboard = A,
                            resize_keyboard = True
                        )
                    )
        except:
            await state.clear()
            await state.set_state(classes.toMarketPlace.TypeViewAd_maxprice)
            await message.answer(text = "Ошибка! Введите числовое значение\n\nПример: <code>30</code>", parse_mode = "html", reply_markup = types.ReplyKeyboardMarkup(
                            keyboard=[
                                [
                                    types.KeyboardButton(text="Отмена")
                                ]
                            ],
                            resize_keyboard=True,
                        ),
                    )
        
@router.message(classes.toMarketPlace.TypeViewAd_price_view)
async def button_viewprice(message: types.Message, state: FSMContext):
    if message.text and message.text.lower() == 'отмена':
        await state.clear()
        await state.set_state(classes.toMarketPlace.selectTypeViewAd)
        await message.answer(text = "Выберите тип просмотра", reply_markup = types.ReplyKeyboardMarkup(
                    keyboard=[
                            [
                                types.KeyboardButton(text="Поиск по диапозону цен")
                            ],
                            [
                                types.KeyboardButton(text="Пролистывание")
                            ],
                            [
                                types.KeyboardButton(text="Все объявления")
                            ],
                            [
                                types.KeyboardButton(text="Назад")
                            ]
                        ],
                    resize_keyboard=True,
                ),
            )
    if message.text and str(message.text.lower())[0] == '#':
        try:
            chooseAd = int(str(message.text.lower()).replace("#", "", 1))
            data = await state.get_data()
            max_price = data["TypeViewAd_maxprice"]
            min_price = data["TypeViewAd_minprice"]
            count = 0
            await state.clear()
            await state.set_state(classes.toMarketPlace.TypeViewAd_maxprice)
            await state.update_data(TypeViewAd_price_view_max = max_price)
            await state.update_data(TypeViewAd_price_view_min = min_price)
            for row in base.cursor.execute(f"SELECT * FROM marketplace WHERE price >= {min_price} AND price <= {max_price}"):
                count += 1
                if count == chooseAd:
                    if str(row[5]) == '0': 
                        await message.answer(text = f'<b>{row[2]}</b>\n\nСостояние: <code>{row[3]}</code>\nЦена: <code>{row[4]}</code>\nКомментарий: <code>{row[6]}</code>\n\n\
Продавец: {base.cursor.execute(f"SELECT username FROM users WHERE userid = {row[1]}").fetchone()[0]} [ID: <a href="tg://user?id={row[1]}">{row[1]}</a>]', parse_mode = "html", reply_markup = types.ReplyKeyboardMarkup(
                            keyboard=[
                                [
                                    types.KeyboardButton(text="Назад")
                                ]
                            ],
                            resize_keyboard=True,
                        ),
                    )
                    else:
                        await message.answer_photo(photo = row[5], caption = f'<b>{row[2]}</b>\n\nСостояние: <code>{row[3]}</code>\nЦена: <code>{row[4]}</code>\nКомментарий: <code>{row[6]}</code>\n\n\
Продавец: {base.cursor.execute(f"SELECT username FROM users WHERE userid = {row[1]}").fetchone()[0]} [ID: <a href="tg://user?id={row[1]}">{row[1]}</a>]', parse_mode = "html", reply_markup = types.ReplyKeyboardMarkup(
                            keyboard=[
                                [
                                    types.KeyboardButton(text="Назад")
                                ]
                            ],
                            resize_keyboard=True,
                        ),
                    )

        except:
            await state.clear()
            await state.set_state(classes.toMarketPlace.selectTypeViewAd)
            await message.answer(text = "Ошибка! Обратитесь в <b>Support/Help</b>\n\nПеренаправляем Вас назад.", reply_markup = types.ReplyKeyboardMarkup(
                        keyboard=[
                                [
                                    types.KeyboardButton(text="Поиск по диапозону цен")
                                ],
                                [
                                    types.KeyboardButton(text="Пролистывание")
                                ],
                                [
                                    types.KeyboardButton(text="Все объявления")
                                ],
                                [
                                    types.KeyboardButton(text="Назад")
                                ]
                            ],
                        resize_keyboard=True,
                    ),
                )


@router.message(classes.toMarketPlace.chooseMyAd)
async def button_choosemyad(message: types.Message, state: FSMContext):
    if message.text and message.text.lower() == 'назад':
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
        
    if message.text and message.text.lower() == 'добавить объявление':
        await state.set_state(classes.toMarketPlace.addAdName)
        await message.answer(text = "Введите название Вашего устройства\n\nПример: <code>Smoant Pasito 2</code>", parse_mode = "html", reply_markup = types.ReplyKeyboardRemove())
        
    if message.text and str(message.text.lower())[0] == '#':
        try:
            chooseAd = int(str(message.text.lower()).replace("#", "", 1))
            ad = base.cursor.execute(f"SELECT * FROM marketplace WHERE uid = {message.from_user.id}")
            count = 0
            for row in base.cursor.execute(f"SELECT * FROM marketplace WHERE uid = {message.from_user.id}"):
                count += 1
                if chooseAd == count:
                    await state.update_data(chooseMyAd = row[0])
                    await state.set_state(classes.toMarketPlace.selectedAd)
                    # добавить проверку, если прикреплено photo_id, то answer_photo
                    if str(row[5]) == '0': 
                        await message.answer(text = f"<b>{row[2]}</b>\n\nСостояние: <code>{row[3]}</code>\nЦена: <code>{row[4]}</code>\nВаш комментарий: <code>{row[6]}</code>\n\n", parse_mode = "html", reply_markup = types.ReplyKeyboardMarkup(
                            keyboard=[
                                [
                                    types.KeyboardButton(text="Редактировать объявление"),
                                    types.KeyboardButton(text="Удалить объявление"),
                                    types.KeyboardButton(text="Назад")
                                ]
                            ],
                            resize_keyboard=True,
                        ),
                    )
                    else:
                        await message.answer_photo(photo = row[5],caption = f"<b>{row[2]}</b>\n\nСостояние: <code>{row[3]}</code>\nЦена: <code>{row[4]}</code>\nВаш комментарий: <code>{row[6]}</code>\n\n", parse_mode = "html", reply_markup = types.ReplyKeyboardMarkup(
                            keyboard=[
                                [
                                    types.KeyboardButton(text="Редактировать объявление"),
                                    types.KeyboardButton(text="Удалить объявление"),
                                    types.KeyboardButton(text="Назад")
                                ]
                            ],
                            resize_keyboard=True,
                        ),
                    )
        except:
            await state.clear()
            await state.set_state(classes.toMarketPlace.chooseMenu)
            await message.answer(text = "Ошибка! Обратитесь в <b>Support/Help</b>\n\nПеренаправляем Вас назад.", parse_mode = "html", reply_markup = types.ReplyKeyboardMarkup(
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
            
@router.message(classes.toMarketPlace.selectedAd)
async def edit_ad(message: types.Message, state: FSMContext):
    if message.text and message.text.lower() == 'редактировать объявление':
        #переправлять в addAd
        await message.answer(text = "Что желаете отредактировать?", reply_markup = types.ReplyKeyboardMarkup(
                    keyboard=[
                        [
                            types.KeyboardButton(text="Название"),
                            types.KeyboardButton(text="Состояние")
                        ],
                        [
                            types.KeyboardButton(text="Цену"),
                            types.KeyboardButton(text="Комментарий")
                        ],
                        [
                            types.KeyboardButton(text="Фотографию"),
                        ],
                        [
                            types.KeyboardButton(text="Отмена"),
                        ]
                    ],
                    resize_keyboard=True,
                )
            )
        await state.set_state(classes.toMarketPlace.editAd)

    if message.text and message.text.lower() == 'удалить объявление':
        await message.answer(text = f"Вы уверены, что хотите удалить данное объявление? \n\n\
", parse_mode = "html", reply_markup = types.ReplyKeyboardMarkup(
                    keyboard=[
                        [
                            types.KeyboardButton(text="Да, уверен"),
                            types.KeyboardButton(text="Отмена")
                        ]
                    ],
                    resize_keyboard=True,
                )
)
        await state.set_state(classes.toMarketPlace.confirmDeleteAd)

    if message.text and message.text.lower() == 'назад':
        await state.clear()
        await state.set_state(classes.toMarketPlace.chooseMyAd)
        # await message.answer(text = "В разработке", reply_markup = markup.mainMenu)
        allText = '<b>Ваши объявления: </b>\n\n'
        count = 0
        keyboard = [[types.KeyboardButton(text = f"Назад")]]
        for row in base.cursor.execute(f"SELECT * FROM marketplace WHERE uid = {message.from_user.id}"):
            count += 1
            allText += f'<b>#{count} </b>| {row[2]} | {row[4]} BYN\n'
            keyboard.insert(count, [types.KeyboardButton(text = f"#{count}")]) 
        allText += "\n<i>Выберите номер объявления ниже, для редактирования</i>"
        keyboard.insert(count + 1, [types.KeyboardButton(text = "Добавить объявление")])
        await message.answer(text = allText, parse_mode = "html", reply_markup = types.ReplyKeyboardMarkup(
                    keyboard=keyboard,
                    resize_keyboard=True
                )
            )
        
@router.message(classes.toMarketPlace.confirmDeleteAd)
async def confirmDeteleAd(message: types.Message, state: FSMContext):
    if message.text and message.text.lower() == 'да, уверен':
        data = await state.get_data()
        id_Ad = data["chooseMyAd"]

        print(id_Ad)

        base.cursor.execute(f"DELETE FROM marketplace WHERE id = '{id_Ad}'") # удаляем с бд
        base.conn.commit()

        for row in range(len(localdata.localMarketPlaceAllAd)): # ищем в локалке
            if int(id_Ad) == int(localdata.localMarketPlaceAllAd[row]["id"]):
                localdata.localMarketPlaceAllAd.pop(row) # удаляем с локалки
                break
        

        await state.clear()
        await state.set_state(classes.toMarketPlace.chooseMenu)
        await message.answer(text = "<b>Вы успешно удалили объявление</b>\n\nПеренаправляем Вас назад.", parse_mode = "html", reply_markup = types.ReplyKeyboardMarkup(
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
    if message.text and message.text.lower() == 'отмена':
        await state.clear()
        await state.set_state(classes.toMarketPlace.chooseMenu)
        await message.answer(text = "<b>Вы отказались от удаления объявления</b>\n\nПеренаправляем Вас назад.", parse_mode = "html", reply_markup = types.ReplyKeyboardMarkup(
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


@router.message(classes.toMarketPlace.editAd)
async def editAd(message: types.Message, state: FSMContext):
    if message.text and message.text.lower() == 'название':
        await message.answer(text = "Введите название Вашего устройства\n\nПример: <code>Smoant Pasito 2</code>", parse_mode = "html", reply_markup = types.ReplyKeyboardMarkup(
                    keyboard=[
                        [
                            types.KeyboardButton(text="Отмена")
                        ]
                    ],
                    resize_keyboard=True,
                )
            )
        await state.set_state(classes.toMarketPlace.editAdName)
    if message.text and message.text.lower() == 'состояние':
        await message.answer(text = "Введите состояние Вашего устройства\n\nПример: <code>нормальное</code>", parse_mode = "html", reply_markup = types.ReplyKeyboardMarkup(
                    keyboard=[
                        [
                            types.KeyboardButton(text="Отмена")
                        ]
                    ],
                    resize_keyboard=True,
                )
            )
        await state.set_state(classes.toMarketPlace.editAdStatus)
    if message.text and message.text.lower() == 'цену':
        await message.answer(text = "Сколько BYN вы хотите за Ваше устройство? (цифру)\n\nПример: <code>65</code>", parse_mode = "html", reply_markup = types.ReplyKeyboardMarkup(
                    keyboard=[
                        [
                            types.KeyboardButton(text="Отмена")
                        ]
                    ],
                    resize_keyboard=True,
                )
            )
        await state.set_state(classes.toMarketPlace.editAdPrice)
    if message.text and message.text.lower() == 'комментарий':
        await message.answer(text = "Введите комментарий покупателю\n\nПример: <code>В комплекте: фулл допы. Возможен торг</code>", parse_mode = "html", reply_markup = types.ReplyKeyboardMarkup(
                    keyboard=[
                        [
                            types.KeyboardButton(text="Отмена")
                        ]
                    ],
                    resize_keyboard=True,
                )
            )
        await state.set_state(classes.toMarketPlace.editAdComment)
    if message.text and message.text.lower() == 'фотографию':
        await message.answer(text = "Прикрепите фотографию Вашего устройства (1 шт.)", parse_mode = "html", reply_markup = types.ReplyKeyboardMarkup(
                    keyboard=[
                        [
                            types.KeyboardButton(text="Отмена")
                        ]
                    ],
                    resize_keyboard=True,
                )
            )
        await state.set_state(classes.toMarketPlace.editAdPhoto)
    if message.text and message.text.lower() == 'отмена':
        pass

@router.message(classes.toMarketPlace.editAdName)
async def editAd(message: types.Message, state: FSMContext):
    data = await state.get_data()
    id_Ad = data["chooseMyAd"]
    base.cursor.execute(f"UPDATE marketplace SET name = '{message.text}' WHERE id = '{id_Ad}'")
    base.conn.commit()

    for row in range(len(localdata.localMarketPlaceAllAd)): # ищем в локалке
        if int(id_Ad) == int(localdata.localMarketPlaceAllAd[row]["id"]):
            localdata.localMarketPlaceAllAd[row]["name"] = message.text
    
    await state.clear()
    await message.answer(text = "<b>✅Вы успешно изменили название Вашего устройства!</b>\n\nВы были перенаправлены в главное меню", reply_markup = markup.mainMenu, parse_mode = "html")

@router.message(classes.toMarketPlace.editAdStatus)
async def editAd(message: types.Message, state: FSMContext):
    data = await state.get_data()
    id_Ad = data["chooseMyAd"]
    base.cursor.execute(f"UPDATE marketplace SET status = '{message.text}' WHERE id = '{id_Ad}'")
    base.conn.commit()

    for row in range(len(localdata.localMarketPlaceAllAd)): # ищем в локалке
        if int(id_Ad) == int(localdata.localMarketPlaceAllAd[row]["id"]):
            localdata.localMarketPlaceAllAd[row]["name"] = message.text

    await state.clear()
    await message.answer(text = "<b>✅Вы успешно изменили статус Вашего устройства!</b>\n\nВы были перенаправлены в главное меню", reply_markup = markup.mainMenu, parse_mode = "html")

@router.message(classes.toMarketPlace.editAdPrice)
async def editAd(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        data = await state.get_data()
        id_Ad = data["chooseMyAd"]
        base.cursor.execute(f"UPDATE marketplace SET price = '{message.text}' WHERE id = '{id_Ad}'")
        base.conn.commit()

        for row in range(len(localdata.localMarketPlaceAllAd)): # ищем в локалке
            if int(id_Ad) == int(localdata.localMarketPlaceAllAd[row]["id"]):
                localdata.localMarketPlaceAllAd[row]["name"] = message.text

        await state.clear()
        await message.answer(text = "<b>✅Вы успешно изменили название Вашего устройства!</b>\n\nВы были перенаправлены в главное меню", reply_markup = markup.mainMenu, parse_mode = "html")
    else:
        await state.clear()
        await message.answer(text = "<b>Ошибка, указана не цифра</b>\n\nВы были перенаправлены в главное меню", reply_markup = markup.mainMenu, parse_mode = "html")

@router.message(classes.toMarketPlace.editAdComment)
async def editAd(message: types.Message, state: FSMContext):
    data = await state.get_data()
    id_Ad = data["chooseMyAd"]
    base.cursor.execute(f"UPDATE marketplace SET comment = '{message.text}' WHERE id = '{id_Ad}'")
    base.conn.commit()

    for row in range(len(localdata.localMarketPlaceAllAd)): # ищем в локалке
        if int(id_Ad) == int(localdata.localMarketPlaceAllAd[row]["id"]):
            localdata.localMarketPlaceAllAd[row]["name"] = message.text

    await state.clear()
    await message.answer(text = "<b>✅Вы успешно изменили название Вашего устройства!</b>\n\nВы были перенаправлены в главное меню", reply_markup = markup.mainMenu, parse_mode = "html")

@router.message(classes.toMarketPlace.editAdPhoto)
async def editAd(message: types.Message, state: FSMContext):
    if message.photo[-1]:
        data = await state.get_data()
        id_Ad = data["chooseMyAd"]
        base.cursor.execute(f"UPDATE marketplace SET photo_id = '{message.photo[-1].file_id}' WHERE id = '{id_Ad}'")
        base.conn.commit()

        for row in range(len(localdata.localMarketPlaceAllAd)): # ищем в локалке
            if int(id_Ad) == int(localdata.localMarketPlaceAllAd[row]["id"]):
                localdata.localMarketPlaceAllAd[row]["name"] = message.photo[-1].file_id

        await state.clear()
        await message.answer(text = "<b>✅Вы успешно изменили название Вашего устройства!</b>\n\nВы были перенаправлены в главное меню", reply_markup = markup.mainMenu, parse_mode = "html")
    else:
        await state.clear()
        await message.answer(text = "<b>Ошибка, не прикреплена фотография</b>\n\nВы были перенаправлены в главное меню", reply_markup = markup.mainMenu, parse_mode = "html")

@router.message(classes.toMarketPlace.addAdPhoto)
async def button_skip(message: types.Message, state: FSMContext):
    if message.text and message.text.lower() == 'пропустить':
        data = await state.get_data()
        namePod = data["addAdName"]
        statusPod = data["addAdStatus"]
        pricePod = data["addAdPrice"]
        addAdComment = data["addAdComment"]
        await state.clear()
        await message.answer(text = "<b>✅ - Вы успешно добавили своё объявление</b>\n\nВы были перенаправлены в главное меню.", reply_markup = markup.mainMenu, parse_mode = "html")
        # TODO пересылку сделать

        localdata.localMarketPlaceAllAd.insert(len(localdata.localMarketPlaceAllAd), {
                  "id":len(localdata.localMarketPlaceAllAd),
                  "uid":message.from_user.id,
                  "name":namePod,
                  "status":statusPod,
                  "price":pricePod,
                  "photo_id":'0',
                  "comment":addAdComment
            })
        base.cursor.execute(f"INSERT INTO marketplace (uid, name, status, price, photo_id, comment) VALUES ('{message.from_user.id}', '{namePod}', '{statusPod}', '{pricePod}', '0', '{addAdComment}')")
        base.conn.commit()
        await state.clear()
    else:
        if message.photo[-1]:
            data = await state.get_data()
            namePod = data["addAdName"]
            statusPod = data["addAdStatus"]
            pricePod = data["addAdPrice"]
            addAdComment = data["addAdComment"]
            await state.clear()
            await message.answer(text = "<b>✅ - Вы успешно добавили своё объявление</b>\n\nВы были перенаправлены в главное меню.", reply_markup = markup.mainMenu, parse_mode = "html")
            # TODO сделать добавление в локал

            localdata.localMarketPlaceAllAd.insert(len(localdata.localMarketPlaceAllAd), {
                  "id":len(localdata.localMarketPlaceAllAd),
                  "uid":message.from_user.id,
                  "name":namePod,
                  "status":statusPod,
                  "price":pricePod,
                  "photo_id":message.photo[-1].file_id,
                  "comment":addAdComment
            })
            base.cursor.execute(f"INSERT INTO marketplace (uid, name, status, price, photo_id, comment) VALUES ('{message.from_user.id}', '{namePod}', '{statusPod}', '{pricePod}', '{message.photo[-1].file_id}', '{addAdComment}')")
            base.conn.commit()
            await state.clear()
        else:
            await state.clear()
            await message.answer(text = "<b>Ошибка, не прикреплена фотография</b>\n\nВы были перенаправлены в главное меню", reply_markup = markup.mainMenu, parse_mode = "html")
        
@router.message(classes.toMarketPlace.addAdName)
async def process_sellpod_stage1(message: types.Message, state: FSMContext):
    await state.update_data(addAdName = message.text)

    await message.answer(text = "Какое состояние вашего устройства?\n\nПример: <code>нормальное</code>", parse_mode = "html")
    await state.set_state(classes.toMarketPlace.addAdStatus)

@router.message(classes.toMarketPlace.addAdStatus)
async def process_sellpod_stage1(message: types.Message, state: FSMContext):
    await state.update_data(addAdStatus = message.text)

    await message.answer(text = "Желаете оставить комментарий покупателю?\n\nПример: <code>В комплекте: фулл допы. Возможен торг</code>", parse_mode = "html")
    await state.set_state(classes.toMarketPlace.addAdComment)

@router.message(classes.toMarketPlace.addAdComment)
async def process_sellpod_stage1(message: types.Message, state: FSMContext):
    await state.update_data(addAdComment = message.text)

    await message.answer(text = "Сколько BYN вы хотите за Ваше устройство? (цифру)\n\nПример: <code>65</code>", parse_mode = "html")
    await state.set_state(classes.toMarketPlace.addAdPrice)

@router.message(classes.toMarketPlace.addAdPrice)
async def process_sellpod_stage1(message: types.Message, state: FSMContext):
    await state.update_data(addAdPrice = message.text)

    await message.answer(text = "Прикрепите 1 фотографию вашего устройства. (по желанию)\n\nЛибо нажмите \"Пропустить\"", parse_mode = "html", reply_markup = types.ReplyKeyboardMarkup(
                keyboard=[
                    [
                        types.KeyboardButton(text="/отмена")
                    ],
                    [
                        types.KeyboardButton(text="Пропустить")
                    ]
                ],
                resize_keyboard=True,
            ),
        )

    await state.set_state(classes.toMarketPlace.addAdPhoto)
