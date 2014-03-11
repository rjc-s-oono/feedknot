from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render_to_response('feedknot/Mypage.html',{'login_flg':'0','user_name':''})

