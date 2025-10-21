import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

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

def start(update: Update, context: CallbackContext):
    try:
        user = update.message.from_user
        welcome_text = f"""
👋 Привет, {user.first_name}!

Я бот для связи с администратором. 
Просто напишите ваше сообщение, и я перешлю его администратору.
        """
        update.message.reply_text(welcome_text)
    except Exception as e:
        logger.error(f"Ошибка в команде /start: {e}")

def handle_user_message(update: Update, context: CallbackContext):
    try:
        BOT_TOKEN, ADMIN_CHAT_ID = check_environment()
        if not BOT_TOKEN or not ADMIN_CHAT_ID:
            update.message.reply_text("❌ Бот временно недоступен")
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
        
        context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=admin_message
        )
        update.message.reply_text("✅ Ваше сообщение отправлено администратору!")
        
    except Exception as e:
        logger.error(f"Ошибка обработки сообщения: {e}")
        update.message.reply_text("❌ Ошибка при отправке сообщения")

def main():
    logger.info("🔄 Запуск бота...")
    
    # Проверяем переменные окружения
    BOT_TOKEN, ADMIN_CHAT_ID = check_environment()
    if not BOT_TOKEN or not ADMIN_CHAT_ID:
        logger.error("⛔ Не удалось запустить бота: отсутствуют переменные окружения")
        return
    
    try:
        # Создаем updater
        updater = Updater(BOT_TOKEN, use_context=True)
        
        # Получаем dispatcher для регистрации обработчиков
        dp = updater.dispatcher
        
        # Добавляем обработчики
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_user_message))
        
        # Запускаем бота
        updater.start_polling()
        logger.info("✅ Бот успешно запущен и готов к работе!")
        print("✅ Бот успешно запущен и готов к работе!")
        
        # Бесконечный цикл
        updater.idle()
        
    except Exception as e:
        logger.error(f"⛔ Критическая ошибка при запуске бота: {e}")

if __name__ == "__main__":
    main()
