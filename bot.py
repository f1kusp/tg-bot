import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def start(update, context):
    user = update.message.from_user
    update.message.reply_text(f"👋 Привет, {user.first_name}! Я бот для связи с администратором.")

def handle_message(update, context):
    try:
        user = update.message.from_user
        message_text = update.message.text
        
        user_info = f"{user.first_name} {user.last_name or ''} (@{user.username or 'нет'})"
        admin_message = f"📩 Новое сообщение:\n👤 {user_info}\n🆔 ID: {user.id}\n💬 {message_text}"
        
        admin_chat_id = os.getenv('ADMIN_CHAT_ID')
        if admin_chat_id:
            context.bot.send_message(chat_id=admin_chat_id, text=admin_message)
        
        update.message.reply_text("✅ Сообщение отправлено администратору!")
        
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        update.message.reply_text("❌ Ошибка при отправке")

def main():
    logger.info("🔄 Запуск бота...")
    
    token = os.getenv('BOT_TOKEN')
    if not token:
        logger.error("❌ BOT_TOKEN не найден!")
        return
    
    try:
        # Используем use_context=False для совместимости
        updater = Updater(token, use_context=False)
        dp = updater.dispatcher
        
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(MessageHandler(Filters.text, handle_message))
        
        updater.start_polling()
        logger.info("✅ Бот запущен успешно!")
        
        # Бесконечный цикл
        updater.idle()
        
    except Exception as e:
        logger.error(f"❌ Ошибка запуска: {e}")

if __name__ == "__main__":
    main()
