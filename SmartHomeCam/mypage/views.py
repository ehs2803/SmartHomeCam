from django.contrib.auth.models import User
from django.shortcuts import render


# Create your views here
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
    user = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))

    context = {
        'user': user
    }
    return render(request, "mypage/family_register.html", context=context)

def chart(request):
    user = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))

    context = {
        'user': user
    }
    return render(request, "mypage/chart.html", context=context)