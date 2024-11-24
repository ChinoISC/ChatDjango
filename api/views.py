from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder
import json

TOKEN = '7726637693:AAFGRFI1fhRqmBucmztsVvaidi1IYp1gSRs'

# Responder a los mensajes recibidos
async def process_update(update: Update, bot: Bot):
    if update.message:
        text = update.message.text
        await update.message.reply_text(f"Recibí tu mensaje: {text}")

# Vista que manejará el webhook
@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        update_data = json.loads(request.body.decode('utf-8'))
        bot = Bot(TOKEN)
        update = Update.de_json(update_data, bot)

        # Procesar el mensaje recibido y enviar una respuesta
        application = ApplicationBuilder().token(TOKEN).build()
        application.dispatcher.process_update(update)

        return HttpResponse(status=200)

    return JsonResponse({'error': 'Invalid request'}, status=400)
