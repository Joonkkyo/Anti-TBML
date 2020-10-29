from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from .models import User

def home(request):
    if 'emp_no' in request.session.keys():
        return render(request, 'templates/home.html')

def logout(request):
    if request.session.get('user'):
        del(request.session['user'])

    return redirect('/')

def login(request):
    if request.method == "GET":
        return render(request, 'user/login.html')
    elif request.method == "POST":
        emp_no = request.POST.get('emp_no', None)
        password = request.POST.get('password', None)

        response_data = {}
        if not (emp_no and password):
            response_data['error'] = '모든 값을 입력해야합니다.'
        #등록된 유저정보에서 비밀번호 확인하여 비교하는 로직
        else:
            user = User.objects.get(emp_no=emp_no)
            if check_password(password, user.password):
                #비밀번호가 일치, 로그인 처리됨!
                return redirect('/')
            else:
                response_data['error'] = '비밀번호가 틀렸습니다.'

    return render(request, 'user/login.html', response_data)

def register(request):
    if request.method == "GET":
        return render(request, 'user/register.html')
    elif request.method == "GET":
        emp_no = request.POST['emp_no']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        re_password = request.POST['re_password']

        response_data = {}

        if not {emp_no and username and email and password and re_password}:
            response_data['error'] = '모든 값을 입력해야 합니다.'
        elif password != re_password:
            response_data['error'] = '비밀번호가 다릅니다.'
        else:
            user = User(
                emp_no=emp_no,
                username=username,
                email=email,
                password=make_password(password)
            )
            user.save()

        return render(request, 'user/register.html', response_data)
