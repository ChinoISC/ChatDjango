from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from telegram import Update, Bot
from telegram.ext import Application, MessageHandler, filters
import json
import logging

# Token del bot de Telegram
TOKEN = '7726637693:AAFGRFI1fhRqmBucmztsVvaidi1IYp1gSRs'

# Configuración del logging (para depuración)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Función que se ejecuta cuando se recibe un mensaje
async def process_message(update: Update, context):
    if update.message:
        text = update.message.text  # Obtener el texto del mensaje
        await update.message.reply_text(f"Recibí tu mensaje: {text}")  # Responder al mensaje

# Vista que manejará el webhook
@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        # Los datos de la actualización de Telegram llegan en el cuerpo de la solicitud
        update_data = json.loads(request.body.decode('utf-8'))

        # Crear el objeto Update a partir de los datos recibidos
        bot = Bot(TOKEN)  # Crear el bot
        update = Update.de_json(update_data, bot)  # Crear la actualización

        # Crear la aplicación de Telegram y agregar el handler para los mensajes de texto
        application = Application.builder().token(TOKEN).build()

        # Agregar el handler que procesará los mensajes de texto
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_message))

        # Procesar la actualización (esto hará que se ejecute el callback adecuado)
        application.update_queue.put(update)  # Agregar el update a la cola para ser procesado

        return HttpResponse(status=200)

    return JsonResponse({'error': 'Invalid request'}, status=400)
