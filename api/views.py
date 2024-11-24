# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .telegram_bot import process_update

@csrf_exempt  # Excluir CSRF para que Telegram pueda hacer la solicitud
def telegram_webhook(request):
    # Procesar la actualización recibida desde Telegram
    return process_update(request)
