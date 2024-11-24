from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

TOKEN = '7726637693:AAFGRFI1fhRqmBucmztsVvaidi1IYp1gSRs'

# Crear el bot
bot = Bot(token=TOKEN)

# Configurar el dispatcher y los handlers
def setup_dispatcher(dispatcher):
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

@csrf_exempt
def webhook(request):
    if request.method == "POST":
        # Recibir la actualización de Telegram
        try:
            update = Update.de_json(json.loads(request.body.decode('utf-8')), bot)
            dispatcher = Dispatcher(bot, None)
            setup_dispatcher(dispatcher)
            dispatcher.process_update(update)
            return JsonResponse({"status": "ok"})
        except Exception as e:
            print(f"Error al procesar los datos del webhook: {e}")
            return JsonResponse({"error": "Internal Server Error"}, status=500)
    return JsonResponse({"error": "Método no permitido"}, status=405)

def start(update, context):
    update.message.reply_text("¡Hola! Soy tu bot de Telegram.")

def echo(update, context):
    update.message.reply_text(f"Recibí tu mensaje: {update.message.text}")
