import markup

from aiogram import types
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

class eventState(StatesGroup):
    sendKonkurs = State()

def loadModule():
    
    markup.mainMenu_btns = [[types.KeyboardButton(text = "🔥Лучшая реклама🔥")]] + markup.mainMenu_btns

    markup.mainMenu = types.ReplyKeyboardMarkup(
        keyboard = markup.mainMenu_btns, 
        resize_keyboard = True,
        input_field_placeholder = "Выберите пункт из меню"
    )


@router.message(F.text.lower() == "🔥лучшая реклама🔥")
async def hanler_button_event( message: types.Message , state: FSMContext ):
    await state.set_state(eventState.sendKonkurs)

    video = types.FSInputFile("src/video/event_info.mp4")
    text = "Привет! Оставляй свою заявку на участие в конкурсе ниже.\n<b>Если что-то не понятно - смотри видеоролик выше</b>"
    await message.answer_video(video = video, 
                               caption = text, 
                               parse_mode = "html", 
                               height = 1038, 
                               width = 480, 
                               reply_markup = types.ReplyKeyboardMarkup(
                                    keyboard=[
                                            [
                                                types.KeyboardButton(text="Отмена")
                                            ]
                                        ],
                                    resize_keyboard=True,
                                )
                            )


@router.message(eventState.sendKonkurs)
async def fsm_event(message: types.Message, state: FSMContext):
    if message.text and message.text.lower() == 'отмена':
        await message.answer(text = "Вы вернулись в главное меню", reply_markup = markup.mainMenu)
        await state.clear()
        return
    msg = await message.send_copy(chat_id = message.chat.id) #-1002165443440
    text = f"<b><code>НОВАЯ ЗАЯВКА НА КОНКУРС</code></b>\n\nОтправитель: @{message.from_user.username} \
[ID: <a href=\"tg://user?id={message.from_user.id}\">{message.from_user.id}</a>]"
    await message.bot.send_message(chat_id = message.chat.id, text = text, # -1002165443440
                                   reply_to_message_id = msg.message_id, parse_mode = "html")
    await message.answer(text = "✅ - Ваша заявка была успешно отправлена администраторам!")
    await state.clear()

