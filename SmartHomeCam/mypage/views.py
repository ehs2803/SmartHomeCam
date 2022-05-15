from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here
from account.models import AuthUser
from homecam.models import CapturePicture, RecordingVideo
import homecam.views
from homecam.socket import VideoCamera
from mypage.models import Family

def landing(request):
    CAMERA = homecam.views.CAMERA
    connectNum = None
    idList = ''
    user = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        if CAMERA.threads.get(user.username):
            connectNum = CAMERA.threads.get(user.username).cnt
            for key in CAMERA.threads[user.username].connections:
                idList+=key
                idList+=' '
        else:
            connectNum = 0
    idList.rstrip()
    idList='temp1 temp2 '
    context = {
        'user': user,
        'cnt': connectNum,
        'idList': idList,
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

def update_family(request, id):
    global errorMsg  # 에러메시지
    user = None
    family_member = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        family_member = Family.objects.get(uid=user.id, fid=id)

    context = {
        'user': user,
        'family_member': family_member
    }
    # POST 요청 시 입력된 데이터(사용자 정보) 저장
    if request.method == 'POST':
        update_fields=['name']
        name = request.POST['name']
        email = request.POST['email']
        tel = request.POST['tel']
        try:
            image1 = request.FILES['image1']
        except:
            pass
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
            updatefamily = Family.objects.get(uid=user.id, fid=id)
            print(1)
            updatefamily.name = name
            print(1)
            try:
                updatefamily.email = email
                update_fields.append('email')
            except:
                pass
            try:
                updatefamily.tel = tel
                update_fields.append('tel')
            except:
                pass
            try:
                updatefamily.image1 = image1
                update_fields.append('image1')
            except :
                pass
            try:
                updatefamily.image2 = image2
                update_fields.append('image2')
            except:
                pass
            try:
                updatefamily.image3 = image3
                update_fields.append('image3')
            except:
                pass
            updatefamily.save()
            return redirect('/mypage/familyInfo')  # 회원가입 성공했다는 메시지 출력 후 로그인 페이지로 이동(예정)
        except:
            errorMsg = '빈칸이 존재합니다!'
        return render(request, "mypage/family_update.html",{'error': errorMsg})
    # GET
    return render(request, "mypage/family_update.html", context=context)

def delete_family(request, id):
    family_member = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        family_member = Family.objects.get(uid=user.id, fid=id)
    family_member.delete()
    return redirect('/mypage/familyInfo')

def user_capture_pictures(request):
    user=None
    capture_pictures = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        capture_pictures = CapturePicture.objects.filter(uid=user.id)

    context = {
        'user': user,
        'capture_pictures': capture_pictures,
    }
    return render(request, "mypage/capture_picture.html", context=context)


def delete_capture(request, id):
    capture_picture = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        capture_picture = CapturePicture.objects.get(cpid=id)
    capture_picture.delete()
    return redirect('/mypage/capturePictures')

def user_recording_videos(request):
    user = None
    recording_videos = None
    media = '/media/'
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        recording_videos = RecordingVideo.objects.filter(uid=user.id)

    context = {
        'user': user,
        'recording_videos':recording_videos,
        'mediaa' : media,
    }
    return render(request, "mypage/recording_video.html", context=context)

def delete_video(request, id):
    video = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        video = RecordingVideo.objects.get(rvid=id)
    video.delete()
    return redirect('/mypage/recordingVideos')

def config_mode(request, id):
    user = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))

    context = {
        'user': user
    }
    return render(request, "mypage/config.html", context=context)

def chart(request):
    user = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))

    context = {
        'user': user
    }
    return render(request, "mypage/chart.html", context=context)