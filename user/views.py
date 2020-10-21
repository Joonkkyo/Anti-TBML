from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from .models import User

# Create your views here.
def register(request):                          #회원가입 페이지를 보여주기 위한
    res_data = {}

    if request.method == "GET":
        return render(request, 'user/register.html')

    elif request.method == "POST":
        emp_no = request.POST.get['emp_no', None]           #딕셔너리형태
        username = request.POST.get['username', None]
        password = request.POST.get['password', None]
        re_password = request.POST.get['re_password', None]
        if not (emp_no and password and re_password) :
            res_data['error'] = "모든 값을 입력해야 합니다."
        if password != re_password :
            res_data['error'] = "비밀번호가 다릅니다."
        else:
            user = User(emp_no=emp_no, password=make_password(password))
            user.save()
        return render(request, 'user/register.html', res_data)       #register를 요청받으면 register.html로 응답.


def login(request):
    response_data = {}

    if request.method == "GET":
        return render(request, 'user/login.html')

    elif request.method == "POST":
        login_emp_no = request.POST.get('emp_no', None)
        login_password = request.POST.get('password', None)

        if not (login_emp_no and login_password):
            response_data['error'] = "아이디와 비밀번호를 모두 입력해주세요."
        else:
            user = User.objects.get(login_emp_no==login_emp_no)

            if check_password(login_password, user.password):
                request.session['user'] = user.id
                return redirect('/')
            else:
                response_data['error'] = "비밀번호가 틀렸습니다."
        return render(request, 'user/login.html', response_data)


def home(request):
    user_id = request.session.get('user')
    if user_id:
        user_info = User.objects.get(pk=user_id)  # pk : primary key
        return HttpResponse(user_info.username)  # 로그인을 했다면, username 출력

    return HttpResponse('로그인을 해주세요.')  # session에 user가 없다면, (로그인을 안했다면)


def logout(request):
    request.session.pop('user')
    return redirect('/')