from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder
import json

# Token del bot de Telegram
TOKEN = '7726637693:AAFGRFI1fhRqmBucmztsVvaidi1IYp1gSRs'

# Crea la instancia de la aplicación Telegram
async def process_update(update: Update, bot: Bot):
    # Aquí puedes manejar la lógica de tu bot, como responder a mensajes
    if update.message:
        text = update.message.text
        await update.message.reply_text(f"Recibí tu mensaje: {text}")

# Vista que manejará el webhook
@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        # Los datos de la actualización de Telegram llegan en el cuerpo de la solicitud
        update_data = json.loads(request.body.decode('utf-8'))
        
        # Crear el bot de Telegram
        bot = Bot(TOKEN)

        # Crear el objeto Update a partir de los datos recibidos
        update = Update.de_json(update_data, bot)

        # Procesa el mensaje recibido
        application = ApplicationBuilder().token(TOKEN).build()
        application.dispatcher.process_update(update)

        return HttpResponse(status=200)

    return JsonResponse({'error': 'Invalid request'}, status=400)
