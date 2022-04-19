from threading import Thread

from django.contrib.auth.models import User
from django.http import StreamingHttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

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
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))

    context = {
        'user': user
    }
    print(user.username)
    return render(request, "homecam/basic.html", context=context)

def pet(request):
    user = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))

    context = {
        'user': user
    }
    return render(request, "homecam/pet.html", context=context)

def gen_basic(camera, username):
    while True:
        if camera.threads.get(username):
            break
    conn = camera.threads[username]
    while True:
        frame = conn.get_frame()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def video_basic(request, username):
    return StreamingHttpResponse(gen_basic(CAMERA, username),
                    content_type='multipart/x-mixed-replace; boundary=frame')


def gen_pet(camera):
    while True:
        frame = camera.camera.get_frame()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_pet(request):
    return StreamingHttpResponse(gen_pet(VideoCamera()),
                   content_type='multipart/x-mixed-replace; boundary=frame')

@csrf_exempt
def ajax_method(request):
    sendmessage = "111"
    receive_message = request.POST.get('send_data')
    if CAMERA.threads.get(receive_message):
        sendmessage="1"
    else:
        sendmessage="0"
    send_message = {'send_data' : sendmessage}
    return JsonResponse(send_message) # 라즈베리파이 연결 여부

@csrf_exempt
def ajax_method2(request):
    sendmessage = "222"
    '''
    for i in check_cam: # 모든 라즈베리파이 연결에 대해서
        if i==False: # 평상시
            sendmessage = sendmessage+"0"
        else: # 특정 상황 감지 시
            sendmessage = sendmessage+"1"
    '''
    receive_message = request.POST.get('send_data')
    send_message = {'send_data' : sendmessage}
    return JsonResponse(send_message) # 감지 결과 전송