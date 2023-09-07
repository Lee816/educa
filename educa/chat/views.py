from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def course_char_room(request, course_id):
    try:
        # 현재 사용자가 참여한 주어진 id의 코스를 검색
        course = request.user.courses_joined.get(id=course_id)
    except:
        # 사용자가 코스에 등록되어 있지 않거나 코스가 존재하지 않는다
        return HttpResponseForbidden()
    return render(request, 'chat/room.html', {'course':course})