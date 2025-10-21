import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    await update.message.reply_text(f"👋 Привет, {user.first_name}! Я бот для связи с администратором.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.message.from_user
        message_text = update.message.text
        
        # Информация о пользователе
        user_info = f"{user.first_name} {user.last_name or ''} (@{user.username or 'нет'})"
        
        # Сообщение для администратора
        admin_message = f"📩 Новое сообщение:\n👤 {user_info}\n🆔 ID: {user.id}\n💬 {message_text}"
        
        # Отправляем администратору
        admin_chat_id = os.getenv('ADMIN_CHAT_ID')
        if admin_chat_id:
            await context.bot.send_message(chat_id=admin_chat_id, text=admin_message)
        
        await update.message.reply_text("✅ Сообщение отправлено администратору!")
        
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await update.message.reply_text("❌ Ошибка при отправке сообщения")

def main():
    logger.info("🔄 Запуск бота...")
    
    # Получаем токен из переменных окружения
    token = os.getenv('BOT_TOKEN')
    if not token:
        logger.error("❌ BOT_TOKEN не найден!")
        return
    
    try:
        # Создаем и запускаем бота
        application = Application.builder().token(token).build()
        
        # Обработчики команд
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        # Запускаем бота
        application.run_polling()
        logger.info("✅ Бот запущен успешно!")
        
    except Exception as e:
        logger.error(f"❌ Ошибка запуска: {e}")

if __name__ == "__main__":
    main()
