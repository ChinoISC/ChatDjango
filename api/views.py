
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import sync_and_async_middleware
from .telegram_bot import process_update

@csrf_exempt
@sync_and_async_middleware
async def telegram_webhook(request):
    # Utilizar 'await' para manejar la coroutine de 'process_update'
    response_data = await process_update(request)
    return JsonResponse(response_data)