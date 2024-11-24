
import logging
import json
from django.http import JsonResponse
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from django.conf import settings

# Habilitar los registros de logging para Telegram
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context):
    await update.message.reply_text('¡Hola! Soy tu bot en Django.')

async def echo(update: Update, context):
    # Repetir el mensaje de vuelta al usuario
    await update.message.reply_text(update.message.text)

def process_update(request):
    try:
        # Decodificar correctamente el cuerpo del request
        json_str = request.body.decode('UTF-8')  # Convertir de bytes a string
        update = Update.de_json(json.loads(json_str))  # Convertir string a objeto JSON

        # Crear la aplicación en vez de ‘Updater’ y configurar handlers
        application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()

        # Añadir manejadores
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

        # Procesar la actualización
        application.update_queue.put(update)

        # Esto es importante para correr el polling/asynchronous processing.
        application.initialize()
        application.start()
        application.stop()

        print(json_str)
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        logger.error(f"Error al procesar la actualización: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)})