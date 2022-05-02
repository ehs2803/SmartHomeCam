from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here
from account.models import AuthUser
from mypage.models import Family


def landing(request):
    user = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))

    context = {
        'user': user
    }
    return render(request, "mypage/mypage.html", context=context)

def family(request):
    user = None
    family_members = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        family_members = Family.objects.filter(uid=user.id)

    context = {
        'user': user,
        'family_members' : family_members,
    }
    return render(request, "mypage/familyInfo.html", context=context)

def family_detail(request, id):
    user = None
    family_members = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        family_member = Family.objects.get(uid=user.id, fid=id)

    context = {
        'user': user,
        'family_member' : family_member,
    }
    return render(request, "mypage/family_detail.html", context=context)

def register_family(request):
    global errorMsg  # 에러메시지
    user = None
    if request.session.get('id'):                                     # 로그인 중이면
        user = AuthUser.objects.get(pk=request.session.get('id'))       # 사용자 정보 저장
    context = {
        'user': user
    }
    # POST 요청 시 입력된 데이터(사용자 정보) 저장
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        tel = request.POST['tel']
        image1 = request.FILES['image1']
        try:
            image2 = request.FILES['image2']
        except:
            pass

        try:
            image3 = request.FILES['image3']
        except:
            pass

        # 회원가입
        try:
            # 회원가입 실패 시
            if not (name and image1):
                errorMsg = '빈칸이 존재합니다!'
            # 회원가입 성공 시 회원정보 저장
            else:
                regfamily = Family()
                regfamily.uid = user
                regfamily.name = name
                regfamily.image1 = image1
                try:
                    regfamily.email=email
                except:
                    pass
                try:
                    regfamily.tel = tel
                except:
                    pass
                try:
                    regfamily.image2 = image2
                except:
                    pass
                try:
                    regfamily.image3 = image3
                except:
                    pass
                regfamily.save()
                return redirect('/mypage/familyInfo')         # 회원가입 성공했다는 메시지 출력 후 로그인 페이지로 이동(예정)
        except:
            errorMsg = '빈칸이 존재합니다!'
        return render(request, 'mypage/family_register.html', {'error': errorMsg})
    # GET
    return render(request, "mypage/family_register.html")


def chart(request):
    user = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))

    context = {
        'user': user
    }
    return render(request, "mypage/chart.html", context=context)