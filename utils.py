from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def create_status_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Получить задачи", callback_data="get_issues")]
        ]
    )