import logging
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from django.conf import settings

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context):
    # Responder al comando /start
    await update.message.reply_text('¡Hola! Soy tu bot en Django.')

async def echo(update: Update, context):
    # Repetir cualquier mensaje enviado por el usuario
    await update.message.reply_text(update.message.text)

async def process_update(request):
    # Procesar una actualización recibida del webhook de Telegram
    try:
        # Decodificar el cuerpo de la solicitud HTTP
        json_str = request.body.decode('UTF-8')
        update = Update.de_json(json.loads(json_str))

        # Crear la aplicación de Telegram
        application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()

        # Añadir handlers para comandos y mensajes
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

        # Procesar la actualización de forma asincrónica
        await application.update_queue.put(update)

        # Iniciar y detener la aplicación para procesar la actualización
        await application.initialize()
        await application.start()
        await application.stop()

        # Responder con éxito
        return {'status': 'ok'}
    except Exception as e:
        logger.error(f"Error al procesar la actualización: {e}")
        return {'status': 'error', 'message': str(e)}