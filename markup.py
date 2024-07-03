from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types


# --- Main Menu ---
mainMenu_btns = [
    [
        types.KeyboardButton(text = "Моя скидочка 💸")
    ],
    [
        types.KeyboardButton(text = "ТОП 🔝"), 
        types.KeyboardButton(text = "О нас")
    ],
    [
        types.KeyboardButton(text = "Правила"),
        types.KeyboardButton(text = "Support/Help")
    ],
    [
        types.KeyboardButton(text = "Скупка устройств 🛍"),
        types.KeyboardButton(text = "Барахолка")
    ],
    [
        types.KeyboardButton(text = "Реферальная система")
    ]
]

mainMenu = types.ReplyKeyboardMarkup(
        keyboard = mainMenu_btns, 
        resize_keyboard = True,
        input_field_placeholder = "Выберите пункт из меню"
    )


# --- Back To Main Menu ---
backToMainMenu_btns = [
    [
        types.KeyboardButton(text = "Назад в меню")
    ]
]

backToMainMenu = types.ReplyKeyboardMarkup(
    keyboard = backToMainMenu_btns,
    resize_keyboard = True
)


# --- Admin menu ---
adminMenu_btns = [
    [
        types.KeyboardButton(text = "Информация о юзере")
    ],
    [
        types.KeyboardButton(text = "Выдать скидку"), 
        types.KeyboardButton(text = "Выдать продажу")
    ],
    [
        types.KeyboardButton(text = "Моя статистика"),
        types.KeyboardButton(text = "Назад в меню")
    ]
]

adminMenu = types.ReplyKeyboardMarkup(
        keyboard = adminMenu_btns, 
        resize_keyboard = True,
        input_field_placeholder = "Выберите пункт из меню"
    )

    


