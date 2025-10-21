import os
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Проверка переменных окружения
def check_environment():
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')
    
    if not BOT_TOKEN:
        logger.error("❌ BOT_TOKEN не установлен!")
        return None, None
    
    if not ADMIN_CHAT_ID:
        logger.error("❌ ADMIN_CHAT_ID не установлен!")
        return None, None
    
    logger.info("✅ Переменные окружения загружены успешно")
    return BOT_TOKEN, ADMIN_CHAT_ID

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.message.from_user
        welcome_text = f"""
👋 Привет, {user.first_name}!

Я бот для связи с администратором. 
Просто напишите ваше сообщение, и я перешлю его администратору.
        """
        await update.message.reply_text(welcome_text)
    except Exception as e:
        logger.error(f"Ошибка в команде /start: {e}")

async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        BOT_TOKEN, ADMIN_CHAT_ID = check_environment()
        if not BOT_TOKEN or not ADMIN_CHAT_ID:
            await update.message.reply_text("❌ Бот временно недоступен")
            return

        user = update.message.from_user
        message_text = update.message.text
        
        user_info = f"{user.first_name} {user.last_name or ''} (@{user.username or 'нет'})"
        
        admin_message = f"""
📩 Новое сообщение от пользователя:
👤 {user_info}
🆔 ID: {user.id}
💬 Сообщение: {message_text}
        """
        
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=admin_message
        )
        await update.message.reply_text("✅ Ваше сообщение отправлено администратору!")
        
    except Exception as e:
        logger.error(f"Ошибка обработки сообщения: {e}")
        await update.message.reply_text("❌ Ошибка при отправке сообщения")

def main():
    logger.info("🔄 Запуск бота...")
    
    # Проверяем переменные окружения
    BOT_TOKEN, ADMIN_CHAT_ID = check_environment()
    if not BOT_TOKEN or not ADMIN_CHAT_ID:
        logger.error("⛔ Не удалось запустить бота: отсутствуют переменные окружения")
        return
    
    try:
        # Создаем приложение
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Добавляем обработчики
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_message))
        
        # Запускаем бота
        logger.info("✅ Бот успешно запущен и готов к работе!")
        print("✅ Бот успешно запущен и готов к работе!")
        
        # Бесконечный polling
        application.run_polling()
        
    except Exception as e:
        logger.error(f"⛔ Критическая ошибка при запуске бота: {e}")

if __name__ == "__main__":
    main()
