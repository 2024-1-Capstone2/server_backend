from django.shortcuts import render


# web socket으로 안내원으로 부터 받은 단계가 표 요청일 때 표 요청하는 화면.
def request_ticket(request):
    return render(request, 'request_ticket.html')

def index(request):
    return render(request, 'refund_index.html')