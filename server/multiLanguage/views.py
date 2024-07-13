from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.conf import settings

@api_view(['GET'])
def request_choice_language(request):
    channel_layer = get_channel_layer()

    async def async_group_send():
        await channel_layer.group_send(
            'javaScript_group',
            {
                'type': 'javaScript_message',
                'message_type': 'url_move',
                'message': str('multiLanguage/choiceLanguage')
            }
    )

    bus_info = {
        'id': settings.LANGUAGE_CODE,
    }
    async_to_sync(async_group_send)()
    return Response(bus_info, status=200)

def choice_language(request):
    return render(request, 'choice_language.html')