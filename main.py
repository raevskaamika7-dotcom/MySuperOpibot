import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import google.generativeai as genai

# Настройки
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

# Настройка Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash-image-preview')

# Логирование
logging.basicConfig(level=logging.INFO)

# Команда /start
async def start(update: Update, context):
    await update.message.reply_text(
        "🍌 Привет! Я бот на Nano Banana.\n"
        "Отправь мне фото и текстовый промпт, и я обработаю его!\n\n"
        "Пример: отправьте фото и в подписи напишите: 'сделай освещение как на этом фото'"
    )

# Обработка фото + текста
async def handle_photo(update: Update, context):
    try:
        # Отправляем сообщение о начале обработки
        await update.message.reply_text("🔄 Обрабатываю... Подождите пару секунд.")
        
        # Получаем фото
        photo_file = await update.message.photo[-1].get_file()
        photo_path = "user_photo.png"
        await photo_file.download_to_drive(photo_path)
        
        # Получаем текст (промпт)
        prompt = update.message.caption or "Сделай освещение профессиональным, как на превью"
        
        # Отправляем в Gemini
        myfile = genai.upload_file(photo_path)
        response = model.generate_content([prompt, myfile])
        
        # Сохраняем результат
        with open("result.png", "wb") as f:
            f.write(response._result.candidates[0].content.parts[0].data)
        
        # Отправляем пользователю
        await update.message.reply_photo(photo=open("result.png", "rb"))
        
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}\n\nПопробуйте ещё раз или измените промпт.")

# Команда /help
async def help_command(update: Update, context):
    await update.message.reply_text(
        "📖 Как пользоваться:\n"
        "1. Отправь фото\n"
        "2. В подписи к фото напиши, что хочешь изменить (например, 'сделай как закат')\n"
        "3. Бот вернёт обработанное фото\n\n"
        "Доступные команды:\n"
        "/start - приветствие\n"
        "/help - помощь"
    )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.PHOTO & filters.CAPTION, handle_photo))
    
    print("Бот запущен и готов к работе...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if name == "main":
    main()
