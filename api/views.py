from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = '7726637693:AAFGRFI1fhRqmBucmztsVvaidi1IYp1gSRs'
bot = Bot(token=TOKEN)

# Handlers para comandos y mensajes
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Soy tu bot de Telegram.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.reply_text(f"Recibí tu mensaje: {user_message}")

# Define la vista para manejar actualizaciones
@csrf_exempt
def webhook(request):
    if request.method == "POST":
        update = Update.de_json(request.body.decode('utf-8'), bot)
        application = Application.builder().token(TOKEN).build()

        # Registra los handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

        # Procesa el update
        application.process_update(update)
        return JsonResponse({"status": "ok"})
    return JsonResponse({"error": "Método no permitido"}, status=405)
