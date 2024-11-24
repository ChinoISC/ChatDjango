import logging
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from django.conf import settings

# Configurar logger para el módulo de Telegram bot
logger = logging.getLogger(__name__)

async def start(update: Update, context):
    await update.message.reply_text('¡Hola! Soy tu bot en Django.')

async def echo(update: Update, context):
    await update.message.reply_text(update.message.text)

async def error(update, context):
    logger.error(f"Update {update} caused error {context.error}")

async def process_update(request):
    try:
        json_str = request.body.decode('UTF-8')
        update = Update.de_json(json.loads(json_str))

        # Construir Application directamente con token
        application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()

        # Añadir manejadores a la aplicación
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

        # Registrar el manejador de errores
        application.add_error_handler(error)

        # Inicializar y configurar la aplicación
        await application.initialize()
        await application.start()
        
        # Procesar el update después de que la aplicación ha sido inicializada
        await application.process_update(update)

        # Detener la aplicación después de procesar (si es que la app se usa para un solo request, en vez de estar siempre en ejecución)
        await application.stop()

        return {'status': 'ok'}
    except Exception as e:
        logger.error(f"Error al procesar la actualización: {e}")
        return {'status': 'error', 'message': str(e)}