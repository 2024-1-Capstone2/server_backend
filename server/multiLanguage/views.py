from django.shortcuts import render
from django.utils import translation
from django.utils.translation import gettext as _
from rest_framework.decorators import api_view
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import GlobalLanguage

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

    async_to_sync(async_group_send)()

    return Response(status=200)

def choice_language(request):
    return render(request, 'choice_language.html')