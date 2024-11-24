import logging
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from django.conf import settings
import json

# Configurar logger para el módulo de Telegram bot
logger = logging.getLogger(__name__)

async def start(update: Update, context):
    await update.message.reply_text('¡Hola! Soy tu bot en Django.')

async def echo(update: Update, context):
    await update.message.reply_text(update.message.text)

async def error(update: Update, context):
    logger.error(f"Update {update} caused error {context.error}")

async def process_update(request):
    try:
        json_str = request.body.decode('UTF-8')
        update = Update.de_json(json.loads(json_str))
        
        # Crea la aplicación y configúrala para que use un bot
        application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()

        # Añadir manejadores
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

        # Registrar manejador de errores
        application.add_error_handler(error)

        # Asociar el objeto Bot manualmente
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        update._effective_chat = update.message.chat
        update._bot = bot  # Ahora el objeto tiene un bot asociado

        # Poner update en cola y procesar
        await application.update_queue.put(update)

        # Iniciar la aplicación (a través de sus coroutines)
        await application.initialize()
        await application.start()
        await application.stop()

        return {'status': 'ok'}
    except Exception as e:
        logger.error(f"Error al procesar la actualización: {e}")
        return {'status': 'error', 'message': str(e)}