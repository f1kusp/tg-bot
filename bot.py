import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# === НАСТРОЙКИ === ЗАМЕНИТЕ НА СВОИ! ===
BOT_TOKEN = "1234567890:ABCDEFGhijklmnopQRSTUVWXYZabcd"  # Токен из шага 1.3
ADMIN_CHAT_ID = "123456789"  # Ваш Chat ID из шага 2.1
# === КОНЕЦ НАСТРОЕК ===

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    welcome_text = """
🤖 Добро пожаловать в бот для предложений!

💡 Просто отправьте ваше предложение, вопрос или отзыв, и я сразу перешлю его администратору.

📝 Вы можете отправлять:
• Текстовые сообщения
• Фотографии с подписями
• Документы

⚡ Администратор получит ваше сообщение мгновенно!
    """
    await update.message.reply_text(welcome_text)

async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Пересылает сообщение администратору"""
    try:
        user = update.message.from_user
        # Формируем информацию о пользователе
        user_info = f"👤 Новое сообщение от: {user.first_name}"
        if user.last_name:
            user_info += f" {user.last_name}"
        if user.username:
            user_info += f" (@{user.username})"
        user_info += f"\n🆔 ID: {user.id}"
        
        # Обрабатываем текстовые сообщения
        if update.message.text:
            message_text = f"{user_info}\n\n💬 Сообщение:\n{update.message.text}"
            await context.bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=message_text
            )
            await update.message.reply_text("✅ Ваше сообщение отправлено администратору!")
        
        # Обрабатываем фото
        elif update.message.photo:
            caption = update.message.caption or "📷 Фото без подписи"
            message_text = f"{user_info}\n\n📸 Фото с подписью:\n{caption}"
            await context.bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=message_text
            )
            # Пересылаем само фото
            await context.bot.send_photo(
                chat_id=ADMIN_CHAT_ID,
                photo=update.message.photo[-1].file_id,
                caption=f"Фото от {user.first_name}"
            )
            await update.message.reply_text("✅ Ваше фото отправлено администратору!")
        
        # Обрабатываем документы
        elif update.message.document:
            caption = update.message.caption or "📎 Документ без описания"
            message_text = f"{user_info}\n\n📄 Документ:\n{caption}"
            await context.bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=message_text
            )
            await context.bot.send_document(
                chat_id=ADMIN_CHAT_ID,
                document=update.message.document.file_id,
                caption=f"Документ от {user.first_name}"
            )
            await update.message.reply_text("✅ Ваш документ отправлен администратору!")
            
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await update.message.reply_text("❌ Произошла ошибка при отправке сообщения")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок"""
    logger.error(f"Ошибка: {context.error}")

def main():
    """Основная функция"""
    print("🚀 Запуск бота...")
    
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики
    application.add_handler(MessageHandler(filters.COMMAND, start_command))
    application.add_handler(MessageHandler(filters.ALL, forward_to_admin))
    
    # Обработчик ошибок
    application.add_error_handler(error_handler)
    
    # Запускаем бота
    print("✅ Бот запущен! Для остановки нажмите Ctrl+C")
    application.run_polling()

if __name__ == "__main__":
    main()
