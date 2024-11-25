from aiogram.types import Message, CallbackQuery
from utils import create_status_keyboard
from github import get_github_issues

async def start(message: Message):
    await message.answer(
        "Привет! Я могу получать задачи из GitHub Projects.\n"
        "Используй кнопку ниже, чтобы получить список задач.",
        reply_markup=create_status_keyboard()
    )

async def process_callback(callback_query: CallbackQuery):
    if callback_query.data == "get_issues":
        await callback_query.answer("Получаю список задач из GitHub...")

        try:
            issues = get_github_issues()
            if not issues:
                await callback_query.message.answer("Задачи не найдены.")
                return

            # Форматируем задачи
            formatted_issues = "\n\n".join(
                f"📊Список всех задач по проекту\n"
                f"**{issue['title']}**\n"
                f" -Описание: {issue['body']}\n"
                f" -Состояние: {issue['state']}\n"
                f" -Статус: {issue['status']}\n"  # Добавляем статус в сообщение
                f" -[Ссылка на задачу]({issue['url']})\n"
                f"Создана: {issue['createdAt']}\n"
                for issue in issues
            )

            await callback_query.message.answer(formatted_issues, parse_mode="Markdown")

        except Exception as e:
            await callback_query.message.answer(f"Ошибка при получении задач: {e}")