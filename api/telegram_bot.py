# telegram_bot.py
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from django.conf import settings
import json  # 

# Habilitar los registros de logging para Telegram
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Definir el comando de inicio
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('¡Hola! Soy tu bot en Django.')

def process_update(request):
    from django.http import JsonResponse
    from telegram import Update
    from telegram.ext import Application

    try:
        # Asegúrate de decodificar correctamente el cuerpo del request
        json_str = request.body.decode('UTF-8')  # Convertir de bytes a string
        update = Update.de_json(json.loads(json_str))  # Convertir string a objeto JSON

        # Crea la aplicación en vez de 'Updater'
        application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()

        # Procesar la actualización
        application.update_queue.put(update)
        print(json_str)
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        logger.error(f"Error al procesar la actualización: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)})