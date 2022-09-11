import datetime
import time
from threading import Thread

from django.contrib.auth.models import User
from django.core import serializers
from django.http import StreamingHttpResponse, JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect

from account.models import AuthUser
from homecam.connect.socket import VideoCamera
from homecam.models import HomecamModeUseHistory, DetectAnimal, Homecam, Alarm

CAMERA  = None

def landing(request):
    global CAMERA
    user = None
    if CAMERA==None:
        CAMERA = VideoCamera()
        socket_run = Thread(target=CAMERA.run_server)
        socket_run.start()
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))

    context = {
        'user': user
    }
    return render(request, "homecam/index.html", context=context)

def basic(request):
    user = None
    connectNum = None
    idList = ''
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

    print(idList)
    context = {
        'user': user,
        'cnt' : connectNum,
        'idList' : idList,
    }
    return render(request, "homecam/basic.html", context=context)

def live_list(request):
    user = None
    alarmCnt = None
    connectNum = None
    idList = ''
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        alarmCnt = Alarm.objects.filter(uid=user.id, confirm=0).count()
        if CAMERA.threads.get(user.username):
            connectNum = CAMERA.threads.get(user.username).cnt
            for key in CAMERA.threads[user.username].connections:
                idList+=key
                idList+=' '
        else:
            connectNum = 0
    idList.rstrip()

    print(idList)
    context = {
        'alarmCnt':alarmCnt,
        'user': user,
        'cnt' : connectNum,
        'idList' : idList,
    }
    return render(request, "homecam/live_list.html", context=context)

def basic_livecam(request, username, id):
    user = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
    camid = id
    context = {
        'user': user,
        'id' : camid,
    }
    return render(request, "homecam/basic_livecam.html", context=context)

def gen_basic(camera, username, id):
    while True:
        if camera.threads.get(username):
            break
    client = camera.threads[username]
    while True:
        try:
            frame = client.connections[id].get_frame()
        except:
            pass
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def video_basic(request, username, id):
    return StreamingHttpResponse(gen_basic(CAMERA, username, id),
                    content_type='multipart/x-mixed-replace; boundary=frame')


def pet(request):
    user = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))

    context = {
        'user': user
    }
    return render(request, "homecam/pet.html", context=context)

def gen_pet(camera):
    while True:
        frame = camera.camera.get_frame()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_pet(request):
    return StreamingHttpResponse(gen_pet(VideoCamera()),
                   content_type='multipart/x-mixed-replace; boundary=frame')

def set_mode_detectPerson(request, id):
    global CAMERA
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        user = AuthUser.objects.get(username=user.username)
        homecam = Homecam.objects.get(camid=id, uid=user)

        mode_history = HomecamModeUseHistory()
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        mode_history.uid=user
        mode_history.camid=id
        mode_history.time=timestamp
        mode_history.mode='DETECT_PERSON'
        if homecam.po_person==1: mode_history.division='OFF'
        else: mode_history.division='ON'
        mode_history.save()

        homecam.po_person = 1-homecam.po_person
        homecam.save()
        if CAMERA.threads.get(user.username):
            client = CAMERA.threads[user.username]
            if client.connections[id] != None:
                client.connections[id].check_detect_person=homecam.po_person
        return redirect('/mypage/homecam/manage')

def set_mode_detectUnknown(request ,id):
    global CAMERA
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        user = AuthUser.objects.get(username=user.username)
        homecam = Homecam.objects.get(camid=id, uid=user)

        mode_history = HomecamModeUseHistory()
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        mode_history.uid=user
        mode_history.camid=id
        mode_history.time=timestamp
        mode_history.mode='DETECT_UNKNOWNFACE'
        if homecam.po_unknown==1: mode_history.division='OFF'
        else: mode_history.division='ON'
        mode_history.save()

        homecam.po_unknown = 1-homecam.po_unknown
        homecam.save()
        if CAMERA.threads.get(user.username):
            client = CAMERA.threads[user.username]
            if client.connections[id] != None:
                client.connections[id].check_recognition_face=homecam.po_unknown
        return redirect('/mypage/homecam/manage')

def set_mode_detectFire(request, id):
    global CAMERA
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        user = AuthUser.objects.get(username=user.username)
        homecam = Homecam.objects.get(camid=id, uid=user)

        mode_history = HomecamModeUseHistory()
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        mode_history.uid=user
        mode_history.camid=id
        mode_history.time=timestamp
        mode_history.mode='DETECT_FIRE'
        if homecam.po_fire==1: mode_history.division='OFF'
        else: mode_history.division='ON'
        mode_history.save()

        homecam.po_fire = 1-homecam.po_fire
        homecam.save()
        if CAMERA.threads.get(user.username):
            client = CAMERA.threads[user.username]
            if client.connections[id] != None:
                client.connections[id].check_detect_fire=homecam.po_fire
        return redirect('/mypage/homecam/manage')

def set_mode_detectAnimal(request, id):
    global CAMERA
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        user = AuthUser.objects.get(username=user.username)
        homecam = Homecam.objects.get(camid=id, uid=user)

        mode_history = HomecamModeUseHistory()
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        mode_history.uid=user
        mode_history.camid=id
        mode_history.time=timestamp
        mode_history.mode='DETECT_ANIMAL'
        if homecam.po_animal==1: mode_history.division='OFF'
        else: mode_history.division='ON'
        mode_history.save()

        homecam.po_animal = 1-homecam.po_animal
        homecam.save()
        if CAMERA.threads.get(user.username):
            client = CAMERA.threads[user.username]
            if client.connections[id] != None:
                client.connections[id].check_detect_animal=homecam.po_animal
        return redirect('/mypage/homecam/manage')

def set_mode_detectNoPerson(request ,id):
    global CAMERA
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        user = AuthUser.objects.get(username=user.username)
        homecam = Homecam.objects.get(camid=id, uid=user)

        mode_history = HomecamModeUseHistory()
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        mode_history.uid=user
        mode_history.camid=id
        mode_history.time=timestamp
        mode_history.mode='SAFEMODE_NOPERSON'
        if homecam.po_safe_noperson==1: mode_history.division='OFF'
        else: mode_history.division='ON'
        mode_history.save()

        homecam.po_safe_noperson = 1-homecam.po_safe_noperson
        homecam.save()
        if CAMERA.threads.get(user.username):
            client = CAMERA.threads[user.username]
            if client.connections[id] != None:
                client.connections[id].check_detect_animal=homecam.po_safe_noperson
        return redirect('/mypage/homecam/manage')

def set_mode_detectNoAction(request, id):
    global CAMERA
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
        user = AuthUser.objects.get(username=user.username)
        homecam = Homecam.objects.get(camid=id, uid=user)

        mode_history = HomecamModeUseHistory()
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        mode_history.uid=user
        mode_history.camid=id
        mode_history.time=timestamp
        mode_history.mode='SAFEMODE_NOACTION'
        if homecam.po_safe_noaction==1: mode_history.division='OFF'
        else: mode_history.division='ON'
        mode_history.save()

        homecam.po_safe_noaction = 1-homecam.po_safe_noaction
        homecam.save()
        if CAMERA.threads.get(user.username):
            client = CAMERA.threads[user.username]
            if client.connections[id] != None:
                client.connections[id].check_detect_animal=homecam.po_safe_noaction
        return redirect('/mypage/homecam/manage')

def set_mode_detectNoPerson_Day(request, id):
    if request.method == 'POST':
        input_time = request.POST['time']
        print(input_time)

        if request.session.get('id'):
            user = User.objects.get(id=request.session.get('id'))
            user = AuthUser.objects.get(username=user.username)
            homecam = Homecam.objects.get(camid=id, uid=user)
            homecam.po_safe_no_person_day = input_time
            homecam.save()
            if CAMERA.threads.get(user.username):
                client = CAMERA.threads[user.username]
                if client.connections[id] != None:
                    client.connections[id].check_detect_no_person_day = homecam.po_safe_no_person_day

        return redirect('/mypage/homecam/manage')

@csrf_exempt
def ajax_connect_config(request, username, id):
    sendmessage = ""
    receive_message = request.POST.get('send_data')
    if CAMERA.threads.get(username):
        if CAMERA.threads.get(username).cnt>0:
            if CAMERA.threads.get(username).connections.get(id):
                sendmessage="1"
            else:
                sendmessage="0"
        else:
            sendmessage="0"
    else:
        sendmessage="0"
    send_message = {'send_data' : sendmessage}
    return JsonResponse(send_message) # 라즈베리파이 연결 여부

@csrf_exempt
def ajax_disconnect(request, username, id):
    client = CAMERA.threads.get(username)
    #client.disconnect_socket(id)
    client.connections[id].check=True
    send_message = {'send_data' : '1'}
    return JsonResponse(send_message)

@csrf_exempt
def ajax_capture(request, username, id):
    user = AuthUser.objects.get(pk=request.session.get('id'))
    client = CAMERA.threads[username]
    check = client.connections[id].capture_picture(user)
    send_message = {'send_data': '1'}
    return JsonResponse(send_message)

@csrf_exempt
def ajax_video_recording(request, username, id):
    user = AuthUser.objects.get(pk=request.session.get('id'))
    client = CAMERA.threads[username]
    client.connections[id].recording_video(user)
    send_message = {'send_data' : '1'}
    return JsonResponse(send_message)

@csrf_exempt
def config_Recording(request, username, id):
    client = CAMERA.threads[username]
    check = client.connections[id].check_current_recording
    if check:
        send_message = {'send_data': '1'}
    else:
        send_message = {'send_data': '0'}
    return JsonResponse(send_message)

@csrf_exempt
def config_info(request, username, id):
    receive_message = request.POST.get('send_data')
    client = CAMERA.threads[username]
    check_deteck_person = client.connections[id].check_detect_person
    check_recognition_face = client.connections[id].check_recognition_face
    check_detect_fire = client.connections[id].check_detect_fire
    check_detect_animal = client.connections[id].check_detect_animal
    check_on_safemode = client.connections[id].check_on_safemode
    safe_mode_time = client.connections[id].SafeMode.time_noDetect
    send_message = {'dp':check_deteck_person, 'rf':check_recognition_face, 'df':check_detect_fire,
                    'da':check_detect_animal, 'sm':check_on_safemode, 'sm_time':safe_mode_time}
    return JsonResponse(send_message)

@csrf_exempt
def config_detect_person(request, username, id):
    client = CAMERA.threads[username]
    if(client.connections[id].check_detect_person):
        client.connections[id].check_detect_person = False
        mode_history = HomecamModeUseHistory()
        user = AuthUser.objects.get(username=username)
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        mode_history.uid=user
        mode_history.camid=id
        mode_history.time=timestamp
        mode_history.mode='DETECT_PERSON'
        mode_history.division='OFF'
        mode_history.save()
    else:
        client.connections[id].check_detect_person = True
        mode_history = HomecamModeUseHistory()
        user = AuthUser.objects.get(username=username)
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        mode_history.uid = user
        mode_history.camid = id
        mode_history.time = timestamp
        mode_history.mode = 'DETECT_PERSON'
        mode_history.division = 'ON'
        mode_history.save()
    send_message = {'send_data' : '1'}
    return JsonResponse(send_message)

@csrf_exempt
def config_recognition_face(request, username, id):
    client = CAMERA.threads[username]
    if (client.connections[id].check_recognition_face):
        client.connections[id].check_recognition_face = False
        mode_history = HomecamModeUseHistory()
        user = AuthUser.objects.get(username=username)
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        mode_history.uid = user
        mode_history.camid = id
        mode_history.time = timestamp
        mode_history.mode = 'DETECT_UNKNOWNFACE'
        mode_history.division = 'OFF'
        mode_history.save()
    else:
        client.connections[id].check_recognition_face = True
        mode_history = HomecamModeUseHistory()
        user = AuthUser.objects.get(username=username)
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        mode_history.uid = user
        mode_history.camid = id
        mode_history.time = timestamp
        mode_history.mode = 'DETECT_UNKNOWNFACE'
        mode_history.division = 'ON'
        mode_history.save()
    send_message = {'send_data' : '1'}
    return JsonResponse(send_message)

@csrf_exempt
def config_detect_fire(request, username, id):
    client = CAMERA.threads[username]
    if (client.connections[id].check_detect_fire):
        client.connections[id].check_detect_fire = False
        mode_history = HomecamModeUseHistory()
        user = AuthUser.objects.get(username=username)
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        mode_history.uid = user
        mode_history.camid = id
        mode_history.time = timestamp
        mode_history.mode = 'DETECT_FIRE'
        mode_history.division = 'OFF'
        mode_history.save()
    else:
        client.connections[id].check_detect_fire = True
        mode_history = HomecamModeUseHistory()
        user = AuthUser.objects.get(username=username)
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        mode_history.uid = user
        mode_history.camid = id
        mode_history.time = timestamp
        mode_history.mode = 'DETECT_FIRE'
        mode_history.division = 'ON'
        mode_history.save()
    send_message = {'send_data' : '1'}
    return JsonResponse(send_message)

@csrf_exempt
def config_detect_animal(request, username, id):
    client = CAMERA.threads[username]
    if (client.connections[id].check_detect_animal):
        client.connections[id].check_detect_animal = False
        mode_history = HomecamModeUseHistory()
        user = AuthUser.objects.get(username=username)
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        mode_history.uid = user
        mode_history.camid = id
        mode_history.time = timestamp
        mode_history.mode = 'DETECT_ANIMAL'
        mode_history.division = 'OFF'
        mode_history.save()
    else:
        client.connections[id].check_detect_animal = True
        mode_history = HomecamModeUseHistory()
        user = AuthUser.objects.get(username=username)
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        mode_history.uid = user
        mode_history.camid = id
        mode_history.time = timestamp
        mode_history.mode = 'DETECT_ANIMAL'
        mode_history.division = 'ON'
        mode_history.save()
    send_message = {'send_data' : '1'}
    return JsonResponse(send_message)

@csrf_exempt
def config_safe_mode(request, username, id):
    client = CAMERA.threads[username]
    if (client.connections[id].check_on_safemode):
        client.connections[id].check_on_safemode = False
        mode_history = HomecamModeUseHistory()
        user = AuthUser.objects.get(username=username)
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        mode_history.uid = user
        mode_history.camid = id
        mode_history.time = timestamp
        mode_history.mode = 'SAFEMODE'
        mode_history.division = 'OFF'
        mode_history.save()
    else:
        client.connections[id].SafeMode.init_noDetectTime()
        client.connections[id].check_on_safemode = True
        mode_history = HomecamModeUseHistory()
        user = AuthUser.objects.get(username=username)
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        mode_history.uid = user
        mode_history.camid = id
        mode_history.time = timestamp
        mode_history.mode = 'SAFEMODE'
        mode_history.division = 'ON'
        mode_history.save()
    send_message = {'send_data' : '1'}
    return JsonResponse(send_message)


@csrf_exempt
def config_safe_mode_set_time(request, username, id):
    receive_message = request.POST.get('send_data')
    client = CAMERA.threads[username]
    print(int(receive_message))
    client.connections[id].SafeMode.time_noDetect = int(receive_message)
    send_message = {'send_data' : '1'}
    return JsonResponse(send_message)

@csrf_exempt
def ajax_getData_Animal(request):
    day = request.POST.get('datetime')
    username = request.POST.get('username')
    user = AuthUser.objects.get(username=username)
    mode_history = HomecamModeUseHistory.objects.filter(uid=user.id, mode='DETECT_ANIMAL',
                                                        time__year=day.split('-')[0],time__month=day.split('-')[1],
                                                        time__day=day.split('-')[2])
    detect_cat_data = DetectAnimal.objects.filter(uid=user.id, time__year=day.split('-')[0], species=15,
                                                      time__month=day.split('-')[1],
                                                      time__day=day.split('-')[2]).all()
    detect_dog_data = DetectAnimal.objects.filter(uid=user.id, time__year=day.split('-')[0], species=16,
                                                  time__month=day.split('-')[1],
                                                  time__day=day.split('-')[2]).all()

    print(detect_dog_data, detect_cat_data)
    cat_hour = []
    dog_hour = []
    if len(detect_cat_data)==0:
        for i in range(25):
            cat_hour.append(0)
    else:
        cat_hour_dic={}
        for i in range(25):
            cat_hour_dic[i]=[]
        for data in detect_cat_data:
            location = data.location
            hour = int(data.time.strftime("%H:%M:%S").split(':')[0])
            cat_hour_dic[hour].append(location)
        for key in cat_hour_dic:
            if len(cat_hour_dic[key])==0:
                cat_hour.append(0)
            else:
                total_cnt = len(cat_hour_dic[key])
                check_sleep=False
                max_cnt_continuity=0
                pre_location=-1
                temp_cnt=0
                for data in cat_hour_dic[key]:
                    if data==pre_location:
                        temp_cnt+=1
                    else:
                        temp_cnt=1
                        if max_cnt_continuity<temp_cnt:
                            max_cnt_continuity=temp_cnt
                        pre_location=data

                if max_cnt_continuity>int(total_cnt*0.5):
                    check_sleep=True

                location_one=0
                location_two=0
                location_three=0
                location_four=0
                for data in cat_hour_dic[key]:
                    if data==1:
                        location_one+=1
                    elif data==2:
                        location_two+=1
                    elif data==3:
                        location_three+=1
                    elif data==4:
                        location_four+=1
                location_one_percent = int(location_one/total_cnt)
                location_two_percnet = int(location_two/total_cnt)
                location_three_percent = int(location_three/total_cnt)
                location_four_percent = int(location_four/total_cnt)

                # 360
                if total_cnt<120: #20min - 0,1
                    if check_sleep and max_cnt_continuity > int(total_cnt * 0.9):
                        cat_hour.append(0)
                    else:
                        cat_hour.append(1)
                elif total_cnt<240: #40min - 0,1,2
                    if check_sleep and max_cnt_continuity > int(total_cnt * 0.9):
                        cat_hour.append(0)
                    elif location_one_percent>40 or location_two_percnet>40 or location_three_percent>40 or location_four_percent>40:
                        cat_hour.append(1)
                    else:
                        cat_hour.append(2)
                else: #60min - 0,1,2,3
                    if check_sleep and max_cnt_continuity > int(total_cnt * 0.9):
                        cat_hour.append(0)
                    elif location_one_percent > 60 or location_two_percnet > 60 or location_three_percent > 60 or location_four_percent > 60:
                        cat_hour.append(1)
                    elif location_one_percent > 40 or location_two_percnet > 40 or location_three_percent > 40 or location_four_percent > 40:
                        cat_hour.append(2)
                    else:
                        cat_hour.append(3)

    if len(detect_dog_data)==0:
        for i in range(25):
            dog_hour.append(0)
    else:
        dog_hour_dic = {}
        for i in range(25):
            dog_hour_dic[i]=[]
        for data in detect_dog_data:
            location = data.location
            hour = int(data.time.strftime("%H:%M:%S").split(':')[0])
            dog_hour_dic[hour].append(location)
        for key in dog_hour_dic:
            if len(dog_hour_dic[key]) == 0:
                dog_hour.append(0)
            else:
                total_cnt = len(dog_hour_dic[key])
                check_sleep = False
                max_cnt_continuity = 0
                pre_location = -1
                temp_cnt = 0
                for data in dog_hour_dic[key]:
                    if data == pre_location:
                        temp_cnt += 1
                    else:
                        temp_cnt = 1
                        if max_cnt_continuity < temp_cnt:
                            max_cnt_continuity = temp_cnt
                        pre_location = data

                if max_cnt_continuity > int(total_cnt * 0.5):
                    check_sleep = True

                location_one = 0
                location_two = 0
                location_three = 0
                location_four = 0
                for data in dog_hour_dic[key]:
                    if data == 1:
                        location_one += 1
                    elif data == 2:
                        location_two += 1
                    elif data == 3:
                        location_three += 1
                    elif data == 4:
                        location_four += 1
                location_one_percent = int(location_one / total_cnt)
                location_two_percnet = int(location_two / total_cnt)
                location_three_percent = int(location_three / total_cnt)
                location_four_percent = int(location_four / total_cnt)

                # 360
                if total_cnt < 120:  # 20min - 0,1
                    if check_sleep and max_cnt_continuity > int(total_cnt * 0.9):
                        dog_hour.append(0)
                    else:
                        dog_hour.append(1)
                elif total_cnt < 240:  # 40min - 0,1,2
                    if check_sleep and max_cnt_continuity > int(total_cnt * 0.9):
                        dog_hour.append(0)
                    elif location_one_percent > 40 or location_two_percnet > 40 or location_three_percent > 40 or location_four_percent > 40:
                        dog_hour.append(1)
                    else:
                        dog_hour.append(2)
                else:  # 60min - 0,1,2,3
                    if check_sleep and max_cnt_continuity > int(total_cnt * 0.9):
                        dog_hour.append(0)
                    elif location_one_percent > 60 or location_two_percnet > 60 or location_three_percent > 60 or location_four_percent > 60:
                        dog_hour.append(1)
                    elif location_one_percent > 40 or location_two_percnet > 40 or location_three_percent > 40 or location_four_percent > 40:
                        dog_hour.append(2)
                    else:
                        dog_hour.append(3)

    mode_history_hour = []
    for data in mode_history:
        state = data.division
        hour = data.time.strftime("%H:%M:%S").split(':')[0]
        minute = data.time.strftime("%H:%M:%S").split(':')[1]
        second = data.time.strftime("%H:%M:%S").split(':')[2]
        mode_history_hour.append([hour, state])

    mode_state = []
    iter_index = 0
    check = False
    if len(mode_history_hour)>0:
        for hour in range(0, 24):
            once_on = False
            while True:
                if int(mode_history_hour[iter_index][0]) == hour:
                    if mode_history_hour[iter_index][1] == 'ON':
                        check = True
                        once_on = True
                    else:
                        check = False
                    iter_index += 1
                    if iter_index == len(mode_history_hour):
                        iter_index = 0
                        break
                else:
                    break
            if check or once_on:
                mode_state.append('ON')
            else:
                mode_state.append('OFF')
    else:
        for i in range(24):
            mode_state.append('OFF')

    mode_json = serializers.serialize("json", mode_history)
    #return HttpResponse(data_json, content_type="text/json-comment-filtered")
    send_message = {'mode_state' : mode_state, 'cat_activity' : cat_hour, 'dog_activity' : dog_hour}
    return JsonResponse(send_message)


@csrf_exempt
def main_state(request):
    user=None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
    uid = request.POST.get('send_data')
    homecam_list = Homecam.objects.filter(uid=uid)
    data= {}
    for homecam in homecam_list:
        data_dic = {}
        data_dic['camid'] = homecam.camid
        data_dic['connect'] = 0
        data_dic['alarm'] = 0
        if CAMERA.threads.get(user.username):
            if CAMERA.threads.get(user.username).cnt > 0:
                if CAMERA.threads.get(user.username).connections.get(homecam.camid):
                    data_dic['connect'] = 1
        alarm_list = Alarm.objects.filter(camid=homecam.camid, confirm=0)
        if(alarm_list.count()>0):
            data_dic['alarm']=1
        if data_dic['connect'] ==0:
            data_dic['alarm'] = 0
        data[homecam.camid]=data_dic

    send_message = data
    print(send_message)
    return JsonResponse(send_message)