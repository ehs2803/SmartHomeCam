from threading import Thread

from django.contrib.auth.models import User
from django.http import StreamingHttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from account.models import AuthUser
from homecam.algorithm.basic import detect_person
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
    idList='1 2 3 4 5 '

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
        frame = client.connections[id].get_frame()
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
    client.disconnect_socket(id)
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
    send_message = {'send_data' : '1'}
    return JsonResponse(send_message)