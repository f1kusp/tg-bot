import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update, context):
    update.message.reply_text("👋 Привет! Напишите сообщение для администратора.")

def echo(update, context):
    user = update.message.from_user
    admin_msg = f"📩 От {user.first_name} (ID: {user.id}): {update.message.text}"
    
    # Отправляем администратору
    admin_id = os.getenv('ADMIN_CHAT_ID')
    if admin_id:
        context.bot.send_message(chat_id=admin_id, text=admin_msg)
    
    update.message.reply_text("✅ Отправлено!")

def main():
    token = os.getenv('BOT_TOKEN')
    if not token:
        logger.error("❌ BOT_TOKEN не найден")
        return
        
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, echo))
    
    updater.start_polling()
    logger.info("✅ Бот запущен!")
    updater.idle()

if __name__ == "__main__":
    main()
