import logging
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from django.conf import settings
import asyncio
# Configurar logger para el módulo de Telegram bot
logger = logging.getLogger(__name__)

async def start(update: Update, context):
    await update.message.reply_text('¡Hola! Soy tu bot en Django.')

async def echo(update: Update, context):
    await update.message.reply_text(update.message.text)

async def process_update(request):
    try:
        json_str = request.body.decode('UTF-8')
        update = Update.de_json(json.loads(json_str))
        
        # Usa la aplicación ya construida e inicializada
        application = get_app()        
        await application.process_update(update)

        return {'status': 'ok'}
    except Exception as e:
        logger.error(f"Error al procesar la actualización: {e}")
        return {'status': 'error', 'message': str(e)}

# Función para inicializar la aplicación una vez
async def setup_application():
    application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    await application.initialize()
    await application.start()
    return application

# Mantener una referencia global de la aplicación
application_ref = None

# Obtener la app o inicializarla
def get_app():
    global application_ref
    if application_ref is None:
        application_ref = asyncio.run(setup_application())
    return application_ref