import pytest
from unittest.mock import AsyncMock, patch
from aiogram.types import Message, CallbackQuery
from handlers import start, process_callback


@patch.dict('os.environ', {
    'GITHUB_TOKEN': 'test-token',
    'GITHUB_API_URL': 'https://api.github.com',
    'GITHUB_ORG': 'test-org',
    'GITHUB_PROJECT_NUMBER': '1',
})

@pytest.mark.asyncio
async def test_start_command(mocker):
    # Мокаем Message объект с помощью AsyncMock
    mock_message = AsyncMock(spec=Message)
    mock_message.answer = AsyncMock()  # Ensure answer is an AsyncMock

    # Вызываем хендлер
    await start(mock_message)

    # Проверяем, что метод answer был вызван с нужным текстом
    mock_message.answer.assert_called_once_with(
        "Привет! Я могу получать задачи из GitHub Projects.\n"
        "Используй кнопку ниже, чтобы получить список задач.",
        reply_markup=mocker.ANY  # Игнорируем конкретное содержимое клавиатуры
    )


@pytest.mark.asyncio
async def test_process_callback(mocker):
    # Mock CallbackQuery object with AsyncMock
    mock_callback_query = AsyncMock(spec=CallbackQuery)
    mock_callback_query.answer = AsyncMock()
    mock_callback_query.message = AsyncMock()
    mock_callback_query.message.answer = AsyncMock()

    # Set the callback query data
    mock_callback_query.data = "get_issues"

    # Mock get_github_issues function
    mock_get_issues = mocker.patch(
        "handlers.get_github_issues",
        return_value=[
            {
                "title": "Test Issue",
                "url": "http://example.com",
                "body": "Test Body",
                "state": "OPEN",
                "status": "In Progress",
                "createdAt": "2024-11-25",
            }
        ],  # Ensure it directly returns the list, not a coroutine
    )

    # Call the handler
    await process_callback(mock_callback_query)

    # Assert message.answer was called with the correct formatted text
    mock_callback_query.message.answer.assert_called_once_with(
        "📊Список всех задач по проекту\n"
        "**Test Issue**\n"
        " -Описание: Test Body\n"
        " -Состояние: OPEN\n"
        " -Статус: In Progress\n"
        " -[Ссылка на задачу](http://example.com)\n"
        "Создана: 2024-11-25\n",
        parse_mode="Markdown",
    )

    # Assert get_github_issues was called once
    mock_get_issues.assert_called_once()
