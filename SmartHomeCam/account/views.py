from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from django.utils import timezone

# 회원 가입
def signup(request):
    global errorMsg     # 에러메시지
    # POST 요청 시 입력된 데이터(사용자 정보) 저장
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm']

        # 회원가입
        try:
            # 회원가입 실패 시
            if not (username and password and confirm and  email):
                errorMsg = '빈칸이 존재합니다!'
            elif password != confirm:
                errorMsg = '비밀번호가 일치하지 않습니다!'
            # 회원가입 성공 시 회원정보 저장
            else:
                User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    date_joined=timezone.now()
                ).save()
                return redirect('')         # 회원가입 성공했다는 메시지 출력 후 로그인 페이지로 이동(예정)
        except:
            errorMsg = '빈칸이 존재합니다!'
        return render(request, 'account/register.html', {'error': errorMsg})
    # 회원가입 성공 후 이동
    return render(request, 'account/register.html')

# 로그인
def login(request):
    global errorMsg         # 에러메시지
    # POST 요청시 입력된 데이터 저장
    if request.method == 'POST':                                        # 로그인 버튼 클릭
        username = request.POST['username']
        password = request.POST['password']
        try:
            if not (username and password):                             # 아이디/비밀번호 중 빈칸이 존재할 때
                errorMsg = '아이디/비밀번호를 입력하세요.'
            else:                                                       # 아이디/비밀번호 모두 입력됐을 때
                user = User.objects.get(username=username)                  # 등록된 아이디의 정보 가져오기
                if check_password(password, user.password):                 # 등록된 아이디의 비밀번호가 맞으면
                    request.session['id'] = user.id                         # 세션에 번호 추가
                    request.session['username'] = user.username             # 세션에 아이디 추가
                    request.session['email'] = user.email                   # 세션에 이메일 추가
                    return redirect('/')
                else:                                                   # 등록된 아이디의 비밀번호가 틀리면
                    errorMsg = '비밀번호가 틀렸습니다.'
        except:                                                         # 등록된 아이디의 정보가 없을 때
            errorMsg = '가입하지 않은 아이디 입니다.'

        return render(request, 'account/login.html', {'error': errorMsg})   # 에러 메세지와 로그인 페이지(login.html) 리턴
    # GET 요청시
    return render(request, 'account/login.html')                            # 로그인 페이지(login.html) 리턴

# face login
def FaceLogin(request):
    global errorMsg  # 에러메시지
    # POST 요청시 입력된 데이터 저장
    if request.method == 'POST':  # 로그인 버튼 클릭
        username = request.POST['username']
        try:
            if not (username):  # 아이디/비밀번호 중 빈칸이 존재할 때
                errorMsg = '아이디를 입력하세요.'
            else:  # 아이디/비밀번호 모두 입력됐을 때
                user = User.objects.get(username=username)  # 등록된 아이디의 정보 가져오기
                if check_password(password, user.password):  # 등록된 아이디의 비밀번호가 맞으면
                    request.session['id'] = user.id  # 세션에 번호 추가
                    request.session['username'] = user.username  # 세션에 아이디 추가
                    request.session['email'] = user.email  # 세션에 이메일 추가
                    return redirect('/')
                else:  # 등록된 아이디의 비밀번호가 틀리면
                    errorMsg = '비밀번호가 틀렸습니다.'
        except:  # 등록된 아이디의 정보가 없을 때
            errorMsg = '가입하지 않은 아이디 입니다.'

        return render(request, 'account/facelogin.html', {'error': errorMsg})  # 에러 메세지와 로그인 페이지(login.html) 리턴
    # GET 요청시
    return render(request, 'account/facelogin.html')  # 로그인 페이지(login.html) 리턴

# 로그아웃
def logout(request):
    # 사용자 정보 로드
    if request.session.get('id', None):
        del(request.session['id'])          # 사용자 번호 제거
        del(request.session['username'])    # 사용자 아이디 제거
    return redirect('/')            # 메인 페이지(functionselect.html) 리턴