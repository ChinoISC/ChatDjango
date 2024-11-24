# telegram_bot.py
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from django.conf import settings

# Habilitar los registros de logging para Telegram
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Definir el comando de inicio
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('¡Hola! Soy tu bot en Django.')

# Función principal para conectar con Telegram usando webhook
def set_webhook():
    # Configuración del token y el webhook
    webhook_url = settings.TELEGRAM_WEBHOOK_URL  # Este debe ser un URL accesible públicamente
    token = settings.TELEGRAM_BOT_TOKEN
    
    updater = Updater(token)

    # Set webhook en Telegram
    updater.bot.setWebhook(webhook_url)
    logger.info(f"Webhook configurado en {webhook_url}")

# Función para procesar las actualizaciones desde el webhook
def process_update(request):
    from django.http import JsonResponse

    # Aquí recibirás las actualizaciones de Telegram
    update = Update.de_json(request.body.decode('UTF-8'))
    dispatcher = Updater(token=settings.TELEGRAM_BOT_TOKEN).dispatcher
    dispatcher.process_update(update)
    return JsonResponse({'status': 'ok'})
