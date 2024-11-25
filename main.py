import os
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from dotenv import load_dotenv
import asyncio

# Загружаем переменные окружения из .env
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_ORG = os.getenv("GITHUB_ORG")
GITHUB_PROJECT_NUMBER = int(os.getenv("GITHUB_PROJECT_NUMBER"))
GITHUB_API_URL = os.getenv("GITHUB_API_URL")

# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()


# Функция для получения списка задач из GitHub Project
def get_github_issues():
    query = """
    query GetProjectItems {
      organization(login: "teamofeydev") {
        projectV2(number: 1) {
          items(first: 20) {
            nodes {
              content {
                ... on Issue {
                  title
                  url
                  body
                  state
                  createdAt
                }
              }
              fieldValues(first: 10) {
                nodes {
                  ... on ProjectV2ItemFieldSingleSelectValue {
                    field {
                      ... on ProjectV2FieldCommon {
                        name
                      }
                    }
                    name
                  }
                }
              }
            }
          }
        }
      }
    }
    """
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    response = requests.post(GITHUB_API_URL, json={"query": query}, headers=headers)
    data = response.json()

    if "errors" in data:
        raise Exception(f"GraphQL errors: {data['errors']}")

    issues = []
    for node in data["data"]["organization"]["projectV2"]["items"]["nodes"]:
        content = node["content"]
        field_values = node.get("fieldValues", {}).get("nodes", [])
        status = "Не указан"
        for field in field_values:
            if field.get("field", {}).get("name") == "Status":
                status = field.get("name", "Не указан")
                break

        issues.append({
            "title": content["title"],
            "url": content["url"],
            "body": content.get("body", ""),
            "state": content["state"],
            "status": status,  # Добавляем статус в объект задачи
            "createdAt": content["createdAt"]
        })

    return issues


# Функция для создания клавиатуры с кнопкой
def create_status_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Получить задачи", callback_data="get_issues")]
        ]
    )
    return keyboard


# Хэндлер для команды /start
@dp.message(Command("start"))
async def start(message: Message):
    # Отправляем сообщение с клавиатурой
    await message.answer(
        "Пока! Я могу получать задачи из GitHub Projects.\n"
        "Используй кнопку ниже, чтобы получить список задач.",
        reply_markup=create_status_keyboard()
    )


# Хэндлер для получения задач по нажатию на кнопку
@dp.callback_query()
async def process_callback(callback_query: types.CallbackQuery):
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


# Основная асинхронная функция для запуска бота
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())