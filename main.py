import asyncio
import logging
import os
import time

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest

from config import BOT_TOKEN, DOCUMENTS_PATH, RATE_LIMIT

# Логирование
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Хранилище времени последнего запроса пользователя
user_last_request = {}


# 📛 Проверка на флуд
def is_rate_limited(user_id: int) -> bool:
    now = time.time()
    last = user_last_request.get(user_id, 0)

    if now - last < RATE_LIMIT:
        return True

    user_last_request[user_id] = now
    return False


# 📂 Отправка документа
async def send_document(message: Message, filename: str, caption: str):
    user_id = message.from_user.id

    if is_rate_limited(user_id):
        await message.answer("⏳ Подожди немного перед следующей командой.")
        return

    file_path = os.path.join(DOCUMENTS_PATH, filename)

    if not os.path.exists(file_path):
        logging.error(f"Файл не найден: {file_path}")
        await message.answer("❌ Документ не найден. Сообщите администрации.")
        return

    try:
        doc = FSInputFile(file_path)
        await message.answer_document(doc, caption=caption)
        logging.info(f"Пользователь {user_id} запросил {filename}")
    except TelegramBadRequest as e:
        logging.error(f"Ошибка отправки файла: {e}")
        await message.answer("⚠️ Ошибка при отправке документа.")


# 📜 /start
@dp.message(Command("start"))
async def start(message: Message):
    text = """
👋 Добро пожаловать в RP Law Bot!

📚 Доступные команды:
/trydkodeks — Трудовой кодекс
/ocnova — Основы законодательства
/konstityciya — Конституция
/KoAP — Кодекс об административных правонарушениях
/YK — Уголовный кодекс
/help — список команд
"""
    await message.answer(text)


# 📜 /help
@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer("""
📚 Список команд:

/trydkodeks
/ocnova
/konstityciya
/KoAP
/YK
""")


# 📄 Команды документов
@dp.message(Command("trydkodeks"))
async def tryd(message: Message):
    await send_document(message, "trydkodeks.pdf", "📄 Трудовой кодекс")


@dp.message(Command("ocnova"))
async def ocnova(message: Message):
    await send_document(message, "ocnova.pdf", "📄 Основы законодательства")


@dp.message(Command("konstityciya"))
async def konst(message: Message):
    await send_document(message, "konstityciya.pdf", "📄 Конституция")


@dp.message(Command("KoAP"))
async def koap(message: Message):
    await send_document(message, "koap.pdf", "📄 КоАП")


@dp.message(Command("YK"))
async def yk(message: Message):
    await send_document(message, "yk.pdf", "📄 Уголовный кодекс")


# 🚀 Запуск бота
async def main():
    logging.info("Бот запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
