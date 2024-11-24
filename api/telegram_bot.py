
from django.http import JsonResponse
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from django.conf import settings
import json
import logging

logger = logging.getLogger(__name__)

async def telegram_webhook(request):
    try:
        # Decodificar adecuadamente el cuerpo del request
        json_str = request.body.decode('UTF-8')  # Convertir de bytes a string
        update = Update.de_json(json.loads(json_str))  # Convertir string a objeto JSON

        # Inicializar la aplicación
        application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()

        # Añadir los manejadores de comandos y mensajes
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

        # Procesar la actualización
        await application.update_queue.put(update)

        # Inicializar y procesar aplicaciones correctas asincrónicamente
        await application.initialize()
        await application.start()
        await application.stop()

        # Enviar una respuesta JSON
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        logger.error(f"Error al procesar la actualización: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)})

async def start(update: Update, context):
    await update.message.reply_text('¡Hola! Soy tu bot en Django.')

async def echo(update: Update, context):
    await update.message.reply_text(update.message.text)