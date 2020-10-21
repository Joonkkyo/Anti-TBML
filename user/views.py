from django.shortcuts import render

# Create your views here.
def register(request):                          #회원가입 페이지를 보여주기 위한
    return render(request, 'register.html')     #register를 요청받으면 register.html로 응답.