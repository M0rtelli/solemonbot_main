from aiogram import F, Router
from aiogram import types
from aiogram.fsm.context import FSMContext
from typing import Any, Dict

import markup as markup
import app.classes as classes

router = Router()

@router.message(classes.sellPod.photoPod)
async def button_skip(message: types.Message, state: FSMContext):
    if message.text and message.text.lower() == 'пропустить':
        data = await state.get_data()
        namePod = data["namePod"]
        statusPod = data["statusPod"]
        pricePod = data["pricePod"]
        await state.clear()
        await message.answer(text = "<b>✅ - Ваша заявка была успешно отправлена! Ожидайте ответа от администрации</b>\n\nВы были перенаправлены в главное меню.", reply_markup = markup.mainMenu, parse_mode = "html")
        # TODO пересылку сделать
        text = f'<b>Новая заявка</b>\n\n\
Отправитель - @{message.from_user.username} [ID: <a href="tg://user?id={message.from_user.id}">{message.from_user.id}</a>]\n\
Устройство - {namePod}\n\
Состояние - {statusPod}\n\
Цена - {pricePod}'
        await message.bot.send_message(chat_id = -1002124965943, text = text, parse_mode = "html")
    else:
        if message.photo[-1]:
            data = await state.get_data()
            namePod = data["namePod"]
            statusPod = data["statusPod"]
            pricePod = data["pricePod"]
            await state.clear()
            await message.answer(text = "<b>✅ - Ваша заявка была успешно отправлена! Ожидайте ответа от администрации</b>\n\nВы были перенаправлены в главное меню.", reply_markup = markup.mainMenu, parse_mode = "html")
            # TODO пересылку сделать
            text = f'<b>Новая заявка</b>\n\n\
Отправитель - @{message.from_user.username} [ID: <a href="tg://user?id={message.from_user.id}">{message.from_user.id}</a>]\n\
Устройство - {namePod}\n\
Состояние - {statusPod}\n\
Цена - {pricePod}'
            await message.bot.send_photo(chat_id = -1002124965943, photo = message.photo[-1].file_id,caption = text, parse_mode = "html")
        else:
            await state.clear()
            await message.answer(text = "<b>Ошибка, не прикреплена фотография</b>\n\nВы были перенаправлены в главное меню", reply_markup = markup.mainMenu, parse_mode = "html")
        
@router.message(classes.sellPod.namePod)
async def process_sellpod_stage1(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await message.reply('Действие отменено.', reply_markup=markup.mainMenu)
        await state.clear()
        return
    await state.update_data(namePod = message.text)

    await message.answer(text = "Какое состояние вашего устройства?\n\nПример: <code>нормальное</code>", parse_mode = "html")
    await state.set_state(classes.sellPod.statusPod)

@router.message(classes.sellPod.statusPod)
async def process_sellpod_stage1(message: types.Message, state: FSMContext):
    await state.update_data(statusPod = message.text)

    await message.answer(text = "Сколько BYN вы хотите за Ваше устройство?\n\nПример: <code>65 BYN</code>", parse_mode = "html")
    await state.set_state(classes.sellPod.pricePod)

@router.message(classes.sellPod.pricePod)
async def process_sellpod_stage1(message: types.Message, state: FSMContext):
    await state.update_data(pricePod = message.text)

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

    await state.set_state(classes.sellPod.photoPod)
