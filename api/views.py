import logging
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import sync_and_async_middleware
from .telegram_bot import process_update

# Configurar logger para las vistas
logger = logging.getLogger(__name__)

@csrf_exempt
@sync_and_async_middleware
async def telegram_webhook(request):
    if request.method != "POST":
        logger.warning("Recibida solicitud no POST al webhook")
        return HttpResponseNotAllowed(['POST'])

    try:
        response_data = await process_update(request)
        return JsonResponse(response_data)
    except ValueError as e:
        logger.error(f"Error al procesar la actualización: {e}")
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON received'}, status=400)