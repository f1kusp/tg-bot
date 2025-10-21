import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update, context):
    update.message.reply_text("👋 Привет! Напишите сообщение для администратора.")

def handle_message(update, context):
    user = update.message.from_user
    message_text = update.message.text
    
    # Формируем сообщение для администратора
    admin_message = f"📩 Новое сообщение:\n👤 {user.first_name}\n🆔 ID: {user.id}\n💬 {message_text}"
    
    # Получаем ID администратора
    admin_id = os.getenv('ADMIN_CHAT_ID')
    
    if admin_id:
        try:
            # Отправляем администратору
            context.bot.send_message(chat_id=admin_id, text=admin_message)
            update.message.reply_text("✅ Сообщение отправлено администратору!")
        except Exception as e:
            logger.error(f"Ошибка отправки: {e}")
            update.message.reply_text("❌ Ошибка при отправке")
    else:
        update.message.reply_text("❌ Администратор не настроен")

def main():
    logger.info("🔄 Запуск бота...")
    
    # Получаем токен
    token = os.getenv('BOT_TOKEN')
    if not token:
        logger.error("❌ BOT_TOKEN не найден")
        return
    
    try:
        # Создаем бота
        updater = Updater(token, use_context=True)
        dispatcher = updater.dispatcher
        
        # Добавляем обработчики
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(MessageHandler(Filters.text, handle_message))
        
        # Запускаем
        updater.start_polling()
        logger.info("✅ Бот успешно запущен!")
        
        # Бесконечный цикл
        updater.idle()
        
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()
