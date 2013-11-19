from django.shortcuts import render_to_response

def index(request):
    return render_to_response('feedknot/Mypage.html',{'login_flg':'0','user_name':''})

def oAuth(request):
    return render_to_response('feedknot/OAuth.html',{})

def login(request):
    return render_to_response('feedknot/Mypage.html',{'login_flg':'1','user_name':'RJC9999'})

def logout(request):
    return render_to_response('feedknot/Mypage.html',{'login_flg':'0','user_name':''})
