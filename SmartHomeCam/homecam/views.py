import datetime
import time
from threading import Thread

from django.contrib.auth.models import User
from django.http import StreamingHttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from account.models import AuthUser
from homecam.models import HomecamModeUseHistory
from homecam.socket import VideoCamera

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