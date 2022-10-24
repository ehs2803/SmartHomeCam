import copy

from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here
from SmartHomeCam.storages import FileUpload, s3_client
from account.models import AuthUser
from homecam.models import CapturePicture, RecordingVideo, DetectAnimal, DetectPerson, DetectUnknown, DetectFire, \
    SafeModeNodetect, SafeModeNoaction, CamConnectHistory, Homecam, Alarm
import homecam.views
from homecam.connect.socket import VideoCamera
from mypage.models import Family

# 데시보드
def landing(request):
    fireCnt = None
    personCnt = None
    unknownCnt = None
    nopersonCnt = None
    noactionCnt = None
    alarmCnt = None
    CAMERA = homecam.views.CAMERA
    connectNum = None
    idList = ''
    cam_connect_history = None
    user = None
    homecam_list = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        fireCnt = DetectFire.objects.filter(uid=user.id).count()
        personCnt = DetectPerson.objects.filter(uid=user.id).count()
        unknownCnt = DetectUnknown.objects.filter(uid=user.id).count()
        nopersonCnt = SafeModeNodetect.objects.filter(uid=user.id).count()
        noactionCnt = SafeModeNoaction.objects.filter(uid=user.id).count()
        alarmCnt = Alarm.objects.filter(uid=user.id, confirm=0).count()
        homecam_list = Homecam.objects.filter(uid=user.id)
        if CAMERA.threads.get(user.username):
            connectNum = CAMERA.threads.get(user.username).cnt
            for key in CAMERA.threads[user.username].connections:
                idList+=key
                idList+=' '
        else:
            connectNum = 0
        cam_connect_history = CamConnectHistory.objects.filter(uid=user.id).order_by('-time')
    idList.rstrip()

    context = {
        'fireCnt' : fireCnt,
        'personCnt' : personCnt,
        'unknownCnt' : unknownCnt,
        'nopersonCnt' : nopersonCnt,
        'noactionCnt' : noactionCnt,
        'alarmCnt':alarmCnt,
        'user': user,
        'cnt': connectNum,
        'idList': idList,
        'cam_connect_history':cam_connect_history,
        'homecam_list' : homecam_list,
    }
    return render(request, "mypage/mypage.html", context=context)

# 가족 정보 페이지
def family(request):
    user = None
    alarmCnt=None
    family_members = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        alarmCnt = Alarm.objects.filter(uid=user.id, confirm=0).count()
        family_members = Family.objects.filter(uid=user.id)

    context = {
        'alarmCnt':alarmCnt,
        'user': user,
        'family_members' : family_members,
    }
    return render(request, "mypage/familyInfo.html", context=context)

# 가족 정보 삭제
def family_detail(request, id):
    user = None
    alarmCnt = None
    family_members = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        alarmCnt = Alarm.objects.filter(uid=user.id, confirm=0).count()
        family_member = Family.objects.get(uid=user.id, fid=id)

    context = {
        'alarmCnt':alarmCnt,
        'user': user,
        'family_member' : family_member,
    }
    return render(request, "mypage/family_detail.html", context=context)

# 가족 정보 등록
def register_family(request):
    global errorMsg  # 에러메시지
    alarmCnt = None
    user = None
    if request.session.get('id'):                                     # 로그인 중이면
        user = AuthUser.objects.get(pk=request.session.get('id'))       # 사용자 정보 저장
        alarmCnt = Alarm.objects.filter(uid=user.id, confirm=0).count()
    context = {
        'alarmCnt':alarmCnt,
        'user': user
    }
    # POST 요청 시 입력된 데이터(사용자 정보) 저장
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        tel = request.POST['tel']
        image1 = request.FILES['image1']
        image1_s3 = copy.deepcopy(image1)
        image1_url = FileUpload(s3_client).upload(image1_s3, 'family/')
        try:
            image2 = request.FILES['image2']
            image2_s3 = copy.deepcopy(image2)
            image2_url = FileUpload(s3_client).upload(image2_s3 ,'family/')
        except:
            pass

        try:
            image3 = request.FILES['image3']
            image3_s3 = copy.deepcopy(image3)
            image3_url = FileUpload(s3_client).upload(image3_s3, 'family/')
        except:
            pass

        try:
            if not (name and image1):
                errorMsg = '빈칸이 존재합니다!'
            else:
                regfamily = Family()
                regfamily.uid = user
                regfamily.name = name
                regfamily.image1 = image1
                regfamily.image1_s3 = image1_url

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
                    regfamily.image2_s3 = image2_url
                except:
                    pass
                try:
                    regfamily.image3 = image3
                    regfamily.image3_s3 = image3_url
                except:
                    pass
                try:
                    regfamily.save()
                except Exception as e:
                    print(e)
                return redirect('/mypage/familyInfo')
        except:
            errorMsg = '빈칸이 존재합니다!'
        return render(request, 'mypage/family_register.html', {'error': errorMsg})
    # GET
    return render(request, "mypage/family_register.html", context=context)

# 가족 정보 업데이트
def update_family(request, id):
    global errorMsg  # 에러메시지
    user = None
    alarmCnt=None
    family_member = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        alarmCnt = Alarm.objects.filter(uid=user.id, confirm=0).count()
        family_member = Family.objects.get(uid=user.id, fid=id)

    context = {
        'alarmCnt':alarmCnt,
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
            updatefamily.name = name
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

# 가족 정보 삭제
def delete_family(request, id):
    family_member = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        family_member = Family.objects.get(uid=user.id, fid=id)
    family_member.delete()
    return redirect('/mypage/familyInfo')

# 사용자 캡처 이미지 목록
def user_capture_pictures(request):
    user=None
    alarmCnt=None
    capture_pictures = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        alarmCnt = Alarm.objects.filter(uid=user.id, confirm=0).count()
        capture_pictures = CapturePicture.objects.filter(uid=user.id).order_by('-time')

    context = {
        'alarmCnt':alarmCnt,
        'user': user,
        'capture_pictures': capture_pictures,
    }
    return render(request, "mypage/user/media/capture_picture.html", context=context)

# 사용자 캡처 이미지 상세 페이지
def user_capture_picture_detail(request, id):
    user=None
    alarmCnt=None
    capture_picture = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        alarmCnt = Alarm.objects.filter(uid=user.id, confirm=0).count()
        capture_picture = CapturePicture.objects.get(cpid=id)

    context = {
        'alarmCnt':alarmCnt,
        'user': user,
        'capture_picture': capture_picture,
    }
    return render(request, "mypage/user/media/capture_picture_detail.html", context=context)

# 사용자 캡처 이미지 삭제
def delete_capture(request, id):
    capture_picture = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        capture_picture = CapturePicture.objects.get(cpid=id)
    capture_picture.delete()
    return redirect('/mypage/capturePictures')

# 사용자 녹화 동영상 목록
def user_recording_videos(request):
    user = None
    alarmCnt = None
    recording_videos = None
    media = '/media/'
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        alarmCnt = Alarm.objects.filter(uid=user.id, confirm=0).count()
        recording_videos = RecordingVideo.objects.filter(uid=user.id).order_by('-time')

    context = {
        'alarmCnt': alarmCnt,
        'user': user,
        'recording_videos':recording_videos,
        'mediaa' : media,
    }
    return render(request, "mypage/user/media/recording_video.html", context=context)

# 사용자 녹화 동영상 상세 페이지
def user_recording_video_detail(request, id):
    user = None
    alarmCnt = None
    recording_video = None
    media = '/media/'
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        alarmCnt = Alarm.objects.filter(uid=user.id, confirm=0).count()
        recording_video = RecordingVideo.objects.get(rvid=id)

    context = {
        'alarmCnt': alarmCnt,
        'user': user,
        'recording_video':recording_video,
        'mediaa' : media,
    }
    return render(request, "mypage/user/media/recording_video_detail.html", context=context)

# 사용자 녹화 동영상 삭제
def delete_video(request, id):
    video = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        video = RecordingVideo.objects.get(rvid=id)
    video.delete()
    return redirect('/mypage/recordingVideos')

# 사람 탐지 목록
def record_detect_person(request):
    user = None
    alarmCnt = None
    records_detect_person = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        alarmCnt = Alarm.objects.filter(uid=user.id, confirm=0).count()
        records_detect_person = DetectPerson.objects.filter(uid=user.id).order_by('-time')

    context = {
        'alarmCnt': alarmCnt,
        'user': user,
        'records_detect_person': records_detect_person,
    }
    return render(request, "mypage/detect_person_record.html", context=context)

# 사람 탐지 상세
def record_detect_person_detail(request, id):
    user = None
    alarmCnt = None
    record_detect_person = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        alarmCnt = Alarm.objects.filter(uid=user.id, confirm=0).count()
        record_detect_person = DetectPerson.objects.get(id=id)
        try:
            alarm = Alarm.objects.get(uid=user.id, did=id, type='PERSON')
            alarm.confirm=1
            alarm.save()
        except:
            print('해당 alarm 존재하지 않음')

    context = {
        'alarmCnt': alarmCnt,
        'user': user,
        'record_detect_person': record_detect_person,
    }
    return render(request, "mypage/detect/detect_person_record_detail.html", context=context)

# 사람 탐지 기록 삭제
def delete_record_detect_person(request, id):
    record = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        record = DetectPerson.objects.get(id=id)
    record.delete()
    return redirect('/mypage/records/detectPerson')

# 외부인 탐지 목록
def record_detect_unknown(request):
    user = None
    alarmCnt = None
    records_detect_unknown = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        alarmCnt = Alarm.objects.filter(uid=user.id, confirm=0).count()
        records_detect_unknown = DetectUnknown.objects.filter(uid=user.id).order_by('-time')

    context = {
        'alarmCnt': alarmCnt,
        'user': user,
        'records_detect_unknown': records_detect_unknown,
    }
    return render(request, "mypage/detect_unknown_record.html", context=context)

# 외부인 탐지 상세
def record_detect_unknown_detail(request, id):
    user = None
    alarmCnt = None
    record_detect_unknown = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        alarmCnt = Alarm.objects.filter(uid=user.id, confirm=0).count()
        record_detect_unknown = DetectUnknown.objects.get(id=id)
        try:
            alarm = Alarm.objects.get(uid=user.id, did=id, type='UNKNOWN')
            alarm.confirm=1
            alarm.save()
        except:
            print('해당 alarm 존재하지 않음')

    context = {
        'alarmCnt': alarmCnt,
        'user': user,
        'record_detect_unknown': record_detect_unknown,
    }
    return render(request, "mypage/detect/detect_unknown_record_detail.html", context=context)

# 외부인 탐지 기록 삭제
def delete_record_detect_unknown(request, id):
    record = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        record = DetectUnknown.objects.get(id=id)
    record.delete()
    return redirect('/mypage/records/unknownDetect')

# 화재탐지 목록
def record_detect_fire(request):
    user = None
    alarmCnt = None
    records_detect_fire = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        alarmCnt = Alarm.objects.filter(uid=user.id, confirm=0).count()
        records_detect_fire = DetectFire.objects.filter(uid=user.id).order_by('-time')

    context = {
        'alarmCnt': alarmCnt,
        'user': user,
        'records_detect_fire': records_detect_fire,
    }
    return render(request, "mypage/detect_fire_record.html", context=context)

# 화재 탐지 상세
def record_detect_fire_detail(request, id):
    user = None
    alarmCnt = None
    record_detect_fire = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        alarmCnt = Alarm.objects.filter(uid=user.id, confirm=0).count()
        record_detect_fire = DetectFire.objects.get(id=id)
        try:
            alarm = Alarm.objects.get(uid=user.id, did=id, type='FIRE')
            alarm.confirm=1
            alarm.save()
        except:
            print('해당 alarm 존재하지 않음')

    context = {
        'alarmCnt': alarmCnt,
        'user': user,
        'record_detect_fire': record_detect_fire,
    }
    return render(request, "mypage/detect/detect_fire_record_detail.html", context=context)

# 화재 탐지 기록 삭제
def delete_record_detect_fire(request, id):
    record = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        record = DetectFire.objects.get(id=id)
    record.delete()
    return redirect('/mypage/records/detectFire')

# 반려동물 활동성 통계 그래프
def record_detect_animal(request):
    user = None
    alarmCnt = None
    records_detect_aniaml = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        alarmCnt = Alarm.objects.filter(uid=user.id, confirm=0).count()
        records_detect_aniaml = DetectAnimal.objects.filter(uid=user.id).order_by('-time')

    context = {
        'alarmCnt': alarmCnt,
        'user': user,
        'records_detect_animal': records_detect_aniaml,
    }
    return render(request, "mypage/detect_animal.html", context=context)

# 사람 미감지 탐지 목록
def record_safemode_noPerson(request):
    user = None
    alarmCnt = None
    records_detect_noPerson = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        alarmCnt = Alarm.objects.filter(uid=user.id, confirm=0).count()
        records_detect_noPerson = SafeModeNodetect.objects.filter(uid=user.id).order_by('-time')
        alarm_list = Alarm.objects.filter(uid=user.id, type='NOPERSON', confirm=0)
        for alarm in alarm_list:
            alarm.confirm=1
            alarm.save()

    context = {
        'alarmCnt': alarmCnt,
        'user': user,
        'records_detect_noPerson': records_detect_noPerson,
    }
    return render(request, "mypage/safemode_detect_noperson.html", context=context)

# 사람 행동 미감지 목록
def record_safemode_noAction(request):
    user = None
    alarmCnt = None
    records_detect_noAction = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        alarmCnt = Alarm.objects.filter(uid=user.id, confirm=0).count()
        records_detect_noAction = SafeModeNoaction.objects.filter(uid=user.id).order_by('-time')

    context = {
        'alarmCnt': alarmCnt,
        'user': user,
        'records_detect_noAction': records_detect_noAction,
    }
    return render(request, "mypage/safemode_detect_noaction.html", context=context)

# 사람 행동 미감지 상세
def record_safemode_noAction_detail(request, id):
    user = None
    alarmCnt = None
    record_detect_noAction = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        alarmCnt = Alarm.objects.filter(uid=user.id, confirm=0).count()
        record_detect_noAction = SafeModeNoaction.objects.get(id=id)
        try:
            alarm = Alarm.objects.get(uid=user.id, did=id, type='NOACTION')
            alarm.confirm=1
            alarm.save()
        except:
            print('해당 alarm 존재하지 않음')


    context = {
        'alarmCnt': alarmCnt,
        'user': user,
        'record_detect_noAction': record_detect_noAction,
    }
    return render(request, "mypage/detect/detect_safemode_noaction_detail.html", context=context)

# 사람 행동 미감지 기록 삭제
def record_safemode_noAction_delete(request, id):
    record = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        record = SafeModeNoaction.objects.get(id=id)
    record.delete()
    return redirect('/mypage/records/safemode/noAction')

# 홈카메라 관리 페이지
def homecam_manage_list(request):
    user=None
    alarmCnt = None
    homecam_list = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        alarmCnt = Alarm.objects.filter(uid=user.id, confirm=0).count()
        homecam_list = Homecam.objects.filter(uid=user.id)
    context = {
        'alarmCnt': alarmCnt,
        'user': user,
        'homecam_list': homecam_list,
    }
    return render(request, "mypage/homecam/homecam_list.html", context=context)

# 미확인 알림 페이지
def alarm_list(request):
    user=None
    alarmCnt = None
    alarm_list = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        alarmCnt = Alarm.objects.filter(uid=user.id, confirm=0).count()
        alarm_list = Alarm.objects.filter(uid=user.id, confirm=0)
    context = {
        'alarmCnt': alarmCnt,
        'user': user,
        'alarm_list': alarm_list,
    }
    return render(request, "mypage/alarm/alarm_all_list.html", context=context)

# 특정 홈캠 알림 페이지
def alarm_list_homecam(request, id):
    user=None
    alarmCnt = None
    alarm_confirm_list = None
    alarm_noconfirm_list=None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        alarmCnt = Alarm.objects.filter(uid=user.id, confirm=0).count()
        alarm_confirm_list = Alarm.objects.filter(uid=user.id, camid=id, confirm=1).order_by('-time')
        alarm_noconfirm_list = Alarm.objects.filter(uid=user.id, camid=id, confirm=0).order_by('-time')
    context = {
        'alarmCnt': alarmCnt,
        'user': user,
        'alarm_confirm_list': alarm_confirm_list,
        'alarm_noconfirm_list': alarm_noconfirm_list,
    }
    return render(request, "mypage/alarm/alarm_list_homecam.html", context=context)

'''
def record_safemode_falldown(request):
    user = None
    records_detect_falldown = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        records_detect_falldown = DetectFalldown.objects.filter(uid=user.id)

    context = {
        'user': user,
        'records_detect_falldown': records_detect_falldown,
    }
    return render(request, "mypage/safemode_detect_falldown.html", context=context)
'''